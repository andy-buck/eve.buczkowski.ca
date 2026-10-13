"""Copy the latest Substack posts into _data/posts.yml so the homepage can show them.

Runs on every publish and once a night, from .github/workflows/pages.yml.
Uses only the Python standard library.

Substack blocks requests from GitHub's servers, so if reading the feed live
fails it uses the copy saved in _substack/feed.xml by scripts/update-blog.sh
(run from a home computer, where Substack doesn't block). If both fail,
_data/posts.yml is left as it is (it can be edited by hand).
"""
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path

FEED = "https://evetbuczkowski.substack.com/feed"
ROOT = Path(__file__).resolve().parent.parent
SAVED_FEED = ROOT / "_substack" / "feed.xml"
OUT = ROOT / "_data" / "posts.yml"
MAX_POSTS = 6
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8",
}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=30) as resp:
        return resp.read()


def strip_html(text):
    return re.sub(r"<[^>]+>", "", text or "").strip() or None


def parse_feed(raw):
    # A feed saved from a browser can have a note in front of the XML; skip it.
    root = ET.fromstring(raw[raw.find(b"<rss"):])
    posts = []
    for item in root.iter("item"):
        enclosure = item.find("enclosure")
        posts.append({
            "title": (item.findtext("title") or "").strip(),
            "url": (item.findtext("link") or "").strip(),
            "date": parsedate_to_datetime(item.findtext("pubDate")).strftime("%Y-%m-%d"),
            "subtitle": strip_html(item.findtext("description")),
            "image": enclosure.get("url") if enclosure is not None else None,
        })
    return posts


def live_feed():
    return parse_feed(get(FEED))


def saved_feed():
    return parse_feed(SAVED_FEED.read_bytes())


for source in (live_feed, saved_feed):
    try:
        posts = source()[:MAX_POSTS]
        break
    except Exception as err:
        print(f"{source.__name__} failed: {err}")
else:
    print("Could not read Substack, leaving posts unchanged")
    sys.exit(0)

# JSON is valid YAML, and avoids needing a YAML library.
OUT.write_text("# Filled in automatically from Substack when the sync works. Can also be edited by hand.\n"
               + json.dumps(posts, indent=2, ensure_ascii=False) + "\n")
print(f"Wrote {len(posts)} posts")
