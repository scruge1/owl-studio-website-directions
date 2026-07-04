---
id: owl-studio-running-context
title: Owl Studio Running Context
role: verified-state-log
temporal_class: data
status: stable
owner: claude-main
last_verified: 2026-05-17
verified_by: append-only verified-work log; newest entry 2026-05-17 (CallMeIE SEO blog posts pushed + live-verified, sitemap fix, GSC diagnosis, GBP status corrected); ICM Branch E in-place reformat 2026-05-18 added frontmatter + em-dash purge only, no history altered
refresh_cadence: append-only (HANDOVER side); never overwrite completed facts; forward intent goes to NEXT-STEPS.md; re-audit every 20 sessions per CORE-FILE-ICM-STANDARD.md
enforcement: see Enforcement section; oracle _running_context_text matches this file by endsWith("RUNNING-CONTEXT.md") and _status_date reads frontmatter last_verified first (frontmatter-aware); prose-only otherwise (MF-07)
built_from: CORE-FILE-ICM-STANDARD.md continuity-class profile (gates 1,2,4,5,6,7,8 + 3a) + work-diary.md data/intent split, NOT by imitating a prior migrated file (Pattern 14)
---

# Owl Studio -- Running Context

Append-only verified-state log (work-diary HANDOVER side). Facts only:
what happened, what was built, current verified state. No forward plans
here -- those live in `NEXT-STEPS.md`. No completed fact is ever
overwritten or deleted.

## 2026-05-30 -- CallMeIE backend identity corrected + demo-line block

Verified during demo-line prank triage: the live receptionist admin is
**`https://admin.callmeie.ie`** (Hetzner/Coolify, `178.104.205.255`), DB
current to 2026-05-30 21:23 (idmax 1587). `callmeie.onrender.com` is a
**stale secondary deploy** (separate DB frozen id<=45 / 2026-04-26) that
still answers + accepts admin writes with the same `ADMIN_TOKEN` -- a real
hazard (BUG-07). INFRA.md §3 banner updated to name Coolify canonical;
Render marked non-authoritative. Demo line `+35361788120` now fronted by a
Twilio Serverless call-screen (`callmeie-call-screen` / `.../screen`):
denylist `+353852345595` -> `<Reject>`, all others -> `<Redirect>` to Vapi,
VoiceFallbackUrl -> Vapi (fault-safe). Live 21:26 UTC; self-test PASS;
not yet exercised by a real inbound call. Five prank calls flagged `spam`
on the live backend. Leads/SMS/recordings confirmed working (an earlier
"leads dropping" claim was a wrong-backend artifact, retracted). Commit
`724399f` (this repo, INFRA) + `594255c` (callmeie-fix). Unpushed.

## Status (2026-05-08)

Active. Phase 5 books module live; portal recovered from 24h silent outage. Cockpit + onboarding feature shipped. Adam-keyboard reduced to Revenue/VAT items. `deployed`

### 2026-05-20 -- PDR-CLIENT-FULFILLMENT.md drafted `verified` `(verified 2026-05-20)`

- `PDR-CLIENT-FULFILLMENT.md` written (171 lines, status `draft`) -- synthesis of 4 opus agents (Stripe-readiness sweep, fulfillment-pipeline audit, merge-inventory pass, gap-owner identification). Captures 2026-05-20 audit verdict (D5 Managed Websites 0/10 fulfillment), 7 decisions (single workspace, 5 stages, 65/25/10 mix, bundle new-service-site skill, etc.), 10 out-of-workspace gaps with owners, merge map (in / link / archive / 7 conflicts). Workspace itself being built in parallel at `jake-van-clief-icm/workspaces/client-fulfillment/`. Sibling PDR formula matched: `PDR-BACKEND.md` (numbered sections, "What this PDR does NOT cover" non-goals, decision record, changelog). Awaiting Adam press-back to promote `draft` -> `accepted`.

### 2026-05-17 -- CallMeIE SEO: blog post live, sitemap indexing-gap fixed, GSC diagnosed, GBP status corrected `verified` `(verified 2026-05-17)`

