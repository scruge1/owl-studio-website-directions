"""
Repoint the main gallery + demo-hook thumbs + showcase iframe
from the legacy style-only samples to the new industry samples.

Each gallery card now carries an Irish SMB vertical as the headline,
with its paired style as the kicker. Links resolve to
`samples/industries/0X-<slug>.html`.

Also adds 3 new themed-miniature classes (.t-sol, .t-fin, .t-aes)
for pairings that didn't exist in the old 10-style legacy set.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "interactive-gallery.html"
src = HTML.read_text(encoding="utf-8")

# ---------------------------------------------------------------
# 1. Inject 3 new themed miniatures into the CSS block
#    (Swiss Authority dark, Brutalism Editorial quiet, Aurora Luxe)
# ---------------------------------------------------------------

new_minis = """
    /* t-sol — Solicitor · Swiss Authority (ink base, cream reverse-out) */
    .t-sol { background: #0b0a08; }
    .t-sol::before {
      content: "02";
      position: absolute;
      left: 12px; top: 14px;
      font-family: var(--display);
      font-weight: 900; font-size: 72px; line-height: 0.85;
      letter-spacing: -0.05em;
      color: #F5F1E8;
    }
    .t-sol::after {
      content: "";
      position: absolute;
      left: 12px; right: 12px; top: 10px;
      height: 3px; background: #F5F1E8;
      box-shadow: 0 40px 0 0 #B38B6D;
    }
    .card-stage.t-sol::before { font-size: clamp(140px, 19vw, 220px); left: 24px; top: 30px; }
    .card-stage.t-sol::after { left: 24px; right: 24px; top: 20px; height: 6px; box-shadow: 0 72px 0 0 #B38B6D; }

    /* t-fin — Financial · Brutalism Editorial (cream paper, ink rules, burgundy) */
    .t-fin { background: #F5F1E8; }
    .t-fin::before {
      content: "";
      position: absolute;
      inset: 0;
      background:
        linear-gradient(to bottom, transparent 0 18%, #0b0a08 18% 19%, transparent 19% 100%),
        linear-gradient(to bottom, transparent 0 52%, #0b0a08 52% 53%, transparent 53% 100%),
        linear-gradient(to bottom, transparent 0 82%, #5A1420 82% 84%, transparent 84% 100%);
    }
    .t-fin::after {
      content: "KW";
      position: absolute;
      left: 12px; bottom: 42%;
      font-family: var(--display);
      font-weight: 900; font-size: 40px; letter-spacing: -0.04em;
      color: #0b0a08;
      z-index: 2;
    }
    .card-stage.t-fin::after { font-size: clamp(60px, 9vw, 140px); bottom: 42%; left: 24px; }

    /* t-aes — Aesthetic clinic · Aurora Luxe (deep ink + gold anchor) */
    .t-aes {
      background:
        radial-gradient(ellipse 60% 40% at 18% 22%, rgba(124, 58, 255, 0.55) 0%, transparent 60%),
        radial-gradient(ellipse 55% 40% at 82% 18%, rgba(255, 0, 204, 0.45) 0%, transparent 60%),
        radial-gradient(ellipse 60% 45% at 50% 82%, rgba(255, 179, 71, 0.4) 0%, transparent 60%),
        #0a0718;
    }
    .t-aes::before {
      content: "";
      position: absolute;
      left: 42%; top: 34%;
      width: 16%; height: 24%;
      border: 1px solid rgba(255, 215, 0, 0.65);
      box-shadow: 0 0 18px rgba(255, 215, 0, 0.25);
    }
"""

marker = "    /* 10 — Retro-Futurism (samples/10):"
assert marker in src, "themed-art block not found"
# insert just before the existing t-10 block so new minis live with their cousins
src = src.replace(marker, new_minis + "\n" + marker, 1)

# ---------------------------------------------------------------
# 2. Rewire the main gallery: 10 cards, each repointed to an industry
# ---------------------------------------------------------------

INDUSTRIES = [
    # (n, h2, kicker, mini-class, slug, mailto-subject-slug)
    ("01", "Dental Practice",               "01 · Swiss Editorial",       "t-01",  "01-dental-swiss",                       "Dental%20practice%20website"),
    ("02", "Solicitors",                    "02 · Swiss Authority",       "t-sol", "02-solicitor-swiss",                    "Solicitor%20practice%20website"),
    ("03", "Chartered Accountants",         "03 · Numbers-forward",       "t-01",  "03-accountant-minimalism",              "Accountancy%20practice%20website"),
    ("04", "Physiotherapy Clinic",          "04 · Soft Neumorphism",      "t-02",  "04-physio-neumorphism",                 "Physiotherapy%20clinic%20website"),
    ("05", "Opticians",                     "05 · Glassmorphism",         "t-03",  "05-opticians-glassmorphism",            "Opticians%20website"),
    ("06", "Audiology · Hearing Care",      "06 · Aurora Calm",           "t-09",  "06-audiologist-aurora",                 "Audiology%20clinic%20website"),
    ("07", "Veterinary Practice",           "07 · Claymorphism",          "t-08",  "07-vet-claymorphism",                   "Veterinary%20practice%20website"),
    ("08", "Wealth · Financial Advisors",   "08 · Editorial Brutalism",   "t-fin", "08-financial-brutalism-editorial",      "Wealth%20advisor%20website"),
    ("09", "Architects · Engineering",      "09 · 3D Hyperrealism",       "t-05",  "09-architects-3d",                      "Architects%20practice%20website"),
    ("10", "Aesthetic · Medical Clinic",    "10 · Aurora Luxe",           "t-aes", "10-aesthetic-clinic-aurora-luxe",       "Aesthetic%20clinic%20website"),
]

# Replace each of the 10 .card blocks. Pattern: from <article class="card"> to </article>,
# matched one at a time by keying off the old iframe src (still in the kicker comments).

# The existing structure:
# <article class="card">
#   <header class="card-header"><h2>...</h2><span class="kicker">...</span></header>
#   <div class="card-stage t-XX">
#     <div class="card-overlay">
#       <div class="card-cta-row">
#         <a class="card-cta primary" href="samples/01-minimalism-swiss.html" ...>Open full page ↗</a>
#         <a class="card-cta" href="mailto:...">Build this style</a>
#       </div>
#     </div>
#   </div>
# </article>
#
# Identify each card by its t-XX class + card-cta href to the legacy sample.

LEGACY_SLUGS = [
    "01-minimalism-swiss", "02-neumorphism", "03-glassmorphism", "04-brutalism",
    "05-3d-hyperrealism", "06-vibrant-block", "07-dark-oled", "08-claymorphism",
    "09-aurora-ui", "10-retro-futurism",
]

for (ind, (n, h2, kicker, mini, slug, mail)) in zip(INDUSTRIES, INDUSTRIES):
    # each entry iterates itself — zip for symmetry; we only need INDUSTRIES
    pass

for i, (n, h2, kicker, mini, slug, mail) in enumerate(INDUSTRIES):
    legacy = LEGACY_SLUGS[i]
    # card template: match from <article class="card"> up through the first
    # .card-stage following the legacy href. Pin by legacy href (unique per card).
    old_pattern = re.compile(
        r'<article class="card">\s*'
        r'<header class="card-header">\s*'
        r'<h2>[^<]+</h2>\s*'
        r'<span class="kicker">[^<]+</span>\s*'
        r'</header>\s*'
        r'<div class="card-stage t-\d{2}">\s*'
        r'<div class="card-overlay">\s*'
        r'<div class="card-cta-row">\s*'
        r'<a class="card-cta primary" href="samples/' + re.escape(legacy) + r'\.html"[^>]*>[^<]+</a>\s*'
        r'<a class="card-cta" href="mailto:[^"]+">[^<]+</a>\s*'
        r'</div>\s*</div>\s*</div>\s*</article>',
        re.MULTILINE,
    )
    new_block = f'''<article class="card">
        <header class="card-header">
          <h2>{h2}</h2>
          <span class="kicker">{kicker}</span>
        </header>
        <div class="card-stage {mini}">
          <div class="card-overlay">
            <div class="card-cta-row">
              <a class="card-cta primary" href="samples/industries/{slug}.html" target="_blank" rel="noreferrer">Open full sample ↗</a>
              <a class="card-cta" href="mailto:callmeie@proton.me?subject={mail}">Build this for me</a>
            </div>
          </div>
        </div>
      </article>'''
    new_src, count = old_pattern.subn(new_block, src, count=1)
    if count != 1:
        print(f"MISS card {n} ({legacy})", file=sys.stderr)
        sys.exit(1)
    src = new_src

# ---------------------------------------------------------------
# 3. Rewire demo-hook Panel 01 thumbs to industries too
# ---------------------------------------------------------------

DEMO_INDUSTRIES = [
    # (thumb-class, slug, num, name, aud)
    ("t-01",  "01-dental-swiss",                        "01", "Dental Practice",        "Clinical · Swiss editorial"),
    ("t-sol", "02-solicitor-swiss",                     "02", "Solicitors",             "Legal · Swiss authority"),
    ("t-01",  "03-accountant-minimalism",               "03", "Chartered Accountants",  "Numbers-forward minimalism"),
    ("t-02",  "04-physio-neumorphism",                  "04", "Physiotherapy",          "Wellness · soft neumorphism"),
    ("t-03",  "05-opticians-glassmorphism",             "05", "Opticians",              "Premium · glassmorphism"),
    ("t-09",  "06-audiologist-aurora",                  "06", "Audiology",              "Calm-tech · aurora"),
    ("t-08",  "07-vet-claymorphism",                    "07", "Veterinary",             "Village vet · claymorphism"),
    ("t-fin", "08-financial-brutalism-editorial",       "08", "Wealth Advisor",         "Private wealth · editorial"),
    ("t-05",  "09-architects-3d",                       "09", "Architects",             "Tactile · 3D hyperrealism"),
    ("t-aes", "10-aesthetic-clinic-aurora-luxe",        "10", "Aesthetic Clinic",       "Medical · aurora luxe"),
]

# Existing pattern for each demo-thumb:
# <a class="demo-thumb t-XX" href="samples/0X-*.html" target="_blank" rel="noopener">...
# Replace all 10.
for (mini, slug, num, name, aud), legacy in zip(DEMO_INDUSTRIES, LEGACY_SLUGS):
    thumb_old = re.compile(
        r'<a class="demo-thumb t-\d{2}" href="samples/' + re.escape(legacy) + r'\.html"[^>]*>'
        r'<span class="meta"><span class="num">\d{2}</span>'
        r'<span class="name">[^<]+</span>'
        r'<span class="aud">[^<]+</span></span></a>'
    )
    thumb_new = (
        f'<a class="demo-thumb {mini}" href="samples/industries/{slug}.html" target="_blank" rel="noopener">'
        f'<span class="meta"><span class="num">{num}</span>'
        f'<span class="name">{name}</span>'
        f'<span class="aud">{aud}</span></span></a>'
    )
    new_src, count = thumb_old.subn(thumb_new, src, count=1)
    if count != 1:
        print(f"MISS demo-thumb {num} ({legacy})", file=sys.stderr)
        sys.exit(1)
    src = new_src

# ---------------------------------------------------------------
# 4. Repoint the demo-hook showcase iframe to the strongest prototype
# ---------------------------------------------------------------

showcase_old = '<iframe src="samples/06-vibrant-block.html" loading="lazy" tabindex="-1" aria-hidden="true"></iframe>'
showcase_new = '<iframe src="samples/industries/01-dental-swiss.html" loading="lazy" tabindex="-1" aria-hidden="true"></iframe>'
assert showcase_old in src, "showcase iframe not found"
src = src.replace(showcase_old, showcase_new, 1)

# ---------------------------------------------------------------
# 5. Update the gallery intro + demo-hook copy to reflect industries
# ---------------------------------------------------------------

copy_swaps = [
    (
        'Start with one of ten directions — or brief a new one',
        'Ten Irish-SMB samples — or brief a fresh vertical',
    ),
    (
        '<section class="shell gallery" aria-label="Ten website starting directions">',
        '<section class="shell gallery" aria-label="Ten Irish industry samples">',
    ),
    (
        '<div class="section-label">Ten starting directions · every card a real working page · bespoke on request</div>',
        '<div class="section-label">Ten Irish industries · every card a real working sample · bespoke on request</div>',
    ),
    (
        "The ten cards below are concrete starting directions, all real\n        working pages built in this repo. You pick one — or brief us on a\n        new direction entirely. We keep the structure and feel, then\n        replace every word, image, and link with yours.",
        "The ten cards below are full working samples for ten Irish SMB\n        verticals — real businesses, real fees, real Irish context.\n        Pick the one closest to yours (we adapt it to your brand), or\n        brief us on a vertical not shown.",
    ),
    # FAQ line
    (
        "The ten directions in the gallery above are real hand-built pages",
        "The ten industry samples in the gallery above are real hand-built pages",
    ),
]

for old, new in copy_swaps:
    if old not in src:
        print(f"MISS copy: {old[:80]!r}", file=sys.stderr)
        sys.exit(1)
    src = src.replace(old, new, 1)

HTML.write_text(src, encoding="utf-8")
print("rewire complete.")
print(f"  - 10 main gallery cards repointed to samples/industries/")
print(f"  - 10 demo-hook thumbs repointed to samples/industries/")
print(f"  - demo-hook showcase iframe: industry dental prototype")
print(f"  - 3 new themed miniatures injected (.t-sol, .t-fin, .t-aes)")
print(f"  - gallery/demo copy updated to industry framing")
