#!/usr/bin/env python3
"""Generate responsive WebP variants of the @t1.research photos for the
T1 website (v0.23). Reads originals from photos_raw/, writes into
site/images/ alongside the existing progressive JPEGs.

Variants per photo: 400 / 800 / 1200px wide, plus the native width
when it is meaningfully larger than the biggest standard variant
(the 1440px hero gets a 1440 variant; the 812px pansy does not get a
redundant 812 variant next to its 800).

The existing JPEGs are NOT re-saved: they already live in the repo,
and the push tool cannot carry binaries, so rewriting them here would
only create local/remote drift. A JPEG is generated only if it is
missing entirely (fresh setup).

field.jpg is skipped for WebP: it is orphaned (no page references it)
and due for deletion (#5 in the performance report) — no point
generating variants for a file that is about to go.
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))  # tools/
PARENT = os.path.dirname(HERE)
# Site root: PARENT/site when the generator sits next to a site/
# directory (Sabrent's working copy), otherwise PARENT itself
# (repo checkout: tools/ sits next to the site files at the repo root).
if os.path.isdir(os.path.join(PARENT, "site")):
    SITE = os.path.join(PARENT, "site")
else:
    SITE = PARENT
SRC = os.path.join(PARENT, "photos_raw")
DST = os.path.join(SITE, "images")
os.makedirs(DST, exist_ok=True)

WEBP_WIDTHS = (400, 800, 1200)
WEBP_QUALITY = 80
# Orphaned images: no page references them — skip their WebP variants.
SKIP_WEBP = {"field.jpg"}

# (source post id, output name, max width, jpeg quality)
IMAGES = [
    ("18001798849928156", "hero.jpg", 1600, 82),          # ocean sunset — home hero
    ("17869982618862800", "about-field.jpg", 1200, 80),   # sunset over GA field — about
    ("17987568299073347", "field.jpg", 1200, 80),         # green field, blue sky — home
    ("17970717179271652", "g-sunset-red.jpg", 1200, 80),  # red sunset over water
    ("17884440345053432", "g-portrait-wisteria.jpg", 1200, 80),
    ("17995109687524717", "g-portrait-stairs.jpg", 1200, 80),
    ("18279361306205940", "g-graduation.jpg", 1200, 80),
    ("17933652470607688", "g-cave.jpg", 1200, 80),
    ("17954432498609480", "g-cliff.jpg", 1200, 80),
    ("17966258612598970", "g-lakeside.jpg", 1200, 80),
    ("18052607179709361", "g-atrium.jpg", 1200, 80),
    ("18443202094004021", "g-stringlights.jpg", 1200, 80),
    ("18006802411813776", "g-lake-sunset.jpg", 1200, 80),
    ("17949688484693033", "p-flowers.jpg", 1200, 80),     # orange flowers — photo refresh
    ("18116767366324014", "p-pansy.jpg", 1200, 80),       # red pansy — photo refresh
    # Walton County additions (Nov 12) — gallery grows 10 -> 18, home showcase + strip
    ("18330311167070894", "g-pink-sunset.jpg", 1200, 80), # pink sky over pines, Walton Co — 23 likes
    ("17875550037197338", "g-foggy-night.jpg", 1200, 80), # foggy night street, Monroe
    ("18042633715715646", "g-dusk-fields.jpg", 1200, 80), # dusk over ball fields, Walton Co
    ("17892672935846279", "g-canopy.jpg", 1200, 80),      # looking up through trees, Walton Co
    ("17946807134809276", "g-starry-pines.jpg", 1200, 80),# stars over pines, Monroe
    ("18024625423450367", "g-dusk-orange.jpg", 1200, 80), # orange dusk sky, Walton Co
    ("18389630749103223", "g-neon-storefront.jpg", 1200, 80), # neon storefront at night
]


def webp_widths(native_w):
    """Widths of the WebP variants for a photo of native width native_w:
    400/800/1200 below the native width, plus the native width itself
    when it is more than 5% above the biggest standard variant."""
    variants = [w for w in WEBP_WIDTHS if w < native_w]
    if not variants or native_w - variants[-1] > 0.05 * native_w:
        variants.append(native_w)
    return variants


total_webp = 0
n_webp = 0
for pid, name, max_w, q in IMAGES:
    src = os.path.join(SRC, f"{pid}.jpg")
    dst_jpg = os.path.join(DST, name)
    im = Image.open(src).convert("RGB")
    if im.width > max_w:
        im = im.resize((max_w, int(im.height * max_w / im.width)), Image.LANCZOS)
    if not os.path.exists(dst_jpg):
        im.save(dst_jpg, "JPEG", quality=q, optimize=True, progressive=True)
        print(f"{name}: JPEG generated {im.size[0]}x{im.size[1]} (was missing)")
    if name in SKIP_WEBP:
        print(f"{name}: WebP skipped (orphaned — no page references it)")
        continue
    stem = name.rsplit(".", 1)[0]
    for w in webp_widths(im.width):
        variant = im if w == im.width else im.resize(
            (w, int(im.height * w / im.width)), Image.LANCZOS)
        out = os.path.join(DST, f"{stem}-{w}.webp")
        variant.save(out, "WEBP", quality=WEBP_QUALITY, method=6)
        size = os.path.getsize(out)
        total_webp += size
        n_webp += 1
        print(f"{stem}-{w}.webp: {variant.size[0]}x{variant.size[1]} {size // 1024}KB")

print(f"total WebP: {total_webp // 1024}KB across {n_webp} files")
