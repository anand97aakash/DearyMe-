# DearyMe-

Snapshot Wisconsin: Oh Deer hackathon. See `plan.md` for the staged MVP
plan and `CONTRIBUTING.md` for team conventions.

## Setup

```bash
pip install -r requirements.txt
```

## Step 0: environment check

Confirms a device is available (CUDA/MPS/CPU), a pretrained
EfficientNet-B0 loads and runs a forward pass, and BadgerBrain's
OpenAI-style API responds.

```bash
export BADGERBRAIN_BASE_URL=...   # BadgerBrain's OpenAI-compatible endpoint
export BADGERBRAIN_API_KEY=...    # if required
python scripts/check_env.py
```

Run the automated checks with:

```bash
pytest tests/
```

The EfficientNet-B0 and BadgerBrain checks need network access (to
Hugging Face Hub, and to BadgerBrain respectively) and will skip
themselves with a clear reason if that access or the BadgerBrain env
vars aren't available — this is expected in a restricted sandbox, not on
the laptop or on BadgerBrain itself.

Competition data goes in `/data` — see `data/README.md` to download it.
