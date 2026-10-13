#!/usr/bin/env bash
# Saves Eve's Substack feed into the repo so the website can show her latest posts.
# Substack blocks GitHub's servers, so this has to run from a home computer.
#
# Run it from anywhere inside the repo after a new post goes up:
#   ./scripts/update-blog.sh
# It downloads the feed, commits it, and pushes. The site republishes on its own.
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"
git pull --quiet --rebase

curl --fail --silent --show-error --location \
  --user-agent "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36" \
  https://evetbuczkowski.substack.com/feed --output _substack/feed.xml

if git diff --quiet -- _substack/feed.xml; then
  echo "No new posts since last time."
  exit 0
fi

git add _substack/feed.xml
git commit --quiet -m "Update Substack feed"
git push --quiet
echo "Feed saved. The site will show the new posts in a couple of minutes."
