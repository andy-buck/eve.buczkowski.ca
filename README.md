# eve.buczkowski.ca

Eve Buczkowski's cycling website. It's free to run: GitHub Pages hosts it, and
the blog stays on Substack.

## How to update it

Everything you'd normally change is a plain text file in the `_data` folder.
You never need to touch the design files.

| To change… | Edit this file |
|---|---|
| Race results | `_data/results.yml` |
| Power numbers | `_data/power.yml` |
| Bio, team, highlight boxes, top photo | `_data/profile.yml` |
| References | `_data/references.yml` |
| Photo gallery | Add or delete photos in `images/gallery/` |
| Blog posts on the homepage | Run `./scripts/update-blog.sh` on a home computer after posting (Substack blocks GitHub from fetching it directly) |

**With an AI assistant:** open this repo in Claude (claude.ai/code) and ask in
plain words, like *"Add 2nd in the Ontario Cup road race, May 2027"* or
*"Swap the top photo for the new one I uploaded"*. Claude follows the rules in
`CLAUDE.md`.

**By hand:** click a file on github.com, click the pencil, edit, then
**Commit changes**. The site updates within a couple of minutes.

**Undo a mistake:** every change is saved in the history. If something
breaks, ask Claude to "undo the last change", or find the file's History
on github.com and restore the older version.

## One-time setup (already done)

- Settings → Pages → Source: **GitHub Actions**
- Settings → Pages → Custom domain: `eve.buczkowski.ca`, with **Enforce HTTPS** on
- DNS at the registrar: `CNAME  eve  →  <github-username>.github.io`
