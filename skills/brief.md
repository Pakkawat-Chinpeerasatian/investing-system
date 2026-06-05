# /brief — Company Research Card

**Trigger:** `/brief NVDA` or `/brief "Taiwan Semiconductor"`
**Output:** `vault/companies/TICKER.md` + NotebookLM company notebook

---

## Rule #1: Never use AI memory for financial numbers

Every revenue figure, margin, EPS, price, and ratio must be fetched from a real source at run time. Cite the URL. If data is unavailable, write "Data unavailable — check [source] manually."

---

## Step-by-Step SOP

### Step 1 — Resolve ticker + check existing

1. If input is a company name, resolve the ticker: `WebSearch: "[company name] stock ticker symbol"`
2. Check if `vault/companies/[TICKER].md` already exists → ask "Update existing brief?"

---

### Step 2 — Check NotebookLM for prior research

```bash
notebooklm list --json
```

If a per-company notebook `"[TICKER] — [Company Name]"` exists:
```bash
notebooklm ask "Summarize everything known about [company] — business model, financials, competitive position, risks"
```
Use the summary to enrich Step 4.

---

### Step 3 — Fetch current price

```
https://query1.finance.yahoo.com/v8/finance/chart/[TICKER]?interval=1d&range=1d
```

Extract: current price, day %, 52-week high/low, market cap.

---

### Step 4 — Research the 10 sections

#### 1 — Business Overview
What does the company do (2 sentences)? Who are their customers?
Source: investor relations page or Wikipedia.

#### 2 — Revenue Growth
Revenue for last 3 years (YoY growth %). Accelerating or decelerating?
Source: Macrotrends `https://www.macrotrends.net/stocks/charts/[TICKER]/[name]/revenue`

#### 3 — Margins
Gross margin % and operating margin % for last 3 years. Expanding or contracting?
Source: Macrotrends gross-profit-margin chart.

#### 4 — Free Cash Flow
FCF for last 2 years. FCF margin (FCF / Revenue). Generating cash or burning it?
Source: Macrotrends or Yahoo Finance financials.

#### 5 — Debt
Total debt, debt-to-equity ratio. Can they service it comfortably?
Source: Macrotrends balance sheet.

#### 6 — Valuation
P/E (if profitable) or P/S (if not). Compare vs 5-year historical average and 2 sector peers.
Source: Yahoo Finance or Macrotrends P/E chart.

#### 7 — Competition & Moat
Who is the #1 competitor? What is the main differentiation? Is the moat strengthening or weakening?
Source: `WebSearch: "[TICKER] vs competitors moat analysis [year]"`

#### 8 — Bull vs Bear
3 data-supported bullets each.

#### 9 — Thesis Killers
"What would have to be true for this thesis to be completely wrong?"

#### 10 — Questions Before Buying
5 specific questions to answer before putting real money in.

---

### Step 5 — The Index Fund Test (mandatory)

> "Why own [TICKER] instead of just buying VOO (S&P 500 index fund)?"

Acceptable: "VOO doesn't give concentrated exposure to [specific thesis]"
Unacceptable: "It could go up" / "Everyone is talking about it"

If there is no good answer: write "No compelling reason over VOO found." That is honest research, not a failure.

---

### Step 6 — Price snapshot at research time

| Ticker | Price | Day % | 52w Range | Market Cap |
|--------|-------|-------|-----------|-----------|
| [TICKER] | $XXX | +X% | $X–$X | $XXXb |
| QQQ | $XXX | +X% | — | — |
| SPY | $XXX | +X% | — | — |

---

### Step 7 — Save to vault

`vault/companies/[TICKER].md` — structured brief with all 10 sections, sources list, index fund test, and price context.

---

### Step 8 — Update NotebookLM company notebook

```bash
# Create if doesn't exist
notebooklm create "[TICKER] — [Company Name]" --json

# Add investor relations page as source
notebooklm source add "https://[company IR page]" --notebook [id] --json
```

Save the notebook ID in the vault file.

---

## Rules

- Never state a financial number without citing the source URL
- ETFs (VOO, QQQ) get a simplified brief — skip competition/moat, focus on holdings, expense ratio, historical returns
- This skill does NOT make buy/sell recommendations — it organizes facts for a human decision
