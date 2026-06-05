# /digest — Evening Summary

**Trigger:** Auto at 17:45 (after `/news-filter`), or manual `/digest`
**Output:** `vault/digests/YYYY-MM-DD-evening.md`

The daily run happens at 17:45 BKK (~10:45 ET) — before the US market opens. So
/digest scores **yesterday's** dots against the now-closed overnight session.

---

## Step-by-Step SOP

### Step 1 — Load YESTERDAY's dots

`[today] - 1 day` = the file to score.

Read `vault/dots/[yesterday].md`.

If it doesn't exist: look back up to 5 days for the most recent un-scored dot file. If none within 5 days: output "No un-scored dots in the last 5 days" and exit.

---

### Step 2 — Compute close-to-close reaction

Use the helper script:
```bash
python tools/compute-reaction.py [TICKER1] [TICKER2] ... --json
```

Returns per ticker: `close_before` (baseline date), `close_after` (reacting session date), `reaction_pct`.

Internally it fetches a 5-day window, drops any in-progress bar, and takes the two most recent completed daily closes:
- `close_after` = most recent completed close (the session that reacted to yesterday's news)
- `close_before` = the close just before it (the baseline)
- `Reaction % = (close_after − close_before) / close_before`

This is run-time-proof — always measures the first full session after the news, regardless of when the pipeline fired.

**ONLY score FRESH dots.** STALE dots (already priced in) go under "Already Priced In — not scored."

Expected direction by news type:

| News Type | Expected direction |
|-----------|-------------------|
| GEOPOLITICAL | VIX↑, Gold↑, SPY↓, QQQ↓ |
| MACRO (rate hike/inflation) | VIX↑, SPY↓, QQQ↓, Gold↑ |
| MACRO (rate cut/stimulus) | SPY↑, QQQ↑, VIX↓ |
| SECTOR (positive AI/tech) | QQQ↑, sector ETF↑ |
| SECTOR (negative, regulation) | QQQ↓, sector ETF↓ |
| COMPANY (positive) | That stock↑ |
| COMPANY (negative) | That stock↓ |
| STRUCTURAL | No same-day reaction expected |
| DECISION | No same-day expectation — record price only |

Mark each FRESH dot as:
- ✓ Consistent — reaction moved in expected direction
- ✗ Inconsistent — reaction moved opposite to expected
- ~ Flat — no meaningful move (< 0.3%)

**A single ✓/✗ is one noisy data point.** Meaning only emerges in the monthly aggregate (/pattern-report).

---

### Step 3 — Flag watchlist companies

Read `vault/watchlist.md`. Check if any company in today's dots also appears in the watchlist.

Flag: "⚠️ WATCHLIST: [TICKER] appeared in recent news — consider running /brief [TICKER]"

---

### Step 4 — Detect building themes

Read last 7 days of dot files. Look for:
- 3+ consecutive days of the same news type
- Same sector mentioned 3+ times this week
- Same company mentioned 3+ times this week

---

### Step 5 — Save evening digest

```markdown
# Evening Digest — YYYY-MM-DD

_Scoring dots from [YESTERDAY]. Reactions are close-to-close. Only FRESH dots scored._

## Consistency Check (FRESH dots only)
| Dot | Expected | SPY | VIX | Gold | QQQ | Result |
|------|----------|-----|-----|------|-----|--------|
| [summary] (GEOPOLITICAL) | VIX↑ Gold↑ SPY↓ | -0.6% | +8.2% | +0.9% | -0.8% | ✓ consistent |
| [summary] (MACRO) | SPY↓ | +0.2% | — | — | — | ✗ inconsistent |

## Already Priced In (STALE — not scored)
[Dots already priced in before reaching the feed, or "None today"]

## Watchlist Alerts
[Flagged companies, or "None today"]

## Building Themes
[3+ day patterns, or "No strong theme yet"]

## Inconsistent Moves Worth Investigating
[✗ FRESH dots — fed to /why next Sunday]
```

---

## Rules

- Score from COMPLETED daily closes (5d window), never `regularMarketPrice`
- ✗ unexpected moves are NOT bad — they are data; record them, don't ignore them
- STRUCTURAL and DECISION dots never get a ✓/✗
- Backfill: range=5d still holds closes up to 5 days back — can score any recent un-scored atom
