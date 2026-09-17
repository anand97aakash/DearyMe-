#!/usr/bin/env python3
"""Run this on the laptop and on BadgerBrain to confirm plan.md Step 0:
both environments can load the data location, pick a torch device, run
a pretrained EfficientNet-B0 forward pass, and reach BadgerBrain's
OpenAI-style API.

Usage:
    python scripts/check_env.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from oh_deer.env_check import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