- **2 new blog posts LIVE** on callmeie.ie (GEO/AEO-engineered: front-loaded answer block, triple JSON-LD Article+FAQPage+BreadcrumbList, sourced stats, cohesion-injected, sitemap+lastmod):
  - `the-cost-of-missed-calls-for-irish-businesses.html` -- sector loss table + calculator. Pushed `3c66bec..152353a`, verified live.
  - `is-an-ai-phone-receptionist-gdpr-compliant-ireland.html` -- controller/processor, Art 28 DPA, EU AI Act Art 50 disclosure, recording consent, retention; links /legal/dpa.html. Pushed `152353a..1b57cac`, verified live 200 + valid schema.
  - Blog index reordered (GDPR=1, missed-calls=2, pillar=3); coming-soon refreshed.
- **GBP edits applied (driven in-browser, Adam at keyboard, all submitted + pending Google review ~10min):** primary category Software company to **Telephone answering service** (Web Designer + Computer consultant kept; Software company removed); description replaced (no US number / no dead "Irish number lands May 2026"); phone 085 to **(061) 788 120**; website www to **https://callmeie.ie/**; Facebook page linked; service area Limerick to **Limerick + Munster**. NAP now consistent site to GBP. WATCH: category edits Google-reviewed + this profile had a prior category rejection -- confirm approved (not reverted) next session. Remaining: GBP Services list (11, separate dashboard UI, queued NEXT-STEPS #4).
- **Sitemap indexing gap found + fixed.** Root `callmeie-hub/sitemap.xml` (robots.txt target) was MISSING the existing pillar post (`what-is-an-ai-phone-receptionist.html`) AND the live `/local-seo/` product page entirely -- Google had no sitemap path to either. Added both + new post, with `lastmod`. GSC confirmed both were "URL unknown to Google / no referring sitemaps" -- this orphaning was a real, now-fixed cause of non-indexing.
- **GSC diagnosis (sc-domain:callmeie.ie):** 6 indexed / 25 not indexed. 20 of 25 = "Discovered - currently not indexed" = new-domain low authority/crawl-priority, NOT a technical bug. Other 4 = 1 noindex (`/dental.html`, old pre-migration root stub -- benign), 1 4xx, 1 redirect, 1 alt-canonical (benign migration artifacts from #18332). `/receptionist/` itself was "Discovered, not indexed". Request-indexing submitted + queued for `/`, `/receptionist/`, `/local-seo/`, new blog post (4/5). Pillar post hit Google's daily request-indexing quota -- deferred (sitemap+lastmod will carry it).
- **GBP status CORRECTED (claude-mem #20165/#20416/#20420 were stale).** "CallMeIE Technologies, Limerick, Ireland" GBP **exists and is Verified (100%)** as of 2026-05-17 -- created+verified between May 9 and now. The "not in Google / unverified" blocker is RESOLVED. Read-only audit (no edits made) found: rejected category edit pending (red-dot); primary appears = "Telephone answering service" (correct) with unresolved not-approved overlay; description stale (US demo number +1 661 764-3212 + "Irish number lands May 2026" though +353 61 788 120 went live 2026-05-11); GBP phone = 085 786 3564 (mobile) not the +353 61 landline; website = www. variant (site canonical is non-www); social profiles empty (FB page 1105012356028968 not linked). NAP inconsistency across site/GBP/sitemap confirmed.

### 2026-05-08 -- Phase 5 books module + 24h portal outage resolved `verified` `(verified 2026-05-08)`

- **books.callmeie.ie LIVE** -- CNAME at Cloudflare (id `9bffe51891f3ecbc9e95a0e15c09a475`), DNS-only / grey cloud, target `portal.callmeie.ie`. Coolify FQDN list updated to `https://portal.owlzone.trade,https://portal.callmeie.ie,https://books.callmeie.ie`. LE cert auto-issued post force-deploy.
- **24h silent outage discovered + fixed.** Root cause: security commit `805d7a6` (2026-05-07) made `LS_WEBHOOK_SECRET` REQUIRED in `app/config.py` Settings; Coolify env never had it set; container crashlooped on every restart; both portal.callmeie.ie + portal.owlzone.trade returned 503 silently for ~24h before noticed during Phase 5 FQDN flip. Pushed `LS_WEBHOOK_SECRET` from `~/.claude/routes/.env` to Coolify env via API (env_uuid `oxzed6n6jk8wc53y3nrv8g69`); force-redeploy; all 3 hostnames now 200 healthz.
- **Permanent prevention shipped:** `document-ops-portal/scripts/coolify_env_check.py` (~210 lines) introspects `app.config.Settings.model_fields` for required `Field(alias=...)` keys, diffs against `GET /applications/{uuid}/envs`, exits 1 if any required missing. `--sync` mode interactively pushes vault values via `POST /envs`. PHASE-5-BOOKS-DEPLOYMENT.md gained section 0 mandatory pre-deploy step. INFRA.md section 14.1a documents the gotcha + Coolify env API quirks (`is_build_time` field rejected with 422; env-only changes do NOT auto-restart container, must `POST /deploy?force=true`).
- **Verified live:** portal.callmeie.ie/healthz, portal.owlzone.trade/healthz, books.callmeie.ie/healthz all `200 {"ok":true,"env":"production"}`.
- Commits: portal `fed03ac` (env-check script + PHASE-5 section 0), this repo `4fa7342` (INFRA section 14.1a + Phase 5 CNAME entry).

### 2026-05-08 (later) -- Books module + Cockpit code DEPLOYED to production `verified` `(verified 2026-05-08)`

- 10 portal commits pushed to `scruge1/document-ops-portal:main` (e0023cb..fed03ac). GitHub Action triggered Coolify auto-deploy (deploy_uuid `lp35q3p14k47lqy66f4bv9gy`). Container rebuilt + healthy.
- Alembic auto-runs at container start (Coolify entrypoint). Live Postgres now at `0005_customers (head)`. Books module 18 tables + cockpit `customers` table all created. Verified via `docker exec rs0jyp5cj24hutaxijacye6r-160631392188 alembic current`.
- Live routes confirmed:
  - `/healthz` 200 (both portal.callmeie.ie + books.callmeie.ie)
  - `/books/dashboard` GET to 401 (admin-gated, books module router LIVE)
  - `/cockpit` GET to 401 (admin-gated, cockpit router LIVE)
  - `books.callmeie.ie/` GET to 303 to `/books/dashboard` (subdomain middleware LIVE -- commit b38f856)
- Books module Phase 1+2+3+4+5 + cockpit-onboarding R1+R2+R3+R4 are now production-live + accessible to Adam after magic-link login. Tests 199 green; live-side smoke confirms all routes respond as designed.
- This repo: pushed `4fa7342` + `6cb8b48` to `scruge1/owl-studio-website-directions:main`.

### Adam-keyboard remaining as recorded 2026-05-08 (forward items now tracked in NEXT-STEPS.md)

> Data note: these were the open Adam-keyboard items at 2026-05-08. The
> live, mutable version of any still-open item is in `NEXT-STEPS.md`
> (gate 3a). Kept here verbatim as the historical record at that date.

1. ~~Phase 5 books DNS + Coolify FQDN~~ DONE 2026-05-08
2. ~~PIT cert email~~ DONE 2026-05-07 (auto-reply received; awaits human reply)
3. Confirm Revenue VAT basis (cash vs invoice) -- code defaulted to invoice basis, runtime-switchable; check ROS portal or send MyEnquiries.
4. Q2-2026 VAT3 dry-run via ROS Off-line Upload after Jul 1 (calendar wait).
5. ROS XML decimal format decision on first submission (1-line switch in `app/books/ros_xml.py` if Revenue rejects 2dp).

### 2026-04-26 -- original status `verified` `(verified 2026-04-26)`

Active client agency project. Gallery + 7 demo sites live.

## Live surfaces

| URL | Status | Notes |
|---|---|---|
| https://websites.owlzone.trade | Live, HTTPS | Gallery + 10 directions. Cert expires 2026-07-20 (auto-renew). |
| /demos/vetcare-limerick | Live | Fraunces Variable font. Mobile fix shipped 2026-04-25. |
| /demos/curtin-electrical | Live | tokens.css fix shipped 2026-04-26 |
| /demos/slaney-dental-wexford | Live | |
| /demos/aran-vets-galway | Live | |
| /demos/murphy-plumbing-cork | Live | |
| /demos/strand-road-dental | Live | |
| /demos/clancys-restaurant-cork | Live | HeroFullBleed + ScrollNarrative |

## Recent work (last 5 commits as of 2026-04-26)

- `aa6bb87` fix(curtin-electrical): add missing tokens.css, fix broken path
- `54de7a8` fix(demos): self-host GSAP to fix animations in DuckDuckGo browser
- `f227329` fix: 3 audit bugs -- duplicate ID, fetch error handling, focus trap
- `94f173b` feat: Lab samples open in overlay too
- `191933b` feat: full-screen demo preview overlay

## Pipeline

Build: design-hub `clients/[slug]/dist/` to copy to `demos/[slug]/` to commit to push main to GitHub Pages rebuilds ~30s.

Image pipeline: Tier 3 Pollinations `model=turbo` (free, 35s delays). JPEG magic-byte check `ffd8ff` required.

## Read on any infra session

`INFRA.md` in this repo -- sole source of truth for Hetzner VPS, Coolify, Stripe, Porkbun DNS, CallMeIE routes.

## Enforcement

Standard: `CORE-FILE-ICM-STANDARD.md` continuity-class profile (gates
1,2,4,5,6,7,8 + 3a). Append-only HANDOVER data: no completed fact was
overwritten or deleted in this reformat (frontmatter + em-dash purge +
status tags only). Forward intent is NOT here -- it lives in
`NEXT-STEPS.md` (gate 3a data/intent split); the one Adam-keyboard
block kept above is flagged as the 2026-05-08 historical snapshot, with
the live version pointed to NEXT-STEPS. The oracle's
`_running_context_text` matches this file by
`endsWith("RUNNING-CONTEXT.md")` and `_status_date` reads the
frontmatter `last_verified:` first (frontmatter-aware after the
STATE_FILES patch) -- stamped `2026-05-17` (newest verified body date,
NOT 2026-05-18) so the oracle reflects true verified age. Reformat was
in-place, name unchanged -- no path consumer breaks (grep = doc
pointers only; INFRA.md untouched and out of scope). Prose-only
otherwise (MF-07: ~4-session drift without a gate); standing gates are
the oracle frontmatter read every staleness scan plus the 20-session
re-audit cadence in `refresh_cadence`.

## 2026-07-03 (eve) — cal.com + Truth CMS editor MIGRATED off ZBook lab-rig → EPYC
ZBook lab-rig (`100.78.148.106`) developed a hardware charge-circuit fault (AC-plug hard-kills it, any adapter). Both self-hosted CallMeIE services it hosted were migrated to EPYC `adam@100.84.3.33` and VERIFIED live from the public URLs (served by EPYC alone):
- **cal.com** → `https://cal.callmeie.ie`→307, `/adam`→200. EPYC `/mnt/data/zbook-migration/restore/calcom/`, host :3000, pg dump restored.
- **Truth CMS editor** → `https://cms.callmeie.ie`→302. EPYC `/mnt/data/zbook-migration/restore/truth-editor/`, host :8081 (remapped from :8080), site re-cloned from scruge1/truth-store, 2-min git-sync cron re-established.
- **Cloudflare tunnel** `bba50ca4…` relocated to EPYC docker `cf-tunnel` (same UUID → no DNS change); ZBook cloudflared `disable --now`'d to kill split-brain.
- `cartel.owlzone.trade`→302 confirmed unaffected (independent tunnel).
**INFRA.md §17 + §18.2 updated with MIGRATED banners in BOTH mirrors** (this dir + `callmeie-fix/INFRA.md`), old lab-rig lines annotated-in-place as historical. Full migration forensics + ZBook hardware verdict in `New repos/NEW-REPOS-RUNNING-CONTEXT.md` (2026-07-03 eve sections) + memory `reference_lab-rig-hardware-ec-latchup`.
