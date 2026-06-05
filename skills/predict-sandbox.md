# /predict-sandbox — Self-Improving Prediction Experiment

> ⚠️ **This is an AI-building experiment, not an investing tool.** Its only purpose is to watch whether a prediction loop's **calibration improves** over time. Output must NEVER inform a real decision.

**Trigger:** Daily (after `/news-filter` + `/digest`), or manual `/predict-sandbox`
**Output:** `sandbox-predictions/` only — never writes to the investing vault

---

## The Wall (binding)

- **READ** freely from the investing vault (dots, theses, mistakes-log, watchlist)
- **WRITE only** to `sandbox-predictions/`
- Every output file opens with the ⚠️ EXPERIMENT banner
- If a step would touch anything outside `sandbox-predictions/` (other than reading), abort

---

## Architecture

```
sandbox-predictions/
  predictions/YYYY-MM-DD.md   ← today's calls (scored tomorrow)
  scores/YYYY-MM-DD.md        ← yesterday's calls vs actual outcomes
  playbook.md                 ← current beliefs (rewritten each run)
  lessons-log.md              ← append-only learning log
  calibration.json            ← hit rates by confidence bin
```

---

## Step-by-Step SOP

### Step 0 — Setup
Resolve `[today]` and `[yesterday]` (same convention as /digest — same-day lag model).

### Step 1 — Score yesterday's predictions

Read `sandbox-predictions/predictions/[yesterday].md`. For each predicted ticker, get completed close-to-close move:
```bash
python tools/compute-reaction.py [TICKER1] [TICKER2] ... --json
```
Classify outcome: **UP** (≥ +0.3%) / **DOWN** (≤ -0.3%) / **FLAT** (|move| < 0.3%)

### Step 2 — Brier score per call

```
Brier = (p − hit)²    where p = confidence in called direction (0–1), hit ∈ {1, 0}
```

Low Brier = good (correct + confident). High Brier = bad (wrong + overconfident).

### Step 3 — Write score file + update calibration

`sandbox-predictions/scores/[yesterday].md`:

```markdown
> ⚠️ EXPERIMENT — sandbox prediction scores. Never used for real decisions.

# Sandbox Scores — predictions from [yesterday], scored [today]

| Ticker | Dot (type) | Predicted | Conf | Actual | Outcome | Hit | Brier |
|--------|-------------|-----------|------|--------|---------|-----|-------|
| NVDA   | ... (COMPANY) | UP | 70% | +6.26% | UP | ✓ | 0.09 |

**Day mean Brier:** 0.XX  ·  **Hits:** X/N
```

Update `calibration.json`: for each confidence bin (50-59, 60-69, 70-79, 80-89, 90-100), track calls, hits, hit_rate. Append a history entry.

### Step 4 — Update the playbook (learn)

Append to `lessons-log.md`: only concrete lessons the misses taught. "No clear lesson — outcomes were noise" is a valid, honest entry.

Rewrite `playbook.md`: update header stats, edit "Calibration corrections" section to adjust future confidence by bin where hit_rate diverges from stated range. Keep it tight (≤12 bullets).

### Step 5 — Predict today

Read `vault/dots/[today].md`. For each **FRESH dot only** (skip STALE, STRUCTURAL, DECISION), predict using the now-updated playbook + knowledge base:

```markdown
> ⚠️ EXPERIMENT — sandbox predictions. NOT investing advice.

# Sandbox Predictions — [today] (scored tomorrow)

| Ticker | Dot (type) | Predicted | Conf | One-line reason |
|--------|-------------|-----------|------|-----------------|
| NVDA   | ... (COMPANY) | UP | 65% | playbook: COMPANY+ prior, but feed often pre-priced → trimmed conf |
```

---

## Rules

- Confidence must be **honest**: calibrated 55% beats performative 90% — Brier punishes bluffing
- Outcomes from `compute-reaction.py` only — never from `regularMarketPrice`
- FLAT is a real prediction
- **Drift is data, not a bug** — if the loop becomes overconfident or self-confirming, log it
- Never fabricate an outcome — if a ticker can't be scored, mark "unscored" and continue
- No buy/sell/watchlist signals — this tracks calibration, not returns
