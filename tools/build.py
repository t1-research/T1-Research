#!/usr/bin/env python3
"""Generate the T1 Research & Development multi-page website.

Builds 22 pages (home, about, services, contact + 18 service pages),
sitemap.xml, robots.txt and a deploy README into the site root.

Layout: this script lives in tools/. The site root is the tools/
directory's parent when that parent holds a site/ directory (Sabrent's
working copy), otherwise the parent itself (repo checkout: tools/ sits
next to the site files at the repo root).

All copy is Brayden's own: the 17 liked AWS business ideas (Nov 11,
easiest-to-hardest order) plus Photography as the 18th service.
Website design & hosting is the flagship offer, featured on the home
page; it is also a choice in the contact form's service picker.
Photos are Brayden's own @t1.research Instagram photography, already
optimized into site/images/ by optimize_images.py.
"""
import json
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
IMG_DIR = os.path.join(SITE, "images")

SITE_NAME = "T1 Research & Development"
TAGLINE = "Websites, Technology & Digital Solutions for Businesses and Homes."
PHONE = "770-820-7364"
PHONE_TEL = "tel:+17708207364"
EMAIL = "tasikxdevelopment@gmail.com"
CITY = "Walton County, Georgia"
# Canonical / Open Graph base. The live test site today; update to the
# real domain (e.g. https://t1research.com) once it exists.
BASE_URL = "https://t1-research.vercel.app"
FORMSUBMIT = "https://formsubmit.co/7e187b0c46c60a1073f4bba1528b454c"
INSTAGRAM = "https://www.instagram.com/t1.research"

# ---------------------------------------------------------------- services
# Order: Brayden's difficulty order, easiest first. Photography is #18.

