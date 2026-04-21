"""
Render a client site from a Business Profile JSON + a template HTML.

Usage:
  python scripts/render-site.py --profile rathborne-dental
  # -> reads profiles/rathborne-dental.json + templates/01-dental-swiss.template.html
  # -> writes client-builds/rathborne-dental/index.html

Replaces `{{dotted.path}}` placeholders in the template with values
from the profile. Supports:
  {{display_name}}                 simple key
  {{address.line1}}                nested key
  {{hero.primary_cta.href}}        deep nested
  {{{hero.headline_emphasis}}}     TRIPLE-brace = HTML-safe (rendered as-is)
  {{#loop team}} ... {{/loop}}     for-each loop over a list
    inside: {{name}}, {{credentials}} refer to current item's keys

This is the v1 renderer (intentionally no Jinja dependency — stdlib
only so anyone can run it). Upgrade to Jinja2 planned in
BUSINESS-PROFILE-SCHEMA.md §5.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
PROFILES_DIR = ROOT / "profiles"
TEMPLATES_DIR = ROOT / "templates"
OUT_DIR = ROOT / "client-builds"


def dig(obj: Any, path: str, default: str = "") -> Any:
    """Resolve `a.b.c` against nested dicts/lists. Returns default if missing."""
    cur = obj
    for key in path.split("."):
        if cur is None:
            return default
        if isinstance(cur, list):
            try:
                cur = cur[int(key)]
            except (ValueError, IndexError):
                return default
        elif isinstance(cur, dict):
            cur = cur.get(key, None)
            if cur is None:
                return default
        else:
            return default
    return cur if cur is not None else default


def html_escape(s: str) -> str:
    return (str(s or "")
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;"))


def render_loops(template: str, profile: dict[str, Any]) -> str:
    """Expand {{#loop key}} ... {{/loop}} blocks. Each iteration renders
    the body with the current item as its own scope (plus access to parent
    via $parent.key if needed — v1 keeps it simple, no $parent)."""
    loop_re = re.compile(r"\{\{#loop\s+([a-zA-Z0-9_.]+)\s*\}\}(.*?)\{\{/loop\}\}", re.DOTALL)

    def replace_loop(m: re.Match) -> str:
        path, body = m.group(1), m.group(2)
        items = dig(profile, path, [])
        if not isinstance(items, list):
            return ""
        rendered = []
        for item in items:
            # For each item, render the body with item-scope substitutions.
            # We support {{key}} / {{nested.key}} / {{{key}}} referring to item fields.
            scope = item if isinstance(item, dict) else {}
            rendered.append(render_scalars(body, scope))
        return "".join(rendered)

    return loop_re.sub(replace_loop, template)


def render_scalars(template: str, scope: dict[str, Any]) -> str:
    """Replace {{key}} / {{a.b.c}} / {{{key}}} placeholders.
    Triple-brace = HTML-safe (value rendered as-is).
    Double-brace = HTML-escaped."""

    def safe_sub(m: re.Match) -> str:
        return str(dig(scope, m.group(1).strip(), ""))

    def escaped_sub(m: re.Match) -> str:
        return html_escape(dig(scope, m.group(1).strip(), ""))

    # Triple-brace first so they don't get caught by the double-brace regex.
    template = re.sub(r"\{\{\{\s*([a-zA-Z0-9_.]+)\s*\}\}\}", safe_sub, template)
    template = re.sub(r"\{\{\s*([a-zA-Z0-9_.]+)\s*\}\}", escaped_sub, template)
    return template


def render(template: str, profile: dict[str, Any]) -> str:
    # Loops first so their expanded bodies can still have top-level placeholders
    template = render_loops(template, profile)
    # Now substitute remaining scalars against the top-level profile scope
    return render_scalars(template, profile)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True, help="slug or full path to profiles/*.json")
    ap.add_argument("--template", help="template slug (defaults to profile['template'])")
    ap.add_argument("--out", help="output path (defaults to client-builds/<slug>/index.html)")
    args = ap.parse_args()

    prof_path = Path(args.profile)
    if not prof_path.is_file():
        prof_path = PROFILES_DIR / f"{args.profile}.json"
    if not prof_path.is_file():
        raise SystemExit(f"profile not found: {args.profile}")
    profile = json.loads(prof_path.read_text(encoding="utf-8"))

    tmpl_slug = args.template or profile.get("template")
    if not tmpl_slug:
        raise SystemExit("no template specified and profile has no 'template' key")
    tmpl_path = TEMPLATES_DIR / f"{tmpl_slug}.template.html"
    if not tmpl_path.is_file():
        raise SystemExit(f"template not found: {tmpl_path}")
    template = tmpl_path.read_text(encoding="utf-8")

    out_path = Path(args.out) if args.out else (OUT_DIR / profile["slug"] / "index.html")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rendered = render(template, profile)
    out_path.write_text(rendered, encoding="utf-8")
    print(f"rendered {prof_path.name} x {tmpl_path.name}")
    print(f"         -> {out_path.relative_to(ROOT)}  ({len(rendered):,} chars)")

    # Sanity: warn on any leftover placeholders
    leftover = set(re.findall(r"\{\{\s*[a-zA-Z0-9_.]+\s*\}\}", rendered))
    if leftover:
        print(f"  WARN: {len(leftover)} placeholders unresolved:", file=sys.stderr)
        for p in sorted(leftover)[:10]:
            print(f"    {p}", file=sys.stderr)


if __name__ == "__main__":
    main()
