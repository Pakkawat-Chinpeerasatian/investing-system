# AI Investing Pipeline

An automated investing research and analysis pipeline built with Claude Code and Anthropic Routines. The system transforms daily news into structured investment signals, tracks patterns over time, and applies rigorous adversarial checks before any thesis is saved.

**Status:** Active — knowledge-building phase (no live trades)

---

## Pipeline Overview

```
DAILY (auto, 17:45)
──────────────────────────────────────────────────
/news-filter
  → Fetches longtundiary.com + Brew Markets + The Diff
  → Scores articles 1–3 by relevance
  → Applies durability filter → extracts Dots
  → Classifies by type: COMPANY / SECTOR / MACRO / GEOPOLITICAL / COMMODITY
  → Snapshots relevant prices (stock, sector ETF, SPY, VIX, gold)
  → Pushes long-form articles to NotebookLM for deep storage

/digest
  → Reads today's dots
  → Checks: did prices move in the direction the news type predicted?
  → Flags any watchlist companies mentioned in today's news
  → Spots building multi-day themes (3+ consecutive same-type dots)

WEEKLY (auto, Sunday 18:00)
──────────────────────────────────────────────────
/why
  → Reviews the week's price-vs-news misses and matches
  → WebSearches what actually happened on notable days
  → Tests candidate causes, rates confidence
  → Logs confirmed lessons (explicitly allowed to conclude "noise")

MONTHLY (auto, 1st of month 08:00)
──────────────────────────────────────────────────
/pattern-report
  → Reads all dots from the previous month
  → Groups by news type, computes average price reactions
  → Identifies strongest patterns (e.g., GEOPOLITICAL → gold +0.9%)
  → Audits old dots against the durability filter

ON DEMAND
──────────────────────────────────────────────────
/brief TICKER   → 10-section company research card (fetches real financials, no AI memory)
/critics TICKER   → Adversarial attack on thesis — refuses to say anything positive
/predict-sandbox → Paper trading log — track predictions before real capital
```

---

## Key Design Principles

**durability filter** — Only save news dots and theses that will still be valid in 2 years. Discard quarterly noise, short-term sentiment, and earnings surprises.

**No AI Memory for Numbers** — Every financial figure (revenue, margins, EPS, price) is fetched from a live source (Yahoo Finance, Macrotrends, SEC EDGAR) at research time. The AI never recalls numbers from training.

**Adversarial Gate** — Every thesis must pass `/critics` before being saved. The critics agent attacks on 7 vectors: valuation, growth slowdown, competition, customer concentration, regulation, hype, and "why not just buy an index fund?"

**Different Model = Different Biases** — `/critics` uses a different model family (Gemini or GPT-4o) by design. Same-model critique produces same-model blind spots.

---

## Automation Architecture

All scheduled runs use **Anthropic Routines** (cloud-hosted agents) rather than local cron jobs. The routines are live and running.

| Routine | Schedule | Model |
|---------|----------|-------|
| Investing-Daily | 10:45 UTC daily (17:45 Bangkok) | claude-sonnet-4-6 |
| Investing-Weekly | 11:00 UTC Sunday (18:00 Bangkok) | claude-sonnet-4-6 |
| Investing-Monthly | 01:00 UTC 1st of month (08:00 Bangkok) | claude-sonnet-4-6 |

Each routine runs in Anthropic's cloud, clones the private workspace repo, executes the relevant skill, and commits outputs back. A background hourly `git pull` in the local dashboard syncs the results down.

---

## Repository Structure

```
investing-system/
  README.md             ← this file
  pipeline-design.md    ← full pipeline architecture document
  skills/
    news-filter.md      ← daily news dot extractor SOP
    digest.md           ← evening price check SOP
    why.md              ← weekly investigator SOP
    pattern-report.md   ← monthly pattern analysis SOP
    brief.md            ← company research card SOP
    critics.md            ← adversarial thesis attacker SOP
    predict-sandbox.md  ← paper trading log SOP
  tools/
    fetch-longtun-news.py      ← longtundiary.com news JSON fetcher
    fetch-price-history.py     ← Yahoo Finance price history fetcher
    fetch-substack-decisions.py← Substack decision diary fetcher
    compute-reaction.py        ← news-type → price-reaction calculator
```

---

## Skills (Slash Commands)

| Skill | Trigger | Output Location |
|-------|---------|-----------------|
| `/news-filter` | Daily auto | `vault/dots/YYYY-MM-DD.md` |
| `/digest` | Daily auto | `vault/digests/YYYY-MM-DD-evening.md` |
| `/why` | Weekly auto | `vault/why/YYYY-MM-DD-why.md` |
| `/pattern-report` | Monthly auto | `vault/patterns/YYYY-MM-pattern-report.md` |
| `/brief TICKER` | On demand | `vault/companies/TICKER.md` |
| `/critics TICKER` | On demand | `vault/theses/TICKER-YYYY-MM-DD.md` |

---

## Tools

Python utilities called by skills during automated runs:

- **fetch-longtun-news.py** — hits `longtundiary.com/data/news.json` directly (pre-filtered AI-curated feed from Bloomberg/Reuters/CNBC). Falls back to Substack RSS.
- **fetch-price-history.py** — Yahoo Finance yfinance wrapper, returns OHLCV data
- **fetch-substack-decisions.py** — parses Substack RSS for decision diary entries
- **compute-reaction.py** — given a news type and date, fetches same-day and next-day % changes for SPY, QQQ, VIX, gold, sector ETF

---

## Tech Stack

| Component | Tool |
|-----------|------|
| Agent framework | Claude Code (CLI) + SKILL.md SOPs |
| Scheduling | Anthropic Routines (RemoteTrigger API) |
| Knowledge storage | Obsidian-format `.md` vault |
| Long-form article storage | Google NotebookLM |
| Price data | Yahoo Finance (yfinance) |
| Adversarial model | Gemini 2.5 Pro → GPT-4o → Claude fallback |
| Dashboard | FastAPI + local server |