SERVICES = [
    {
        "slug": "link-in-bio",
        "name": "Link-in-Bio Pages",
        "short": "One link that holds all of yours — every profile, page, and booking link in one clean page.",
        "price": "$9/month",
        "price_head": "$9/month",
        "price_note": "One page, every link. Updates included.",
        "intro": [
            "Your Instagram bio gives you one link. This page makes it count: every profile, booking page, menu, and contact link in one clean place your customers can actually use.",
            "I build the page, host it, and keep it online. When a link changes, tell me and it's updated.",
        ],
        "features": [
            "Every link in one place — Instagram, Facebook, website, booking, directions, phone",
            "Your branding, your colors, your photo",
            "Loads fast on every phone",
            "Link updates included — just ask",
            "Hosted and kept online for you",
        ],
        "faq": [
            ("How do I update my links?",
             "Text or email me the change and it's updated, usually the same day."),
            ("Does it work with Instagram?",
             "Yes — it's made for the bio link. One tap takes your followers to everything."),
        ],
    },
    {
        "slug": "personal-website",
        "name": "Personal Website",
        "short": "A one-page site for job seekers and professionals — résumé, portfolio, and contact in one place.",
        "price": "$35/month",
        "price_head": "$35/month",
        "price_note": "One page, built and hosted. Updates when your career moves.",
        "intro": [
            "A clean personal site makes you memorable. Your story, your experience, your work, and a way to reach you — all on one page you can link from your résumé and LinkedIn.",
            "I build it, host it, and keep it updated as your career moves.",
        ],
        "features": [
            "Your name, your story, your experience",
            "Résumé and portfolio in one place",
            "Contact form so opportunities reach you",
            "Updates when you change jobs or add work",
            "Fast, mobile-friendly, always online",
        ],
        "faq": [
            ("What do I need to provide?",
             "Your résumé, a photo, and any links you want on the page. I handle the rest."),
            ("Can it help me get a job?",
             "A clean personal site sets you apart — hiring managers remember the candidate with a real site."),
        ],
    },
    {
        "slug": "photo-refresh",
        "name": "Monthly Photo Refresh",
        "short": "Fresh photos of your business every month — new shots for your site, Google, and social.",
        "price": "$79–$149/month",
        "price_head": "$79–$149/month",
        "price_note": "Monthly on-site shoot. Edited photos, ready to post.",
        "intro": [
            "The same three photos from 2019 aren't doing your business any favors. I come out every month and shoot fresh photos — your products, your space, your people, the season — and deliver them edited and ready to post.",
            "New shots for your website, your Google Business Profile, and your social feeds, every single month.",
        ],
        "features": [
            "Monthly on-site photo shoot",
            "Edited, web-ready photos delivered to you",
            "Fresh shots for your site, Google, and social",
            "Seasonal and new-product coverage",
            "Shot by a photographer, not a phone snapshot",
        ],
        "faq": [
            ("What do you shoot?",
             "Products, your space, your team, seasonal displays — whatever shows your business at its best."),
            ("How do I get the photos?",
             "Delivered digitally, edited and ready to post, after each visit."),
        ],
        "images": [("p-flowers.jpg", "Fresh orange flowers, photographed for a local business"),
                   ("p-pansy.jpg", "Close-up of a red pansy flower")],
    },
    {
        "slug": "home-inventory",
        "name": "Home Inventory for Insurance",
        "short": "A photo catalog of everything you own, stored safely offsite — so a claim takes hours, not weeks.",
        "price": "$149 one-time + $9/month",
        "price_head": "$149 one-time + $9/month",
        "price_note": "One visit to catalog everything. Secure offsite storage after that.",
        "intro": [
            "After a fire or a burglary, your insurer asks what you owned — and from memory, most people get about half of it. I photograph and catalog your belongings room by room, record serial numbers and receipts, and store it all safely offsite.",
            "If you ever need to file a claim, the proof is ready on day one.",
        ],
        "features": [
            "Room-by-room photo catalog of your belongings",
            "Serial numbers and receipts recorded",
            "Stored offsite in encrypted cloud storage",
            "Update it when you buy something big",
            "Ready for your insurer whenever you need it",
        ],
        "faq": [
            ("Why not just take photos myself?",
             "You can — but most people never finish. I do the whole house in one visit and keep it organized."),
            ("Is my information private?",
             "Yes. Your inventory is encrypted, and only you can access it."),
        ],
    },
    {
        "slug": "parental-controls",
        "name": "Parental Controls & Safe Wi-Fi Setup",
        "short": "Safer internet for your kids — content filtering and screen-time limits set up on your home Wi-Fi.",
        "price": "$99 one-time",
        "price_head": "$99 one-time",
        "price_note": "Set up once at your home. No monthly fee.",
        "intro": [
            "Your home Wi-Fi can do more than connect — it can protect. I set up content filtering on your router and screen-time limits on your kids' devices, so the internet in your house is safer without you having to hover.",
            "One visit, one price, no monthly fee.",
        ],
        "features": [
            "Content filtering on your home network",
            "Screen-time schedules for kids' devices",
            "Works on every device in the house",
            "Simple instructions so you stay in control",
            "No monthly fee — set up once and it runs",
        ],
        "faq": [
            ("Will it slow my internet?",
             "No — filtering adds no noticeable slowdown to your connection."),
            ("Can my kids bypass it?",
             "A determined teenager can bypass almost anything. This stops accidental exposure and casual workarounds, which is what most families need."),
        ],
    },
    {
        "slug": "church-hosting",
        "name": "Church & Sermon Media Hosting",
        "short": "Your sermons online every week — audio and video hosting with a simple page your congregation can find.",
        "price": "$29–$49/month",
        "price_head": "$29–$49/month",
        "price_note": "Weekly sermon uploads, audio and video. Archive included.",
        "intro": [
            "Your congregation shouldn't have to hunt for last Sunday's sermon. I post your sermons online every week — audio and video — on a simple page anyone can find and play on their phone.",
            "Send me the recording after service. I handle the rest.",
        ],
        "features": [
            "New sermons posted every week",
            "Audio and video hosting",
            "Searchable archive of past sermons",
            "Plays on any phone, no app needed",
            "Shareable links for each sermon",
        ],
        "faq": [
            ("How do sermons get to you?",
             "Send the recording after service — I upload, label, and post it."),
            ("Can members listen on their phones?",
             "Yes. Everything plays right in the browser, no app or account needed."),
        ],
    },
    {
        "slug": "family-backup",
        "name": "Family Backup",
        "short": "Your family's photos and files, backed up automatically every night — so a dead laptop never means lost memories.",
        "price": "$19/month per household",
        "price_head": "$19/month",
        "price_note": "Per household. Automatic nightly backups, tested monthly.",
        "intro": [
            "Family photos, school projects, tax documents — all of it lives on one laptop, until the day that laptop doesn't turn on. Family Backup copies everything automatically every night to secure cloud storage.",
            "And once a month, I test the backup by restoring a file — because a backup you've never tested is a hope, not a backup.",
        ],
        "features": [
            "Automatic nightly backups — nothing to remember",
            "30-day version history — recover deleted files",
            "Monthly restore test — I prove it actually works",
            "Encrypted cloud storage",
            "One assisted restore a year included",
        ],
        "faq": [
            ("What gets backed up?",
             "Documents, photos, everything you choose. You pick the folders; the rest is automatic."),
            ("What if my computer dies?",
             "I help you restore everything to your new computer. That's the whole point."),
        ],
    },
    {
        "slug": "tech-help",
        "name": "Tech Help House Calls",
        "short": "A patient tech expert who comes to you — setup, fixes, and plain-English answers.",
        "price": "$49 per visit or $29/month",
        "price_head": "$49 per visit or $29/month",
        "price_note": "In-person help at your home, in Walton County and nearby.",
        "intro": [
            "New phone won't connect to the Wi-Fi. Printer stopped printing. Computer's slower than it used to be. I come to your house, fix it on the spot, and explain what happened in plain English — no jargon, no condescension.",
            "Book a single visit, or a monthly plan that covers regular check-ins.",
        ],
        "features": [
            "I come to you — no hauling equipment anywhere",
            "Setup and fixes done on the spot",
            "Plain-English explanations of what went wrong",
            "Wi-Fi, printers, phones, tablets, computers",
            "Monthly plan covers regular check-ins",
        ],
        "faq": [
            ("What areas do you cover?",
             "Walton County and nearby."),
            ("What if you can't fix it?",
             "If it's beyond repair, I'll tell you straight and help you figure out the next step."),
        ],
    },
    {
        "slug": "family-security",
        "name": "Family Security",
        "short": "A security checkup for your whole family — strong passwords, two-factor authentication, and frozen credit.",
        "price": "$99 one-time + $9/month",
        "price_head": "$99 one-time + $9/month",
        "price_note": "One checkup visit, then password manager hosting.",
        "intro": [
            "Most families are one reused password away from a bad week. In about an hour at your kitchen table, I set up a password manager for the family, turn on two-factor authentication everywhere it matters, and freeze your credit at all three bureaus.",
            "After that, the $9 a month keeps your password manager hosted and running.",
        ],
        "features": [
            "Password manager set up for the whole family",
            "Two-factor authentication on your important accounts",
            "Credit frozen at all three bureaus",
            "Scam-proofing walkthrough — what to watch for",
            "Ongoing password manager hosting",
        ],
        "faq": [
            ("Is a password manager safe?",
             "Yes — it's the single best step most families can take. Your passwords are encrypted, and only you hold the key."),
            ("How long does the checkup take?",
             "About an hour at your kitchen table."),
        ],
    },
]

