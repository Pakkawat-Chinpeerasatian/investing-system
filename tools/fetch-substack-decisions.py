#!/usr/bin/env python3
"""Backfill ลงทุน Diary's Substack INVESTMENT-DECISION posts into the vault.

His Substack is mostly an AI-workflow diary; only a few posts are real
stock/decision content. This pulls the full text of the ones given in
DECISION_SLUGS and dumps clean text so the decision notes can be written.

Usage:  PYTHONUTF8=1 python investing/tools/fetch-substack-decisions.py
Output: prints clean article text per post (manual write-up into vault).
"""
import json
import re
import sys
import time
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE = "https://longtundiary.substack.com/api/v1/posts/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
}

# Only the genuine investment-decision posts. Add slugs here as new ones appear.
DECISION_SLUGS = [
    "intel-part1",          # Intel — what went wrong (5 mistakes, moat erosion)
    "intel-now-or-never-2",  # Intel — is now the time? (the actual decision)
    "moat",                  # "Moat may not be enough" — how he judges durability
]


def strip_html(html: str) -> str:
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html or "", flags=re.S)
    html = re.sub(r"</p>|</li>|<br[^>]*>", "\n", html)
    html = re.sub(r"<[^>]+>", " ", html)
    html = (html.replace("&nbsp;", " ").replace("&amp;", "&")
                .replace("&lt;", "<").replace("&gt;", ">").replace("&#39;", "'"))
    html = re.sub(r"[ \t]+", " ", html)
    html = re.sub(r"\n\s*\n+", "\n\n", html)
    return html.strip()


def main():
    for slug in DECISION_SLUGS:
        try:
            req = urllib.request.Request(BASE + slug, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as r:
                d = json.load(r)
            post = d.get("post", d)
            title = post.get("title", "")
            date = (post.get("post_date") or "")[:10]
            text = strip_html(post.get("body_html") or "")
            print("=" * 70)
            print(f"DATE: {date}")
            print(f"TITLE: {title}")
            print(f"URL: https://longtundiary.substack.com/p/{slug}")
            print("-" * 70)
            print(text)
            print()
        except Exception as e:
            print(f"[FAIL] {slug}: {e!r}")
        time.sleep(0.4)


if __name__ == "__main__":
    main()
