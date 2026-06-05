#!/usr/bin/env python3
"""Compute the close-to-close reaction for /digest, using COMPLETED daily bars only.

Why this exists: the digest scores yesterday's news against the first full US
session after it was captured. That requires the two most recent *completed* daily
closes — and an LLM reading a Yahoo JSON by eye can mis-read the timestamps (it has).
This script parses `timestamp[]` with the exchange's own UTC offset, drops any
in-progress bar, and prints the exact close_before / close_after / reaction %.

Usage:
    PYTHONUTF8=1 python investing/tools/compute-reaction.py NVDA QQQ SPY INTC
    PYTHONUTF8=1 python investing/tools/compute-reaction.py NVDA --json

Output (per ticker): the baseline close, the reacting-session close, and the move.
The digest then only needs to apply the expected-direction rule table.
"""
import json
import sys
import time
import urllib.request
from datetime import datetime, timezone, timedelta

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

RANGE = "5d"
INTERVAL = "1d"
MARKET_CLOSE_HOUR = 16  # 16:00 exchange-local = regular session close

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
}


def fetch(ticker: str):
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        f"?interval={INTERVAL}&range={RANGE}"
    )
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.load(resp)
    return data["chart"]["result"][0]


def completed_closes(result):
    """Return [(date_str, close), ...] for COMPLETED daily bars, oldest -> newest.

    A bar is completed if its exchange-local date is before today's exchange-local
    date, OR it is today and the local time is at/after the 16:00 close. The
    exchange's own UTC offset comes from meta.gmtoffset, so this is DST-correct
    without any timezone library.
    """
    meta = result["meta"]
    offset = timedelta(seconds=meta.get("gmtoffset", 0))
    timestamps = result["timestamp"]
    closes = result["indicators"]["quote"][0]["close"]

    now_local = datetime.now(timezone.utc) + offset
    out = []
    for ts, close in zip(timestamps, closes):
        if close is None:
            continue
        bar_local = datetime.fromtimestamp(ts, tz=timezone.utc) + offset
        is_completed = (
            bar_local.date() < now_local.date()
            or (bar_local.date() == now_local.date()
                and now_local.hour >= MARKET_CLOSE_HOUR)
        )
        if is_completed:
            out.append((bar_local.strftime("%Y-%m-%d"), round(close, 4)))
    return out


def reaction(ticker: str):
    result = fetch(ticker)
    bars = completed_closes(result)
    if len(bars) < 2:
        raise ValueError(f"only {len(bars)} completed bar(s) in {RANGE} window")
    (before_date, before), (after_date, after) = bars[-2], bars[-1]
    pct = (after - before) / before * 100
    return {
        "ticker": ticker,
        "close_before": before,
        "before_date": before_date,
        "close_after": after,
        "after_date": after_date,
        "reaction_pct": round(pct, 2),
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv[1:]
    if not args:
        args = ["NVDA", "QQQ", "SPY"]

    results = []
    for ticker in args:
        try:
            r = reaction(ticker)
            results.append(r)
        except Exception as e:
            results.append({"ticker": ticker, "error": str(e)})
        time.sleep(0.4)  # be polite to Yahoo

    if as_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    print(f"{'TICKER':8} {'BASELINE (before)':24} {'REACTING (after)':24} {'MOVE':>8}")
    print("-" * 68)
    for r in results:
        if "error" in r:
            print(f"{r['ticker']:8} ERROR: {r['error']}")
            continue
        before = f"{r['before_date']}  ${r['close_before']}"
        after = f"{r['after_date']}  ${r['close_after']}"
        sign = "+" if r["reaction_pct"] >= 0 else ""
        print(f"{r['ticker']:8} {before:24} {after:24} {sign}{r['reaction_pct']:.2f}%")


if __name__ == "__main__":
    main()
