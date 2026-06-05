# /why — Weekly "Why Did It Move?" Investigator

**Trigger:** Auto Sundays 18:00 (after week's digests), or manual `/why`
**Output:** `vault/whys/YYYY-MM-DD-why.md` + lessons appended to `vault/mistakes-log.md`

---

## ⚠️ The one rule that matters most

Most small daily moves have NO clean cause — they are noise. **"No clear cause — likely noise" is a correct, respected verdict.** Use it freely. Never manufacture a story to fill the report.

---

## Step-by-Step SOP

### Step 1 — Load the week's data

Read last 7 days of:
- `vault/digests/[date]-evening.md` — ✓/✗/~ results + % moves
- `vault/dots/[date].md` — underlying news + price snapshots

If fewer than 2 digests exist: output "Not enough digests this week" and exit.

---

### Step 2 — Select investigation candidates (cap at 5)

Investigate if ANY of these is true:
1. **Big miss:** ✗ unexpected AND |move| ≥ 1.5%
2. **Repeat miss:** same news-type + wrong-direction appears 2+ times this week
3. **Notable match (max 1):** one strong ✓ (≥ 1.5%) worth confirming to learn what worked

Skip: all `~` flat moves, sub-1.5% one-off ✗, STRUCTURAL/DECISION dots.

If nothing qualifies: write "Quiet week — no meaningful misses" and exit. That is a good outcome.

---

### Step 3 — Form candidate causes

For each move, test these before researching:

| Candidate | How to test |
|-----------|-------------|
| Already priced in | Did price move in prior days? Check prior dot snapshots |
| Bigger story dominated | Find the dominant market event that day (Fed, jobs, mega-cap earnings) |
| Classification was wrong | Re-read dot — was the news type label correct? |
| News was minor | Headline sounded big but markets didn't care |
| Just noise | No identifiable cause — valid verdict |

---

### Step 4 — Research each move

```
WebSearch: "stock market [YYYY-MM-DD] why did markets move"
WebSearch: "[ticker or sector] news [YYYY-MM-DD]"
WebSearch: "[date] Fed OR jobs report OR CPI OR earnings major market event"
```

Evidence standard:
- "Bigger story dominated" → only valid if you find that story AND price moved in line with IT
- "Already priced in" → requires prior snapshots to show the move happened before the news date
- If nothing fits → **verdict is noise**

---

### Step 5 — Verdict + confidence

- **HIGH** — direct evidence found
- **MEDIUM** — plausible and partly supported
- **LOW** — hypothesis only (not written to mistakes log)
- **NOISE** — no identifiable cause (valid result)

---

### Step 6 — Save report

`vault/whys/YYYY-MM-DD-why.md`:

```markdown
# Weekly Why-Report — week ending YYYY-MM-DD

## Top Finding
[ONE sentence — the single most useful explanation, or "Quiet week."]

## Investigated [N] moves

### 1. [ticker] ±X.X% on [date] — [news type], marked ✗
- **Expected:** [direction table prediction]
- **What happened:** [cause found or "no clear cause"]
- **Verdict:** [cause] — Confidence: [HIGH/MED/LOW/NOISE]
- **Lesson:** [one line, or "none — this was noise"]

## Honest noise count
[X] of [N] investigated moves had no identifiable cause.
```

Append only MEDIUM+ lessons to `vault/mistakes-log.md`:
```markdown
## YYYY-MM-DD (from /why)
- [Lesson text]
```

---

## Rules

- Noise is a valid verdict — never invent causation
- "Bigger story" / "priced in" requires evidence or it becomes noise
- Only MEDIUM+ findings become lessons in mistakes-log
- This skill gives NO buy/sell signals — it builds understanding of WHY prices react