SERVICES += [
    {
        "slug": "smart-home",
        "name": "Smart Home Setup",
        "short": "Smart lights, locks, and speakers that actually work together — installed and explained in plain English.",
        "price": "$99–$199 per visit",
        "price_head": "$99–$199 per visit",
        "price_note": "You buy the devices; I install and set them up.",
        "intro": [
            "Smart home gear is great when it works together — and a drawer full of remotes when it doesn't. I install your lights, locks, thermostats, speakers, and doorbells, connect them into one system, and show you how to use it.",
            "Lights on at sunset. Doors locked at night. One app to control it all.",
        ],
        "features": [
            "Devices installed and connected as one system",
            "One app to control everything",
            "Automations — lights at sunset, doors locked at night",
            "Plain-English walkthrough when I'm done",
            "Your choice of brands — I work with what you have",
        ],
        "faq": [
            ("Do I buy the devices or do you?",
             "You buy them — I'll recommend what fits your home and budget. I install and set everything up."),
            ("Will it work with what I already have?",
             "Usually, yes. I'll check what you own before we start."),
        ],
    },
    {
        "slug": "cold-storage",
        "name": "Cold Storage Archiving",
        "short": "Your raw footage and photo archives, stored safely in the cloud for pennies — retrievable whenever you need them.",
        "price": "$19–$29/month",
        "price_head": "$19–$29/month",
        "price_note": "For photographers and videographers with terabytes of raw files.",
        "intro": [
            "Raw footage and photo archives pile up fast, and hard drives fail — usually the one with the project you need. Cold storage moves your archives to deep cloud storage, organized by project and date, for a fraction of what drives cost over time.",
            "It's an archive, not a working drive: your files are safe, and retrievable within a few hours whenever you need them.",
        ],
        "features": [
            "Raw photos and video archived to deep cloud storage",
            "Organized by project and date",
            "Retrieval within a few hours when you need a file",
            "Costs a fraction of hard drives over time",
            "Your originals stay yours — always",
        ],
        "faq": [
            ("How fast can I get a file back?",
             "Standard retrieval takes a few hours. It's an archive, not a working drive — built for files you keep, not files you open daily."),
            ("Is it cheaper than hard drives?",
             "For terabytes of footage you rarely touch, yes — and unlike a drive on a shelf, it can't be lost in a fire."),
        ],
    },
    {
        "slug": "competitor-watch",
        "name": "Competitor Watch Report",
        "short": "A monthly report on what your competitors are doing — prices, reviews, new services, and openings.",
        "price": "$49/month",
        "price_head": "$49/month",
        "price_note": "Up to five competitors tracked. Plain-English report, monthly.",
        "intro": [
            "You can't out-compete what you can't see. Every month I research your top competitors — their prices, their reviews, their new services, what's opening and closing — and send you a plain-English report.",
            "Spot the gaps, price with confidence, and see what customers are saying about the other guy.",
        ],
        "features": [
            "Monthly report on your top competitors",
            "Price and service changes tracked",
            "Review trends — what customers praise and complain about",
            "New openings and closings in your area",
            "Plain English, no jargon",
        ],
        "faq": [
            ("How many competitors do you track?",
             "Up to five — your choice."),
            ("What do I do with the report?",
             "Use it to price with confidence, spot services nobody nearby offers, and fix the things customers complain about before they complain about you."),
        ],
    },
    {
        "slug": "digitizing",
        "name": "Digitizing & Archiving",
        "short": "Paper files and family photos, scanned and stored safely — searchable, backed up, and always findable.",
        "price": "Documents $199+/cabinet + $29/month · Photos $199–$499/box + $9/month",
        "price_head": "From $199",
        "price_note": "Documents $199+/cabinet + $29/mo · Family photos & video $199–$499/box + $9/mo.",
        "intro": [
            "The filing cabinet in the back room and the box of family photos in the closet have the same problem: if something happens to them, they're gone. I scan documents and photos to digital, organize them, and store them safely in the cloud.",
            "Your originals come back to you. The digital copies stay searchable, backed up, and findable forever.",
        ],
        "features": [
            "Documents scanned and searchable",
            "Family photos and video digitized",
            "Organized by year and topic",
            "Stored in encrypted cloud storage",
            "Originals returned to you",
        ],
        "faq": [
            ("What do you do with my originals?",
             "They're yours — I return everything after scanning."),
            ("How long does it take?",
             "It depends on volume. A box of photos is usually a week or two."),
        ],
    },
    {
        "slug": "business-backup",
        "name": "Business Backup",
        "short": "Your business files and cloud apps, backed up automatically every night — with a monthly restore test that proves it works.",
        "price": "$39/month files + $39/month cloud apps",
        "price_head": "$39/month",
        "price_note": "Per computer, up to 250 GB (+$15/mo per extra computer). Cloud apps $39/mo. $49 setup waived for the first 3 clients.",
        "intro": [
            "If your computer died tonight, how much of your business goes with it? Business Backup copies your files automatically every night to secure cloud storage — and backs up your cloud apps too, because Google and Microsoft don't keep your deleted emails and files forever.",
            "Once a month, I test the backup by restoring a file and verifying it. A backup you've never tested is a hope, not a backup.",
        ],
        "features": [
            "Nightly automatic backups of your business computers",
            "Cloud app backup — Google Workspace and Microsoft 365",
            "30-day version history — recover deleted or overwritten files",
            "Monthly restore test — I prove it works, every month",
            "Failure alerts — if a backup misses, I know",
            "One assisted restore a year included",
        ],
        "faq": [
            ("What if my computer dies tonight?",
             "That's the question this service answers. With Business Backup, we restore your files to a new computer and you're back to work."),
            ("Do you really test the backups?",
             "Every month. I restore a file and verify it. If a backup ever fails a test, I fix it before it matters."),
            ("What's the cloud apps backup for?",
             "Google and Microsoft keep deleted items for a short window, then they're gone. This keeps your emails, Drive files, and documents backed up on your schedule, not theirs."),
        ],
    },
    {
        "slug": "vpn",
        "name": "Secure Remote Access (VPN)",
        "short": "Reach your office from anywhere, safely — your team connects to files, printers, and apps from home or the road.",
        "price": "$39/month",
        "price_head": "$39/month",
        "price_note": "Your own private network. Each business fully separated.",
        "intro": [
            "Your team shouldn't have to be in the office to reach the office. Secure remote access connects your office and your people's devices on a private, encrypted network — files, printers, and apps, from home or the road.",
            "Each business gets its own fully separated network. Your employees install one app and log in. I set it up and keep it running.",
        ],
        "features": [
            "Work from anywhere, securely",
            "Reach office files, printers, and apps remotely",
            "Each business fully separated — no shared access",
            "Simple apps on Windows, Mac, iPhone, and Android",
            "I set it up and keep it running",
        ],
        "faq": [
            ("Is this the same as the VPNs I see advertised?",
             "No. Those hide your browsing from your internet provider. This connects your team to your office — a different job."),
            ("Do my employees need to be tech-savvy?",
             "No. They install one app and log in. If they can use email, they can use this."),
        ],
    },
    {
        "slug": "game-servers",
        "name": "Managed Game Servers",
        "short": "Your own Minecraft or game server, hosted and managed — always online, always updated, no hassle.",
        "price": "$19–$49/month per server",
        "price_head": "$19–$49/month",
        "price_note": "Per server. Minecraft Java and Bedrock, plus others on request.",
        "intro": [
            "Running your own game server is fun until it's 11 PM and the server's down, a mod broke, or the world needs restoring. I host and manage it for you — always online, always updated, backed up regularly.",
            "You and your friends just play.",
        ],
        "features": [
            "Always-online server, hosted for you",
            "Updates and patches handled",
            "Mods and plugins installed",
            "Regular world backups",
            "Support when something breaks",
        ],
        "faq": [
            ("Which games?",
             "Minecraft (Java and Bedrock) is the main one. Ask about others."),
            ("Can my friends join?",
             "Yes — that's the point. Share the address and play together."),
        ],
    },
    {
        "slug": "security-system",
        "name": "Security System Setup & Maintenance",
        "short": "Cameras and sensors, installed and kept healthy — see what's happening at home or at work, from your phone.",
        "price": "Home $349–$549 setup + $29/month · Business $799–$1,499 setup + $79–$129/month",
        "price_head": "From $349 setup + $29/month",
        "price_note": "Hardware included in setup. Home $349–$549 + $29/mo · Business $799–$1,499 + $79–$129/mo.",
        "intro": [
            "Cameras and sensors are only useful if they're working when it matters. I install your system — hardware included — configure alerts to your phone, back up your footage to the cloud, and keep everything healthy with monthly maintenance.",
            "One honest boundary: I'm not a 24/7 monitoring center. Alerts go to your phone, and you decide what to do. My job is making sure the system works when you need it.",
        ],
        "features": [
            "Cameras and sensors installed — hardware included",
            "Footage backed up to the cloud",
            "Alerts sent to your phone",
            "Monthly health checks — cameras online, sensors reporting, footage uploading",
            "Firmware kept up to date",
        ],
        "faq": [
            ("Do you watch my cameras?",
             "No. Alerts go to your phone; you decide what to do. I keep the system healthy — I'm not a dispatch center."),
            ("What's included in setup?",
             "Hardware, installation, and configuration. The monthly fee covers maintenance and footage backup."),
        ],
    },
    {
        "slug": "photography",
        "name": "Photography",
        "short": "Landscape and portrait photography from Walton County, Georgia — see the work at @t1.research.",
        "price": "Contact for pricing",
        "price_head": "Sessions & prints",
        "price_note": "Portrait sessions and prints available — get in touch for details.",
        "intro": [
            "Before T1 Research & Development was a web and tech business, it was a camera. I shoot landscapes and portraits around Walton County — golden hour over Georgia fields, quiet streets, and the people who live here.",
            "Every photo on this site is mine, from @t1.research on Instagram. Portrait sessions and prints are available — get in touch and we'll plan one.",
        ],
        "features": [
            "Landscape photography — Georgia fields, lakes, and light",
            "Portrait sessions — individuals, graduates, families",
            "Golden-hour shoots around Walton County",
            "Prints available of any photo here",
            "See the latest work at @t1.research",
        ],
        "faq": [
            ("Do you do portrait sessions?",
             "Yes — individuals, graduates, and families. Get in touch and we'll plan a time and place."),
            ("Can I buy a print?",
             "Yes. Contact me about prints of any photo on this site or on @t1.research."),
        ],
        "gallery": [
            ("g-pink-sunset.jpg", "Pink sky over Walton County pines"),
            ("g-foggy-night.jpg", "Foggy night on a Walton County street"),
            ("g-dusk-fields.jpg", "Dusk over the ball fields"),
            ("g-canopy.jpg", "Looking up through the trees"),
            ("g-starry-pines.jpg", "Stars over the pines"),
            ("g-dusk-orange.jpg", "Orange dusk over Walton County"),
            ("g-neon-storefront.jpg", "Neon storefront at night"),
            ("g-sunset-red.jpg", "Red sunset over the water"),
            ("g-portrait-wisteria.jpg", "Portrait under wisteria on a downtown sidewalk"),
            ("g-portrait-stairs.jpg", "Portrait on metal stairs"),
            ("g-graduation.jpg", "Graduation portrait"),
            ("g-cave.jpg", "Rock overhang above the water, kayaks below"),
            ("g-cliff.jpg", "Pine trees on a rocky cliff"),
            ("g-lakeside.jpg", "Lakeside chairs behind a white picket fence"),
            ("g-atrium.jpg", "Looking up inside a glass atrium"),
            ("g-stringlights.jpg", "String lights in the trees at night"),
            ("g-lake-sunset.jpg", "Sunset over the lake"),
        ],
    },
]

