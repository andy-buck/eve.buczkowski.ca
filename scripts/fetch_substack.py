"""Copy the latest Substack posts into _data/posts.yml so the homepage can show them.

Runs on every publish and once a night, from .github/workflows/pages.yml.
Uses only the Python standard library.
"""
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path

FEED = "https://evetbuczkowski.substack.com/feed"
OUT = Path(__file__).resolve().parent.parent / "_data" / "posts.yml"
MAX_POSTS = 6

req = urllib.request.Request(FEED, headers={"User-Agent": "eve.buczkowski.ca feed sync"})
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        root = ET.fromstring(resp.read())
except Exception as err:  # keep the old posts if Substack is unreachable
    print(f"Could not read feed, leaving posts unchanged: {err}")
    sys.exit(0)

posts = []
for item in root.iter("item"):
    enclosure = item.find("enclosure")
    subtitle = re.sub(r"<[^>]+>", "", item.findtext("description") or "").strip()
    posts.append({
        "title": (item.findtext("title") or "").strip(),
        "url": (item.findtext("link") or "").strip(),
        "date": parsedate_to_datetime(item.findtext("pubDate")).strftime("%Y-%m-%d"),
        "subtitle": subtitle or None,
        "image": enclosure.get("url") if enclosure is not None else None,
    })
    if len(posts) == MAX_POSTS:
        break

# JSON is valid YAML, and avoids needing a YAML library.
OUT.write_text("# Filled in automatically from Substack each time the site publishes. No need to edit.\n"
               + json.dumps(posts, indent=2, ensure_ascii=False) + "\n")
print(f"Wrote {len(posts)} posts")
