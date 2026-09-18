"""Step 0 environment check: confirm a device works locally and that
BadgerBrain's OpenAI-style API is reachable, before any training code
is written.

Run directly with `python scripts/check_env.py`, or import the pieces
from tests.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any


def detect_device() -> str:
    """Return the best available torch device: cuda, mps, or cpu.

    Never raises — a laptop with no GPU is expected to fall back to cpu.
    """
    import torch

    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) is not None and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def load_pretrained_efficientnet_b0(device: str):
    """Load an ImageNet-pretrained EfficientNet-B0 via timm, on `device`.

    timm is used (rather than torchvision's own efficientnet_b0) to match
    the backbone already chosen in Snapshot_WI_Oh_Deer_starter_1.ipynb, so
    later steps share one implementation.
    """
    import timm

    model = timm.create_model("efficientnet_b0", pretrained=True, num_classes=1000)
    model.eval()
    return model.to(device)


def run_forward_pass(model, device: str) -> dict[str, Any]:
    """Run one forward pass on a dummy 224x224 RGB batch and return timing
    + output-shape info. A dummy tensor is enough to prove the model,
    device, and library versions are wired up correctly; it does not
    require the competition data.
    """
    import torch

    x = torch.randn(1, 3, 224, 224, device=device)
    start = time.perf_counter()
    with torch.no_grad():
        out = model(x)
    elapsed_ms = (time.perf_counter() - start) * 1000

    return {
        "device": device,
        "output_shape": tuple(out.shape),
        "output_has_nan": bool(torch.isnan(out).any().item()),
        "elapsed_ms": round(elapsed_ms, 2),
    }


@dataclass
class BadgerBrainResult:
    ok: bool
    model: str
    base_url: str
    detail: str
    elapsed_ms: float | None = None


def check_badgerbrain(
    base_url: str | None = None,
    api_key: str | None = None,
    model: str | None = None,
    timeout_s: float = 30.0,
) -> BadgerBrainResult:
    """Send a minimal chat-completion request to BadgerBrain's
    OpenAI-style API and confirm a response comes back.

    Reads BADGERBRAIN_BASE_URL / BADGERBRAIN_API_KEY / BADGERBRAIN_MODEL
    from the environment when not passed explicitly, since the URL and
    key are per-person and must never be committed to the repo.
    """
    base_url = base_url or os.environ.get("BADGERBRAIN_BASE_URL")
    api_key = api_key or os.environ.get("BADGERBRAIN_API_KEY", "not-needed")
    model = model or os.environ.get("BADGERBRAIN_MODEL", "qwen3.8-27b")

    if not base_url:
        return BadgerBrainResult(
            ok=False,
            model=model,
            base_url="",
            detail="BADGERBRAIN_BASE_URL is not set; skipping live request.",
        )

    from openai import OpenAI

    client = OpenAI(base_url=base_url, api_key=api_key, timeout=timeout_s)
    start = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Reply with the single word: pong"}],
            max_tokens=5,
        )
        elapsed_ms = (time.perf_counter() - start) * 1000
        reply = response.choices[0].message.content
        return BadgerBrainResult(
            ok=True,
            model=model,
            base_url=base_url,
            detail=f"reply={reply!r}",
            elapsed_ms=round(elapsed_ms, 2),
        )
    except Exception as exc:  # noqa: BLE001 - report any failure back, don't crash the check
        return BadgerBrainResult(
            ok=False,
            model=model,
            base_url=base_url,
            detail=f"{type(exc).__name__}: {exc}",
        )


def main() -> int:
    device = detect_device()
    print(f"[torch]       device = {device}")

    try:
        model = load_pretrained_efficientnet_b0(device)
        n_params = sum(p.numel() for p in model.parameters()) / 1e6
        print(f"[timm]        efficientnet_b0 loaded, pretrained ({n_params:.1f}M params)")

        fwd = run_forward_pass(model, device)
        print(
            f"[forward]     shape={fwd['output_shape']}  "
            f"nan={fwd['output_has_nan']}  {fwd['elapsed_ms']} ms"
        )
        model_ok = not fwd["output_has_nan"] and fwd["output_shape"] == (1, 1000)
    except Exception as exc:  # noqa: BLE001 - report, don't dump a stack trace
        print(f"[timm]        FAILED: {type(exc).__name__}: {exc}")
        print("              (needs internet access to download pretrained weights)")
        model_ok = False

    bb = check_badgerbrain()
    status = "OK" if bb.ok else "SKIPPED/FAILED"
    print(f"[badgerbrain] {status}  model={bb.model}  {bb.detail}")

    return 0 if model_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
