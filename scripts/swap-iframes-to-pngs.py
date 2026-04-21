"""
Swap each main-gallery card's live <iframe> preview for the static
PNG screenshot at renders/industries/<slug>.png. Root cause of the
earlier reload-on-scroll bug: 10 iframes each rendering a 1440x900
viewport = renderer OOM on mid-tier devices. Screenshots are the
canonical fix (same pattern Dribbble / Awwwards / Siteinspire use).

Also updates the card-stage CSS block to drop the iframe sizing
rules and replace with img rules that stretch to fit.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / "interactive-gallery.html"
src = HTML.read_text(encoding="utf-8")

SLUGS = [
    "01-dental-swiss",
    "02-solicitor-swiss",
    "03-accountant-minimalism",
    "04-physio-neumorphism",
    "05-opticians-glassmorphism",
    "06-audiologist-aurora",
    "07-vet-claymorphism",
    "08-financial-brutalism-editorial",
    "09-architects-3d",
    "10-aesthetic-clinic-aurora-luxe",
]

INDUSTRY_NAMES = {
    "01-dental-swiss": "Dental Practice",
    "02-solicitor-swiss": "Solicitors",
    "03-accountant-minimalism": "Chartered Accountants",
    "04-physio-neumorphism": "Physiotherapy Clinic",
    "05-opticians-glassmorphism": "Opticians",
    "06-audiologist-aurora": "Audiology · Hearing Care",
    "07-vet-claymorphism": "Veterinary Practice",
    "08-financial-brutalism-editorial": "Wealth · Financial Advisors",
    "09-architects-3d": "Architects · Engineering",
    "10-aesthetic-clinic-aurora-luxe": "Aesthetic · Medical Clinic",
}


# 1. Swap each iframe -> img. Keep the opening .card-stage <div> + .card-overlay intact.
for slug in SLUGS:
    old_iframe = re.compile(
        r'<iframe src="samples/industries/' + re.escape(slug) + r'\.html"[^>]*></iframe>'
    )
    alt = f"{INDUSTRY_NAMES[slug]} — Owl Studio sample preview"
    new_img = (
        f'<img src="renders/industries/{slug}.png" '
        f'alt="{alt}" loading="lazy" decoding="async" width="1440" height="900" '
        f'class="card-preview">'
    )
    new_src, n = old_iframe.subn(new_img, src, count=1)
    if n != 1:
        print(f"MISS: iframe for {slug}", file=sys.stderr)
        sys.exit(1)
    src = new_src
    print(f"  swapped  {slug}")


# 2. Replace the .card-stage iframe CSS block with img rules.
iframe_css_old = '''    /* Live iframe preview — rendered at fixed desktop viewport, scaled to fit card */
    .card-stage iframe {
      position: absolute;
      top: 0; left: 0;
      width: 1440px;
      height: 900px;
      border: 0;
      pointer-events: none;
      background: #fff;
      transform-origin: top left;
      transform: scale(0.23);
      z-index: 1;
    }
    @media (min-width: 480px)  { .card-stage iframe { transform: scale(0.30); } }
    @media (min-width: 640px)  { .card-stage iframe { transform: scale(0.40); } }
    @media (min-width: 900px)  { .card-stage iframe { transform: scale(0.34); } }
    @media (min-width: 1100px) { .card-stage iframe { transform: scale(0.40); } }
    @media (min-width: 1280px) { .card-stage iframe { transform: scale(0.46); } }
    @media (min-width: 1440px) { .card-stage iframe { transform: scale(0.50); } }'''

iframe_css_new = '''    /* Static PNG preview — screenshots of each sample at 1440x900.
       Replaces the old live-iframe pattern that OOM-crashed on
       mid-tier devices when 3-4 cards were visible simultaneously. */
    .card-stage .card-preview {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: top center;
      display: block;
      background: transparent;
      z-index: 1;
    }'''

if iframe_css_old in src:
    src = src.replace(iframe_css_old, iframe_css_new, 1)
    print("  replaced card-stage iframe CSS")
else:
    print("[warn] iframe CSS block not found — may already be replaced", file=sys.stderr)


HTML.write_text(src, encoding="utf-8")
print("done.")
