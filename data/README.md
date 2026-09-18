# /data

This directory is where the Kaggle dataset lives locally. It is
**gitignored** (per `CONTRIBUTING.md`: never commit real/large datasets) —
everyone on the team downloads it themselves.

## Download

The data is gated behind the hackathon rules, so you need a Kaggle
account that has joined the competition, plus the Kaggle CLI configured
(`~/.kaggle/kaggle.json` — see
[Kaggle API docs](https://www.kaggle.com/docs/api)):

```bash
pip install kaggle
kaggle competitions download -c snapshot-wi-oh-deer -p data/
unzip -q data/snapshot-wi-oh-deer.zip -d data/
```

## Expected layout

```
data/
  Snapshot_WI-Oh_Deer_data-v1.csv   # one row per image, 10 columns, includes bounding box
  Snapshot_WI-Oh_Deer_Photos/       # 4880 .jpg files
```

`src/oh_deer/data.py` auto-detects the CSV and photos folder under
`data/` (fuzzy-matching, same approach as
`Snapshot_WI_Oh_Deer_starter_1.ipynb`), so exact subfolder naming isn't
critical — just make sure both end up somewhere under `data/`.
