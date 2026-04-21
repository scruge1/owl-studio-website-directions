"""
Inject one lazy <iframe> into each of the 10 gallery cards, pointing
to its matching industry sample. Safe for tab stability because:

  - content-visibility: auto on .card defers render for off-screen cards
  - loading="lazy" on iframe defers fetch until near-viewport
  - tabindex=-1 + aria-hidden + pointer-events:none keep iframe inert
  - iframe sits at z-index:1 with themed miniature as paint fallback
    (so if iframe fails to load, the .t-XX art still shows)

Card-stage wiring (each card's iframe src is pinned by its t-class):

  t-01  -> 01-dental-swiss.html      (Dental, first card)
  t-sol -> 02-solicitor-swiss.html
  t-01  -> 03-accountant-minimalism.html  (also t-01, second occurrence)
  t-02  -> 04-physio-neumorphism.html
  t-03  -> 05-opticians-glassmorphism.html
  t-09  -> 06-audiologist-aurora.html
  t-08  -> 07-vet-claymorphism.html
  t-fin -> 08-financial-brutalism-editorial.html
  t-05  -> 09-architects-3d.html
  t-aes -> 10-aesthetic-clinic-aurora-luxe.html

Because t-01 appears twice (Dental + Accountant), the script walks the
10 cards IN ORDER via the existing card-cta primary href anchor.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / "interactive-gallery.html"
src = HTML.read_text(encoding="utf-8")

# Each card currently has:
# <div class="card-stage <miniclass>">
#   <div class="card-overlay">
#     <div class="card-cta-row">
#       <a class="card-cta primary" href="samples/industries/<slug>.html" ...>Open full sample</a>
#
# Use the industry slug in the primary href to key each insert.

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

for slug in SLUGS:
    # Find the .card-stage whose overlay primary CTA points at this slug
    # and inject an iframe right after the opening tag.
    pattern = re.compile(
        r'(<div class="card-stage [^"]+">)(\s*<div class="card-overlay">\s*<div class="card-cta-row">\s*'
        r'<a class="card-cta primary" href="samples/industries/' + re.escape(slug) + r'\.html")',
        re.MULTILINE,
    )
    replacement = (
        r'\1\n          <iframe src="samples/industries/' + slug
        + r'.html" loading="lazy" aria-hidden="true" tabindex="-1" scrolling="no" title="'
        + slug.replace("-", " ").title()
        + r' preview"></iframe>\2'
    )
    new_src, count = pattern.subn(replacement, src, count=1)
    if count != 1:
        print(f"MISS: iframe insert for {slug}", file=sys.stderr)
        sys.exit(1)
    src = new_src

HTML.write_text(src, encoding="utf-8")
print(f"injected {len(SLUGS)} lazy iframes into gallery cards")
