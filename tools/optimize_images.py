#!/usr/bin/env python3
"""Optimize selected @t1.research photos for the new T1 website.
Hero at 1600px wide, everything else at 1200px wide, progressive JPEG.
Run once; outputs into site/images/."""
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
    # Walton County additions (Nov 12) — gallery grows 10 -> 18, home showcase + strip
    ("18330311167070894", "g-pink-sunset.jpg", 1200, 80), # pink sky over pines, Walton Co — 23 likes
    ("17875550037197338", "g-foggy-night.jpg", 1200, 80), # foggy night street, Monroe
    ("18042633715715646", "g-dusk-fields.jpg", 1200, 80), # dusk over ball fields, Walton Co
    ("17892672935846279", "g-canopy.jpg", 1200, 80),      # looking up through trees, Walton Co
    ("17946807134809276", "g-starry-pines.jpg", 1200, 80),# stars over pines, Monroe
    ("18024625423450367", "g-dusk-orange.jpg", 1200, 80), # orange dusk sky, Walton Co
    ("18389630749103223", "g-neon-storefront.jpg", 1200, 80), # neon storefront at night
]

total = 0
for pid, name, max_w, q in IMAGES:
    src = os.path.join(SRC, f"{pid}.jpg")
    dst = os.path.join(DST, name)
    im = Image.open(src).convert("RGB")
    if im.width > max_w:
        im = im.resize((max_w, int(im.height * max_w / im.width)), Image.LANCZOS)
    im.save(dst, "JPEG", quality=q, optimize=True, progressive=True)
    size = os.path.getsize(dst)
    total += size
    print(f"{name}: {im.size[0]}x{im.size[1]} {size // 1024}KB")

print(f"total: {total // 1024}KB across {len(IMAGES)} images")
