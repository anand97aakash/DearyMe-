"""Locate the competition data under /data, wherever exactly it landed."""
from __future__ import annotations

import glob
import os
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"


def find_dataset(data_dir: Path = DATA_DIR) -> tuple[str, str]:
    """Return (csv_path, photos_dir), auto-detected under `data_dir`.

    Raises FileNotFoundError with a pointer to data/README.md if the
    dataset hasn't been downloaded yet.
    """
    csvs = glob.glob(os.path.join(data_dir, "**", "*.csv"), recursive=True)
    jpgs = glob.glob(os.path.join(data_dir, "**", "*.jpg"), recursive=True)

    if not csvs or not jpgs:
        raise FileNotFoundError(
            f"no CSV/JPGs found under {data_dir} - see data/README.md to download the dataset"
        )

    return csvs[0], os.path.dirname(jpgs[0])
