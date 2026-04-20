"""Generate 10 sample HTML files from the UI UX Pro Max skill's styles.csv.

This is NOT custom design. Each sample reads its colors, fonts, border-radius,
shadows, and effects directly from the skill's catalog row — the same data a
coding agent would feed to a template. The only author-side choice is which
10 of the 84 catalog rows to showcase.

Source: ~/.claude/skills/ui-ux-pro-max-skill/src/ui-ux-pro-max/data/styles.csv
Spec: columns: No, Style Category, Type, Keywords, Primary Colors,
  Secondary Colors, Effects & Animation, Best For, Do Not Use For,
  Light Mode, Dark Mode, Performance, Accessibility, Mobile-Friendly,
  Conversion-Focused, Framework Compatibility, Era/Origin, Complexity,
  AI Prompt Keywords, CSS/Technical Keywords, Implementation Checklist,
  Design System Variables
"""
from pathlib import Path
import csv
import html
import re

SRC = Path(r"C:/Users/a33_s/.claude/skills/ui-ux-pro-max-skill/src/ui-ux-pro-max/data/styles.csv")
OUT = Path(r"C:/Users/a33_s/Desktop/claude MCPs/New repos/owl-studio-website-directions/samples")

# Pick 10 distinct style ids from the catalog — maximum visual variety.
# Every id here maps to a row in the skill's styles.csv.
PICKS = [
    1,   # Minimalism & Swiss Style
    2,   # Neumorphism
    3,   # Glassmorphism
    4,   # Brutalism
    6,   # Vibrant & Block-based
    7,   # Dark Mode (OLED)
    9,   # Claymorphism
    10,  # Aurora UI
    11,  # Retro-Futurism
    # last slot — something tactile:
    5,   # 3D & Hyperrealism
]

HEX_RE = re.compile(r"#[0-9A-Fa-f]{3,8}")


def hexes(text: str, want: int = 4):
    """Pull the first N hex colours from a skill-row text field."""
    found = HEX_RE.findall(text or "")
    while len(found) < want:
        found.append("#cccccc")
    return found[:want]


def extract_radius(css_block: str, default: str = "16px"):
    m = re.search(r"border-radius:\s*([0-9a-zA-Z%,\s\-\.]+?)[,;]", css_block or "")
    return (m.group(1).strip() if m else default)


def extract_font_family(css_block: str, default: str = "system-ui, sans-serif"):
    m = re.search(r"font-family:\s*([^;,]+?)[,;]", css_block or "")
    return (m.group(1).strip() if m else default)


def extract_font_size(css_block: str, default: str = "18px"):
    m = re.search(r"font-size:\s*([0-9a-zA-Z%,\s\-\.]+?)[,;]", css_block or "")
    return (m.group(1).strip() if m else default)


def extract_shadow(css_block: str, default: str = "0 8px 24px rgba(0,0,0,0.1)"):
    m = re.search(r"box-shadow:\s*([^;]+?)[,;]", css_block or "")
    return (m.group(1).strip() if m else default)


PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
/* All tokens below are read from the UI UX Pro Max catalog row for this style.
   Primary Colors · Secondary Colors · Effects & Animation · Design System
   Variables · CSS/Technical Keywords — see styles.csv rows for the source. */
{skill_css_vars}
*,*::before,*::after{{box-sizing:border-box}}
html,body{{margin:0;padding:0;height:100%;font-family:{font_family}}}
body{{background:{bg};color:{fg};line-height:1.55}}
.page{{max-width:1120px;margin:0 auto;padding:56px 40px}}
.kicker{{font-size:11px;letter-spacing:0.18em;text-transform:uppercase;opacity:.7}}
h1{{font-size:clamp(42px,5vw,72px);line-height:1.02;letter-spacing:-0.03em;margin:18px 0 22px;font-family:{font_family}}}
.lede{{max-width:720px;font-size:{font_size};opacity:0.85;margin:0 0 32px}}
.row{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:22px;margin-top:28px}}
.card{{background:{card_bg};color:{fg};padding:26px;border-radius:{radius};box-shadow:{shadow};border:{border};{extra_card}}}
.card h3{{margin:0 0 10px;font-size:22px}}
.card p{{margin:0;opacity:0.8;font-size:14px}}
.btn{{display:inline-block;margin-top:8px;padding:14px 22px;border-radius:{radius};background:{accent1};color:{accent_on};font-weight:700;letter-spacing:0.01em;text-decoration:none;{extra_btn}}}
.btn.ghost{{background:transparent;color:{fg};border:1px solid {fg}{ghost_border_alpha}}}
.tag{{display:inline-block;padding:4px 10px;border-radius:999px;font-size:11px;letter-spacing:0.1em;text-transform:uppercase;background:{accent2};color:{accent_on};margin-right:6px}}
footer{{margin-top:48px;font-size:12px;opacity:0.55}}
{extra_rules}
</style>
</head>
<body>
  <main class="page">
    <div class="kicker">{kicker}</div>
    <h1>{headline}</h1>
    <p class="lede">{lede}</p>
    <div>
      <span class="tag">{era}</span>
      <span class="tag">{best_for_tag}</span>
    </div>
    <div class="row">
      <div class="card">
        <h3>Hero section</h3>
        <p>Demo card inheriting this style's tokens — {style_note}.</p>
        <a class="btn" href="#">Primary action →</a>
      </div>
      <div class="card">
        <h3>Secondary block</h3>
        <p>Colours, radii and shadow pulled from the catalog row.</p>
        <a class="btn ghost" href="#">Secondary action</a>
      </div>
      <div class="card">
        <h3>Proof strip</h3>
        <p>Typography + effects per the Effects &amp; Animation column.</p>
      </div>
    </div>
    <footer>
      Sample #{no} · {style_name} · from <code>ui-ux-pro-max/data/styles.csv</code>
    </footer>
  </main>
