# Notes for AI assistants

This is Eve Buczkowski's personal cycling website (Jekyll on GitHub Pages).
Eve is not a programmer. Keep changes small and in the content files.

## Where content lives
- `_data/results.yml`: race results, newest year first. Within a year, newest
  event first. Fields: `year`, `event`, `race`, `discipline` (`track` or
  `road`), `place` (a number), optional `note` (time, record, "World Champion").
  Results from the same `event` and `year` are grouped into one card.
- `_data/power.yml`: power profile best efforts. Update `updated` too.
- `_data/profile.yml`: bio, team, facts, the highlight boxes, `hero_photo`.
- `_data/references.yml`: names and roles only. Never add phone numbers or
  emails for references.
- `images/gallery/`: every image in here shows in the gallery automatically.
- `_data/posts.yml`: the latest Substack posts shown on the homepage. Rebuilt
  on every publish by `scripts/fetch_substack.py` from the live feed, or from
  `_substack/feed.xml` when Substack blocks GitHub (it usually does). To pick up
  a new post, run `scripts/update-blog.sh` from a home computer, or replace
  `_substack/feed.xml` with a copy of https://evetbuczkowski.substack.com/feed.
  Don't edit `posts.yml` by hand; the next publish overwrites it.

## Rules
- Prefer editing `_data/*.yml` over `index.html` or `assets/css/site.css`.
  Only change the design when Eve asks for a design change.
- Keep YAML valid: quote text containing a colon, like `note: "1:11.374"`.
- Before committing, build to check nothing broke: `jekyll build` (Jekyll 3.x
  or 4.x). If it errors, fix it before committing.
- Commit straight to `main` with a short message in plain words
  (e.g. "Add Ontario Cup result"). The site redeploys on push.
- Compress big photos before adding them (aim for under ~500 KB, 2000px wide).
