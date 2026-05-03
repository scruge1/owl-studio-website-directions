# Owl Studio — Cold Boot

*Last updated: 2026-04-24. Derived from CLAUDE.md + INFRA.md + repo state.*

One-page orientation for a Claude instance starting work here. Read
this first. If anything looks stale, regenerate from CLAUDE.md + INFRA.md.

## What this is

Sales-pitch static site (`websites.owlzone.trade`) for **Owl Studio**,
a web-design business. Prospects browse 10 website "directions",
pick one, email the studio. The project also *operates* the live
client fleet (7 demo sites) and the wider Hetzner/Stripe/Render
infrastructure for CallMeIE + owlzone.trade. **HIGH-SENSITIVITY
project — touches live paying infrastructure.**

## Current status

- Phase: **ACTIVE — live and enforced**
- Last worked: 2026-04-23 (Clancy's Cork added as 7th demo, showcase direction)
- Cursor: P0 (HTTPS + enforcement) DONE 2026-04-21. Next open: P1 (OG/Twitter preview cards) → P2 (10-samples content review) → P3 (favicon).
- HTTPS: approved + enforced, expires 2026-07-20 (GitHub Pages auto-renews ~30 days prior)
- Deploy model: GitHub Pages (`main` → `/`), ~30s rebuild on push

## Three immediate actions

Do these in order after reading this file.

1. **Read [`INFRA.md`](INFRA.md) cover to cover** (§1–§13) — required before ANY infra work. Covers Hetzner VPS, Coolify tokens, Stripe live-mode webhooks, Porkbun DNS, 10+ client admin tokens, and the known workarounds (Coolify fqdn-cascade bug #6281, Render `/tmp` wipe).
2. **If editing infra**, mirror the change to `C:/Users/a33_s/Desktop/callmeie-fix/INFRA.md` in the same commit.
3. **If the task is pure site-content** (P1/P2/P3), work in `interactive-gallery.*` + `unique-samples.*`, push to `main`, wait 30s, verify on `https://websites.owlzone.trade`.

If none of the above applies, read the NEW-REPOS-RUNNING-CONTEXT.md
to see what the collaborator session is actually trying to move.

## Parallel context

- **Other Claude instances:** possible — this project is co-worked with `callmeie-fix/` (INFRA.md is mirrored across both). Always check the sister repo state before touching INFRA.
- **Git branch:** `main` (GitHub Pages deploys directly from `main`)
- **Cursor-sharing risk:** **MEDIUM** — any INFRA.md edit must be committed in BOTH `owl-studio-website-directions/INFRA.md` and `callmeie-fix/INFRA.md` in the same commit, or the mirrors drift.

## Quick links

| Purpose | File |
|---|---|
| Full routing + punch-list | [`CLAUDE.md`](CLAUDE.md) |
| Sole infra source-of-truth (§1–§13) | [`INFRA.md`](INFRA.md) |
| Main sales page | [`interactive-gallery.html`](interactive-gallery.html) |
| Ten website directions (sales content) | [`unique-samples.js`](unique-samples.js) |
| Sister-repo infra mirror | `C:/Users/a33_s/Desktop/callmeie-fix/INFRA.md` |
| Parent routing | [`../CLAUDE.md`](../CLAUDE.md) |

## Known risks

- **HTTPS cert** — auto-renews, but if a future cert stalls >24h after a DNS change, apply the CNAME drop/re-add recipe in CLAUDE.md §HTTPS status.
- **Render `/tmp` wipe** — CallMeIE FastAPI on Render loses `/tmp` on cold-start cycle. Fallback in INFRA.md §9.
- **Coolify fqdn-cascade bug (#6281)** — cascades into broken DNS on Hetzner if triggered. Workaround in INFRA.md §known-workarounds.
- **Porkbun DNS + Stripe webhook** — live-mode; any misconfig costs real money. Always dry-run via Coolify read-token before write-token actions.
- **Image pipeline** — Pollinations `model=turbo` is the free Tier-3 fallback (always-available); sites must never deploy SVG placeholders (they're live sales pitches, not mocks).

## If this surface looks stale

Regenerate from:
- **Phase / Last worked** → last commit on `main`
- **HTTPS cert status** → `gh api /repos/scruge1/owl-studio-website-directions/pages`
- **Punch-list** → CLAUDE.md §Next punch-list
