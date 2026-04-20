"""One-shot: rewire interactive-gallery.html card titles / kickers / mailto
subjects / sample paths to match the new skill-driven samples in /samples/."""
from pathlib import Path

p = Path(__file__).resolve().parent.parent / "interactive-gallery.html"
html = p.read_text(encoding="utf-8")

replacements = [
    # sample file paths
    ("samples/01-glass-morphism.html", "samples/01-minimalism-swiss-style.html"),
    ("samples/02-brutalist-raw.html", "samples/02-neumorphism.html"),
    ("samples/03-dark-chrome.html", "samples/03-glassmorphism.html"),
    ("samples/04-silver-editorial.html", "samples/04-brutalism.html"),
    ("samples/05-industrial.html", "samples/05-vibrant-block-based.html"),
    ("samples/06-thermal-imaging.html", "samples/06-dark-mode-oled.html"),
    ("samples/07-phosphor-terminal.html", "samples/07-claymorphism.html"),
    ("samples/08-topographic.html", "samples/08-aurora-ui.html"),
    ("samples/09-apple-bento-dark.html", "samples/09-retro-futurism.html"),
    ("samples/10-apple-bento-light.html", "samples/10-3d-hyperrealism.html"),
    # Card <h2> titles
    (">Glass Morphism<", ">Minimalism / Swiss<"),
    (">Brutalist Raw<", ">Neumorphism<"),
    (">Dark Chrome<", ">Glassmorphism<"),
    (">Silver Editorial<", ">Brutalism<"),
    (">Industrial<", ">Vibrant &amp; Block<"),
    (">Thermal Imaging<", ">Dark Mode (OLED)<"),
    (">Phosphor Terminal<", ">Claymorphism<"),
    (">Topographic<", ">Aurora UI<"),
    (">Apple Bento &middot; Dark<", ">Retro-Futurism<"),
    (">Apple Bento · Dark<", ">Retro-Futurism<"),
    (">Apple Bento &middot; Light<", ">3D &amp; Hyperrealism<"),
    (">Apple Bento · Light<", ">3D &amp; Hyperrealism<"),
    # Kicker lines
    ("01 · Liquid translucent", "01 · Grid, hierarchy, whitespace"),
    ("02 · Hard edges, loud proof", "02 · Soft 3D, subtle depth"),
    ("03 · Metallic editorial", "03 · Frosted blur, layered"),
    ("04 · Print-weight hierarchy", "04 · Raw, anti-design"),
    ("05 · Raw material, honest data", "05 · Big blocks, big energy"),
    ("06 · Heat-map UI, data dense", "06 · OLED-deep, neon accents"),
    ("07 · CRT green, command line", "07 · Playful, chunky, toy-like"),
    ("08 · Contour map aesthetic", "08 · Northern-lights gradients"),
    ("09 · Zero-gap metric grid", "09 · CRT glow, cyberpunk"),
    ("10 · Clean metric grid", "10 · Depth, 3D, tactile"),
    # mailto subjects
    ("Glass%20Morphism", "Minimalism%20Swiss"),
    ("Brutalist%20Raw", "Neumorphism"),
    ("Dark%20Chrome", "Glassmorphism"),
    ("Silver%20Editorial", "Brutalism"),
    ("Industrial%20style", "Vibrant%20Block%20style"),
    ("Thermal%20Imaging", "Dark%20Mode%20OLED"),
    ("Phosphor%20Terminal", "Claymorphism"),
    ("Topographic", "Aurora%20UI"),
    ("Apple%20Bento%20Dark", "Retro-Futurism"),
    ("Apple%20Bento%20Light", "3D%20Hyperrealism"),
]
for old, new in replacements:
    html = html.replace(old, new)

# Retitle the intro paragraph to name the skill source
html = html.replace(
    "Every card below is a <em>real hand-built page</em> — not a rendered\n"
    "        screenshot, not a themed variant, not AI-generated chrome.",
    "Every card below was generated directly from a row in the\n"
    "        <em>UI UX Pro Max</em> skill catalog (84 styles, each carrying its\n"
    "        own colours, fonts, radii, shadows, and effects as ready CSS tokens).",
)

p.write_text(html, encoding="utf-8")
print(f"rewired {p.name}")
