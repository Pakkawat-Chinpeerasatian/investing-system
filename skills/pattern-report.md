# /pattern-report — Monthly Pattern Analysis

**Trigger:** Auto 1st of each month at 08:00, or manual `/pattern-report`
**Output:** `vault/patterns/YYYY-MM-pattern-report.md` + pushed to NotebookLM

---

## Step-by-Step SOP

### Step 1 — Load last month's data

Read all:
- `vault/dots/[YYYY-MM-]*.md`
- `vault/digests/[YYYY-MM-]*-evening.md`

If fewer than 10 dots total: note "Insufficient data for reliable patterns" but still produce the report.

---

### Step 2 — Build news type → price reaction table

From evening digests, extract all ✓/✗/~ results grouped by news type.

For each news type with 3+ data points, calculate average SPY / VIX / Gold / QQQ moves and hit rate (% moved in expected direction).

Confidence thresholds:
- LOW: < 10 events
- MEDIUM: 10–20 events
- HIGH: 20+ events

---

### Step 3 — Identify strongest and weakest patterns

**Strongest:** highest hit rate with MEDIUM+ confidence
**Weakest/noise:** lowest hit rate, or too few events to judge

---

### Step 4 — durability filter audit (if 6+ months of data exist)

For dots 6+ months old, WebSearch current state:
- ✅ Aged well — still valid, reinforced by events
- ❌ Aged poorly — proven wrong → move to `vault/dots/archived/`
- ⏳ Too early — not enough time to judge

---

### Step 5 — Save pattern report

`vault/patterns/YYYY-MM-pattern-report.md`:

```markdown
# Monthly Pattern Report — YYYY-MM

## Dot Volume
- Total: [X] dots | [X] digests processed
- By type: COMPANY(X) SECTOR(X) MACRO(X) GEOPOLITICAL(X)

## News Type → Price Reaction

| News Type | Events | SPY avg | VIX avg | Gold avg | QQQ avg | Hit Rate | Confidence |
|-----------|--------|---------|---------|---------|---------|---------|-----------|
| GEOPOLITICAL | 4 | -0.6% | +8.2% | +0.9% | -0.8% | 75% | LOW |
| SECTOR/AI | 7 | +0.3% | -1.0% | flat | +1.1% | 86% | MEDIUM |

## Strongest Pattern This Month
"[News type] → [price] moved [direction] [X]% of the time. [X] data points."

## Unexpected Moves Worth Studying
[Any ✗ that appeared multiple times — where market surprised you]

## durability filter Audit
[Only if 6+ months of data exist]
- Aged well ✅: [list]
- Aged poorly ❌: [list — archived]

## Recommendation for Next Month
- Pattern to confirm: [strongest pattern]
- Theme carrying over: [multi-month building theme]
```

---

### Step 6 — Push to NotebookLM

```bash
notebooklm list --json
# find or create "Investing Pattern Reports"
notebooklm source add "vault/patterns/YYYY-MM-pattern-report.md" --notebook [id] --json
```

Over time this notebook answers: "Across all months, what is the most reliable pattern I've found?"

---

## Rules

- Never delete dots without moving to `archived/` first
- LOW-confidence patterns are observations, not rules — never act on them yet
- STRUCTURAL dots are exempt from hit rate calculation
- This skill does NOT give buy/sell signals — it builds pattern awareness
