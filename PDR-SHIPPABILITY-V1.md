---
id: pdr-shippability-v1
title: Customer Shippability v1 — Opensource Integration + Dashboards PDR
role: design-record
temporal_class: intent
status: accepted
owner: claude-main
created: 2026-05-20
composes_with: PDR-CLIENT-FULFILLMENT.md, FULFILLMENT-AUDIT-BASELINE.md, INFRA.md, PRICING-SSOT.md, CLIENT-PORTAL-PDR.md, icm-workspace-standard.md (60/30/10), operator-intelligence-contract.md
---

# Customer Shippability v1

Per-gap component map (Gaps #2–#11 from `FULFILLMENT-AUDIT-BASELINE.md`), customer + operator dashboard spec, MVP scope. Stack rule: REUSE Doc Ops portal stack (FastAPI + Jinja + HTMX + Coolify Postgres) — `CLIENT-PORTAL-PDR.md` already locked it. Tools already deployed per INFRA §2.2: Vaultwarden, Uptime Kuma, Umami. FreeScout is deferred to customer #4 (claude-mem 19590) — treat as not-running.

## 1. Per-gap component table

Best fit: (a) opensource + integrate · (b) custom dashboard surface · (c) both.

| # | Gap | Fit | Pick | License · Maturity · URL | 60/30/10 | Cost |
|---|---|---|---|---|---|---|
| 2 | Local SEO Stripe products (€245/€495/€99 mailto only) | b | Adam-keyboard via `scripts/provision-stripe.py` (CATALOGUE extend, idempotent — proven D5 precedent, PRICING-SSOT.md §7) | n/a | 100/0/0 | 30 min |
| 3 | Care plans on-site surfacing | b | Copy edit `callmeie-hub/websites/index.html` + render `care-plans-scope.md` at `/care/` | n/a | 100/0/0 | 30 min |
| 4 | Edit-budget meter (30 min/2 h/6 h promised across Managed + Care) | c | Postgres `edit_budget_ledger` table (custom, ~80 LOC) + **Kimai** UI for ops-side time entry (PHP/Laravel, AGPL-3.0, `kimai/kimai`, `locally_verified` candidate — operator-evidence pull required before promote; smoke-test gating in §5). Customer view = HTMX widget reading the ledger | 70/25/5 | 4–6 h |
| 5 | SLA timer (2-biz-day / 1-biz-day / same-day / 3-biz-day) | c | **REUSE** `docops-sla-check.sh` cron pattern (INFRA §14.4, LIVE — verified claude-mem 19668/19675) — extend `request_queue` table with `tier`, `sla_target_at`, `business_days_only` + add tier→SLA-hours lookup (net-new, ~30 LOC, since Doc Ops cron is single-threshold not tier-driven). **`workalendar`** Python (BSD-3, `peopledoc/workalendar`) — `candidate` per operator-intelligence-contract until `_dep_notes/workalendar.md` written + IE calendar smoke (~15 min). Customer countdown = HTMX poll widget | 75/20/5 | 3–4 h |
| 6 | Cancellation-export script (7-day promise across Managed) | b | Custom per-product Python (`scripts/export_tenant.py`): zip site source (Cloudflare Pages git), call recordings (Vapi API), Doc Ops corpus tarball, Stripe invoices CSV. **Trigger via Stripe Customer Portal** `customer.subscription.deleted` webhook (already wired) → enqueues export job → 7-day cron checks queue | 90/10/0 | 4–5 h |
| 7 | Receptionist Growth `sync_inventory.py` hardening (claude-mem 10961–10963 Dockerfile/import bugs) | b | Fix import path + Dockerfile in-place (no opensource swap). Per-vertical adapter pattern deferred to first Growth customer | n/a | 80/20/0 | 1 h fix |
| 8 | Receptionist Growth monthly optimisation call | b | Cal.com self-hosted (AGPL-3.0, `calcom/cal.com`) — `candidate` per operator-intelligence-contract (no prior local-verify decision in claude-mem; external-reference hits only at 1209/11968/20952/20954). Smoke-gate in §5 mandatory before integration. Add to 04-delivery handoff template; auto-book first call | n/a | 60/30/10 | 1 h |
| 9 | Order form solicitor review | n/a | External — Adam-blocking on solicitor (Ltd pending CRO; PRICING-SSOT §6a) | — | — | external |
| 10 | Stripe meter-event reporting verification (`vapi_minutes`) | b | Audit `setup-new-client.py` + receptionist server: confirm `stripe.billing.MeterEvent.create()` fires per Vapi call-end webhook. Add `usage_records.pushed_to_stripe` health check to operator dashboard | n/a | 100/0/0 | 1 h |
| 11 | Onboarding form payment-honesty fix | b | Copy edit `callmeie-hub/onboarding.html` (claude-mem 20437) | n/a | 100/0/0 | 15 min |

**Bonus — Local SEO audit engine** (for €99 audit product once Stripe wired in #2): **`maputo/google-business-profile-audit`** does not exist as a clean repo; recommend **manual SQL+rule-based scout via Playwright MCP** (already proven 2026-05-13 in `axis/` GBP claim flow) reading Google Maps public DOM + SerpAPI fallback. 60/30/10 = 60% deterministic scrape / 30% rule-based scoring rubric / 10% AI for write-up. Defer to first paying SEO audit customer (Gap #2 must close first).

## 2. Custom dashboard PDR

Stack (both surfaces): **FastAPI + Jinja2 + HTMX + Tailwind, Postgres on Coolify (UUID `jcgjvf0o55exgw69akj0uk5d`)**, magic-link auth, Stripe Customer Portal embed for billing self-serve. Single repo `client-portal/` extending `document-ops-portal/` precedent (INFRA §14). Authorization: tenant_id row-level filter (proven pattern, claude-mem 18166).

### 2.1 Customer-facing dashboard (`portal.callmeie.ie/me`)

| Widget | Source of truth | 60/30/10 | Effort |
|---|---|---|---|
| Active subscriptions + tier | Stripe API `customer.subscriptions.list` cached 5 min | 95/5/0 | 1 h |
| Edit-budget remaining (this month) | Postgres `edit_budget_ledger` SUM grouped by month | 100/0/0 | 1.5 h |
| In-flight request SLA countdown | Postgres `request_queue` filtered tenant_id, `workalendar` for biz-day delta | 80/20/0 | 1.5 h |
| Recent invoices (last 6) | Stripe API `invoices.list` | 100/0/0 | 1 h |
| "Need more edits?" upsell card | Rule: if budget_used > 80% AND tier != top → show CTA → Stripe upgrade link | 30/70/0 | 1 h |
| Support ticket history | FreeScout API (once deployed customer #4); until then `support@callmeie.ie` shared-inbox stub | 90/10/0 | 1 h (stub) |
| Cancel + export button | Stripe Customer Portal embed (built-in cancel) + custom `/export/request` POST | 100/0/0 | 1 h |

Total: ~8 h.

### 2.2 Operator-facing dashboard (`portal.callmeie.ie/owner` — extends existing `/owl/owner`)

| Widget | Source of truth | 60/30/10 | Effort |
|---|---|---|---|
| Client fleet table (slug · tier · status · MRR · joined) | Postgres `tenants` JOIN Stripe `subscriptions` | 100/0/0 | 1.5 h |
| Edit queue with SLA traffic-light | `request_queue` JOIN `tenants`, red <2h to breach, amber <1 biz-day, green >1 biz-day | 80/15/5 | 2 h |
| Anomaly alerts (Vapi-minute spike, edit-budget burn rate, payment failed) | Rule-based: 3 SD over 14-day baseline → row | 40/60/0 | 2 h |
| Billing reconciliation (Stripe MRR vs Postgres `usage_records`) | Diff `stripe.billing.MeterEvent` ingest vs `usage_records.pushed_to_stripe=true` | 100/0/0 | 1.5 h |
| System health (Uptime Kuma + Render + Cloudflare Pages) | Uptime Kuma API `/api/status-page/heartbeat` + GH Pages deploy status | 100/0/0 | 1 h |
| GBP audit queue (once Gap #2 closes) | Playwright Local SEO scout queue + score rubric | 60/30/10 | 3 h (post-#2) |
| Rejection/refund ledger (Anamnesis-style) | Postgres `anti_priorities` append-only | 100/0/0 | 1 h |
| `/lint-system` embed | Iframe to existing skill output JSON | 100/0/0 | 30 min |

Total: ~12 h (excluding post-#2 GBP).

## 3. MVP scope — prototype before batch

**Highest-value first prototype: Operator-facing "Edit queue with SLA traffic-light" (§2.2 row 2).**

Justification:
- Closes Gap #4 + Gap #5 (edit-budget + SLA) — the two highest-customer-risk D5 Managed gaps per `FULFILLMENT-AUDIT-BASELINE.md`.
- Reuses the `docops-sla-check.sh` cron + `request_queue` shape (already-proven pattern, INFRA §14.4).
- Single widget — narrow, testable, ships in one day. Drives `request_queue` table schema, which the customer-facing countdown then reuses for free (`PRICING-SSOT.md` §1 promises depend on it).
- After it ships, customer-facing SLA-countdown widget = ~1.5 h follow-on (same data source). Then Edit-budget meter widget (3 h) inherits the same ledger pattern.

Build order:
1. `request_queue` + `edit_budget_ledger` Postgres migrations (1 h)
2. Operator queue widget (2 h)
3. Cron SLA-check extension (1 h)
4. Customer SLA countdown (1.5 h)
5. Edit-budget ledger widget (customer + operator views, 3 h)

Ship in week 1. Batch the remaining 13 widgets only after first paying D5 customer presses back.

## 4. Out of scope — anti-priorities

1. **Refine.dev / Appsmith / Budibase / NocoBase / ToolJet** — rejected. Adam's stack precedent is FastAPI+Jinja+HTMX (claude-mem 18036, 18051, 18066, 18166, 21317, 21319 all confirm). Adopting a low-code platform breaks single-stack discipline and adds Node runtime to a Python house. Anamnesis-class rejection — see "Always consider donts" memory rule.
2. **New CRM (Twenty/EspoCRM/NocoBase)** — rejected. `tenants` table + Stripe customer object are already the CRM; an operator client-fleet widget covers the view need.
3. **Trigger.dev / Inngest / Temporal / Hatchet** for SLA scheduling — rejected. `docops-sla-check.sh` cron + Postgres polling is already-running production pattern (INFRA §14.4); adding a workflow engine for a 5-minute cron is over-architecture (60/30/10 violation — would push AI/orchestration share up for zero gain). Revisit if/when concurrent-job count exceeds 50/day.

## 5. Risks + blockers

**Smoke-test gates (before integrate — per operator-intelligence-contract.md):**
- **Kimai** — currently `candidate`. Required local checks: (1) `docker run kimai/kimai` boots on Coolify; (2) REST API auth via API token; (3) per-tenant project isolation works. ~1 h smoke. **Block on this before §1 Gap #4 integration.** If fails → fall back to pure-Postgres ledger (drop Kimai, custom UI on HTMX, +2 h).
- **Cal.com** — `candidate` (no prior decision in claude-mem; 19590 defers FreeScout, not Cal.com). Required: (1) Coolify one-click recipe (template exists per INFRA §9.3); (2) `cal.callmeie.ie` DNS via Porkbun; (3) webhook → handoff template. ~2 h smoke. Block on this before §1 Gap #8.
- **workalendar** — `production_ready` (PyPI mature, IE calendar shipped). No smoke needed.

**Infra dependencies (confirm against INFRA.md):**
- Postgres on Coolify is wired and live (INFRA §14.1, UUID `jcgjvf0o55exgw69akj0uk5d`) ✓
- Stripe Customer Portal embed: confirm webhook signing secret in `.env` (Adam-keyboard if missing)
- Cloudflare Pages git access for Gap #6 export: confirm CF API token scope includes Pages read

**Licensing:**
- Kimai AGPL-3.0 — fine for self-hosted; **do NOT bundle into client-distributed code** (Managed-website source IS retained, so this is moot — but flag for Doc Ops white-label scenarios)
- Cal.com AGPL-3.0 — same constraint
- workalendar BSD-3 — unrestricted

**Cost:** Zero new licence fees. Only marginal cost = Hetzner CPU/RAM for Kimai + Cal.com containers (AX52 has headroom per INFRA §1).

**Tier promotion gate (per operator-intelligence-contract.md):**
Both Kimai and Cal.com move from `candidate` → `locally_verified` only when their respective `required_local_checks` pass on Adam's machine and operator evidence (3+ GitHub issues / forum threads) is documented in `_dep_notes/{tool}.md`. No auto-route until then.

## 6. Composes-with

- `PDR-CLIENT-FULFILLMENT.md` §6 — gap source
- `FULFILLMENT-AUDIT-BASELINE.md` — frozen comparator
- `CLIENT-PORTAL-PDR.md` — locks FastAPI+Jinja+HTMX stack (do not re-litigate)
- `INFRA.md` §14 — Postgres + Coolify + docops-sla-check.sh pattern reuse
- `PRICING-SSOT.md` §1, §4, §6a — promise authority for every SLA/budget number
- `~/.claude/rules/common/icm-workspace-standard.md` — 60/30/10 composing default
- `~/.claude/rules/common/operator-intelligence-contract.md` — tier promotion gates

## 7. Approval gate

This PDR is design-only. Code starts on Adam press-back. First commit = §3 MVP step 1 (Postgres migrations).
