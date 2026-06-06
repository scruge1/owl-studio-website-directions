---
id: owl-studio-cold-boot
title: Owl Studio Cold Boot
role: claude-orientation
temporal_class: data
status: at-risk
owner: claude-main
last_verified: 2026-04-24
verified_by: body distilled from CLAUDE.md + INFRA.md + repo state at 2026-04-24; NOT re-verified against the 2026-05-08 / 2026-05-17 work in RUNNING-CONTEXT this session -- treat status/cursor below as stale, cross-check RUNNING-CONTEXT.md before acting
refresh_cadence: regenerate from CLAUDE.md + INFRA.md + RUNNING-CONTEXT.md whenever this surface looks stale; full re-derive every 20 sessions per CORE-FILE-ICM-STANDARD.md
enforcement: see Enforcement section; oracle reads this file's frontmatter last_verified (frontmatter-aware _status_date) as the owl-studio continuity status date alongside RUNNING-CONTEXT.md; prose-only otherwise (MF-07)
built_from: CORE-FILE-ICM-STANDARD.md continuity-class profile (gates 1,2,4,5,6,7,8 + 3a) + work-diary.md, NOT by imitating a prior migrated file (Pattern 14)
---

# Owl Studio -- Cold Boot

*Body last updated: 2026-04-24. Derived from CLAUDE.md + INFRA.md + repo
state. `at-risk`: newer verified work (2026-05-08 Phase 5 books, 2026-05-17
SEO/GBP) landed in RUNNING-CONTEXT.md AFTER this body was written -- the
status/cursor below predates it. Cross-check RUNNING-CONTEXT.md before
acting on the cursor.*

One-page orientation for a Claude instance starting work here. Read
this first. If anything looks stale, regenerate from CLAUDE.md + INFRA.md
+ RUNNING-CONTEXT.md.

## What this is

Sales-pitch static site (`websites.owlzone.trade`) for **Owl Studio**,
a web-design business. Prospects browse 10 website "directions",
pick one, email the studio. The project also *operates* the live
client fleet (7 demo sites) and the wider Hetzner/Stripe/Render
infrastructure for CallMeIE + owlzone.trade. **HIGH-SENSITIVITY
project -- touches live paying infrastructure.**

## Current status (as of 2026-04-24 body -- see at-risk note above)

