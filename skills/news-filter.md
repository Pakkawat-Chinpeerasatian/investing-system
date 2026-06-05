# /news-filter — Daily Investing Dots + Price Context

**Trigger:** `/news-filter` once per day (morning)
**Output:** `vault/dots/YYYY-MM-DD.md`

---

## Step-by-Step SOP

### Step 1 — Check date + existing dots

- Get today's date (YYYY-MM-DD)
- If `vault/dots/[today].md` already exists: ask "Already ran today. Run again?"
- If it doesn't exist: proceed

---

### Step 2 — Fetch the 4 sources

**Source 1: ลงทุน Diary News Feed (primary)**
- Run: `python tools/fetch-longtun-news.py`
- Parses: `https://www.longtundiary.com/data/news.json`
- Category mapping: A → Score 3, B → Score 2, C → Score 1
- Pre-filtered for tech/AI/semiconductors by his AI agent "Press"

**Source 2: Brew Markets**
- URL: `https://www.brewmarkets.com/issues/latest`
- Extract: market overview, major movers, key headlines with % changes

**Source 3: The Diff**
- Fetch archive: `https://www.thediff.co/archive` → get 3 most recent slugs
- Fetch each article: `https://www.thediff.co/archive/[slug]/`

**Source 4: ลงทุน Diary Substack (decision study)**
- RSS: `https://longtundiary.substack.com/feed`
- Not market news — these are the author's personal investment decisions
- Extract as **DECISION dots**: WHAT he did + WHY + what changed his mind
- Never apply durability filter here — studied for reasoning, not durability

If any source fails: skip it, note failure, continue.

---

### Step 3 — Score for relevance

- **3 = High** — directly about Tech stocks, semiconductors, AI, ETFs
- **2 = Medium** — macro trends, broad business strategy affecting target sectors in 2+ years
- **1 = Low** — short-term noise, quarterly earnings, crypto, meme stocks → discard

---

### Step 4 — Apply the durability filter

For each score 2 or 3 article, ask:

> "Will this insight still matter in 2 years?"

- YES → extract as one-sentence Atom
- NO → discard
- UNSURE → keep, mark ⚠️

Good Dots:
- "Nvidia's CUDA ecosystem creates a switching-cost moat that competitors cannot replicate cheaply"
- "AI inference demand is shifting from training to deployment, benefiting smaller chip companies"

Bad Dots (discard):
- "Apple stock rose 2% after Q2 beat"
- "Fed raised rates by 25bps"

---

### Step 5 — Classify by news type

| Type | Description |
|------|-------------|
| `COMPANY` | News about a specific named company |
| `SECTOR` | News affecting a whole industry |
| `MACRO` | Broad economic or monetary policy |
| `GEOPOLITICAL` | Wars, sanctions, trade conflicts |
| `COMMODITY` | Food, energy, raw materials |
| `STRUCTURAL` | Long-term shifts in how the world works |
| `DECISION` | Source 4 personal investment decisions |

---

### Step 5.4 — Tag freshness (critical for honest scoring)

Markets price genuinely new information in seconds. By the time news reaches a daily feed, the move has usually already happened.

- **FRESH** — event announced today, or future event not yet priced
- **STALE** — news reports something that already happened and already moved the price

Rules:
- Brew Markets is a recap of the prior session → default to STALE
- When unsure, mark STALE (better to under-score than score noise)
- STRUCTURAL and DECISION dots: leave blank (never same-day predictions)

---

### Step 5.5 — Push long-form articles to NotebookLM

**Qualifies:** Score 3 only, full article URL accessible (not paywalled)

For each qualifying URL:
1. Find or create notebook `"Investing News — YYYY-MM"`:
   ```bash
   notebooklm list --json
   notebooklm create "Investing News — YYYY-MM" --json
   ```
2. Add as source:
   ```bash
   notebooklm source add "[URL]" --notebook [id] --json
   ```
3. Don't wait for processing — fire and continue

One notebook per month prevents any single notebook from becoming too large.

---

### Step 6 — Snapshot prices by news type

Fetch a 5-day window to get the most recent **completed daily close** (not `regularMarketPrice` which is intraday):
```
https://query1.finance.yahoo.com/v8/finance/chart/{TICKER}?interval=1d&range=5d
```

| News Type | Prices to snapshot |
|-----------|-------------------|
| `COMPANY` | That company's stock + QQQ |
| `SECTOR` | Relevant sector ETF (SOXX for chips, XLK for tech) |
| `MACRO` | SPY + VIX + XAUUSD |
| `GEOPOLITICAL` | SPY + VIX + XAUUSD |
| `COMMODITY` | The commodity (GC=F for gold, CL=F for oil) + SPY |
| `STRUCTURAL` | SPY + QQQ + named sector ETF |
| `DECISION` | Ticker acted on + QQQ |

**These prices are the baseline — /digest scores the reaction tomorrow.** At daily run time the US market hasn't opened yet; today's full session closes overnight and is scored by tomorrow's digest.

---

### Step 7 — Write vault output

```markdown
# News Dots — YYYY-MM-DD

## High Relevance (Score 3)

### "[Dot sentence]"
- **Type:** COMPANY
- **Freshness:** FRESH (scored by /digest) / STALE (already priced in — not scored)
- **Source:** longtundiary.com
- **Price snapshot:**
  | Ticker | Prior Close | Latest | Reaction % | 52w Range |
  |--------|-------------|--------|------------|-----------|
  | NVDA   | $XXX        | $XXX   | +1.2%      | $400–$950 |

---

## Decision Study (ลงทุน Diary Substack)

### "[Decision] because [reasoning]"
- **Type:** DECISION
- **What he did:** trimmed / added / held / changed thesis
- **His reasoning:** [the WHY]
- **Price snapshot:** [ticker] $XXX | QQQ $XXX

---

## Sources checked
- longtundiary.com JSON — ok / failed
- Brew Markets — ok / failed
- The Diff — ok / failed
- Substack — ok / failed
```

**ALWAYS write the dots file**, even if no qualifying news. At minimum, write the watchlist price snapshot (Step 7.5) with a note "No FRESH dots today — all news was a recap of prior session."

---

### Step 7.5 — Daily watchlist price snapshot

Read `vault/watchlist.md`. For each ticker + fixed benchmarks (SPY, QQQ, GC=F, ^VIX, CL=F), fetch and append:

```markdown
## Daily Prices

### Watchlist
| Ticker | Price | Day % |
|--------|-------|-------|

### Benchmarks
| Ticker | Price | Day % |
|--------|-------|-------|
| SPY    | $XXX  | +X%   |
| QQQ    | $XXX  | +X%   |
| GC=F   | $XXX  | +X%   |
```

---

## Rules

- ALWAYS write the dots file — pipeline health checks depend on this file existing
- Never save a Dot that is just a price movement or earnings beat
- Never invent prices — only record what Yahoo Finance returns
- Keep each Dot to one sentence maximum
- This skill does NOT make buy/sell recommendations
- STRUCTURAL dots are the most valuable long-term — never discard them
