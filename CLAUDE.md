---
id: owl-studio-router
title: Owl Studio Website Directions Router
role: router
temporal_class: reference
status: stable
owner: claude-main
last_verified: 2026-05-18
verified_by: ICM Phase 2 / Branch E router-class press-back 2026-05-18 -- _route_check.js run BEFORE+AFTER yields identical empty route (project-local CLAUDE.md is human-routing, not session-boot injected; parent New-repos CLAUDE.md carries the injected load_order); 0 hard machine consumers of this filename (grep = doc pointers only)
refresh_cadence: on any infra/routing change or every 20 sessions per CORE-FILE-ICM-STANDARD.md
enforcement: see Enforcement section; route-inject.js parses the parent New-repos CLAUDE.md, not this file (no matching trigger heading here by design -- empty route before and after); INFRA.md remains the sole infra source of truth and is out of scope for this reformat
built_from: CORE-FILE-ICM-STANDARD.md router-class profile (gates 1,2,6,7,8) + work-diary.md, NOT by imitating a prior migrated file (Pattern 14)
---

# Owl Studio -- Website Directions, Claude Routing Surface

## High-priority infra load (read before any infra work)

Every session working anywhere in this repo or its sibling `callmeie-fix/`
must load `INFRA.md` in this directory **before doing any infra work**.
It is the single source of truth for:

- Hetzner VPS (178.104.205.255) + root SSH creds location
- Coolify API tokens (write + read) + API reference
- CallMeIE FastAPI service (**Hetzner/Coolify since 2026-05-30; migrated off Render** — canonical `api.callmeie.ie` / `admin.callmeie.ie`, `callmeie.onrender.com` dead) + all `/owl/*` routes + DB tables
- Stripe live-mode account + 7 Payment Links + webhook secret
- Porkbun DNS + current records
- 10+ registered Owl Studio client sites + admin tokens
- `~/.claude/routes/.env` credential vault structure
- Operational runbooks section 9 (onboard client, provision Stripe, deploy/redeploy Coolify service)
- Known workarounds (Coolify fqdn-cascade bug; Render `/tmp` wipe — historical, backend now Coolify Postgres, persistent)
- Active backlog + session-end log

Without loading INFRA.md you will duplicate work, miss running services,
or hit previously-solved blockers blind. Load order:

1. `~/.claude/CLAUDE.md` (already loaded automatically)
2. `C:/Users/a33_s/Desktop/claude MCPs/New repos/CLAUDE.md` (parent)
3. `C:/Users/a33_s/Desktop/claude MCPs/New repos/NEW-REPOS-RUNNING-CONTEXT.md`
4. `INFRA.md` (THIS DIRECTORY, read cover to cover section 1 to section 13)
5. This file (project-local CLAUDE.md)

Sister-repo `C:/Users/a33_s/Desktop/callmeie-fix/INFRA.md` is an
identical mirror of the above -- update both in the same commit on any
infra change.

If you need details not in INFRA.md, escalate the gap by **adding them
to INFRA.md before continuing work** so the next session has them.

---

## What this is

Sales-pitch static site for **Owl Studio**, a web design business being
launched from this domain. Purpose: a prospect lands on the site,
browses ten website "directions" (distinct visual/structural styles),
picks one that fits, and emails the studio to start a project.

- **Live (HTTP)**: http://websites.owlzone.trade/
- **Live (HTTPS)**: https://websites.owlzone.trade (cert approved, enforced, expires 2026-07-20)
- **GitHub**: https://github.com/scruge1/owl-studio-website-directions
- **Deploy model**: GitHub Pages (legacy, `main` branch, `/` root)
- **Domain**: Porkbun -- `websites.owlzone.trade` CNAME to `scruge1.github.io`
- **Contact**: callmeie@proton.me

## Mode

Collaborator mode. Same gates as the parent `New repos/CLAUDE.md`:
research, prototype-before-batch, save, live demo, business intent,
real automation, routed writeback, touch (valid second thing pressed back -- runtime,
Adam, archive, oracle, or Codex; not another Claude).

## What landed before this handoff (Codex session, 2026-04-20 ~20:48 UTC)

Codex built the entire static site in one commit (`ffd6459`) and stood
up DNS + GitHub Pages. Listed in order of what a fresh reader should
inspect:

- `index.html` -- minimal redirect shell; `<meta http-equiv="refresh">`
  to `interactive-gallery.html`. Keeps `/` working if someone types
  the bare domain.
- `interactive-gallery.html` -- the actual sales page. Hero, samples
  section placeholder (rendered at runtime), closing CTA. Modal for
  expanded views of any sample.
- `interactive-gallery.{css,js}` -- chrome for the gallery, modal
  open/close, overall layout.
- `unique-samples.{css,js}` -- the ten website directions rendered as
  cards inside `<section id="samples">`. This is the sales content.