# Service groups, "by who it's for" (Brayden's pick, Nov 12). Order within
# each group follows the SERVICES list (easiest -> hardest). Website design
# & hosting is the flagship and lives outside the groups (home page tiers,
# services-page CTA band, first contact-form option).
GROUPS = [
    ("websites", "Websites",
     ["link-in-bio", "personal-website"]),
    ("business", "For Businesses",
     ["photo-refresh", "competitor-watch", "business-backup", "vpn",
      "security-system"]),
    ("home", "For Homes & Families",
     ["home-inventory", "parental-controls", "family-backup", "tech-help",
      "family-security", "smart-home", "cold-storage", "digitizing",
      "game-servers"]),
    ("media", "Photography & Media",
     ["church-hosting", "photography"]),
]

# Hosting tiers (flagship offer, featured on the home page).
TIERS = [
    {
        "key": "starter", "name": "Starter", "setup": 349, "monthly": 49,
        "year": 937, "popular": False,
        "blurb": "A clean, professional site for a small business getting online.",
        "features": [
            "Up to 5 pages",
            "Mobile-friendly design",
            "Contact form and click-to-call",
            "Basic care plan — 30 min of changes a month",
        ],
    },
    {
        "key": "standard", "name": "Standard", "setup": 499, "monthly": 75,
        "year": 1399, "popular": True,
        "blurb": "Our core plan — everything most local businesses need.",
        "features": [
            "Everything in Starter",
            "Booking or menu integration",
            "Photo cleanup and optimization",
            "Monthly report — visitors, calls, and updates",
        ],
    },
    {
        "key": "premium", "name": "Premium", "setup": 749, "monthly": 99,
        "year": 1937, "popular": False,
        "blurb": "For businesses that want more pages and more hands-on care.",
        "features": [
            "Everything in Standard",
            "Up to 10 pages",
            "Owner walkthrough when we launch",
            "2 hours of changes a month, priority response",
        ],
    },
]


# ---------------------------------------------------------------- helpers

