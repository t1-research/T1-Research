# T1 Research & Development — Website

A 22-page static website: home, about, services, contact, and one page
for each of the 18 services. All CSS lives in `assets/site.css` and all
JavaScript in `assets/site.js` — no inline styling or scripting.

## Deploy (Vercel, same as the current test site)

1. Unzip this folder.
2. Upload the contents to the `t1-research/t1test` GitHub repo
   (replace the old files) — Vercel redeploys automatically.
   Or drag the folder into a new Vercel project.

## Before going live with a real domain

- The canonical URLs, sitemap, and Open Graph tags point at
  https://t1test.vercel.app. When the real domain is ready, search-replace that
  address with the new one in every file (or re-run `build.py`
  after changing `BASE_URL` there).
- The contact form posts to FormSubmit. It needs a one-time
  activation: click the "Activate Form" link in the
  tasikxdevelopment@gmail.com inbox (several copies may be there).

## Photos

Every photo on this site is Brayden's own work from Instagram
@t1.research, optimized for the web (hero 1440px, gallery 1200px,
progressive JPEG).

## Files

- `index.html` — home (hero, hosting tiers, services preview)
- `about.html`, `services.html`, `contact.html`
- `services/*.html` — one page per service (18)
- `assets/site.css`, `assets/site.js` — the only CSS/JS
- `images/` — 16 optimized @t1.research photos
- `sitemap.xml`, `robots.txt`
