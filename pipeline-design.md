# Investing Pipeline — Full Design
**Drafted:** 2026-05-31
**Goal:** From morning news → dots → price context → pattern recognition → investment readiness

---

## The Big Picture

```
EVERY DAY
─────────────────────────────────────────────────────────────
Morning (auto)     /news-filter
                       ↓ dots + prices + NotebookLM articles

Evening (auto)     /digest
                       ↓ what moved today, did news type predict it?
                       ↓ flag any watchlist companies in today's news

─────────────────────────────────────────────────────────────
EVERY WEEK
─────────────────────────────────────────────────────────────
Sunday (manual)    Weekly chart practice → patterns/YYYY-MM-DD.md
                       ↓ one chart, one observation

─────────────────────────────────────────────────────────────
EVERY MONTH
─────────────────────────────────────────────────────────────
1st of month       /pattern-report
(auto or manual)       ↓ read all dots from last month
                       ↓ group by news type
                       ↓ compare to price movements
                       ↓ answer: is the durability filter filtering correctly?
                       ↓ what news type → what market reaction?

─────────────────────────────────────────────────────────────
ON DEMAND
─────────────────────────────────────────────────────────────
Anytime            /brief TICKER    → 10-section research card
                   /critics TICKER    → GPT-4o attacks your thesis

─────────────────────────────────────────────────────────────
EVERY QUARTER
─────────────────────────────────────────────────────────────
Manual review      Are old dots still valid? (durability filter check)
                   Watchlist: any theses strengthened or broken?
                   Paper trading: am I beating VOO or not?

─────────────────────────────────────────────────────────────
MILESTONE: WHEN YOU HAVE CAPITAL
─────────────────────────────────────────────────────────────
/readiness-check   Pulls all theses, dots, mistakes-log, paper
                   trading vs VOO, and answers:
                   "Are you ready to invest real money?"
```

---

## New Skills Needed

### 1. `/digest` — Evening Summary (daily, auto)

**When:** Runs each evening at ~20:00 (after market close)

**What it does:**
1. Reads today's dots file (`dots/YYYY-MM-DD.md`)
2. For each dot with a price snapshot, checks current end-of-day price:
   - Did the price move in the direction the news type would predict?
   - e.g. GEOPOLITICAL dot → did VIX rise? Did gold rise?
3. Scans today's dots for any company that appears in `watchlist.md` or `companies/` → flags it
4. Compares today's dot types to yesterday's and last week's:
   - Is a theme building? (3 consecutive SECTOR dots about chip shortage = trend)
5. Saves to `Pakkawat-Vault/investing/digests/YYYY-MM-DD-evening.md`

**Output format:**
```
## Evening Digest — [date]

### Price vs News Check
- GEOPOLITICAL dot about [X] → VIX +2.1% ✓ (expected) | Gold +0.8% ✓
- SECTOR dot about [Y] → SOXX -1.2% ✓ (expected)
- MACRO dot about [Z] → SPY unchanged ✗ (unexpected — note this)

### Watchlist Mentions Today
- NVDA appeared in Morning Brew (score 3) → check brief

### Building Themes (3+ days)
- MACRO: 4 consecutive days of interest rate / inflation dots
  → bond yields rising → watch effect on growth stocks

### Tomorrow: nothing special flagged
```

---

### 2. `/pattern-report` — Monthly Analysis (1st of each month, auto)

**When:** 1st of every month, auto-triggered

**What it does:**
1. Reads ALL dots from the previous month (`dots/YYYY-MM-*.md`)
2. Groups dots by news type: COMPANY / SECTOR / MACRO / GEOPOLITICAL / COMMODITY / STRUCTURAL
3. For each type, pulls all price snapshots from those days
4. Calculates: when this news type appeared, what did SPY / VIX / gold / QQQ do on average?
5. Identifies strongest patterns — e.g.:
   - "GEOPOLITICAL dots → gold +avg 0.9% same day, SPY -avg 0.6%"
   - "SECTOR (chips) dots → SOXX moved +/-2% within 3 days"
6. Checks if any durability filter dots from 6+ months ago have proven right or wrong (if old enough data exists)
7. Saves to `Pakkawat-Vault/investing/patterns/YYYY-MM-pattern-report.md`
8. Pushes to NotebookLM "Pattern Reports" notebook for long-term querying

