# MVP Plan — Snapshot Wisconsin: Oh Deer

## What the challenge actually scores

From the Kaggle page (this is a judged hackathon, not an auto-scored
leaderboard — final deliverable is a public MIT/Apache-2.0 repo + writeup
reviewed by judges):

- **Required predictions, both of them:** Antlers (Antlered/Antlerless)
  *and* Age (Adult/Young). F1 score × 100 = up to 100 of 150 points.
- **Usefulness (50 pts):** additional useful predictions (15), inference
  speed (15), compute efficiency (10), ease of setup/use/maintainability
  for research software engineers (10).
- **Data:** one CSV (10 columns, exact schema not yet confirmed — Kaggle
  data preview is rules-gated) + 4880 images, with bounding boxes for
  where the deer is in each photo. No separate hidden test set is
  mentioned — we self-report F1 from our own held-out split, so that
  split has to be trustworthy.

## Is "EfficientNet + Antlers-first + crop/uncrop" a good MVP?

**Partially — the model choice is fine, but the plan as stated starts one
layer too deep and is missing pieces you need before you can call
anything a "baseline" you A/B against.** Specifically:

1. **No evaluation harness.** "Understand it end-to-end" means building
   the scoring script first — even against a dummy prediction — not
   picking an architecture first. As written, there's no step that
   produces a number comparable to what judges compute.
2. **Age is dropped.** It's scored identically to Antlers. An MVP that
   only predicts Antlers isn't a valid baseline to A/B against, because
   it can't produce a real submission.
3. **No leak-safe split.** Camera-trap images come in bursts — several
   near-duplicate frames per trigger event, same site, same animal. A
   random image-level split will leak near-duplicates between train and
   val and inflate your self-reported F1 in a way that won't survive
   judge scrutiny. This needs to be decided before any model is trained.
4. **Cropping is baked into the baseline instead of being the first
   experiment.** If MVP v1 already crops to the ground-truth box, you
   have nothing uncropped to compare it to, so you can't tell whether
   cropping is actually buying you anything — which defeats the stated
   purpose of having an MVP to A/B against.
5. **"Uncrop" is undefined.** If it means "run our own detector at
   inference because real deployment images won't have hand-drawn boxes,"
   that's a separate object-detection subproject, not a quick MVP step —
   scope it separately once you know cropping helps.
6. **Speed/efficiency (25 of 150 points) aren't measured anywhere in the
   plan**, so there's no baseline number to compare future components
   against on the axes the judges explicitly grade.

Net: keep EfficientNet and keep antlers/age as the target — just reorder
so the harness and both labels come first, and treat cropping as
experiment #1 against that baseline rather than part of it.

## Plan

### Step 0 — Environment + repo skeleton
Confirm the laptop and BadgerBrain can both load the data and run a
forward pass of a pretrained EfficientNet-B0.
**Works when:** `import torch; torch.cuda.is_available()` (or MPS/CPU
fallback) succeeds on a laptop, and a test request to BadgerBrain's
OpenAI-style API returns a response. Data lives under `/data` per
`CONTRIBUTING.md`.

### Step 1 — Data audit
Load the CSV, list all 10 columns, check label distribution for Antlers
and Age, and identify whether there's a site/camera/sequence/burst
identifier column to group on.
**Works when:** a short written data profile (row count, column names,
% Antlered vs Antlerless, % Adult vs Young, whether a grouping key
exists) is checked into the repo and the team has agreed on the grouping
key for Step 2.

### Step 2 — Leak-safe train/val split
Split by the grouping key from Step 1 (camera/site/burst — not by raw
image id), roughly 80/20.
**Works when:** a script asserts zero overlap of grouping-key values
between train and val, and reports class balance in each split is
reasonably close to the full dataset.

### Step 3 — Evaluation harness
Write the script that takes a predictions file (`image_id, antlers_pred,
age_pred`) and a ground-truth file and outputs F1, matching the rubric
as closely as we can determine it.
**Works when:** feeding it the ground truth as "predictions" returns
F1 = 1.0, and feeding it a clearly-wrong constant prediction returns a
lower, sane number.

### Step 4 — Dumb baseline (majority class)
Predict the majority class for Antlers and for Age on the val split, no
model at all.
**Works when:** the harness from Step 3 reports a real F1 number for
this. This is baseline #0 — the floor every later component must beat to
be worth keeping.

### Step 5 — MVP v1: whole-image EfficientNet, both labels
Fine-tune a pretrained EfficientNet-B0 with two heads (or two small
models) for Antlers and Age, on **uncropped** full images.
**Works when:** training loss decreases, and val F1 via the Step 3
harness beats the Step 4 majority-class floor on *both* labels.

### Step 6 — Speed/efficiency baseline
Measure inference throughput (images/sec) and peak memory for MVP v1 on
the laptop and on BadgerBrain.
**Works when:** a logged number exists for both environments — this is
the number every later variant is compared against for the rubric's
speed/efficiency points.

### Step 7 — Experiment #1: crop-to-bounding-box
Using the provided ground-truth boxes, crop train/val images and retrain
the same architecture. Compare val F1 and speed against Steps 5–6 using
the same harness.
**Works when:** you have a quantified delta (F1 and speed, cropped vs.
uncropped) — this tells you whether cropping is worth keeping, not just
whether it "feels" better.

### Step 8 (only if Step 7 justifies it) — Test-time deer localization ("uncrop")
Only pursue if cropping meaningfully helped in Step 7 *and* the team
decides that working on future, un-annotated trail-camera images matters
for the "ease of use" rubric criterion. Try an off-the-shelf detector
(e.g. MegaDetector) on BadgerBrain before building anything custom.
**Works when:** a success criterion (e.g. detection recall at a chosen
IoU threshold, on a hand-checked sample) is written down *before*
starting, since this is new scope, not a tweak — don't let it expand
silently into the MVP.

### Stretch (for the 15-pt "additional predictions" bucket, not blocking)
Time-of-day, land cover, or animal alertness tags using BadgerBrain's
qwen3-vl-embedding-8b or similar, once Steps 0–6 are solid. Don't start
this before the required-label pipeline is working end-to-end.
