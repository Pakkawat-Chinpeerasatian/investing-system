"""
fetch-longtun-news.py
Fetches longtundiary.com/data/news.json directly.
Outputs JSON array of today's (and optionally yesterday's) headlines to stdout.
Falls back to Substack RSS if JSON endpoint is blocked.

Usage:
    python fetch-longtun-news.py            # today only
    python fetch-longtun-news.py --days 3   # last 3 days
"""

import sys
import json
import urllib.request
import urllib.error
from datetime import date, timedelta

# force UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

LONGTUN_JSON = "https://www.longtundiary.com/data/news.json"
SUBSTACK_RSS  = "https://longtundiary.substack.com/feed"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer":    "https://www.longtundiary.com/news",
    "Accept":     "application/json, */*",
}

def fetch_json():
    req = urllib.request.Request(LONGTUN_JSON, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))

def fetch_substack_fallback():
    """Returns minimal headline list from Substack RSS."""
    import xml.etree.ElementTree as ET
    req = urllib.request.Request(SUBSTACK_RSS, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        tree = ET.fromstring(r.read())
    items = tree.findall(".//item")
    return [{"title": i.findtext("title",""), "bullets": [i.findtext("description","")],
             "category": "B", "source": "Substack"} for i in items[:5]]

def main():
    days_back = 1
    if "--days" in sys.argv:
        idx = sys.argv.index("--days")
        days_back = int(sys.argv[idx + 1])

    try:
        data = fetch_json()
        all_days = data.get("days", [])
        updated = data.get("updated", "")

        # collect headlines from requested date range
        results = []
        for day_entry in all_days[:days_back]:
            for h in day_entry.get("headlines", []):
                results.append({
                    "date":     day_entry.get("date", ""),
                    "ticker":   h.get("ticker", ""),
                    "blurb":    h.get("blurb", ""),
                    "emoji":    h.get("emoji", ""),
                    "category": h.get("category", "B"),  # A=top, B=medium, C=context
                    "source":   "longtundiary",
                })

        print(json.dumps({
            "source":  "longtundiary.com/data/news.json",
            "updated": updated,
            "count":   len(results),
            "items":   results,
        }, ensure_ascii=False, indent=2))

    except Exception as e:
        # fallback to Substack
        sys.stderr.write(f"JSON endpoint failed ({e}), falling back to Substack RSS\n")
        try:
            items = fetch_substack_fallback()
            print(json.dumps({
                "source":  "substack_fallback",
                "updated": str(date.today()),
                "count":   len(items),
                "items":   items,
            }, ensure_ascii=False, indent=2))
        except Exception as e2:
            print(json.dumps({"error": str(e2), "items": []}))

if __name__ == "__main__":
    main()
