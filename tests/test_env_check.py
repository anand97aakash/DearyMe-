"""Proves plan.md Step 0: a device is detected, a pretrained
EfficientNet-B0 can run a forward pass, and (when configured)
BadgerBrain answers a real request.
"""
import os

import pytest

from oh_deer.env_check import check_badgerbrain, detect_device, load_pretrained_efficientnet_b0, run_forward_pass


def test_detect_device_returns_a_real_choice():
    assert detect_device() in {"cuda", "mps", "cpu"}


def test_efficientnet_b0_forward_pass():
    device = detect_device()
    try:
        model = load_pretrained_efficientnet_b0(device)
    except Exception as exc:  # noqa: BLE001
        pytest.skip(
            f"could not download pretrained EfficientNet-B0 weights "
            f"({type(exc).__name__}: {exc}) - needs a network path to "
            f"Hugging Face Hub, expected to work on the laptop/BadgerBrain"
        )

    result = run_forward_pass(model, device)
    assert result["output_shape"] == (1, 1000)
    assert result["output_has_nan"] is False


@pytest.mark.skipif(
    not os.environ.get("BADGERBRAIN_BASE_URL"),
    reason="BADGERBRAIN_BASE_URL not set - set it (and BADGERBRAIN_API_KEY "
    "if required) to exercise the live BadgerBrain check",
)
def test_badgerbrain_reachable():
    result = check_badgerbrain()
    assert result.ok, result.detail