_img_cache = {}


def img_size(name):
    """(width, height) of an optimized image, cached."""
    if name not in _img_cache:
        with Image.open(os.path.join(IMG_DIR, name)) as im:
            _img_cache[name] = im.size
    return _img_cache[name]


def img_tag(name, alt, depth="", cls="", lazy=True, fetchpriority=""):
    """An <img> with explicit dimensions (prevents layout shift)."""
    w, h = img_size(name)
    attrs = [f'src="{depth}images/{name}"', f'alt="{alt}"',
             f'width="{w}"', f'height="{h}"']
    if cls:
        attrs.append(f'class="{cls}"')
    if lazy:
        attrs.append('loading="lazy"')
        attrs.append('decoding="async"')
    if fetchpriority:
        attrs.append(f'fetchpriority="{fetchpriority}"')
    return "<img " + " ".join(attrs) + ">"


def money(n):
    return "$" + f"{n:,}"


# ---------------------------------------------------------------- templates

def head(title, description, path, og_image="hero.jpg", json_ld=None, preload=None):
    """The <head> block: SEO meta, Open Graph, canonical, JSON-LD."""
    canon = BASE_URL + "/" + path
    og_url = BASE_URL + "/images/" + og_image
    ld = ""
    if json_ld:
        ld = ('\n  <script type="application/ld+json">\n'
              + json.dumps(json_ld, indent=2)
              + "\n  </script>")
    pre = ""
    if preload:
        w, h = img_size(preload)
        pre = (f'\n  <link rel="preload" as="image" href="images/{preload}" '
               f'imagesrcset="images/{preload} {w}w" imagesizes="100vw">')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canon}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="{og_url}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{og_url}">{pre}
  <link rel="stylesheet" href="{'../' if path.startswith('services/') else ''}assets/site.css">{ld}
  <script src="{'../' if path.startswith('services/') else ''}assets/site.js" defer></script>
</head>"""


def header(active, depth=""):
    """Site header + nav."""
    def link(page, label, key):
        cls = ' class="active"' if key == active else ""
        return f'<a href="{depth}{page}"{cls}>{label}</a>'

    return f"""<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="{depth}index.html">
        <span class="brand-name">{SITE_NAME}</span>
        <span class="brand-tag">{TAGLINE}</span>
      </a>
      <button class="nav-toggle" aria-expanded="false" aria-label="Open menu">☰ Menu</button>
      <nav class="site-nav" aria-label="Main">
        <div class="nav-mobile-head">
          <button class="nav-close" aria-label="Close menu">✕</button>
        </div>
        <div class="nav-body">
          {link("index.html", "Home", "home")}
          {link("services.html", "Services", "services")}
          {link("about.html", "About", "about")}
          <a class="nav-cta" href="{depth}contact.html">Get in touch</a>
        </div>
      </nav>
    </div>
  </header>
"""


def footer(depth=""):
    return f"""  <footer class="site-footer">
    <div class="container">
      <div class="footer-inner">
        <div>
          <div class="footer-brand">{SITE_NAME}</div>
          <div class="footer-tag">{TAGLINE}</div>
          <p>{CITY}<br>
          <a href="{PHONE_TEL}">{PHONE}</a><br>
          <a href="mailto:{EMAIL}">{EMAIL}</a></p>
        </div>
        <div>
          <p><strong>Pages</strong><br>
          <a href="{depth}index.html">Home</a><br>
          <a href="{depth}services.html">Services</a><br>
          <a href="{depth}about.html">About</a><br>
          <a href="{depth}contact.html">Contact</a></p>
        </div>
        <div>
          <p><strong>Photography</strong><br>
          <a href="{INSTAGRAM}">@t1.research on Instagram</a><br>
          <a href="{depth}services/photography.html">Photography service</a></p>
        </div>
      </div>
      <p class="footer-note">&copy; 2026 {SITE_NAME}. All photography on this site is by Brayden Downey, from @t1.research.</p>
    </div>
  </footer>
