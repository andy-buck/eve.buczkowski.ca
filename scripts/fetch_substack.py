"""Copy the latest Substack posts into _data/posts.yml so the homepage can show them.

Runs on every publish and once a night, from .github/workflows/pages.yml.
Uses only the Python standard library.

Substack sometimes blocks requests from GitHub's servers, so if reading the
feed directly fails it tries Substack's archive API, then the free rss2json.com
relay. If all fail, _data/posts.yml is left as it is (it can be edited by hand).
"""
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path

FEED = "https://evetbuczkowski.substack.com/feed"
RELAY = "https://api.rss2json.com/v1/api.json?rss_url=" + urllib.parse.quote(FEED, safe="")
OUT = Path(__file__).resolve().parent.parent / "_data" / "posts.yml"
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


def from_feed():
    root = ET.fromstring(get(FEED))
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


def from_archive_api():
    data = json.loads(get("https://evetbuczkowski.substack.com/api/v1/archive?sort=new&limit=12"))
    return [{
        "title": post["title"].strip(),
        "url": post["canonical_url"],
        "date": post["post_date"][:10],
        "subtitle": post.get("subtitle") or None,
        "image": post.get("cover_image") or None,
    } for post in data if post.get("audience", "everyone") in ("everyone", "only_free")]


def from_relay():
    data = json.loads(get(RELAY))
    if data.get("status") != "ok":
        raise RuntimeError(data.get("message", "relay error"))
    return [{
        "title": item["title"].strip(),
        "url": item["link"],
        "date": item["pubDate"][:10],
        "subtitle": strip_html(item.get("description")),
        "image": (item.get("enclosure") or {}).get("link") or item.get("thumbnail") or None,
    } for item in data["items"]]


for source in (from_feed, from_archive_api, from_relay):
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
