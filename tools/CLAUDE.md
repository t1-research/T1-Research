# Working on the T1 Research & Development website

This site is generated. Read this file before changing anything.

## The one rule that matters most

`build.py` generates all 22 pages (plus `sitemap.xml`, `robots.txt`, and
`README.md`) from one Python source. **Never edit the HTML files
directly — your changes will be wiped the next time `build.py` runs.**
Edit `tools/build.py` instead.

The two exceptions: `assets/site.css` and `assets/site.js` are edited
directly. `build.py` never touches them.

## Setup

- Python 3 + Pillow (`pip install Pillow`). `verify.py` needs only the
  standard library.
- Everything runs from this directory. No build step, no dependencies
  beyond Pillow.

## Workflow

1. Work on your own branch, cut from `Development`. **Never push to `main`.**
2. Make your changes in `tools/build.py` (and/or `assets/site.css`,
   `assets/site.js`). Run commands from the repo root.
3. Rebuild: `python3 tools/build.py`
4. Verify: `python3 tools/verify.py` — every check must pass before you commit.
5. Open a pull request into `Development`. Brayden reviews and merges.
   Changes reach `main` (production) only through him.

## Layout

The generator lives in `tools/` next to the site files. In a repo
checkout, the site files are at the repo root and the scripts resolve
them as their parent directory. (In Sabrent's working copy the site
lives in a `site/` directory next to `tools/` instead — the scripts
detect which layout they're in.)

- `tools/build.py` — everything: content, templates, page builders. The
  site's single source of truth.
- `tools/verify.py` — checks: no inline styles/scripts (except JSON-LD),
  no broken links, SEO tags on all 22 pages, contact form action, 18
  service cards on the services index, sitemap coverage.
- `tools/optimize_images.py` — optimizes new photos into `images/`. Run
  it BEFORE `build.py`, because the builder reads image dimensions at
  build time (every `<img>` gets explicit width/height). It reads
  originals from `photos_raw/`, which lives with Sabrent — new photos
  from Instagram come through him.
- The site itself: `index.html`, `about.html`, `services.html`,
  `contact.html`, `services/` (18 pages), `assets/` (`site.css` and
  `site.js`, hand-edited — `build.py` never touches them), `images/`
  (the 23 optimized photos), `sitemap.xml`, `robots.txt`, `README.md`.
- Pulling photos from Instagram stays with Sabrent — that step needs his
  Instagram access and isn't in this repo.
- Do NOT commit `site.muse-github-snapshot-sync.json` (sync metadata).

## Content rules (do not break these)

- Location: the site says "Walton County, Georgia" everywhere. Do not add
  "Monroe" back into the site wording.
- Service area is about an hour's radius from Walton County — don't write
  the business as Walton-County-only.
- Photos: every photo is Brayden's own work from @t1.research. Never use
  stock photos or AI-generated images.
- Pricing: Starter $349 setup + $49/mo, Standard $499 + $75/mo,
  Premium $749 + $99/mo. Don't change pricing without being asked.
- Contact form: FormSubmit. The form action must stay the full URL
  `https://formsubmit.co/7e187b0c46c60a1073f4bba1528b454c`.
  Don't change it.
- Don't add claims that aren't confirmed: no "most sites live within two
  weeks", no "cancel any time" — unless Brayden confirms them.
- Services: 18 services in 4 groups — Websites, For Businesses, For Homes
  & Families, Photography & Media. The `GROUPS` list in `build.py` must
  cover every service exactly once (the builder asserts this), and the
  contact-form dropdown groups must match it.
- Website design & hosting is the flagship. It has no service page of its
  own — it lives on the home page, the services-page CTA band, and as the
  first contact-form option.

## Branches

- `main` — production: https://t1-research.vercel.app/. Never push here.
- `Development` — test site: https://t1rtest.vercel.app/. All work merges
  here first, then to `main` by pull request.
- Your branch — cut from `Development`, PR back into `Development`.

## Version naming

Releases are named v0.02, v0.03, v0.04, … (current: v0.06). Commit
messages start with the version and a plain summary, e.g.
"v0.06 grouped the services by who they're for", with a body listing
every change made.
