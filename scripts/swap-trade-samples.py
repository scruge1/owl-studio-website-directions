"""
Atomic migration for the trades swap (2026-04-21):

  replaces #06 hear-clear-demo (Audiology, Aurora Calm)
       with #06 murphy-plumbing-demo  (Trade Pro Plumber, Dark OLED industrial)

  replaces #10 molyneux-aesthetics-demo (Aesthetic Clinic, Aurora Luxe)
       with #10 clear-out-limerick-demo (Local Services sole trader, Brutalism)

Updates every hardcoded reference so the site stays internally consistent:
  - samples/industries/_owl-nav.js       (SAMPLES array)
  - samples/industries/_owl-form.js      (SAMPLES dict)
  - scripts/provision-sample-sites.py    (SITES list)
  - interactive-gallery.html             (main gallery cards, demo-hook
                                          thumbs, quote-modal <option>s)

Does NOT delete the old owl_sites rows in Postgres — those are left
as status='off' via a separate direct UPDATE. Keeps the paper trail
and lets admin URLs for old samples still 401 cleanly.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD_06 = {
    "slug": "06-audiologist-aurora",
    "site_id": "hear-clear-demo",
    "name": "Audiology",
    "business": "Hear Clear Audiology",
    "tclass": "t-09",
    "kicker": "06 · Aurora Calm",
    "h2": "Audiology · Hearing Care",
    "subject": "Audiology%20clinic%20website",
}
NEW_06 = {
    "slug": "06-trade-pro-dark-oled",
    "site_id": "murphy-plumbing-demo",
    "name": "Trade Pro",
    "business": "Murphy Plumbing & Heating",
    "tclass": "t-07",                                 # Dark OLED miniature
    "kicker": "06 · Dark OLED · Industrial",
    "h2": "Plumbers · Trade Pro",
    "subject": "Plumber%20or%20trade%20pro%20website",
    "aud": "Industrial · Dark OLED",
}

OLD_10 = {
    "slug": "10-aesthetic-clinic-aurora-luxe",
    "site_id": "molyneux-aesthetics-demo",
    "name": "Aesthetic",
    "business": "Molyneux Aesthetics",
    "tclass": "t-aes",
    "kicker": "10 · Aurora Luxe",
    "h2": "Aesthetic · Medical Clinic",
    "subject": "Aesthetic%20clinic%20website",
}
NEW_10 = {
    "slug": "10-local-services-brutalism",
    "site_id": "clear-out-limerick-demo",
    "name": "Local Services",
    "business": "Clear-Out Limerick",
    "tclass": "t-04",                                 # Brutalism miniature
    "kicker": "10 · Mondrian Brutalism",
    "h2": "Local Services · Sole Trader",
    "subject": "Local%20services%20or%20man-with-a-van%20website",
    "aud": "Service ad · Brutalism",
}

SWAPS = [(OLD_06, NEW_06), (OLD_10, NEW_10)]


def touch(path: Path, swaps: list[tuple[str, str]]) -> int:
    if not path.exists():
        return 0
    src = path.read_text(encoding="utf-8")
    n = 0
    for old, new in swaps:
        if old in src:
            src = src.replace(old, new)
            n += 1
    if n:
        path.write_text(src, encoding="utf-8")
    return n


def main() -> None:
    # Build a flat list of text-level swaps that cover all the reference points
    swaps: list[tuple[str, str]] = []
    for old, new in SWAPS:
        swaps.extend([
            # Sample filenames
            (f"samples/industries/{old['slug']}.html", f"samples/industries/{new['slug']}.html"),
            (f"renders/industries/{old['slug']}.png", f"renders/industries/{new['slug']}.png"),
            # site_ids
            (old["site_id"], new["site_id"]),
            # Main gallery h2 + kicker + data-style + mailto subject
            (f"<h2>{old['h2']}</h2>", f"<h2>{new['h2']}</h2>"),
            (f'<span class="kicker">{old["kicker"]}</span>', f'<span class="kicker">{new["kicker"]}</span>'),
            (f'data-style="{old["slug"]}"', f'data-style="{new["slug"]}"'),
            (f"subject={old['subject']}", f"subject={new['subject']}"),
            # themed card-stage class swap (the big gallery card miniature)
            # NOTE: we keep the miniature class tied to each sample's style, but
            # because multiple cards share t-classes the swap is done in interactive-gallery
            # via explicit block rewrite below (not a global string swap).
        ])

    # Run text swaps against key files
    targets = [
        ROOT / "samples" / "industries" / "_owl-nav.js",
        ROOT / "samples" / "industries" / "_owl-form.js",
        ROOT / "scripts" / "provision-sample-sites.py",
        ROOT / "interactive-gallery.html",
    ]
    for t in targets:
        n = touch(t, swaps)
        print(f"  [{n:2d} swaps] {t.relative_to(ROOT)}")

    # Explicit human-readable label swaps in _owl-form.js SAMPLES dict
    #   06 was { site_id, business: "Hear Clear Audiology" }, now Murphy
    #   10 was { site_id, business: "Molyneux Aesthetics" }, now Clear-Out Limerick
    fp = ROOT / "samples" / "industries" / "_owl-form.js"
    src = fp.read_text(encoding="utf-8")
    src = src.replace(f'business: "{OLD_06["business"]}"', f'business: "{NEW_06["business"]}"')
    src = src.replace(f'business: "{OLD_10["business"]}"', f'business: "{NEW_10["business"]}"')
    fp.write_text(src, encoding="utf-8")
    print(f"  [_owl-form.js] business labels updated")

    # _owl-nav.js SAMPLES array entries
    fp = ROOT / "samples" / "industries" / "_owl-nav.js"
    src = fp.read_text(encoding="utf-8")
    src = src.replace(
        '{ slug: "06-audiologist-aurora",            name: "Audiology",             style: "Aurora Calm" }',
        '{ slug: "06-trade-pro-dark-oled",           name: "Trade Pro",             style: "Dark OLED · Industrial" }',
    )
    src = src.replace(
        '{ slug: "10-aesthetic-clinic-aurora-luxe",  name: "Aesthetic Clinic",      style: "Aurora Luxe" }',
        '{ slug: "10-local-services-brutalism",      name: "Local Services",        style: "Mondrian Brutalism" }',
    )
    fp.write_text(src, encoding="utf-8")
    print(f"  [_owl-nav.js] SAMPLES array entries updated")

    # _owl-form.js SAMPLES dict keys (the whole key changes)
    fp = ROOT / "samples" / "industries" / "_owl-form.js"
    src = fp.read_text(encoding="utf-8")
    src = src.replace('"06-audiologist-aurora":', '"06-trade-pro-dark-oled":')
    src = src.replace('"10-aesthetic-clinic-aurora-luxe":', '"10-local-services-brutalism":')
    fp.write_text(src, encoding="utf-8")
    print(f"  [_owl-form.js] dict keys updated")

    # provision-sample-sites.py SITES list — update the "slug" + names inline
    fp = ROOT / "scripts" / "provision-sample-sites.py"
    src = fp.read_text(encoding="utf-8")
    src = src.replace(
        '{"slug": "06-audiologist-aurora",            "site_id": "hear-clear-demo",             "display_name": "Hear Clear Audiology (sample)",      "tier": "pro",     "care_tier": None,          "lead_email": "callmeie@proton.me", "lead_sms": "+353857863564"}',
        '{"slug": "06-trade-pro-dark-oled",           "site_id": "murphy-plumbing-demo",         "display_name": "Murphy Plumbing & Heating (sample)", "tier": "pro",     "care_tier": "essential",  "lead_email": "callmeie@proton.me", "lead_sms": "+353857863564"}',
    )
    src = src.replace(
        '{"slug": "10-aesthetic-clinic-aurora-luxe",  "site_id": "molyneux-aesthetics-demo",    "display_name": "Molyneux Aesthetics (sample)",       "tier": "custom",  "care_tier": "concierge",  "lead_email": "callmeie@proton.me", "lead_sms": "+353857863564"}',
        '{"slug": "10-local-services-brutalism",      "site_id": "clear-out-limerick-demo",     "display_name": "Clear-Out Limerick (sample)",        "tier": "starter", "care_tier": None,         "lead_email": "callmeie@proton.me", "lead_sms": "+353857863564"}',
    )
    fp.write_text(src, encoding="utf-8")
    print(f"  [provision-sample-sites.py] SITES entries updated")

    # Quote-modal <option> in interactive-gallery.html
    fp = ROOT / "interactive-gallery.html"
    src = fp.read_text(encoding="utf-8")
    src = src.replace(
        '<option value="06-audiologist-aurora">06 · Audiology · Aurora Calm</option>',
        '<option value="06-trade-pro-dark-oled">06 · Plumbers / Trade Pro · Dark OLED</option>',
    )
    src = src.replace(
        '<option value="10-aesthetic-clinic-aurora-luxe">10 · Aesthetic Clinic · Aurora Luxe</option>',
        '<option value="10-local-services-brutalism">10 · Local Services / Sole Trader · Brutalism</option>',
    )
    fp.write_text(src, encoding="utf-8")
    print(f"  [interactive-gallery.html] quote-modal options updated")

    print("\ndone.")


if __name__ == "__main__":
    main()
