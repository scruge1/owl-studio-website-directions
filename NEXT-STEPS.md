---
id: owl-studio-next-steps
title: Owl Studio Next Steps
role: forward-intent
temporal_class: intent
status: open
owner: claude-main
last_verified: 2026-05-17
verified_by: SYNC/intent side -- queue reflects 2026-05-17 CallMeIE SEO/GBP open follow-through + standing P1-P5 site punch-list; ICM Branch E in-place reformat 2026-05-18 (frontmatter + em-dash purge + enforcement footer; no item dropped -- nothing fully completed+superseded+>7-day at migration time)
refresh_cadence: rewritten freely each session (SYNC side); completed/superseded/>7-day entries move VERBATIM to HISTORY-LOG.md at session close (gate 3a)
enforcement: data/intent split (gate 3a) is the structural gate; oracle status_date for owl-studio derives from RUNNING-CONTEXT.md / COLD-BOOT.md frontmatter, NOT this file, so name-stable in-place reformat is near-zero risk
built_from: CORE-FILE-ICM-STANDARD.md intent-class profile (gate 3a) + work-diary.md data/intent split, NOT by imitating a prior migrated file (Pattern 14)
---

# Owl Studio -- Next Steps

Forward intent only (work-diary SYNC side). What is planned / open /
to-do. Verified facts live in `RUNNING-CONTEXT.md`; completed and
superseded history lives in `HISTORY-LOG.md`. This file is freely
rewritten each session; nothing here is a historical record.

## Recurring discipline

### Monthly — fulfillment audit
Run `/audit-fulfillment-gap` at the start of each calendar month. Diffs current tier readiness + gap state vs `FULFILLMENT-AUDIT-BASELINE.md` (frozen 2026-05-20). Writes delta to `FULFILLMENT-AUDIT-LOG.md` (append-only). Update baseline only when ≥3 readiness rows changed OR a tier crossed READY/PARTIAL/NOT-READY band. Auto-offer also fires from `self-check.md` at session-end if PRICING-SSOT / PDR-CLIENT-FULFILLMENT / `callmeie-hub/*/CLAUDE.md` was edited that session — manual monthly run remains the steady-state cadence.

## Social + Paid-Ads Automation (PRD-SOCIAL-ADS-AUTOMATION.md, 2026-06-12)

New §4b product (Social Starter €149 / Social+Ads €249 / Growth €397) — but "campaigns built/run/optimised" is manual today, not built. PRD = phased build to make it real. **Phase 0 has lead-time items — start before build:**

- [ ] **Decide Ayrshare ($149/mo, zero Meta app-review) vs Mixpost (one-time, self-host, you do the review).** Recommend Ayrshare for speed.
- [ ] **Google Ads MCC + dev token — PARKED 2026-06-13 (blocked by Google manager-creation cap).** Attempted on swarm.agent.2026: cleared 2 stuck accounts, but fresh manager create still hits "reached your limit for creation of manager accounts" — cap is ad-spend-history-tied; no-spend account gets ~zero allowance. NOT critical-path (token only needed for Phase 2 automation, post-sale). **Retry in 24-48h** (cap may propagate-clear post-deletion); if still blocked → needs a spending account first or Google Ads support. Manual delivery needs no API, so no rush.
- [ ] Stand up **n8n** (Docker, Hetzner per INFRA.md) as the automation spine.
- [ ] **Rewrite §4b copy honest** — "managed campaigns, set up + run + report"; DROP "optimise/guarantee" until proven (Doc Ops overclaim guard).
- [ ] Phase 1 = social auto-publish (creative engine → n8n → Ayrshare → FB/IG/GBP) live for the roofer.
- [ ] Phase 2 = Google Ads API campaign-template + budget-cap; Phase 3 = pixel + monthly report; Phase 4 (defer) = Meta Ads + Mixpost swap.

Gated items (live mutations, Adam "go"): §4b website page, `callmeie-hub/social-ads-scope.md`, 3 Stripe links.

## Open punch-list (P1 to P5)

### P1 -- Social preview cards (OG + Twitter) -- NOT DONE
Current `<head>` has title + description but no OG/Twitter tags. Shared links render as naked URLs.
Add to `interactive-gallery.html`:
- `og:title`, `og:description`, `og:image` (1200x630 from one of the three hero PNGs), `og:url`
- `twitter:card: summary_large_image`

### P2 -- 10 samples content review
Read `unique-samples.js` -- every direction must have: specific non-generic name, 3 to 5 concrete section names, named target audience, credible CTA. Nothing generic / AI-filler.

### P3 -- Favicon + PWA polish
No `<link rel="icon">` present. Add SVG owl-themed favicon. Optional: `manifest.json` + `apple-touch-icon`.

