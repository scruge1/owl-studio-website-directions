"""
Register each of the 10 industry samples as its own Owl Studio site,
and inject `<script src="_owl-form.js" defer></script>` into each HTML
file so the live contact form wires automatically.

Idempotent:
  - POST /owl/sites returns 409 if the site_id already exists → skip
  - Script tag injection guarded by <!-- owl-lead-form --> marker comment

Usage:
  source ~/.claude/routes/.env && export OWL_OWNER_TOKEN
  python scripts/provision-sample-sites.py
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
SAMPLES_DIR = ROOT / "samples" / "industries"
CALLMEIE = "https://callmeie.onrender.com"
MARKER = "<!-- owl-lead-form -->"
SCRIPT_TAG = '<script src="_owl-form.js" defer></script>'

# Each sample's real business identity (from the sample's own hero copy)
# and the site_id we register under
SITES = [
    {"slug": "01-dental-swiss",                  "site_id": "rathborne-dental-demo",      "display_name": "Rathborne Dental (sample)",          "tier": "pro",     "care_tier": "growth",     "lead_email": "callmeie@proton.me", "lead_sms": "+353857863564"},
    {"slug": "02-solicitor-swiss",               "site_id": "hennessy-byrne-demo",         "display_name": "Hennessy & Byrne (sample)",          "tier": "pro",     "care_tier": None,          "lead_email": "callmeie@proton.me", "lead_sms": "+353857863564"},
    {"slug": "03-accountant-minimalism",         "site_id": "magee-co-demo",               "display_name": "Magee & Co. (sample)",               "tier": "pro",     "care_tier": "essential",  "lead_email": "callmeie@proton.me", "lead_sms": "+353857863564"},
    {"slug": "04-physio-neumorphism",            "site_id": "quay-physio-demo",            "display_name": "The Quay Physio (sample)",           "tier": "pro",     "care_tier": None,          "lead_email": "callmeie@proton.me", "lead_sms": "+353857863564"},
    {"slug": "05-opticians-glassmorphism",       "site_id": "callanan-opticians-demo",     "display_name": "Callanan Opticians (sample)",        "tier": "pro",     "care_tier": None,          "lead_email": "callmeie@proton.me", "lead_sms": "+353857863564"},
    {"slug": "06-trade-pro-dark-oled",           "site_id": "murphy-plumbing-demo",        "display_name": "Murphy Plumbing & Heating (sample)", "tier": "pro",     "care_tier": "essential",  "lead_email": "callmeie@proton.me", "lead_sms": "+353857863564"},
    {"slug": "07-vet-claymorphism",              "site_id": "main-street-vets-demo",       "display_name": "Main Street Vets (sample)",          "tier": "pro",     "care_tier": None,          "lead_email": "callmeie@proton.me", "lead_sms": "+353857863564"},
    {"slug": "08-financial-brutalism-editorial", "site_id": "kelleher-wealth-demo",        "display_name": "Kelleher Wealth (sample)",           "tier": "custom",  "care_tier": None,          "lead_email": "callmeie@proton.me", "lead_sms": "+353857863564"},
    {"slug": "09-architects-3d",                 "site_id": "carroll-osuilleabhain-demo",  "display_name": "Carroll Ó Súilleabháin (sample)",    "tier": "custom",  "care_tier": None,          "lead_email": "callmeie@proton.me", "lead_sms": "+353857863564"},
    {"slug": "10-local-services-brutalism",      "site_id": "clear-out-limerick-demo",     "display_name": "Clear-Out Limerick (sample)",        "tier": "starter", "care_tier": None,         "lead_email": "callmeie@proton.me", "lead_sms": "+353857863564"},
]


def register(owner_token: str, s: dict) -> tuple[str, str]:
    """Register a site. Returns (admin_url, admin_token). On 409 — fetch existing admin URL."""
    payload = {k: s[k] for k in ("site_id", "display_name", "tier", "lead_email") if s.get(k) is not None}
    if s.get("care_tier"):
        payload["care_tier"] = s["care_tier"]
    if s.get("lead_sms"):
        payload["lead_sms"] = s["lead_sms"]
    payload["edit_emails"] = [s["lead_email"]]
    payload["live_url"] = f"https://websites.owlzone.trade/samples/industries/{s['slug']}.html"
    with httpx.Client(timeout=30) as c:
        r = c.post(f"{CALLMEIE}/owl/sites", params={"token": owner_token}, json=payload)
        if r.status_code == 409:
            print(f"  [exists]  {s['site_id']}")
            return ("(existing — admin URL already in vault)", "(existing)")
        if r.status_code >= 400:
            print(f"  [FAIL]    {s['site_id']}  {r.status_code} {r.text}", file=sys.stderr)
            return ("", "")
        j = r.json()
        print(f"  [created] {s['site_id']:35s}  {j['admin_url']}")
        return j["admin_url"], j["admin_token"]


def inject_script_tag(html_path: Path) -> bool:
    src = html_path.read_text(encoding="utf-8")
    if MARKER in src:
        return False
    if "</body>" not in src:
        return False
    block = f"{MARKER}\n{SCRIPT_TAG}\n"
    new = src.replace("</body>", block + "</body>", 1)
    html_path.write_text(new, encoding="utf-8")
    return True


def main() -> None:
    owner = os.environ.get("OWL_OWNER_TOKEN", "").strip()
    if not owner:
        print("Missing OWL_OWNER_TOKEN env var", file=sys.stderr)
        sys.exit(1)

    print("[1/2] registering 10 sample sites...")
    tokens = {}
    for s in SITES:
        admin_url, admin_token = register(owner, s)
        tokens[s["site_id"]] = (admin_url, admin_token)

    print("\n[2/2] injecting <script src=\"_owl-form.js\"> into each sample...")
    patched = 0
    for s in SITES:
        f = SAMPLES_DIR / f"{s['slug']}.html"
        if not f.exists():
            print(f"  MISS: {f}", file=sys.stderr)
            continue
        if inject_script_tag(f):
            print(f"  [patched] {f.name}")
            patched += 1
        else:
            print(f"  [exists]  {f.name}")

    print()
    print("=" * 64)
    print("DONE  |  tokens (store in vault):")
    print("=" * 64)
    for site_id, (url, tok) in tokens.items():
        print(f"{site_id:35s}  {url}")
        if tok and tok != "(existing)":
            print(f"   token: {tok}")
    print()
    print(f"Patched {patched} sample files with _owl-form.js script tag.")


if __name__ == "__main__":
    main()