</body>
</html>
"""


def write_page(rel_path, content):
    dest = os.path.join(SITE, rel_path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(content)
    return dest


def service_card(svc, depth=""):
    """One service card (a div) for the services index and home preview."""
    return f"""<div class="service-card-wrap">
          <a class="service-card" href="{depth}services/{svc['slug']}.html">
            <h3>{svc['name']}</h3>
            <p>{svc['short']}</p>
            <span class="price">{svc['price']}</span>
            <span class="more">Learn more →</span>
          </a>
        </div>"""


def faq_block(faqs):
    items = []
    for q, a in faqs:
        items.append(f"""<div class="faq-item">
          <button class="faq-question" aria-expanded="false">{q}</button>
          <div class="faq-answer"><p>{a}</p></div>
        </div>""")
    return "\n".join(items)


# ---------------------------------------------------------------- home page

def build_home():
    ld = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": SITE_NAME,
        "description": "Websites, backups, and tech help for Walton County, Georgia. Website design and hosting, business and family backups, and 18 local services.",
        "url": BASE_URL,
        "telephone": "+1-770-820-7364",
        "email": EMAIL,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Walton County",
            "addressRegion": "GA",
            "addressCountry": "US",
        },
        "areaServed": "Walton County, Georgia",
        "sameAs": [INSTAGRAM],
    }
    hero = img_tag("hero.jpg", "Sunset over the ocean, photographed by Brayden Downey",
                   cls="hero-photo", lazy=False, fetchpriority="high")
    tiers = []
    for t in TIERS:
        pop = " tier-popular" if t["popular"] else ""
        badge = '<span class="tier-badge">Most popular</span>' if t["popular"] else ""
        feats = "".join(f"<li>{f}</li>" for f in t["features"])
        tiers.append(f"""<div class="card tier{pop}">
          {badge}
          <h3>{t['name']}</h3>
          <p>{t['blurb']}</p>
          <p class="tier-price">{money(t['setup'])} <small>setup</small></p>
          <p class="tier-monthly">{money(t['monthly'])}/month care</p>
          <p class="tier-year">First year: {money(t['year'])}</p>
          <ul>{feats}</ul>
          <a class="btn btn-primary btn-block" href="contact.html?plan={t['key']}">Start with {t['name']}</a>
        </div>""")
    featured_slugs = ["business-backup", "link-in-bio", "family-backup",
                      "photo-refresh", "church-hosting", "photography"]
    featured = [s for s in SERVICES if s["slug"] in featured_slugs]
    cards = "\n".join(service_card(s) for s in featured)
    strip = (
        img_tag("downtown.jpg", "A brick downtown building in Walton County, Georgia")
        + "\n          "
        + img_tag("field.jpg", "Green Georgia field under a blue sky")
        + "\n          "
        + img_tag("g-dusk-orange.jpg", "Orange dusk over Walton County")
    )
    night_strip = (
        img_tag("g-starry-pines.jpg", "Stars over the pines")
        + "\n          "
        + img_tag("g-neon-storefront.jpg", "Neon storefront at night")
        + "\n          "
        + img_tag("g-stringlights.jpg", "String lights in the trees at night")
    )
    home_faq = [
        ("Where are you located?",
         "Walton County, Georgia. Most of our work is for local businesses and families in Walton County, and several services work anywhere."),
        ("How do we start?",
         "Get in touch and tell us what you need. We'll talk through it — free, no pressure — and you'll get a straight answer on what it costs."),
        ("Do you work with businesses outside Walton County?",
         "Yes. Walk-in services like photo shoots and house calls are local, but websites, backups, hosting, and most online services work anywhere."),
        ("How do I pay?",
         "Setup fees are paid up front, and monthly care is billed monthly by invoice. We'll confirm the details before any work starts."),
    ]
    content = f"""<main id="main">
    <section class="hero-image">
      {hero}
      <div class="container hero-inner">
        <h1>Websites, backups, and tech help for Walton County.</h1>
        <p class="lead">T1 Research &amp; Development builds websites for local businesses — and handles the tech around them, from backups to security to photography. Local, honest, and done right.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="services.html">See our services</a>
          <a class="btn btn-outline" href="contact.html">Get in touch</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2>Websites for local businesses</h2>
        <p class="section-lead">Our flagship service: a professional website for your business, built and hosted by someone local — with a care plan that keeps it fast, updated, and working.</p>
        <div class="grid grid-3">
          {''.join(tiers)}
        </div>
        <p class="center gap-top"><a class="btn btn-dark" href="contact.html?service=website-hosting">Talk about your website</a></p>
      </div>
    </section>

    <section class="section section-soft">
      <div class="container">
        <h2>More than websites — 18 services</h2>
        <p class="section-lead">Backups, security, photography, smart homes, and more. One local person to call for all of it.</p>
        <div class="services-grid">
          {cards}
        </div>
        <p class="center gap-top"><a class="btn btn-primary" href="services.html">See all 18 services</a></p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2>Local to Walton County</h2>
        <p class="section-lead">I'm Brayden Downey. I live here, I shoot here, and I work here. When you call, you get me — not a ticket queue, not a call center.</p>
        <div class="photo-strip">
          {strip}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2>Walton County after dark</h2>
        <p class="section-lead">Night shots from around the county — stars, streetlights, and neon.</p>
        <div class="photo-strip">
          {night_strip}
        </div>
        <p class="center gap-top"><a class="btn btn-primary" href="services/photography.html">See all the photography</a></p>
      </div>
    </section>

    <section class="section section-soft">
      <div class="container">
        <h2>How it works</h2>
        <div class="grid grid-4 steps">
          <div class="step"><h3>Free consult</h3><p>Tell me what you need. I'll give you a straight answer on what it costs.</p></div>
          <div class="step"><h3>Design &amp; build</h3><p>I build it and keep you in the loop as it comes together.</p></div>
          <div class="step"><h3>Review &amp; launch</h3><p>You review it, we fix what's off, then it goes live.</p></div>
          <div class="step"><h3>Care &amp; updates</h3><p>Monthly care keeps everything fast, secure, and up to date.</p></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2>Questions, answered</h2>
        {faq_block(home_faq)}
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="cta-band">
          <h2>Ready to get started?</h2>
          <p>Tell us what you need — a website, a backup, a photo shoot, or something else entirely.</p>
          <a class="btn btn-primary" href="contact.html">Get in touch</a>
        </div>
      </div>
    </section>
  </main>
"""
    page = (head(f"{SITE_NAME} | Websites & Tech Services in Walton County, GA",
                 "T1 Research & Development builds websites for Walton County businesses — plus backups, security, photography, and 18 local tech services. Local, honest, done right.",
                 "index.html", json_ld=ld, preload="hero.jpg")
            + header("home") + content + footer())
    write_page("index.html", page)


# ---------------------------------------------------------------- about page

def build_about():
    photo = img_tag("about-field.jpg", "Sunset over a Georgia field, photographed by Brayden Downey",
                    cls="about-photo")
    portraits = (
        img_tag("g-portrait-wisteria.jpg", "Portrait under wisteria on a downtown sidewalk")
        + "\n          "
        + img_tag("g-portrait-stairs.jpg", "Portrait on metal stairs")
        + "\n          "
        + img_tag("g-graduation.jpg", "Graduation portrait")
    )
    content = f"""<main id="main">
    <section class="page-hero">
      <div class="container">
        <h1>About T1 Research &amp; Development</h1>
        <p>Web &amp; Media, from Walton County, Georgia.</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="grid grid-2">
          <div>
            <h2>Hi, I'm Brayden.</h2>
            <p>I started T1 Research &amp; Development because local businesses in Walton County deserved better than a template site built by someone three states away — or no site at all.</p>
            <p>I'm a photographer first (@t1.research on Instagram) and a tech person second. That combination is the whole business: websites that look good, backups that actually work, and tech help from someone who shows up in person.</p>
            <p>Every service here is something I do myself, for people I can meet face to face. When you call, you get me.</p>
            <div class="stat-row">
              <div class="stat"><div class="value">18</div><div class="label">services offered</div></div>
              <div class="stat"><div class="value">Walton County</div><div class="label">based in Georgia</div></div>
              <div class="stat"><div class="value">@t1.research</div><div class="label">photography on Instagram</div></div>
            </div>
            <a class="btn btn-primary" href="contact.html">Work with me</a>
          </div>
          <div>
            {photo}
            <p class="caption">Sunset over a Georgia field — one of mine, from @t1.research.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2>Portraits</h2>
        <p class="section-lead">Portraits are half the work — individuals, graduates, families. A few recent ones.</p>
        <div class="photo-strip">
          {portraits}
        </div>
        <p class="center gap-top"><a class="btn btn-primary" href="services/photography.html">See all the photography</a></p>
      </div>
    </section>
  </main>