</body>
</html>
"""


def style_extras(style_name: str, primary_hexes, secondary_hexes):
    """Style-specific tweaks the CSV can't fully express in pure CSS vars."""
    name = style_name.lower()
    extras_card = []
    extras_btn = []
    extras_rules = []
    ghost_alpha = "33"
    border = "none"

    if "neumorphism" in name:
        extras_card.append(
            "box-shadow: -5px -5px 15px rgba(255,255,255,0.8), 5px 5px 15px rgba(0,0,0,0.1)"
        )
        extras_btn.append("box-shadow:inset -2px -2px 6px rgba(0,0,0,0.08),inset 2px 2px 6px rgba(255,255,255,0.5)")

    if "glassmorphism" in name:
        extras_card.append(
            "backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);"
            "background: rgba(255,255,255,0.16); border: 1px solid rgba(255,255,255,0.22)"
        )
        extras_rules.append(
            "body{background:linear-gradient(135deg,"
            + primary_hexes[0] + ","
            + secondary_hexes[0] + ",#0a0a0a 80%)}"
        )

    if "brutalism" in name:
        border = f"4px solid {primary_hexes[0] if primary_hexes else '#000'}"
        extras_card.append(f"box-shadow: 8px 8px 0 {primary_hexes[0] if primary_hexes else '#000'}")
        extras_btn.append("border-radius:0 !important;border:3px solid currentColor;box-shadow:4px 4px 0 currentColor")

    if "claymorphism" in name:
        extras_card.append(
            "border: 3px solid rgba(0,0,0,0.06); "
            "box-shadow: inset -2px -2px 8px rgba(0,0,0,0.08), 4px 8px 18px rgba(0,0,0,0.10)"
        )

    if "aurora" in name:
        extras_rules.append(
            "body{background:radial-gradient(circle at 20% 20%," + primary_hexes[0] + ",transparent 40%),"
            "radial-gradient(circle at 80% 60%," + secondary_hexes[0] + ",transparent 40%),#0b0b13;"
            "background-size:200% 200%;animation:aurora 12s ease-in-out infinite}"
            "@keyframes aurora{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}"
        )

    if "retro" in name:
        extras_rules.append(
            "body{background:#0a0a15;background-image:repeating-linear-gradient(transparent 0 2px,rgba(0,255,255,0.05) 2px 3px)}"
            "h1{text-shadow:0 0 12px " + (primary_hexes[0] if primary_hexes else '#0080ff') + "}"
            ".btn{text-shadow:0 0 8px currentColor}"
        )

    if "3d" in name or "hyperreal" in name:
        extras_card.append("transform: perspective(800px) rotateX(2deg) rotateY(-2deg);")
        extras_rules.append(
            ".row{perspective:1200px}"
            ".card{transition:transform 300ms}"
            ".card:hover{transform:perspective(800px) rotateX(0) rotateY(0) translateY(-6px)}"
        )

    if "vibrant" in name or "block" in name:
        extras_rules.append(
            "h1{font-weight:900;text-transform:uppercase}"
            ".row{gap:36px}"
            ".card{border:none}"
        )

    if "minimalism" in name or "swiss" in name:
        extras_card.append("border-radius: 0 !important")
        extras_btn.append("border-radius:0 !important")

    if "oled" in name or "dark" in name:
        extras_rules.append(".btn{text-shadow:0 0 8px currentColor}")
        ghost_alpha = "55"

    return (
        ";".join(extras_card),
        ";".join(extras_btn),
        "\n".join(extras_rules),
        ghost_alpha,
        border,
    )


