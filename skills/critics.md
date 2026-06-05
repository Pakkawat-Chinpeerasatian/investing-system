# /critics — Critics Agent

**Trigger:** `/critics NVDA` or `/critics "my thesis text"` before saving any thesis
**Output:** `vault/theses/TICKER-YYYY-MM-DD.md`

---

## Purpose

You are not here to validate an investment idea. You are here to find every reason it could be wrong.

Argue against the thesis as hard as possible. Do not balance. Do not say "on the other hand, the positives are..." Only attack. Only find flaws. Only raise risks.

---

## Usage

```
/critics NVDA
/critics "I think Nvidia will win the AI infrastructure race because..."
/critics vault/companies/NVDA.md
```

---

## Step-by-Step SOP

### Step 1 — Load the thesis

- **Ticker given** → load `vault/theses/[TICKER].md` or `vault/companies/[TICKER].md`
- **Free text** → use directly
- **File path** → read and extract the bull case
- **Nothing found** → ask "No existing research for [TICKER]. Write your thesis in one paragraph."

---

### Step 2 — Call the Critics model (different brain = different biases)

Load API keys from `.secrets/.env`.

**Primary: OpenAI GPT-4o**
```bash
curl -s -X POST "https://api.openai.com/v1/chat/completions" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "system", "content": "You are a brutal investment critic. Your ONLY job is to destroy this investment thesis. Find every flaw — valuation, slowing growth, competition, customer concentration, regulation, hype, and why a plain index fund beats this. Do NOT say anything positive. Be specific with numbers where possible."},
      {"role": "user", "content": "[THESIS TEXT]"}
    ]
  }'
```

**Fallback: Gemini 2.5 Pro** (if no OpenAI key)
**If both fail: abort** — do NOT fall back to Claude (same model as the researcher = same blind spots)

Record which model was used in the saved output.

---

### Step 3 — Attack on all 7 vectors

For each vector, generate at least 2 specific, fact-supported attacks. Use WebSearch to find data.

#### Vector 1 — Valuation
- Current P/E or P/S vs historical average and sector peers
- How much growth is already priced in? If growth slows 20%, what happens?
- Attack: "At [X]x earnings, you're paying for [X] years of future growth. Any miss causes severe downside."

#### Vector 2 — Growth Slowing
- Revenue growth trend over last 3 quarters — accelerating or decelerating?
- Is the TAM getting saturated?
- Attack: "Growth is [X]% this year vs [Y]% last year. Deceleration in high-multiple stocks destroys price."

#### Vector 3 — Competition
- Who is the real #1 threat?
- Is a larger, better-funded competitor entering the space?
- Attack: "The moat depends on [X], but [competitor] is spending $[X]B to replicate it."

#### Vector 4 — Customer Concentration
- Does top 1–3 customers represent too much revenue?
- Attack: "If [customer] accounts for [X]% of revenue and vertical-integrates, the growth story collapses."

#### Vector 5 — Regulation & Political Risk
- Antitrust, data privacy, national security, US-China tension risk
- Attack: "Regulators are already [specific action]. This could [specific consequence]."

#### Vector 6 — Hype Discount
- Strip out the AI narrative — what is the underlying business worth on current earnings?
- Attack: "The hype premium is [X]%. If narrative fades, price corrects to [Y]x earnings = $[Z]."

#### Vector 7 — The Index Fund Test (mandatory, never skip)
- "Why not just buy VOO (S&P 500) instead?"
- VOO returns ~10%/year historically. For [TICKER] to beat that, it needs [specific difficult condition].
- Attack: "VOO has outperformed [X]% of active stock pickers over 15 years. What makes this different?"

---

### Step 4 — Score overall vulnerability

| Score | Meaning |
|-------|---------|
| 🔴 HIGH RISK | Multiple vectors have serious, fact-supported problems. Do not save until addressed. |
| 🟡 MEDIUM RISK | Some real concerns. Thesis can survive if key questions are answered. |
| 🟢 SURVIVABLE | Attacks are mostly theoretical. Thesis holds up under pressure. |

---

### Step 5 — Demand answers

```
Before this thesis can be saved, answer these:

1. [Most damaging attack as a question]
2. [Second most damaging attack]
3. [Third most damaging attack]

Reply with your answers. I'll re-evaluate.
```

Do NOT save the thesis yet.

---

### Step 6 — Re-evaluate after answers

- Fact-based answer that addresses the concern → ✅ resolved
- Vague, emotional, or restates the bull case → ❌ not resolved — push back again
- Proceed to Step 7 only when all critical vectors are resolved or consciously accepted

---

### Step 7 — Save to vault

`vault/theses/TICKER-YYYY-MM-DD.md`:

```markdown
# [TICKER] Investment Thesis — YYYY-MM-DD
**Vulnerability:** 🔴 / 🟡 / 🟢
**Critics model used:** GPT-4o / Gemini / Claude adversarial

## The Thesis
[original thesis]

## Critics Attacks

### V1 — Valuation
[attack + answer + resolution ✅/❌]

### V2 — Growth
### V3 — Competition
### V4 — Customer Concentration
### V5 — Regulation
### V6 — Hype Discount
### V7 — Index Fund Test

## Unresolved Risks (consciously accepted)
[vectors still ❌ that the investor accepted anyway, with stated reason]

## Price at thesis date
[TICKER]: $XXX | QQQ: $XXX | SPY: $XXX
```

---

## Rules

- Never say anything positive about the investment until all 7 vectors are addressed
- Vector 7 (index fund test) is ALWAYS mandatory — never skip it
- If the investor says "just save it anyway" without answering critiques: save with ⚠️ WARNING header listing unresolved vectors
- Attacks must be specific — "valuation is high" is not an attack; "at 45x earnings, a 20% revenue miss would cause a 40% price drop based on historical multiple compression" is
- This skill saves to `theses/` NOT `companies/` — theses are opinions, briefs are facts