"""
    page = (head(f"About | {SITE_NAME}",
                 "T1 Research & Development is Brayden Downey's web and media business in Walton County, Georgia — websites, backups, tech help, and photography.",
                 "about.html")
            + header("about") + content + footer())
    write_page("about.html", page)


# ---------------------------------------------------------------- services index

def build_services_index():
    by_slug = {s["slug"]: s for s in SERVICES}
    grouped_slugs = [slug for _key, _title, slugs in GROUPS for slug in slugs]
    assert sorted(grouped_slugs) == sorted(by_slug), \
        "GROUPS must cover every service exactly once"
    # The flagship has no service page of its own — its card links to the
    # contact form with website hosting preselected.
    flagship_card = """<div class="service-card-wrap">
          <a class="service-card" href="contact.html?service=website-hosting">
            <h3>Website Design &amp; Hosting</h3>
            <p>Professional websites for local businesses — designed, hosted, and looked after every month.</p>
            <span class="price">From $349 setup + $49/mo</span>
            <span class="more">Get started →</span>
          </a>
        </div>"""
    sections = []
    for key, title, slugs in GROUPS:
        cards = [service_card(by_slug[slug]) for slug in slugs]
        if key == "websites":
            cards.insert(0, flagship_card)
        cards = "\n".join(cards)
        sections.append(f"""<h2 class="group-heading">{title}</h2>
        <div class="services-grid">
          {cards}
        </div>""")
    grouped = "\n".join(sections)
    content = f"""<main id="main">
    <section class="page-hero">
      <div class="container">
        <h1>Services</h1>
        <p>18 services for Walton County businesses and families — plus website design &amp; hosting, our flagship. Click any service to learn more.</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        {grouped}
      </div>
    </section>
  </main>
"""
    page = (head(f"Services | {SITE_NAME}",
                 "All 18 T1 Research & Development services: websites, backups, security, photography, smart homes, and more — for Walton County, Georgia businesses and families.",
                 "services.html")
            + header("services") + content + footer())
    write_page("services.html", page)


# ---------------------------------------------------------------- contact page

def build_contact():
    by_slug = {s["slug"]: s for s in SERVICES}
    options = ['<option value="website-hosting">Website design &amp; hosting</option>']
    for _key, title, slugs in GROUPS:
        options.append(f'<optgroup label="{title}">')
        for slug in slugs:
            options.append(f'<option value="{slug}">{by_slug[slug]["name"]}</option>')
        options.append("</optgroup>")
    options.append('<option value="something-else">Something else / not sure yet</option>')
    opts = "\n              ".join(options)
    content = f"""<main id="main">
    <section class="page-hero">
      <div class="container">
        <h1>Get in touch</h1>
        <p>Tell us what you need. We usually reply within one business day.</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="grid grid-2">
          <div class="card contact-card">
            <p class="contact-line"><a href="{PHONE_TEL}">{PHONE}</a> <button class="copy-btn" data-copy="{PHONE}" type="button">Copy</button></p>
            <p>Call or text — the fastest way to reach us.</p>
          </div>
          <div class="card contact-card">
            <p class="contact-line"><a href="mailto:{EMAIL}">{EMAIL}</a> <button class="copy-btn" data-copy="{EMAIL}" type="button">Copy</button></p>
            <p>Email works too — same-day reply on business days.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section section-soft">
      <div class="container">
        <div class="card form-card">
          <h2>Send a message</h2>
          <p id="plan-status" class="form-status" role="status"></p>
          <p id="form-status" class="form-status" role="status"></p>
          <form id="lead-form" action="{FORMSUBMIT}" method="post">
            <input type="hidden" name="_subject" value="New project inquiry — T1 Research &amp; Development">
            <input type="text" name="_honey" class="honeypot" tabindex="-1" autocomplete="off" aria-hidden="true">
            <label for="fName">Name</label>
            <input id="fName" name="name" type="text" required autocomplete="name">
            <label for="fEmail">Email</label>
            <input id="fEmail" name="email" type="email" required autocomplete="email">
            <label for="fPhone">Phone (optional)</label>
            <input id="fPhone" name="phone" type="tel" autocomplete="tel">
            <label for="fService">What service are you contacting us about?</label>
            <select id="fService" name="service" required>
              <option value="" disabled selected>Choose a service…</option>
              {opts}
            </select>
            <div id="plan-field">
              <label for="fPlan">Which hosting plan?</label>
              <select id="fPlan" name="plan">
                <option value="" disabled selected>Choose a plan…</option>
                <option value="starter">Starter — $349 setup + $49/month</option>
                <option value="standard">Standard — $499 setup + $75/month</option>
                <option value="premium">Premium — $749 setup + $99/month</option>
                <option value="unsure">Not sure yet</option>
              </select>
            </div>
            <label for="fMessage">Tell us about your project</label>
            <textarea id="fMessage" name="message" required></textarea>
            <button class="btn btn-primary btn-block" type="submit">Send message</button>
          </form>
        </div>
      </div>
    </section>
  </main>
