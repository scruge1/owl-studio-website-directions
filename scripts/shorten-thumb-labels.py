"""
Shorten the demo-hook thumb labels so they don't force the
mobile 2-col grid to overflow the viewport. Long labels like
'Chartered Accountants' + 'Numbers-forward minimalism' push the
grid track wider than the phone viewport, which then triggers
the mobile browser's default viewport-fit-to-content behaviour —
rendering the whole page zoomed out.

This is a content fix, not a CSS fix. The original sample site
used one-word labels ('Neumorphism', 'Brutalism'). We match that
cadence now.
"""

from __future__ import annotations

from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / "interactive-gallery.html"
src = HTML.read_text(encoding="utf-8")

# (old name, new name, old aud, new aud)
RULES = [
    ("Dental Practice",       "Dental",       "Clinical · Swiss editorial",   "Swiss editorial"),
    ("Solicitors",             "Solicitors",   "Legal · Swiss authority",      "Swiss authority"),
    ("Chartered Accountants",  "Accountants",  "Numbers-forward minimalism",   "Minimalism"),
    ("Physiotherapy",          "Physio",       "Wellness · soft neumorphism",  "Neumorphism"),
    ("Opticians",              "Opticians",    "Premium · glassmorphism",      "Glassmorphism"),
    ("Audiology",              "Audiology",    "Calm-tech · aurora",           "Aurora calm"),
    ("Veterinary",             "Vet",          "Village vet · claymorphism",   "Claymorphism"),
    ("Wealth Advisor",         "Wealth",       "Private wealth · editorial",   "Editorial"),
    ("Architects",             "Architects",   "Tactile · 3D hyperrealism",    "3D / hyperreal"),
    ("Aesthetic Clinic",       "Aesthetic",    "Medical · aurora luxe",        "Aurora luxe"),
]

for old_name, new_name, old_aud, new_aud in RULES:
    # Only touch the demo-hook panel — these exact spans only appear there.
    old_block = f'<span class="name">{old_name}</span><span class="aud">{old_aud}</span>'
    new_block = f'<span class="name">{new_name}</span><span class="aud">{new_aud}</span>'
    assert old_block in src, f"missed: {old_block[:60]}"
    src = src.replace(old_block, new_block, 1)
    print(f"  + {old_name!r:25s} -> {new_name!r:15s} | {old_aud!r:30s} -> {new_aud!r}")

HTML.write_text(src, encoding="utf-8")
print("done.")
