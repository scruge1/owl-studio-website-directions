"""Rewire gallery iframe paths to match the agent-produced sample filenames.
Update card kickers so each reflects the real industry vertical the agent
designed (editorial / meditation / fintech / agency / audio / launch /
gaming / education / music / podcast)."""
from pathlib import Path

p = Path(__file__).resolve().parent.parent / "interactive-gallery.html"
html = p.read_text(encoding="utf-8")

path_map = [
    ("samples/01-minimalism-swiss-style.html", "samples/01-minimalism-swiss.html"),
    ("samples/05-vibrant-block-based.html", "samples/06-vibrant-block.html"),
    ("samples/06-dark-mode-oled.html", "samples/07-dark-oled.html"),
    ("samples/07-claymorphism.html", "samples/08-claymorphism.html"),
    ("samples/08-aurora-ui.html", "samples/09-aurora-ui.html"),
    ("samples/09-retro-futurism.html", "samples/10-retro-futurism.html"),
    ("samples/10-3d-hyperrealism.html", "samples/05-3d-hyperrealism.html"),
]
for old, new in path_map:
    html = html.replace(old, new)

# kickers per card — each reflects the actual industry vertical the agent designed
kicker_map = [
    ("01 · Grid, hierarchy, whitespace", "01 · Online magazine"),
    ("02 · Soft 3D, subtle depth", "02 · Meditation app"),
    ("03 · Frosted blur, layered", "03 · Fintech dashboard"),
    ("04 · Raw, anti-design", "04 · Design agency portfolio"),
    ("05 · Big blocks, big energy", "05 · Startup launch page"),
    ("06 · OLED-deep, neon accents", "06 · Gaming platform"),
    ("07 · Playful, chunky, toy-like", "07 · Kids education app"),
    ("08 · Northern-lights gradients", "08 · Music streaming"),
    ("09 · CRT glow, cyberpunk", "09 · Synthwave podcast"),
    ("10 · Depth, 3D, tactile", "10 · Premium headphones"),
]
for old, new in kicker_map:
    html = html.replace(old, new)

# Reorder cards in HTML so they match the new file numbering:
# current order (after my earlier rewire): minimalism, neumorphism, glassmorphism,
# brutalism, vibrant-block, dark-oled, claymorphism, aurora, retro, 3d-hyper
# target order matching files 01-10:
# 01 minimalism, 02 neumorphism, 03 glassmorphism, 04 brutalism, 05 3d-hyper,
# 06 vibrant-block, 07 dark-oled, 08 claymorphism, 09 aurora, 10 retro-fut

# Instead of reordering HTML (complex), fix the kicker numbers to match the filenames.
# That means the vibrant/dark/clay/aurora/retro/3d cards need new kicker numbers too.
second_pass = [
    ("05 · Startup launch page", "06 · Startup launch page"),
    ("06 · Gaming platform", "07 · Gaming platform"),
    ("07 · Kids education app", "08 · Kids education app"),
    ("08 · Music streaming", "09 · Music streaming"),
    ("09 · Synthwave podcast", "10 · Synthwave podcast"),
    ("10 · Premium headphones", "05 · Premium headphones"),
]
for old, new in second_pass:
    html = html.replace(old, new)

p.write_text(html, encoding="utf-8")
print(f"rewired {p.name}")
