#!/usr/bin/env python3
"""Generate the T1 Research & Development multi-page website.

Builds 18 pages (home, about, services, contact + 14 service pages),
sitemap.xml, robots.txt and a deploy README into the site root.

Layout: this script lives in tools/. The site root is the tools/
directory's parent when that parent holds a site/ directory (Sabrent's
working copy), otherwise the parent itself (repo checkout: tools/ sits
next to the site files at the repo root).

All copy is Brayden's own: the 17 liked AWS business ideas (Nov 11,
easiest-to-hardest order) plus Photography as the 14th service.
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
FACEBOOK = "https://www.facebook.com/profile.php?id=61596618475986"
NEXTDOOR = "https://nextdoor.com/page/t1-research-development-monroe-ga"

# Footer social icons (inline SVG, currentColor so they match footer links).
ICON_INSTAGRAM = '<svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077"/></svg>'
ICON_FACEBOOK = '<svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"/></svg>'
# Nextdoor's official mark is the full "nextdoor" wordmark — unreadable at 26px —
# so the footer uses the app-icon "n" in Nextdoor green (#8ED500) instead.
ICON_NEXTDOOR = '<svg width="26" height="26" viewBox="0 0 24 24" aria-hidden="true"><rect x="1" y="1" width="22" height="22" rx="6" fill="#8ED500"/><path d="M8 17.5V11a4 4 0 0 1 8 0v6.5" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/></svg>'

# Google Tag Manager (Brayden's container GTM-WBZLTTZM). Verbatim snippet he
# supplied Nov 12 — kept as a constant because the braces would break f-strings.
GTM_HEAD = """  <script async src="https://www.googletagmanager.com/gtm.js?id=GTM-WBZLTTZM"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
  </script>"""

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
# first card under Websites on the services page, first contact-form option).
GROUPS = [
    ("websites", "Websites",
     ["link-in-bio", "personal-website"]),
    ("business", "For Businesses",
     ["business-backup", "vpn", "security-system"]),
    ("home", "For Homes & Families",
     ["parental-controls", "family-backup", "tech-help",
      "smart-home", "cold-storage", "game-servers"]),
    ("media", "Photography & Media",
     ["church-hosting", "photography", "photo-refresh"]),
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
{GTM_HEAD}
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
          <a href="{depth}services/photography.html">Photography service</a></p>
          <p><strong>Socials</strong></p>
          <div class="social-icons">
            <a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram — @t1.research">{ICON_INSTAGRAM}</a>
            <a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="Facebook — T1 Research &amp; Development">{ICON_FACEBOOK}</a>
            <a href="{NEXTDOOR}" target="_blank" rel="noopener" aria-label="Nextdoor — T1 Research &amp; Development">{ICON_NEXTDOOR}</a>
          </div>
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
        "description": "Websites, backups, and tech help for Walton County, Georgia. Website design and hosting, business and family backups, and 14 local services.",
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
        "sameAs": [INSTAGRAM, FACEBOOK, NEXTDOOR],
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

  </main>
"""
    page = (head(f"{SITE_NAME} | Websites & Tech Services in Walton County, GA",
                 "T1 Research & Development builds websites for Walton County businesses — plus backups, security, photography, and 14 local tech services. Local, honest, done right.",
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
              <div class="stat"><div class="value">14</div><div class="label">services offered</div></div>
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
        <p>14 services for Walton County businesses and families — plus website design &amp; hosting, our flagship. Click any service to learn more.</p>
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
                 "All 14 T1 Research & Development services: websites, backups, security, photography, smart homes, and more — for Walton County, Georgia businesses and families.",
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
                 "Contact T1 Research & Development in Walton County, Georgia — call, text, email, or send a message about any of our 14 services.",
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

![Pages](https://img.shields.io/badge/pages-18-0f766e)
![Services](https://img.shields.io/badge/services-14-0f766e)
![Build](https://img.shields.io/badge/build-none%20needed-0f766e)
![Photos](https://img.shields.io/badge/photos-100%25%20original-0f766e)

An 18-page static website for T1 Research & Development — home, about,
services, contact, and one page for each of the 14 services. All CSS
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
├── services.html         All 14 services, one card each
├── contact.html          Contact form with a service picker
├── services/             One page per service (14)
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
- **Facebook:** [T1 Research & Development](https://www.facebook.com/profile.php?id=61596618475986)
- **Nextdoor:** [T1 Research & Development](https://nextdoor.com/page/t1-research-development-monroe-ga)
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
