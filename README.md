# DearyMe-

## Project layout

- `notebooks/annotation/` — notebooks for manual gold-set annotation. This directory is reserved on `main`; no annotation notebook is currently present.
- `notebooks/validation/` — headless and one-by-one validation notebooks. These are not currently present on `main`.
- `notebooks/training/` — training notebooks, including the starter, local-CPU, and Snapshot WI notebooks.
- `notebooks/qwen/` — Qwen deer/head-visibility notebooks.
- `Qwen_model/` — supporting Qwen outputs and model-related data retained in its original location.

## Data paths

Local input data is intentionally kept outside the notebook directories:

- `Snapshot_WI-Oh_Deer_data-v1.csv`
- `Snapshot_WI-Oh_Deer_Photos/`

These paths are covered by `.gitignore` and are expected to be supplied locally. Generated model files and predictions are also ignored. Notebooks that use relative paths should be launched with the repository root as the working directory; notebooks with explicit absolute paths retain those paths unchanged.