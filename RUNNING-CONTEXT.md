# Owl Studio — Running Context

## Status (2026-05-08)

Active. Phase 5 books module live; portal recovered from 24h silent outage. Cockpit + onboarding feature shipped. Adam-keyboard reduced to Revenue/VAT items.

### 2026-05-08 — Phase 5 books module + 24h portal outage resolved

- **books.callmeie.ie LIVE** — CNAME at Cloudflare (id `9bffe51891f3ecbc9e95a0e15c09a475`), DNS-only / grey cloud, target `portal.callmeie.ie`. Coolify FQDN list updated to `https://portal.owlzone.trade,https://portal.callmeie.ie,https://books.callmeie.ie`. LE cert auto-issued post force-deploy.
- **24h silent outage discovered + fixed.** Root cause: security commit `805d7a6` (2026-05-07) made `LS_WEBHOOK_SECRET` REQUIRED in `app/config.py` Settings; Coolify env never had it set; container crashlooped on every restart; both portal.callmeie.ie + portal.owlzone.trade returned 503 silently for ~24h before noticed during Phase 5 FQDN flip. Pushed `LS_WEBHOOK_SECRET` from `~/.claude/routes/.env` to Coolify env via API (env_uuid `oxzed6n6jk8wc53y3nrv8g69`); force-redeploy; all 3 hostnames now 200 healthz.
- **Permanent prevention shipped:** `document-ops-portal/scripts/coolify_env_check.py` (~210 lines) introspects `app.config.Settings.model_fields` for required `Field(alias=...)` keys, diffs against `GET /applications/{uuid}/envs`, exits 1 if any required missing. `--sync` mode interactively pushes vault values via `POST /envs`. PHASE-5-BOOKS-DEPLOYMENT.md gained §0 mandatory pre-deploy step. INFRA.md §14.1a documents the gotcha + Coolify env API quirks (`is_build_time` field rejected with 422; env-only changes do NOT auto-restart container, must `POST /deploy?force=true`).
- **Verified live:** portal.callmeie.ie/healthz · portal.owlzone.trade/healthz · books.callmeie.ie/healthz all `200 {"ok":true,"env":"production"}`.
- Commits: portal `fed03ac` (env-check script + PHASE-5 §0), this repo `4fa7342` (INFRA §14.1a + Phase 5 CNAME entry).

### 2026-05-08 (later) — Books module + Cockpit code DEPLOYED to production

- 10 portal commits pushed to `scruge1/document-ops-portal:main` (e0023cb..fed03ac). GitHub Action triggered Coolify auto-deploy (deploy_uuid `lp35q3p14k47lqy66f4bv9gy`). Container rebuilt + healthy.
- Alembic auto-runs at container start (Coolify entrypoint). Live Postgres now at `0005_customers (head)`. Books module 18 tables + cockpit `customers` table all created. Verified via `docker exec rs0jyp5cj24hutaxijacye6r-160631392188 alembic current`.
- Live routes confirmed:
  - `/healthz` 200 (both portal.callmeie.ie + books.callmeie.ie)
  - `/books/dashboard` GET → 401 (admin-gated, books module router LIVE)
  - `/cockpit` GET → 401 (admin-gated, cockpit router LIVE)
  - `books.callmeie.ie/` GET → 303 → `/books/dashboard` (subdomain middleware LIVE — commit b38f856)
- Books module Phase 1+2+3+4+5 + cockpit-onboarding R1+R2+R3+R4 are now production-live + accessible to Adam after magic-link login. Tests 199 green; live-side smoke confirms all routes respond as designed.
- This repo: pushed `4fa7342` + `6cb8b48` to `scruge1/owl-studio-website-directions:main`.

### Adam-keyboard remaining (4 items)

1. ~~Phase 5 books DNS + Coolify FQDN~~ ✓ DONE 2026-05-08
2. ~~PIT cert email~~ ✓ DONE 2026-05-07 (auto-reply received; awaits human reply)
3. Confirm Revenue VAT basis (cash vs invoice) — code defaulted to invoice basis, runtime-switchable; check ROS portal or send MyEnquiries.
4. Q2-2026 VAT3 dry-run via ROS Off-line Upload after Jul 1 (calendar wait).
5. ROS XML decimal format decision on first submission (1-line switch in `app/books/ros_xml.py` if Revenue rejects 2dp).

### 2026-04-26 — original status

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

## Recent work (last 5 commits)

- `aa6bb87` fix(curtin-electrical): add missing tokens.css, fix broken path
- `54de7a8` fix(demos): self-host GSAP to fix animations in DuckDuckGo browser
- `f227329` fix: 3 audit bugs — duplicate ID, fetch error handling, focus trap
- `94f173b` feat: Lab samples open in overlay too
- `191933b` feat: full-screen demo preview overlay

## Pipeline

Build: design-hub `clients/[slug]/dist/` → copy to `demos/[slug]/` → commit → push main → GitHub Pages rebuilds ~30s.

Image pipeline: Tier 3 Pollinations `model=turbo` (free, 35s delays). JPEG magic-byte check `ffd8ff` required.

## Read on any infra session

`INFRA.md` in this repo — sole source of truth for Hetzner VPS, Coolify, Stripe, Porkbun DNS, CallMeIE routes.
