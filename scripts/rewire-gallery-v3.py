"""
Rewire the main gallery section: strip all 10 <iframe> previews,
add themed `t-XX` class to each `.card-stage`.

Reason: 10 scaled iframes crash Chrome's renderer around sample #8
(Claymorphism). Themed CSS miniatures are already defined in the
page; this script just re-tags each card-stage to pick them up.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / "interactive-gallery.html"
assert HTML.exists(), f"missing {HTML}"

src = HTML.read_text(encoding="utf-8")

# 1. Tag each card-stage with its t-XX class, keyed off the iframe's sample path.
pattern = re.compile(
    r'<div class="card-stage">\s*\n\s*<iframe src="samples/(\d{2})-[^"]+" title="[^"]+" loading="lazy"></iframe>',
    re.MULTILINE,
)


def replace(match: re.Match) -> str:
    n = match.group(1)  # "01" .. "10"
    return f'<div class="card-stage t-{n}">'


new_src, count = pattern.subn(replace, src)
if count != 10:
    print(f"expected 10 card-stage iframes, matched {count}", file=sys.stderr)
    sys.exit(1)

HTML.write_text(new_src, encoding="utf-8")
print(f"rewired {count} card-stage blocks; removed {count} iframes")
