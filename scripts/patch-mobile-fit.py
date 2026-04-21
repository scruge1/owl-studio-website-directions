"""
Append a mobile-fit safety-net CSS block to every sample.

The block implements the frontend-design skill's standard responsive
defenses (anti-AI-slop, battle-tested pattern):

  1. html/body clamp at 100vw with overflow-x hidden — kills any
     horizontal scroll no matter what a child element does
  2. box-sizing: border-box globally — padding can't overflow
  3. * { min-width: 0 } — flex/grid children can shrink below content
     (most common cause of mobile blow-out when long text exists)
  4. media elements scale to container — img/video/iframe/svg cap at 100%
  5. universal 640px collapse — any selector with "grid"/"cols"/"row"
     in its name flips to block display

These are added as a sibling <style> block AFTER the sample's existing
styles so the cascade order lets the safety net win. No existing CSS
is modified — the patch is purely additive and reversible.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = sorted((ROOT / "samples").glob("*.html"))
MARKER = "<!-- mobile-fit-safety -->"

SAFETY = f"""{MARKER}
<style>
/* =========================================================
   Mobile-fit safety net — applied site-wide
   Source: frontend-design skill / standard responsive defenses
   ========================================================= */
html {{ overflow-x: hidden; }}
body {{ max-width: 100vw; overflow-x: hidden; }}
*, *::before, *::after {{ box-sizing: border-box; }}
* {{ min-width: 0; }}
img, video, iframe, svg, canvas {{ max-width: 100%; height: auto; display: block; }}

@media (max-width: 640px) {{
  [class*="grid"], [class*="cols"], [class*="row"], [class*="columns"] {{
    grid-template-columns: 1fr !important;
    flex-direction: column !important;
  }}
  [class*="container"] {{ max-width: 100% !important; padding-inline: 16px !important; }}
  section, header, main, footer, article, aside, nav {{
    max-width: 100% !important;
    padding-inline: clamp(12px, 4vw, 24px) !important;
  }}
  h1 {{ font-size: clamp(30px, 8vw, 44px) !important; line-height: 1.05 !important; }}
  h2 {{ font-size: clamp(24px, 6vw, 34px) !important; }}
}}
</style>
"""


def patch(html: str) -> str | None:
    """Return patched HTML, or None if already patched."""
    if MARKER in html:
        return None
    # Append just before </head>, so cascade-order has the safety net last.
    if "</head>" not in html:
        raise ValueError("no </head> found — unexpected structure")
    return html.replace("</head>", f"{SAFETY}</head>", 1)


patched = 0
skipped = 0
for f in SAMPLES:
    src = f.read_text(encoding="utf-8")
    new = patch(src)
    if new is None:
        skipped += 1
        continue
    f.write_text(new, encoding="utf-8")
    patched += 1
    print(f"[patched] {f.name}")

if skipped:
    print(f"[skipped] {skipped} already patched")
print(f"done · {patched} patched, {skipped} skipped")