- Phase: **ACTIVE -- live and enforced** `{deployed}`
- Last worked (at write time): 2026-04-23 (Clancy's Cork added as 7th demo, showcase direction) `(verified 2026-04-24, superseded -- RUNNING-CONTEXT shows work through 2026-05-17)`
- Cursor (at write time): P0 (HTTPS + enforcement) DONE 2026-04-21. Next open: P1 (OG/Twitter preview cards) then P2 (10-samples content review) then P3 (favicon). `open` -- but NEXT-STEPS.md now also carries the live CallMeIE SEO/GBP queue opened 2026-05-17; read it for the true current cursor.
- HTTPS: approved + enforced, expires 2026-07-20 (GitHub Pages auto-renews ~30 days prior) `verified` `(verified 2026-04-21)`
- Deploy model: GitHub Pages (`main` to `/`), ~30s rebuild on push `stable`

## Three immediate actions

Do these in order after reading this file.

1. **Read [`INFRA.md`](INFRA.md) cover to cover** (section 1 to section 13) -- required before ANY infra work. Covers Hetzner VPS, Coolify tokens, Stripe live-mode webhooks, Porkbun DNS, 10+ client admin tokens, and the known workarounds (Coolify fqdn-cascade bug #6281, Render `/tmp` wipe).
2. **If editing infra**, mirror the change to `C:/Users/a33_s/Desktop/callmeie-fix/INFRA.md` in the same commit.
3. **If the task is pure site-content** (P1/P2/P3), work in `interactive-gallery.*` + `unique-samples.*`, push to `main`, wait 30s, verify on `https://websites.owlzone.trade`.

If none of the above applies, read `NEW-REPOS-RUNNING-CONTEXT.md`
to see what the collaborator session is actually trying to move, and
this directory's `NEXT-STEPS.md` for the live forward queue.

## Parallel context

- **Other Claude instances:** possible -- this project is co-worked with `callmeie-fix/` (INFRA.md is mirrored across both). Always check the sister repo state before touching INFRA. You may be one of several instances running in parallel; do not assume a single linear reader or a single "next" action -- the live queue is in NEXT-STEPS.md.
- **Git branch:** `main` (GitHub Pages deploys directly from `main`)
- **Cursor-sharing risk:** **MEDIUM** -- any INFRA.md edit must be committed in BOTH `owl-studio-website-directions/INFRA.md` and `callmeie-fix/INFRA.md` in the same commit, or the mirrors drift.
- **Mid-migration hazard:** this surface is part of the core-file ICM alignment (Branch E). It is now frontmatter-stamped but the body predates 2026-05-08/05-17 work -- if the cursor here disagrees with RUNNING-CONTEXT.md/NEXT-STEPS.md, those win.

## Quick links

| Purpose | File |
|---|---|
| Full routing + punch-list summary | [`CLAUDE.md`](CLAUDE.md) |
| Live forward queue (intent) | [`NEXT-STEPS.md`](NEXT-STEPS.md) |
| Verified running state (data) | [`RUNNING-CONTEXT.md`](RUNNING-CONTEXT.md) |
| Superseded/completed intent history | [`HISTORY-LOG.md`](HISTORY-LOG.md) |
| Sole infra source-of-truth (section 1 to 13) | [`INFRA.md`](INFRA.md) |
| Main sales page | [`interactive-gallery.html`](interactive-gallery.html) |
| Ten website directions (sales content) | [`unique-samples.js`](unique-samples.js) |
| Sister-repo infra mirror | `C:/Users/a33_s/Desktop/callmeie-fix/INFRA.md` |
| Parent routing | [`../CLAUDE.md`](../CLAUDE.md) |

## Known risks

- **HTTPS cert** -- auto-renews, but if a future cert stalls >24h after a DNS change, apply the CNAME drop/re-add recipe in CLAUDE.md, HTTPS status section.
- **Render `/tmp` wipe (RESOLVED — historical)** -- CallMeIE FastAPI **migrated off Render onto Hetzner/Coolify with Postgres on 2026-05-30**; the `/tmp` SQLite-wipe no longer applies. `callmeie.onrender.com` is a dead/stale deploy — use `api.callmeie.ie` / `admin.callmeie.ie`. See INFRA.md §3 banner.
- **Coolify fqdn-cascade bug (#6281)** -- cascades into broken DNS on Hetzner if triggered. Workaround in INFRA.md known-workarounds.
- **Porkbun DNS + Stripe webhook** -- live-mode; any misconfig costs real money. Always dry-run via Coolify read-token before write-token actions.
- **Image pipeline** -- Pollinations `model=turbo` is the free Tier-3 fallback (always-available); sites must never deploy SVG placeholders (they're live sales pitches, not mocks).

## If this surface looks stale

Regenerate from:
- **Phase / Last worked** to last commit on `main` + RUNNING-CONTEXT.md newest entry
- **HTTPS cert status** to `gh api /repos/scruge1/owl-studio-website-directions/pages`
- **Punch-list / cursor** to NEXT-STEPS.md (live intent) + CLAUDE.md punch-list summary

## Enforcement

Standard: `CORE-FILE-ICM-STANDARD.md` continuity-class profile (gates
1,2,4,5,6,7,8 + 3a). This is append-only data: no history deleted,
forward intent kept in `NEXT-STEPS.md` (gate 3a data/intent split). The
oracle's `_status_date` reads this file's frontmatter `last_verified:`
first (frontmatter-aware after the STATE_FILES patch), and
`_running_context_text` matches this file by `endsWith("COLD-BOOT.md")`,
so this surface is one of owl-studio's two continuity status sources
alongside `RUNNING-CONTEXT.md` -- stamping `last_verified: 2026-04-24`
(NOT 2026-05-18) keeps the oracle honest about the stale body rather
than masking it. Reformat was in-place, name unchanged -- no path
consumer breaks (grep = doc pointers only; INFRA.md untouched and out
of scope). Prose-only otherwise (MF-07: ~4-session drift without a
gate); standing gates are the oracle frontmatter read every staleness
scan plus the 20-session re-audit cadence in `refresh_cadence`.