- `renders/` -- three hero image PNGs used in the hero stack:
  `02-chrome-commerce.png`, `06-local-growth-engine.png`,
  `10-heritage-story.png`.
- `CNAME` -- `websites.owlzone.trade` (committed; this file is how
  GitHub Pages reads the custom domain).

**Typography**: Archivo, DM Sans, Fraunces, JetBrains Mono (Google Fonts).

## HTTPS status (resolved 2026-04-21)

```
status:                    built
cname:                     websites.owlzone.trade
https_enforced:            true
https_certificate.state:   approved
https_certificate.expires: 2026-07-20
build_type:                legacy
```

Cert auto-issued by GitHub Pages (Let's Encrypt). Sister site
`callmeie.ie` also approved + enforced, expires 2026-07-02. Both
return 200 over HTTPS. No action needed until renewal -- GitHub
rotates Let's Encrypt certs automatically ~30 days before expiry.

Recovery recipe if a future cert stalls >24h after DNS change:

```bash
# 1. drop CNAME to re-kick Let's Encrypt
gh api /repos/scruge1/owl-studio-website-directions/pages -X PUT \
  --input - <<<'{"cname": null}'
sleep 30
# 2. re-add custom domain
gh api /repos/scruge1/owl-studio-website-directions/pages -X PUT \
  --input - <<<'{"cname": "websites.owlzone.trade"}'
# 3. once cert approved, enforce
gh api /repos/scruge1/owl-studio-website-directions/pages -X PUT \
  --input - <<<'{"https_enforced": true}'
```

## Working tree

```
owl-studio-website-directions/
|-- CNAME                          (websites.owlzone.trade)
|-- index.html                     (redirect shell)
|-- interactive-gallery.html       (main page)
|-- interactive-gallery.css        (page chrome)
|-- interactive-gallery.js         (gallery + modal logic)
|-- unique-samples.css             (sample-card styles)
|-- unique-samples.js              (10 website-direction definitions)
|-- renders/                       (hero images)
|   |-- 02-chrome-commerce.png
|   |-- 06-local-growth-engine.png
|   `-- 10-heritage-story.png
`-- CLAUDE.md                      (this file)
```

No build step. Push to `main`, GitHub Pages rebuilds in ~30s.

## Acceptance for "live as a sales pitch"

A shareable link is sales-ready when **all** of:

- [ ] HTTPS works without browser warnings
- [ ] Root `/` redirects to gallery without flicker
- [ ] All ten sample cards render without console errors
- [ ] Modal opens on click, closes on ESC / outside click / X button
- [ ] Hero images load (the three poster cards)
- [ ] `mailto:` CTA opens the email client with the right subject line
- [ ] Mobile viewport 375px renders cleanly
- [ ] `<title>` and `<meta description>` are specific (not generic)
- [ ] OG / Twitter preview cards work (og:image, og:title, og:description)

Untested from here: social preview (`og:image`), Lighthouse score,
SEO sitemap. Worth verifying once HTTPS is live.

## Next punch-list (P0 to P5)

> Forward intent now lives in `NEXT-STEPS.md` (data/intent split, gate
> 3a). This section is a stable reference summary; the live ordered
> queue and any new items are in `NEXT-STEPS.md`.

### P0 -- HTTPS live + enforcement -- DONE 2026-04-21

Cert approved + enforced on both websites.owlzone.trade (exp 2026-07-20)
and callmeie.ie (exp 2026-07-02). Auto-renewed by GitHub Pages.

### P1 -- Social preview cards (OG + Twitter)

Current `<head>` has `<title>` + `<meta description>` but nothing for
Open Graph or Twitter. A shared link in WhatsApp / Slack / LinkedIn
will render as a naked URL. Add:

- `<meta property="og:title" content="Owl Studio, Website Directions">`
- `<meta property="og:description" content="...">`
- `<meta property="og:image" content="https://websites.owlzone.trade/renders/...">`
- `<meta property="og:url" content="https://websites.owlzone.trade/">`
- `<meta name="twitter:card" content="summary_large_image">`
- Same image should be 1200x630 for best render; repurpose one of
  the three hero PNGs (they're likely 1600x1200 or so -- verify).

### P2 -- 10 samples content review

Read through `unique-samples.js` -- each of the ten directions should:
- Have a specific, non-generic name (no "Modern Business" / "Clean
  Corporate" filler)
- List 3 to 5 concrete section names (not "About", "Services", "Contact"
  -- something distinctive per direction)
- Name a target audience (product, local service, SaaS, clinic,
  finance, trades, AI, story-led)
- Have a credible CTA appropriate to the direction

If any feel generic, rework them. Nothing should read as AI filler --
this is the sales pitch.

### P3 -- Favicon + PWA polish

No `<link rel="icon">` currently. Add an owl-themed favicon (SVG ideal
for sharpness). Optional but professional: `manifest.json` +
`apple-touch-icon`.

### P4 -- Contact form alternative

`mailto:` is fine for v1 but loses prospects who don't have a mail
client configured. Consider:
- A Formspree / Basin embed that POSTs to callmeie@proton.me
- A simple GitHub Form (Issues backed)
- A Cloudflare Pages Function if we ever migrate off GitHub Pages

Medium effort; adds real lead capture.

### P5 -- Analytics + conversion tracking

Once traffic starts: a lightweight analytics setup (Plausible,
Umami self-hosted, or Cloudflare Web Analytics -- anything not Google
for ethics). Track only `#samples` clicks, modal opens, and the
`mailto:` CTA click. Three events is enough to measure the funnel.

## Anti-scope (do NOT do)

- No heavy framework migration (Next.js / React) -- the site is
  purposely static HTML/CSS/JS for max reliability and zero build step
- No account / auth system -- sales pages don't need it
- No premature A/B testing -- get it live, advertise, then measure
- No ordering mass renders / new imagery until the existing three
  hero images are confirmed to carry the message
- No switching hosts -- GitHub Pages is fine for v1

## Demo client sites (`demos/`)

Seven demo builds live at `websites.owlzone.trade/demos/[slug]/`:
`slaney-dental-wexford`, `aran-vets-galway`, `murphy-plumbing-cork`,
`strand-road-dental`, `vetcare-limerick`, `curtin-electrical`,
`clancys-restaurant-cork` (showcase -- HeroFullBleed + ScrollNarrative, 2026-04-23).

Source builds: `~/Desktop/design-hub/clients/[slug]/`
Build tool: `/new-service-site` skill (`~/.claude/skills/new-service-site/SKILL.md`)

**Design refinement:** After build, use impeccable interventions for corrections -- read `~/.claude/skills/impeccable/content/site/skills/{name}.md`. Trigger: `imp:impeccable` (master audit), then specific skills (`imp:bolder`, `imp:typeset`, `imp:layout`, `imp:quieter` etc.). Prerequisite: run `imp:impeccable` first to set project design context.

**Image generation pipeline** (3-tier, documented in new-service-site SKILL.md section Image Generation):
- Tier 1: Replicate FLUX.1 Dev -- $0.025/image, best quality, needs account credit
- Tier 2: HF ZeroGPU -- shared quota, may queue
- Tier 3: **Pollinations `model=turbo`** -- always free, sequential requests, 35s delays, JPEG magic-byte check (`ffd8ff`)

**Never deploy SVG placeholders to demo sites** -- demos are live sales pitches.
Working bash pattern lives in new-service-site SKILL.md section Image Generation, Tier 3.

To update a demo: build in `design-hub/clients/[slug]/`, copy `dist/` to `demos/[slug]/`, commit + push main.

---

## Where else to look

- Live URL: http://websites.owlzone.trade/
- GitHub repo: https://github.com/scruge1/owl-studio-website-directions
- Porkbun DNS dashboard: owned by scruge1
- Contact inbox: callmeie@proton.me
- Parent routing: `C:/Users/a33_s/Desktop/claude MCPs/New repos/CLAUDE.md`
- Forward intent: `NEXT-STEPS.md` (this directory)
- Cold-boot orientation: `COLD-BOOT.md` (this directory)
- Verified running state: `RUNNING-CONTEXT.md` (this directory)
- Superseded/completed intent history: `HISTORY-LOG.md` (this directory)

---

## Operational state

**Canonical infrastructure reference:** `INFRA.md` in this repo (mirror of `../INFRA-OWL-STUDIO.md`).
Every secret location, every service, every deploy endpoint, every runbook lives there.
When anything changes in infra, update INFRA.md in the same commit -- no exceptions.

## Enforcement

Standard: `CORE-FILE-ICM-STANDARD.md` router-class profile (gates
1,2,6,7,8). This is a project-local CLAUDE.md: `route-inject.js` parses
the **parent** `New repos/CLAUDE.md` for the injected session-boot
load_order, not this file. By design there is no `^Read on entry:` /
`^## On Boot$` trigger heading here, so `_route_check.js` yields an
empty route both before and after this reformat (no regression).
Reformat was in-place, name unchanged -- no path consumer can break;
grep of the tree for this filename returns documentation pointers only
(INFRA.md site registry, parent CLAUDE.md project roster, codex.md,
SYSTEM-CALENDAR-PDR), zero hard machine consumers. The oracle reads
`RUNNING-CONTEXT.md` / `COLD-BOOT.md` (frontmatter-aware via
`_status_date`) for state, never this file for routing. INFRA.md is the
sole infra source of truth and was deliberately NOT touched by this
reformat. Prose-only today (MF-07: drifts in ~4 sessions without a
gate); the standing structural gate is `route-inject.js` parsing the
parent on every SessionStart plus the 20-session re-audit cadence in
`refresh_cadence`.