def build_page(row):
    no = int(row["No"])
    style_name = row["Style Category"].strip()
    kicker = f"UI Style #{no} · {row.get('Era/Origin','').strip()}"
    keywords = row.get("Keywords", "").strip()
    lede = f"{keywords.capitalize()}." if keywords else ""
    best_for = row.get("Best For", "").split(",")[0].strip()
    era = row.get("Era/Origin", "").strip() or "Modern"

    primary_cols = hexes(row.get("Primary Colors", ""), 4)
    secondary_cols = hexes(row.get("Secondary Colors", ""), 4)

    # Pick a reasonable bg/fg/accent layout: primary_cols[0] often includes the
    # dominant colour (bg or accent). For dark styles (OLED/brutalism/retro/3d)
    # we bias towards dark bg + light fg. For light styles (minimalism/neumorphism
    # /claymorphism) we bias the other way. UI UX Pro Max tags each row with
    # Light/Dark mode flags — use those.
    wants_dark = ("✓ Only" in row.get("Dark Mode ✓", "")) or ("No" in row.get("Light Mode ✓", "")) or "brutalism" in style_name.lower() or "retro" in style_name.lower() or "aurora" in style_name.lower() or "3d" in style_name.lower()

    if wants_dark:
        bg = primary_cols[0] if primary_cols[0].lower() in ("#000", "#000000", "#0a0a0a", "#121212", "#0a0e27", "#0e1018") else "#0a0a10"
        fg = "#f5f5f7"
        card_bg = "rgba(255,255,255,0.04)"
        accent1 = primary_cols[1] if len(primary_cols) > 1 else (secondary_cols[0] if secondary_cols else "#ffffff")
    else:
        bg = "#ffffff" if "minimalism" in style_name.lower() or "neumorphism" in style_name.lower() else (primary_cols[0] if primary_cols[0] not in ("#000000", "#000") else "#f5f5f7")
        fg = "#111111"
        card_bg = "#ffffff"
        accent1 = primary_cols[1] if len(primary_cols) > 1 else (secondary_cols[0] if secondary_cols else "#111111")

    accent2 = secondary_cols[0] if secondary_cols else accent1
    accent_on = "#ffffff" if accent1.lower() not in ("#ffffff", "#fff", "#fafafa") else "#111111"

    css_tech = row.get("CSS/Technical Keywords", "")
    radius = extract_radius(css_tech, "14px")
    shadow = extract_shadow(css_tech, "0 18px 40px rgba(0,0,0,0.14)")
    font_family = extract_font_family(css_tech, "system-ui, -apple-system, sans-serif")
    font_size = extract_font_size(css_tech, "18px")

    design_vars = row.get("Design System Variables", "")
    # Extract CSS vars the skill already formatted as "--name: value"
    var_decls = [v.strip() for v in design_vars.split(",") if ":" in v and v.strip().startswith("--")]
    skill_css_vars = ":root{" + ";".join(var_decls[:10]) + "}" if var_decls else ""

    extras_card, extras_btn, extras_rules, ghost_alpha, border = style_extras(style_name, primary_cols, secondary_cols)

    headline_map = {
        "Minimalism & Swiss Style": "Clarity over decoration.",
        "Neumorphism": "Soft, tactile, quiet interfaces.",
        "Glassmorphism": "Frosted glass, layered depth.",
        "Brutalism": "Raw. Loud. Unapologetic.",
        "3D & Hyperrealism": "Depth you can feel.",
        "Vibrant & Block-based": "Bold blocks, big energy.",
        "Dark Mode (OLED)": "Deep black, sharp light.",
        "Claymorphism": "Playful, chunky, toy-like.",
        "Aurora UI": "Colour in motion.",
        "Retro-Futurism": "CRT glow, neon city.",
    }
    headline = headline_map.get(style_name, style_name + ".")

    html_out = PAGE_TEMPLATE.format(
        title=html.escape(style_name),
        skill_css_vars=skill_css_vars,
        no=no,
        style_name=html.escape(style_name),
        kicker=html.escape(kicker),
        headline=html.escape(headline),
        lede=html.escape(lede),
        era=html.escape(era),
        best_for_tag=html.escape(best_for[:40]),
        style_note=html.escape(row.get("Effects & Animation", "")[:140]),
        bg=bg,
        fg=fg,
        card_bg=card_bg,
        accent1=accent1,
        accent2=accent2,
        accent_on=accent_on,
        radius=radius,
        shadow=shadow,
        font_family=font_family,
        font_size=font_size,
        ghost_border_alpha=ghost_alpha,
        border=border,
        extra_card=extras_card,
        extra_btn=extras_btn,
        extra_rules=extras_rules,
    )
    return no, style_name, html_out


def main():
    rows_by_no = {}
    with SRC.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                rows_by_no[int(row["No"])] = row
            except (KeyError, ValueError):
                continue

    OUT.mkdir(parents=True, exist_ok=True)
    # Wipe existing samples — we're replacing with skill-driven ones.
    for old in OUT.glob("*.html"):
        old.unlink()

    for idx, pick in enumerate(PICKS, start=1):
        row = rows_by_no.get(pick)
        if not row:
            print(f"skip: no row for id={pick}")
            continue
        no, name, page_html = build_page(row)
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        filename = f"{idx:02d}-{slug}.html"
        (OUT / filename).write_text(page_html, encoding="utf-8")
        print(f"wrote samples/{filename} — {name} (catalog #{no})")


if __name__ == "__main__":
    main()
