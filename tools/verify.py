#!/usr/bin/env python3
"""Verify the generated site: no inline styles/scripts (outside JSON-LD
and the pre-existing standalone mocks), no broken internal links or
images, SEO tags present on every page, form wired correctly."""
import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))  # tools/
PARENT = os.path.dirname(HERE)
# Site root: PARENT/site when the generator sits next to a site/
# directory (Sabrent's working copy), otherwise PARENT itself
# (repo checkout: tools/ sits next to the site files at the repo root).
if os.path.isdir(os.path.join(PARENT, "site")):
    SITE = os.path.join(PARENT, "site")
else:
    SITE = PARENT

errors = []
warnings = []


class Checker(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.links = []
        self.images = []
        self.scripts = []
        self.inline_styles = 0
        self.inline_handlers = 0
        self.title = ""
        self.in_title = False
        self.meta = {}
        self.has_canonical = False

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "style" in d:
            self.inline_styles += 1
        for k in d:
            if k.startswith("on"):
                self.inline_handlers += 1
        if tag == "a" and d.get("href"):
            self.links.append(d["href"])
        if tag == "link" and d.get("href"):
            self.links.append(d["href"])
            if d.get("rel") == "canonical":
                self.has_canonical = True
        if tag == "img" and d.get("src"):
            self.images.append(d["src"])
            if "alt" not in d:
                errors.append(f"{self.path}: img without alt: {d['src']}")
            if "width" not in d or "height" not in d:
                warnings.append(f"{self.path}: img without dimensions: {d['src']}")
        if tag == "script":
            self.scripts.append(d.get("src", "INLINE"))
            if d.get("type") == "application/ld+json":
                pass  # data block, not scripting
            elif not d.get("src"):
                errors.append(f"{self.path}: inline <script> (not JSON-LD)")
        if tag == "title":
            self.in_title = True
        if tag == "meta":
            if d.get("name"):
                self.meta[d["name"]] = d.get("content", "")
            if d.get("property"):
                self.meta[d["property"]] = d.get("content", "")

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def check_page(rel):
    full = os.path.join(SITE, rel)
    with open(full, encoding="utf-8") as f:
        html = f.read()
    c = Checker(rel)
    c.feed(html)
    # Inline styles / handlers (mocks are standalone by design — skipped)
    if c.inline_styles:
        errors.append(f"{rel}: {c.inline_styles} inline style= attribute(s)")
    if c.inline_handlers:
        errors.append(f"{rel}: {c.inline_handlers} inline on* handler(s)")
    # SEO basics
    if not c.title.strip():
        errors.append(f"{rel}: missing <title>")
    if "description" not in c.meta or len(c.meta["description"]) < 40:
        errors.append(f"{rel}: missing/short meta description")
    if not c.has_canonical:
        errors.append(f"{rel}: missing canonical link")
    for prop in ("og:title", "og:description", "og:url", "og:image"):
        if prop not in c.meta:
            errors.append(f"{rel}: missing {prop}")
    # Internal links resolve
    page_dir = os.path.dirname(rel)
    for href in c.links + c.images:
        if href.startswith(("http", "mailto:", "tel:", "#")):
            continue
        target = href.split("#")[0].split("?")[0]
        if not target:
            continue
        resolved = os.path.normpath(os.path.join(page_dir, target))
        if not os.path.exists(os.path.join(SITE, resolved)):
            errors.append(f"{rel}: broken link to {href} (resolves to {resolved})")
    # Unconfirmed business claims must not appear
    for banned in ("within two weeks", "month to month after the first year",
                   "month-to-month after the first year"):
        if banned in html.lower():
            errors.append(f"{rel}: contains unconfirmed claim: '{banned}'")
    return c


pages = []
for root, _, files in os.walk(SITE):
    for fn in files:
        if fn.endswith(".html"):
            pages.append(os.path.relpath(os.path.join(root, fn), SITE))

main_pages = [p for p in pages if not p.startswith("mocks/")]
mock_pages = [p for p in pages if p.startswith("mocks/")]
print(f"checking {len(main_pages)} main pages (+{len(mock_pages)} mocks skipped for style rules)")

for p in sorted(main_pages):
    check_page(p)

# Mocks: only check their internal links resolve (they are standalone files
# with inline CSS by design, from the earlier walk-in kit).
for p in sorted(mock_pages):
    full = os.path.join(SITE, p)
    with open(full, encoding="utf-8") as f:
        html = f.read()
    for href in re.findall(r'href="([^"]+)"', html):
        if href.startswith(("http", "mailto:", "tel:", "#")):
            continue
        target = href.split("#")[0].split("?")[0]
        resolved = os.path.normpath(os.path.join(os.path.dirname(p), target))
        if not os.path.exists(os.path.join(SITE, resolved)):
            errors.append(f"{p}: broken link to {href}")

# Contact form checks
with open(os.path.join(SITE, "contact.html"), encoding="utf-8") as f:
    contact = f.read()
if "https://formsubmit.co/7e187b0c46c60a1073f4bba1528b454c" not in contact:
    errors.append("contact.html: FormSubmit action is not the full alias URL")
if 'name="_honey"' not in contact:
    errors.append("contact.html: honeypot field missing")
if 'id="fService"' not in contact:
    errors.append("contact.html: service select missing")
opts = re.findall(r'<option value="([^"]+)"', contact)
expected = ["website-hosting"] + [
    "link-in-bio", "personal-website", "photo-refresh", "home-inventory",
    "parental-controls", "church-hosting", "family-backup", "tech-help",
    "family-security", "smart-home", "cold-storage", "competitor-watch",
    "digitizing", "business-backup", "vpn", "game-servers",
    "security-system", "photography"] + ["something-else"]
for e in expected:
    if e not in opts:
        errors.append(f"contact.html: service option missing: {e}")
print(f"contact form options: {len(opts)} (expect {len(expected) + 5} incl. placeholders + plans)")

# Services index: 18 service cards + flagship website card
with open(os.path.join(SITE, "services.html"), encoding="utf-8") as f:
    services_html = f.read()
n_cards = services_html.count('class="service-card"')
print(f"services index cards: {n_cards} (expect 19)")
if n_cards != 19:
    errors.append(f"services.html: {n_cards} cards, expected 19")

# Sitemap covers all pages
with open(os.path.join(SITE, "sitemap.xml"), encoding="utf-8") as f:
    sitemap = f.read()
n_urls = sitemap.count("<url>")
print(f"sitemap urls: {n_urls} (expect {len(pages)})")
if n_urls != len(pages):
    errors.append(f"sitemap has {n_urls} urls, site has {len(pages)} pages")

print()
for w in warnings:
    print("WARN:", w)
if errors:
    print(f"{len(errors)} ERROR(S):")
    for e in errors:
        print("ERROR:", e)
    sys.exit(1)
print("ALL CHECKS PASSED")
