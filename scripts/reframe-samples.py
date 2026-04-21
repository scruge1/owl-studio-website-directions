"""
Reframe the "ten styles" language from a ceiling to a starting menu,
and use the bespoke-direction capacity as a real tier differentiator:

- Starter: pick any direction from the gallery
- Pro:     pick any gallery direction, or brief us on a bespoke one (included)
- Custom:  fully bespoke direction researched to your industry

The gallery keeps ten concrete examples (they do the selling). Copy just
stops implying that ten is the whole menu.
"""

from __future__ import annotations

import sys
from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / "interactive-gallery.html"
src = HTML.read_text(encoding="utf-8")

swaps = [
    # meta description
    (
        "Pick one of 10 styles, we adapt, build, host and hand over the keys in 7–14 days.",
        "Pick a starting direction from the gallery — or brief us on a bespoke one. We adapt, build, host and hand over. 7–14 days.",
    ),
    # og:description
    (
        "Pick one of 10 styles. Bring your business. We adapt it, write copy, build, host, and hand over. 7–14 days. Limerick, Ireland.",
        "Pick a starting direction from the gallery, or brief us on a bespoke one. We adapt, write the copy, build, host and hand over. 7–14 days. Limerick, Ireland.",
    ),
    # twitter:description
    (
        "Pick one of 10 styles. Bring your business. We adapt it, build, host and hand over. 7–14 days. Limerick, Ireland.",
        "Pick a starting direction, or brief us on a bespoke one. Bring your business. We adapt, build, host, hand over. 7–14 days. Limerick, Ireland.",
    ),
    # hero lede
    (
        "Pick one of ten styles below. Bring your business. We adapt it,",
        "Pick a starting direction from the gallery below — or brief us on a bespoke one. Bring your business. We adapt it,",
    ),
    # demo-hook lede
    (
        "The ten cards below aren't stock templates — they're full working\n        pages built in this repo. You pick one. We keep the structure and\n        feel, then replace every word, image, and link with yours.",
        "The ten cards below are concrete starting directions, all real\n        working pages built in this repo. You pick one — or brief us on a\n        new direction entirely. We keep the structure and feel, then\n        replace every word, image, and link with yours.",
    ),
    # demo-hook Panel 01 title
    (
        '<div class="demo-title">You pick any style from the ten below</div>\n          <p class="demo-sub">Each is a separate direction — typography, rhythm, colour system — built for a different kind of business.</p>',
        '<div class="demo-title">Start with one of ten directions — or brief a new one</div>\n          <p class="demo-sub">Each card is a real working page — typography, rhythm, colour system — built for a different kind of business. Want something not shown? On Pro and above we brief and build a bespoke direction at no extra cost.</p>',
    ),
    # Starter tier — first bullet (scope the styles to "the gallery")
    (
        "<li>Single long landing page, adapted from any of the ten gallery styles</li>",
        "<li>Single long landing page, adapted from any direction in the gallery below</li>",
    ),
    # Pro tier — bespoke direction option
    (
        "<li>Custom adaptation of any gallery style to your brand</li>",
        "<li>Custom adaptation of any gallery direction — or brief us on a fresh one, no extra cost</li>",
    ),
    # Entries / audit deliverable
    (
        "which of the ten styles",
        "which gallery direction (or a bespoke one)",
    ),
    # Gallery intro label
    (
        '<div class="section-label">Ten styles · every card a real working page</div>',
        '<div class="section-label">Ten starting directions · every card a real working page · bespoke on request</div>',
    ),
    # Gallery section aria-label
    (
        '<section class="shell gallery" aria-label="Ten website samples">',
        '<section class="shell gallery" aria-label="Ten website starting directions">',
    ),
    # FAQ "ten styles in the gallery above"
    (
        "The ten styles in the gallery above are real hand-built pages",
        "The ten directions in the gallery above are real hand-built pages — and they're a starting menu, not a ceiling (on Pro and above we brief and build a bespoke direction at no extra cost)",
    ),
]

missing = [old for old, _ in swaps if old not in src]
if missing:
    for m in missing:
        print(f"MISS: {m[:90]!r}", file=sys.stderr)
    sys.exit(1)

for old, new in swaps:
    src = src.replace(old, new, 1)

HTML.write_text(src, encoding="utf-8")
print(f"reframed {len(swaps)} copy locations in {HTML.name}")
