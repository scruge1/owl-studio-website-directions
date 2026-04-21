"""
Add `data-quote-open` + preset data attrs (tier/style/care/first-step)
to every CTA that should open the Owl Studio quote modal.

Keeps the original `mailto:` href untouched so it works as a
progressive-enhancement fallback when JS is disabled.

Idempotent: re-run safe (looks for existing `data-quote-open` first).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / "interactive-gallery.html"
src = HTML.read_text(encoding="utf-8")

# (search pattern, extra data attrs) — each matches one specific anchor.
# Using exact href substrings so we don't accidentally tag something else.

RULES = [
    # Starter tier card — "Start a Starter"
    ('href="mailto:callmeie@proton.me?subject=Starter%20website%20%E2%80%94%20%E2%82%AC695"',
     'data-quote-open data-first-step="project" data-tier="starter"'),
    # Pro tier card — "Start a Pro"
    ('href="mailto:callmeie@proton.me?subject=Pro%20website%20%E2%80%94%20%E2%82%AC1595"',
     'data-quote-open data-first-step="project" data-tier="pro"'),
    # Custom tier card — "Book a scoping call"
    ('href="mailto:callmeie@proton.me?subject=Custom%20project%20%E2%80%94%20scoping%20call"',
     'data-quote-open data-first-step="project" data-tier="custom"'),

    # Care plan cards
    ('subject=Essential%20care%20plan%20%E2%80%94%20%E2%82%AC45%2Fmo%20or%20%E2%82%AC450%2Fyr',
     'data-quote-open data-first-step="project" data-care="essential"'),
    ('subject=Growth%20care%20plan%20%E2%80%94%20%E2%82%AC95%2Fmo%20or%20%E2%82%AC950%2Fyr',
     'data-quote-open data-first-step="project" data-care="growth"'),
    ('subject=Concierge%20care%20plan%20%E2%80%94%20%E2%82%AC195%2Fmo%20or%20%E2%82%AC1950%2Fyr',
     'data-quote-open data-first-step="project" data-care="concierge"'),

    # €99 audit — "Order the €99 audit" (two separate instances)
    ('subject=%E2%82%AC99%20style-match%20audit',
     'data-quote-open data-first-step="audit"'),

    # Final CTA — "Book the free 20-min call"
    ('subject=Free%2020-min%20style-match%20call',
     'data-quote-open data-first-step="call"'),

    # Final CTA — "Email the studio" (ready to book)
    ('subject=Website%20project%20%E2%80%94%20ready%20to%20book',
     'data-quote-open data-first-step="project"'),

    # Gallery "Build this for me" on each industry card.
    # The mailto subjects are parameterised per industry (e.g.
    #   Dental%20practice%20website, Solicitor%20practice%20website, …).
    # We match each of the 10 and add the matching data-style slug.
    ('subject=Dental%20practice%20website',
     'data-quote-open data-style="01-dental-swiss"'),
    ('subject=Solicitor%20practice%20website',
     'data-quote-open data-style="02-solicitor-swiss"'),
    ('subject=Accountancy%20practice%20website',
     'data-quote-open data-style="03-accountant-minimalism"'),
    ('subject=Physiotherapy%20clinic%20website',
     'data-quote-open data-style="04-physio-neumorphism"'),
    ('subject=Opticians%20website',
     'data-quote-open data-style="05-opticians-glassmorphism"'),
    ('subject=Audiology%20clinic%20website',
     'data-quote-open data-style="06-audiologist-aurora"'),
    ('subject=Veterinary%20practice%20website',
     'data-quote-open data-style="07-vet-claymorphism"'),
    ('subject=Wealth%20advisor%20website',
     'data-quote-open data-style="08-financial-brutalism-editorial"'),
    ('subject=Architects%20practice%20website',
     'data-quote-open data-style="09-architects-3d"'),
    ('subject=Aesthetic%20clinic%20website',
     'data-quote-open data-style="10-aesthetic-clinic-aurora-luxe"'),
]


def wire_anchor(html: str, href_substring: str, extra_attrs: str) -> tuple[str, int]:
    """Add extra_attrs to every <a ...> that contains href_substring,
    unless it already has data-quote-open. Returns (new_html, count)."""
    # Regex: match opening <a ... href with substring ... >
    # We inject extra_attrs right after the opening <a
    pattern = re.compile(
        r'(<a\b)([^>]*' + re.escape(href_substring) + r'[^>]*)(>)',
    )
    count = 0

    def replace(m: re.Match) -> str:
        nonlocal count
        tag, body, close = m.group(1), m.group(2), m.group(3)
        if "data-quote-open" in body:
            return m.group(0)  # already wired — idempotent
        count += 1
        return f"{tag} {extra_attrs}{body}{close}"

    new = pattern.sub(replace, html)
    return new, count


total_wired = 0
for needle, attrs in RULES:
    src, n = wire_anchor(src, needle, attrs)
    if n == 0:
        # Not fatal — the HTML may already be wired, or this rule is unused.
        # But if nothing in the file contains the needle at all, flag it.
        if needle not in HTML.read_text(encoding="utf-8"):
            print(f"[warn] needle not found in file: {needle[:70]}", file=sys.stderr)
    total_wired += n
    print(f"  + {n:2d}  {needle[:70]}")

HTML.write_text(src, encoding="utf-8")
print(f"\nwired {total_wired} anchors with data-quote-open")