### P4 -- Contact form alternative
Current `mailto:` loses prospects without a mail client. Options: Formspree, Basin, or Cloudflare Pages Function.

### P5 -- Analytics
Plausible / Umami / Cloudflare Web Analytics. Track: `#samples` clicks, modal opens, `mailto:` CTA. Three events.

## CallMeIE SEO / GBP (opened 2026-05-17)

Local-ranking blocker (GBP not live) is RESOLVED -- profile verified. Remaining = optimization + indexing follow-through. Ordered by leverage:

1. **GBP category cleanup** -- DONE 2026-05-17 (submitted, pending Google review ~10min): PRIMARY to "Telephone answering service"; Web Designer + Computer consultant kept secondary; "Software company" removed. **WATCH:** category edits are Google-reviewed and this profile had a prior category rejection -- verify the pending edit is approved (not reverted to Software company) next session via GBP Manager.
2. **GBP description rewrite** -- DONE 2026-05-17 (submitted, pending review): replaced with clean 660/750 text -- no US number, no "Irish number lands May 2026"; leads receptionist + Limerick + GDPR; ends +353 61 788 120 / hello@callmeie.ie.
3. **NAP consistency pass** -- SITE-SIDE DONE 2026-05-17 (pushed `2c83863`, live-verified): #business+#service schema name to "CallMeIE Technologies", areaServed to Limerick+Munster+IE, tel +35361788120; footer "Limerick V94" to "Serving Limerick & Munster" propagated all 85 pages. Canonical resolved: name "CallMeIE Technologies", voice +353 61 788 120, WhatsApp 085 786 3564 (chat), hidden-address service-area Limerick+Munster (no Eircode -- service-area hides it). REMAINING (GBP-side, keyboard): set GBP primary phone 085 to +353 61 788 120; GBP website to non-www `https://callmeie.ie/`.
4. **GBP completeness** -- PARTLY DONE 2026-05-17 (pending review): Facebook linked (page 1105012356028968); service area to Limerick + Munster (was Limerick only); GBP phone to 061, website to non-www also done under #3. **REMAINING:** Services list (11: AI phone receptionist, 24/7 call answering, Appointment booking, Missed-call text-back, After-hours answering, Overflow/busy-line, Dental/Motor-factors/Salon/Solicitor reception, Local SEO & GBP) -- lives in the profile dashboard Services editor (separate UI, not the Business-information dialog); 11 repetitive adds; bulk-add when convenient. Photos: only real ones (none supplied -- skip). GBP Posts: draft from the 2 new blog posts (ongoing cadence).
5. **Re-request indexing for pillar post** -- `receptionist/blog/what-is-an-ai-phone-receptionist.html` (quota-blocked 2026-05-17; retry after ~24h reset). Sitemap+lastmod will carry it regardless.
6. **Recheck GSC Page-indexing in ~1 week** -- expect the 20 "Discovered" to start clearing as sitemap reprocesses + crawl requests land + content/authority builds. Track index-count trend.
7. **Content cadence** -- GEO research = 1 to 2 fresh structured posts/week. 2026-05-17 shipped 2 (missed-calls, GDPR). Next documented topics: AI receptionists for dental practices (angle must NOT cannibalise /receptionist/dental.html), How Irish accents are handled, cost of switching from voicemail.

## Agency expansion
- Second client brief: ready when brief arrives. Pipeline: 6 remaining section templates, Dental/Trades presets.
- New-service-site skill: `~/.claude/skills/new-service-site/SKILL.md`

## Enforcement

Standard: `CORE-FILE-ICM-STANDARD.md` intent-class profile. Gate 3a
(data/intent split) IS the structural gate here: completed, superseded,
or >7-day entries move VERBATIM to `HISTORY-LOG.md` at session close and
are never deleted. Verified facts stay out of this file (they live in
`RUNNING-CONTEXT.md`). At the 2026-05-18 Branch E reformat NO item was
moved out: the entire SEO/GBP queue is 1 day old with live WATCH/
REMAINING follow-through, and the P1-P5 punch-list + Agency expansion
are open forward intent -- none was simultaneously completed AND
superseded AND >7 days old, so per "do not drop any open revenue/infra
item, when unsure keep it" all items were retained verbatim. Gate 8
near-zero risk, FS-verified: in-place, name unchanged, so no path
consumer breaks; the oracle's `_status_date` for owl-studio derives
from `RUNNING-CONTEXT.md` / `COLD-BOOT.md` frontmatter
(`_running_context_text` matches those by suffix), NOT this file, so
this file's frontmatter cannot mislead the staleness scan; INFRA.md
untouched and out of scope. Prose-only otherwise (MF-07); the standing
structural gate is gate 3a enforced at every session close plus the
20-session re-audit cadence in `refresh_cadence`.
