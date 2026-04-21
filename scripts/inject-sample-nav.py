"""
Inject the Owl Studio sample-preview nav bar into every industry sample.

Adds `<script src="_owl-nav.js" defer></script>` just before </body>,
keyed off a marker comment so re-runs are idempotent.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = sorted((ROOT / "samples" / "industries").glob("*.html"))
MARKER = "<!-- owl-sample-nav -->"
SNIPPET = (
    f"{MARKER}\n"
    '<script src="_owl-nav.js" defer></script>\n'
)

patched = 0
skipped = 0
for f in SAMPLES:
    src = f.read_text(encoding="utf-8")
    if MARKER in src:
        skipped += 1
        continue
    if "</body>" not in src:
        print(f"MISS: no </body> in {f.name}", file=sys.stderr)
        sys.exit(1)
    src = src.replace("</body>", SNIPPET + "</body>", 1)
    f.write_text(src, encoding="utf-8")
    patched += 1
    print(f"[patched] {f.name}")

if skipped:
    print(f"[skipped] {skipped} already patched")
print(f"done · {patched} patched, {skipped} skipped")
