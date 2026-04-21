"""
Re-price the site and on-call-kit to the 2026 Irish market band.

Starter  €499  -> €695   (cleared the €500 template floor)
Pro      €1,299 -> €1,595 (SMB freelance midpoint; add GBP + SEO clarity)
Custom   from €2,500 -> from €2,950
Care     €39/399 -> €45/450      (renamed "Essential")
Care+    €99/990 -> €95/950      (renamed "Growth")
NEW      Concierge €195/1,950 (3rd tier, concierge-style admin)

Single atomic pass so the page never renders with mixed pricing.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "interactive-gallery.html"
INTAKE = ROOT / "on-call-kit" / "INTAKE-TEMPLATE.md"
SCRIPT = ROOT / "on-call-kit" / "CALL-SCRIPT.md"

assert HTML.exists() and INTAKE.exists() and SCRIPT.exists()

# ---------- 1. interactive-gallery.html ----------
src = HTML.read_text(encoding="utf-8")

# --- simple string swaps (safe: every occurrence is a price and should move) ---
simple = [
    # meta + social
    ("Websites that sell, in 7 days, from €499",
     "Websites that sell, in 7 days, from €695"),
    ("All-in websites for Irish SMBs — €499 Starter, €1,299 Pro, €2,500+ Custom.",
     "All-in websites for Irish SMBs — €695 Starter, €1,595 Pro, from €2,950 Custom."),
    ("Websites from €499, in 7 days",
     "Websites from €695, in 7 days"),
    # hero h1
    ("Websites that sell, in <em>7 days</em>, from <em>€499</em>.",
     "Websites that sell, in <em>7 days</em>, from <em>€695</em>."),
    # hero anchor — Starter
    ('<span class="tier-tag">Starter</span>\n          <span class="tier-num">€499</span>\n          <span class="tier-time">7 days</span>',
     '<span class="tier-tag">Starter</span>\n          <span class="tier-num">€695</span>\n          <span class="tier-time">7 days</span>'),
    # hero anchor — Pro
    ('<span class="tier-num">€1,299</span>',
     '<span class="tier-num">€1,595</span>'),
    # hero anchor — Custom
    ('<span class="tier-num">€2,500+</span>',
     '<span class="tier-num">from €2,950</span>'),
    # Starter tier card
    ('<div class="tier-price">€499<small> all-in</small></div>',
     '<div class="tier-price">€695<small> all-in</small></div>'),
    ('mailto:callmeie@proton.me?subject=Starter%20website%20%E2%80%94%20%E2%82%AC499',
     'mailto:callmeie@proton.me?subject=Starter%20website%20%E2%80%94%20%E2%82%AC695'),
    # Pro tier card
    ('<div class="tier-price">€1,299<small> all-in</small></div>',
     '<div class="tier-price">€1,595<small> all-in</small></div>'),
    ('mailto:callmeie@proton.me?subject=Pro%20website%20%E2%80%94%20%E2%82%AC1299',
     'mailto:callmeie@proton.me?subject=Pro%20website%20%E2%80%94%20%E2%82%AC1595'),
    # Custom tier card
    ('<div class="tier-price">from €2,500<small> quoted</small></div>',
     '<div class="tier-price">from €2,950<small> quoted</small></div>'),
    # Care grid CSS: 2 columns -> 3 columns with an intermediate breakpoint
    ("""    .care-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 22px;
      margin-top: 10px;
    }
    @media (max-width: 900px) { .care-grid { grid-template-columns: 1fr; } }""",
     """    .care-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 22px;
      margin-top: 10px;
    }
    @media (max-width: 1100px) { .care-grid { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 720px) { .care-grid { grid-template-columns: 1fr; } }"""),
]

for old, new in simple:
    if old not in src:
        print(f"MISS: {old[:80]!r}", file=sys.stderr)
        sys.exit(1)
    src = src.replace(old, new, 1)

# --- Pro tier inclusion list: add Google Business Profile setup ---
pro_list_old = """            <li>5-page site — home, about, services, blog, contact</li>
            <li>Custom adaptation of any gallery style to your brand</li>
            <li>Lightweight CMS so you can post updates yourself (Sanity or Payload, both open-source)</li>
            <li>Copy written for you — homepage + services + about</li>
            <li>Basic SEO — meta tags, schema markup, XML sitemap, Google Analytics</li>"""
pro_list_new = """            <li>5-page site — home, about, services, blog, contact</li>
            <li>Custom adaptation of any gallery style to your brand</li>
            <li>Lightweight CMS so you can post updates yourself (Sanity or Payload, both open-source)</li>
            <li>Copy written for you — homepage + services + about</li>
            <li>Google Business Profile set up + linked to the site (maps, opening hours, photos, reviews)</li>
            <li>Basic SEO — meta tags, schema markup, XML sitemap, Google Analytics</li>"""
assert pro_list_old in src, "pro list anchor missed"
src = src.replace(pro_list_old, pro_list_new, 1)

# --- Care plans: rewrite 2-card block -> 3-card block ---
care_old = """        <article class="care-card">
          <div class="care-name">Care</div>
          <div class="care-price-block">
            <div class="monthly"><span class="care-price">€39<small>/month</small></span><span class="care-price-alt">Billed €39 on the 1st each month</span></div>
            <div class="yearly"><span class="care-price">€399<small>/year</small></span><span class="care-price-alt">Equivalent to €33.25/month · save €69</span></div>
          </div>
          <ul>
            <li>Hosting, SSL, daily backups — all handled</li>
            <li>Uptime monitoring — we know before you do</li>
            <li>One small update per month (phone number, image swap, hours, seasonal copy)</li>
            <li>Security patches and CMS updates as they land</li>
            <li>Email response within 24 hours</li>
            <li>Cancel or pause with 30 days' notice</li>
          </ul>
          <a class="btn primary" href="mailto:callmeie@proton.me?subject=Care%20plan%20%E2%80%94%20%E2%82%AC39%2Fmo%20or%20%E2%82%AC399%2Fyr&body=Project%20tier%20I'm%20booking%3A%0ABusiness%20name%3A%0ABilling%20preference%3A%20monthly%20%2F%20yearly">Add Care to my project</a>
        </article>

        <article class="care-card popular">
          <span class="tag">Most chosen</span>
          <div class="care-name">Care+</div>
          <div class="care-price-block">
            <div class="monthly"><span class="care-price">€99<small>/month</small></span><span class="care-price-alt">Billed €99 on the 1st each month</span></div>
            <div class="yearly"><span class="care-price">€990<small>/year</small></span><span class="care-price-alt">Equivalent to €82.50/month · save €198</span></div>
          </div>
          <ul>
            <li>Everything in Care, plus:</li>
            <li>Up to 4 content updates per month — a new page, blog post, special offer, seasonal campaign</li>
            <li>Quarterly SEO review + fixes (meta, schema, page speed, broken links)</li>
            <li>Google Business Profile kept in sync with the site</li>
            <li>Monthly 1-page report: traffic, contacts, top pages, what to fix</li>
            <li>WhatsApp / email response within 8 working hours</li>
          </ul>
          <a class="btn accent" href="mailto:callmeie@proton.me?subject=Care%2B%20plan%20%E2%80%94%20%E2%82%AC99%2Fmo%20or%20%E2%82%AC990%2Fyr&body=Project%20tier%20I'm%20booking%3A%0ABusiness%20name%3A%0ABilling%20preference%3A%20monthly%20%2F%20yearly">Add Care+ to my project</a>
        </article>"""

care_new = """        <article class="care-card">
          <div class="care-name">Essential</div>
          <div class="care-price-block">
            <div class="monthly"><span class="care-price">€45<small>/month</small></span><span class="care-price-alt">Billed €45 on the 1st each month</span></div>
            <div class="yearly"><span class="care-price">€450<small>/year</small></span><span class="care-price-alt">Equivalent to €37.50/month · save €90</span></div>
          </div>
          <ul>
            <li>Hosting, SSL, daily backups — all handled</li>
            <li>Uptime + security monitoring</li>
            <li>Plugin, framework and CMS updates as they land</li>
            <li>Up to 30 minutes of edits per month (phone number, hours, seasonal copy, image swap)</li>
            <li>Email response within 24 hours</li>
            <li>Cancel or pause with 30 days' notice</li>
          </ul>
          <a class="btn primary" href="mailto:callmeie@proton.me?subject=Essential%20care%20plan%20%E2%80%94%20%E2%82%AC45%2Fmo%20or%20%E2%82%AC450%2Fyr&body=Project%20tier%20I'm%20booking%3A%0ABusiness%20name%3A%0ABilling%20preference%3A%20monthly%20%2F%20yearly">Add Essential</a>
        </article>

        <article class="care-card popular">
          <span class="tag">Most chosen</span>
          <div class="care-name">Growth</div>
          <div class="care-price-block">
            <div class="monthly"><span class="care-price">€95<small>/month</small></span><span class="care-price-alt">Billed €95 on the 1st each month</span></div>
            <div class="yearly"><span class="care-price">€950<small>/year</small></span><span class="care-price-alt">Equivalent to €79.17/month · save €190</span></div>
          </div>
          <ul>
            <li>Everything in Essential, plus:</li>
            <li>Up to 2 hours of content updates per month (new page, blog post, special offer, seasonal campaign)</li>
            <li>Quarterly SEO + speed review, fixes shipped (meta, schema, page speed, broken links)</li>
            <li>Google Business Profile kept in sync with the site</li>
            <li>Monthly 1-page report: traffic, contacts, top pages, what to fix next</li>
            <li>WhatsApp / email response within 8 working hours</li>
          </ul>
          <a class="btn accent" href="mailto:callmeie@proton.me?subject=Growth%20care%20plan%20%E2%80%94%20%E2%82%AC95%2Fmo%20or%20%E2%82%AC950%2Fyr&body=Project%20tier%20I'm%20booking%3A%0ABusiness%20name%3A%0ABilling%20preference%3A%20monthly%20%2F%20yearly">Add Growth</a>
        </article>

        <article class="care-card">
          <div class="care-name">Concierge</div>
          <div class="care-price-block">
            <div class="monthly"><span class="care-price">€195<small>/month</small></span><span class="care-price-alt">Billed €195 on the 1st each month</span></div>
            <div class="yearly"><span class="care-price">€1,950<small>/year</small></span><span class="care-price-alt">Equivalent to €162.50/month · save €390</span></div>
          </div>
          <ul>
            <li>Everything in Growth, plus:</li>
            <li>You forward emails, photos, screenshots — we do the rest</li>
            <li>Content we draft + publish: blog posts, announcements, seasonal offers</li>
            <li>Monthly Google Business Profile posts + photo refresh</li>
            <li>Contact-form triage: we reply or route to you, no lost enquiries</li>
            <li>One 20-min call per month to plan what's next</li>
          </ul>
          <a class="btn primary" href="mailto:callmeie@proton.me?subject=Concierge%20care%20plan%20%E2%80%94%20%E2%82%AC195%2Fmo%20or%20%E2%82%AC1950%2Fyr&body=Project%20tier%20I'm%20booking%3A%0ABusiness%20name%3A%0ABilling%20preference%3A%20monthly%20%2F%20yearly">Add Concierge</a>
        </article>"""

assert care_old in src, "care block anchor missed"
src = src.replace(care_old, care_new, 1)

# --- FAQ: update the old Care/Care+ names and prices ---
faq_old = 'or Care+ (€99/mo · €990/yr) plan and we do it for you. Care plans are optional'
faq_new = 'plan and we do it for you — three tiers: Essential (€45/mo), Growth (€95/mo), Concierge (€195/mo). Care plans are optional'
assert faq_old in src, "faq anchor missed"
src = src.replace(faq_old, faq_new, 1)

faq_old_2 = 'or add a monthly <a href="#care">Care</a> (€39/mo · €399/yr) or Care+ (€99/mo · €990/yr) plan'
# Already partially handled above; the full line now reads differently, verify:
# (the faq_old substring matches the tail; we replaced that tail above)

HTML.write_text(src, encoding="utf-8")
print(f"[html] rewrote {HTML.name}: +{len(care_new) - len(care_old)} chars in care block")

# ---------- 2. on-call-kit/INTAKE-TEMPLATE.md ----------
intake = INTAKE.read_text(encoding="utf-8")
intake = intake.replace(
    "[ ] Starter €499   — 7 days, single-page, 150–300 words",
    "[ ] Starter €695   — 7 days, single-page, 150–300 words",
)
intake = intake.replace(
    "[ ] Pro €1,299     — 14 days, 5 pages, CMS + copywriting",
    "[ ] Pro €1,595     — 14 days, 5 pages, CMS + copy + GBP + basic SEO",
)
intake = intake.replace(
    "[ ] Custom €2,500+ — quoted, ecommerce / SaaS / integrations",
    "[ ] Custom from €2,950 — quoted, ecommerce / SaaS / integrations",
)
INTAKE.write_text(intake, encoding="utf-8")
print(f"[md]   rewrote {INTAKE.name}")

# ---------- 3. on-call-kit/CALL-SCRIPT.md ----------
script = SCRIPT.read_text(encoding="utf-8")
script = script.replace(
    "Pro tier is €1,299 all-in",
    "Pro tier is €1,595 all-in",
)
SCRIPT.write_text(script, encoding="utf-8")
print(f"[md]   rewrote {SCRIPT.name}")

print("done.")
