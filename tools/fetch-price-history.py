#!/usr/bin/env python3
"""Backfill ~6 months of daily closing prices for the watchlist.

This is DISPLAY-ONLY data for the dashboard graphs. It is NOT knowledge —
it lives in dashboard/data/price-history.json, never in the vault.
Re-run anytime to refresh; it overwrites cleanly (no growth over time).

Usage:  PYTHONUTF8=1 python investing/tools/fetch-price-history.py
"""
import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Keep this list in sync with the watchlist. Small on purpose.
TICKERS = {
    "SPY":  "S&P 500",
    "QQQ":  "Nasdaq 100 (tech)",
    "NVDA": "Nvidia",
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "GC=F": "Gold",
    "^VIX": "Fear Index (VIX)",
    "CL=F": "Oil (WTI crude)",
}

RANGE = "6mo"      # keep it modest — enough to see shape, not bloat
INTERVAL = "1d"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
}

OUT = Path(__file__).resolve().parents[2] / "dashboard" / "data" / "price-history.json"


def fetch(ticker: str):
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        f"?interval={INTERVAL}&range={RANGE}"
    )
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.load(resp)
    result = data["chart"]["result"][0]
    timestamps = result["timestamp"]
    closes = result["indicators"]["quote"][0]["close"]
    series = []
    for ts, close in zip(timestamps, closes):
        if close is None:
            continue
        day = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
        series.append({"date": day, "close": round(close, 2)})
    return series


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out = {
        "updated": datetime.now(timezone.utc).isoformat(),
        "range": RANGE,
        "interval": INTERVAL,
        "tickers": {},
    }
    for ticker, name in TICKERS.items():
        try:
            series = fetch(ticker)
            out["tickers"][ticker] = {"name": name, "series": series}
            print(f"[OK] {ticker:6} {name:20} {len(series)} days")
        except Exception as e:
            print(f"[FAIL] {ticker}: {e}")
        time.sleep(0.4)  # be polite to Yahoo
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSaved -> {OUT}")


if __name__ == "__main__":
    main()