**Output format:**
```
## Monthly Pattern Report — [YYYY-MM]

### Dot Volume
- Total dots saved: [X]
- By type: COMPANY(X) SECTOR(X) MACRO(X) GEOPOLITICAL(X) STRUCTURAL(X)

### News Type → Price Reaction Patterns
| News Type | Sample Size | SPY avg | VIX avg | Gold avg | QQQ avg |
|-----------|------------|---------|---------|---------|---------|
| GEOPOLITICAL | 4 events | -0.6% | +8.2% | +0.9% | -0.8% |
| MACRO (rates) | 6 events | -0.3% | +3.1% | +0.4% | -0.5% |
| SECTOR (AI)  | 8 events | +0.2% | -1.0% | flat  | +1.1% |

### Strongest Pattern This Month
"[News type] consistently moved [price] by [amount]. High confidence — [X] data points."

### Weakest / Noise
"[News type] showed no consistent price pattern. May need more data."

### durability filter Audit (if 6+ months of data)
Old dots that proved RIGHT: [list]
Old dots that proved WRONG: [list] → remove or flag in vault

### Recommendation for Next Month
- Keep watching: [sector/theme]
- Pattern worth testing with paper trades: [idea]
```

---

### 3. `/readiness-check` — Investment Readiness (on demand)

**When:** Run when considering opening a real brokerage account or making first real trade

**What it does:**
1. Reads `foundation.md` — legal eligibility, emergency fund, debt
2. Reads `IPS.md` — rules still valid?
3. Counts: months of daily dots collected
4. Counts: number of critics-reviewed theses in `theses/`
5. Reads `mistakes-log.md` — recurring patterns in mistakes?
6. Reads paper trading dashboards — are you beating VOO on paper?
7. Asks NotebookLM: "Based on all stored research, which of Pakkawat's theses are strongest?"
8. Outputs a readiness score: Not Ready / Almost / Ready

---

## Agentic OS Integration Points

### 1. Morning automation (Agentic OS cron — Phase 9)
Add to the OS morning routine (after current tasks):
```
08:00  /news-filter    → runs automatically, no input needed
```

### 2. Evening automation (Agentic OS cron — Phase 9)
Add to OS evening routine:
```
20:00  /digest         → runs automatically after market close
```

### 3. Monthly automation (Agentic OS cron)
```
01 08:00 each month    /pattern-report
```

### 4. Dashboard integration (Codex build)
Add to the Agentic OS dashboard:

| Widget | What it shows |
|--------|--------------|
| News streak | Days in a row /news-filter ran (habit tracker) |
| Last digest | Date + top finding from last evening digest |
| Dots this month | Running count |
| Top pattern so far | Strongest news→price pattern found |
| Watchlist alerts | Companies flagged in news this week |
| Readiness bar | Progress toward investment readiness (% of checklist done) |

### 5. Memory-keeper awareness (add to session start)
The memory-keeper should load at session start:
- Last pattern report summary
- Any watchlist alerts from this week's digests
- Current readiness score

---

## Full Data Flow (compounding over time)

```
Day 1–7:    Dots accumulate → no patterns yet, just data
Day 30:     First pattern-report → weak patterns, small sample
Day 90:     Patterns emerge → GEOPOLITICAL → gold reliable
Day 180:    durability filter audit possible → which dots aged well?
Day 365:    Full year of data → strong pattern confidence
            → paper trading history available for VOO comparison
            → /readiness-check gives meaningful answer
```

This is why it's a pipeline, not just tools. Each day adds to the data.
The system gets smarter as you use it — not because AI learns, but because you accumulate real evidence.

---

## Build Order for Codex

**Phase A — Automation wiring (after manual system works)**
1. Add `/news-filter` to Agentic OS morning cron (08:00)
2. Add `/digest` skill + add to evening cron (20:00)
3. Add `/pattern-report` skill + add to monthly cron (1st of month 08:00)

**Phase B — Dashboard widgets**
4. Add investing widgets to Agentic OS dashboard (habit streak, last digest, top pattern, readiness bar)

**Phase C — Advanced**
5. Build `/readiness-check` skill
6. Add memory-keeper investing context to session start protocol