"""
    page = (head(f"Contact | {SITE_NAME}",
                 "Contact T1 Research & Development in Walton County, Georgia — call, text, email, or send a message about any of our 18 services.",
                 "contact.html")
            + header("contact") + content + footer())
    write_page("contact.html", page)


# ---------------------------------------------------------------- service pages

def build_service_page(svc):
    depth = "../"
    rel = f"services/{svc['slug']}.html"
    ld = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": svc["name"],
        "description": svc["short"],
        "provider": {
            "@type": "LocalBusiness",
            "name": SITE_NAME,
            "telephone": "+1-770-820-7364",
            "email": EMAIL,
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Walton County",
                "addressRegion": "GA",
                "addressCountry": "US",
            },
        },
        "areaServed": "Walton County, Georgia",
        "url": BASE_URL + "/" + rel,
    }
    crumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",
             "item": BASE_URL + "/index.html"},
            {"@type": "ListItem", "position": 2, "name": "Services",
             "item": BASE_URL + "/services.html"},
            {"@type": "ListItem", "position": 3, "name": svc["name"],
             "item": BASE_URL + "/" + rel},
        ],
    }
    intro = "".join(f"<p>{p}</p>" for p in svc["intro"])
    feats = "".join(f"<li>{f}</li>" for f in svc["features"])
    og_image = "hero.jpg"
    extra = ""
    if svc.get("gallery"):
        og_image = "g-sunset-red.jpg"
        figs = []
        for name, alt in svc["gallery"]:
            figs.append(f"""<figure>
              {img_tag(name, alt, depth=depth)}
              <figcaption>{alt}</figcaption>
            </figure>""")
        extra = f"""
        <h2>Selected work</h2>
        <div class="gallery">
          {''.join(figs)}
        </div>
        <p>See more at <a href="{INSTAGRAM}">@t1.research on Instagram</a>.</p>"""
    elif svc.get("images"):
        og_image = svc["images"][0][0]
        imgs = "\n          ".join(
            img_tag(n, a, depth=depth) for n, a in svc["images"])
        extra = f"""
        <h2>The kind of photos you get</h2>
        <div class="photo-strip">
          {imgs}
        </div>"""
    content = f"""<main id="main">
    <section class="page-hero">
      <div class="container">
        <nav class="breadcrumbs" aria-label="Breadcrumb">
          <ol>
            <li><a href="{depth}index.html">Home</a></li>
            <li><a href="{depth}services.html">Services</a></li>
            <li aria-current="page">{svc['name']}</li>
          </ol>
        </nav>
        <h1>{svc['name']}</h1>
        <p>{svc['short']}</p>
      </div>
    </section>

    <section class="section">
      <div class="container service-layout">
        <div class="service-main">
          {intro}
          <h2>What's included</h2>
          <ul class="feature-list">{feats}</ul>
          {extra}
          <h2>Questions</h2>
          {faq_block(svc['faq'])}
          <p><a href="{depth}services.html">← See all services</a></p>
        </div>
        <aside class="price-box">
          <h2 class="no-top">{svc['name']}</h2>
          <p class="price">{svc['price_head']}</p>
          <p>{svc['price_note']}</p>
          <a class="btn btn-primary btn-block" href="{depth}contact.html?service={svc['slug']}">Get in touch about this</a>
          <p class="center gap-top-sm">Or call <a href="{PHONE_TEL}">{PHONE}</a></p>
        </aside>
      </div>
    </section>
  </main>
"""
    # Two JSON-LD blocks: Service + BreadcrumbList.
    ld_block = ("\n  <script type=\"application/ld+json\">\n"
                + json.dumps(ld, indent=2)
                + "\n  </script>\n  <script type=\"application/ld+json\">\n"
                + json.dumps(crumbs, indent=2) + "\n  </script>")
    page = (head(f"{svc['name']} | {SITE_NAME}",
                 f"{svc['short']} {svc['price']}. {SITE_NAME}, {CITY}.",
                 rel, og_image=og_image)
            .replace("</head>", ld_block + "\n</head>")
            + header("services", depth=depth) + content + footer(depth=depth))
    write_page(rel, page)


# ---------------------------------------------------------------- sitemap / robots / readme

def build_sitemap_robots_readme():
    pages = ["index.html", "about.html", "services.html", "contact.html"]
    pages += [f"services/{s['slug']}.html" for s in SERVICES]
    urls = []
    for p in pages:
        freq = "weekly" if p in ("index.html", "services.html") else "monthly"
        urls.append(f"  <url>\n    <loc>{BASE_URL}/{p}</loc>\n"
                    f"    <lastmod>2026-11-11</lastmod>\n"
                    f"    <changefreq>{freq}</changefreq>\n  </url>")
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "\n".join(urls) + "\n</urlset>\n")
    write_page("sitemap.xml", sitemap)
    write_page("robots.txt",
               f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")
    table_rows = "\n".join(
        f"| {s['name']} | {s['price']} |" for s in SERVICES)
    readme = f"""# {SITE_NAME}

**{TAGLINE}**

*{CITY}*

![Sunset over the ocean, photographed by Brayden Downey](images/hero.jpg)

![Pages](https://img.shields.io/badge/pages-22-0f766e)
![Services](https://img.shields.io/badge/services-18-0f766e)
![Build](https://img.shields.io/badge/build-none%20needed-0f766e)
![Photos](https://img.shields.io/badge/photos-100%25%20original-0f766e)

A 22-page static website for T1 Research & Development — home, about,
services, contact, and one page for each of the 18 services. All CSS
lives in `assets/site.css` and all JavaScript in `assets/site.js` —
no inline styling or scripting, no build step, no dependencies.

## ✨ Services

| Service | Price |
| ------- | ----- |
{table_rows}

Plus **website design & hosting**, our flagship — three plans on the
home page (Starter $349 + $49/mo · Standard $499 + $75/mo ·
Premium $749 + $99/mo).

## 📁 Structure

```
├── index.html            Home — hero, hosting tiers, services preview
├── about.html            About Brayden and T1 Research & Development
├── services.html         All 18 services, one card each
├── contact.html          Contact form with a service picker
├── services/             One page per service (18)
├── assets/
│   ├── site.css          The only stylesheet
│   └── site.js           The only script
├── images/               16 optimized @t1.research photos
├── sitemap.xml
└── robots.txt
```

## 👀 Viewing it locally

Open `index.html` in a browser, or serve the folder with any static
server (for example, `python3 -m http.server` from this folder, then
open http://localhost:8000). No build step — the files are the site.

## 📸 Photos

Every photo on this site is Brayden's own work from Instagram
[@t1.research](https://www.instagram.com/t1.research), optimized for
the web (hero 1440px, gallery 1200px, progressive JPEG).

## 📞 Contact

- **Phone:** [{PHONE}]({PHONE_TEL})
- **Email:** [{EMAIL}](mailto:{EMAIL})
- **Instagram:** [@t1.research](https://www.instagram.com/t1.research)
"""
    write_page("README.md", readme)


# ---------------------------------------------------------------- main

def main():
    build_home()
    build_about()
    build_services_index()
    build_contact()
    for svc in SERVICES:
        build_service_page(svc)
    build_sitemap_robots_readme()
    n = sum(len(files) for _, _, files in os.walk(SITE))
    print(f"built {len(SERVICES)} service pages + 4 main pages "
          f"({n} files total under site/)")


if __name__ == "__main__":
    main()
