# PDR · Client Fulfillment (Owl Studio / CallMeIE)

> PDR for the `client-fulfillment` ICM workspace: customer-fulfillment
> audit verdict, decision record, out-of-workspace gaps with owners,
> and merge map for existing artifacts. Composes with `PRICING-SSOT.md`,
> `INFRA.md`, and `~/.claude/rules/common/icm-workspace-standard.md`.
> Status: `accepted` — Adam pressed back 2026-05-20: "scope is good, PRD is good". 5 edits applied post-press-back (2 fact-check + 3 press-back-agent corrections). Push: `a26f86e` on origin/main.

---

## 1. Goals & non-goals

**Goals**
- Capture the 2026-05-20 customer-fulfillment audit verdict before it goes stale
- Justify the single-workspace decision and freeze its scope-fence
- Enumerate out-of-workspace gaps (with owner + effort) that the workspace alone cannot close
- Hand the merge agent a clean map of what to absorb vs link vs archive vs reconcile

**Non-goals**
- This is not the workspace implementation. The workspace lives at `jake-van-clief-icm/workspaces/client-fulfillment/` (built 2026-05-20 by a sibling opus agent — see `client-fulfillment/BUILD-REPORT-2026-05-20.md` for the build receipt).
- This is not the audit itself. The audit was performed by four opus agents on 2026-05-20; this PDR is the synthesis of their findings into a single decision record.
- This is not the live operational state. That lives in `RUNNING-CONTEXT.md` (per-project) and `NEW-REPOS-RUNNING-CONTEXT.md` (parent).
- This is not the forward queue. Gaps in §6 become entries in `NEW-REPOS-NEXT-STEPS.md`.
- Billing reconciliation, lead generation, and ongoing monthly-maintenance are explicitly upstream / downstream of the workspace, not in scope here.

---

## 2. Audit verdict — 2026-05-20 (frozen)

Stripe path: live across all tiers (see `PRICING-SSOT.md` §7).
Fulfillment path: a spectrum from 0/10 (D5 Managed Websites — sold 2026-05-19, no build pipeline) to 7/10 (Doc Ops Pilots via portal).

| Tier (price authority `PRICING-SSOT.md`) | Sell? | Deliver? | Repeatability |
|---|---|---|---|
| Receptionist Starter / Professional | yes | semi-auto via `setup-new-client.py` + admin portal | 5 / 10 |
| Receptionist Growth | yes | inventory sync VERIFIED OPERATIONAL 2026-05-21 (Dockerfile `COPY *.py .` fix landed cm 10964; `/sync-inventory` returns 200 on real Dunne IDs); 30-min monthly optimisation call cadence now in handoff template (manual until Cal.com integration) | 8 / 10 |
| Doc Ops Pilots (€500 / €1,500) | yes | yes, via portal | 7 / 10 |
| Doc Ops Auto subs (€99 / €249 / €499 / €1,500) | yes | site says "email us first" — manual gate | 3 / 10 |
| Own-it-outright websites (€695 / €1,595 / from €2,950) | yes | `new-service-site` skill works; no Stripe → skill trigger | 3 / 10 |
| **D5 Managed Websites (€69 / €100 / €149, launched 2026-05-19)** | **yes** | **NO build pipeline, NO SLA timer, NO edit-budget meter, NO order form, NO cancel export** | **0 / 10** |
| Local SEO (€245 / €495 + €99 audit) | mailto only — BLOCKS SALE | n/a | n/a |
| Care plans (€45 / €95 / €195 × 2) | not on site — BLOCKS SALE | manual via `/owl/care/ticket` | 2 / 10 |

Per-tier evidence sources: `PRICING-SSOT.md`, `INFRA.md §9`, `scripts/setup-new-client.py`, `callmeie-hub/websites/managed-plans-scope.md`, `callmeie-hub/receptionist/CLAUDE.md`.

---

## 3. Decision record

Decisions are captured here as decisions, not as open questions. A sibling agent (workspace builder) has already chosen these in-session; this PDR freezes them for posterity.

| # | Decision | Rationale | Alternatives rejected |
|---|---|---|---|
| D1 | **One workspace `client-fulfillment/`**, not two | Pattern 5 — single canonical home for the customer record. Receptionist + website branches share intake / research / delivery / writeback; branch only at stage 03. | Two parallel workspaces (`receptionist-fulfillment` + `website-fulfillment`) — rejected: duplicates intake + research + writeback, splits the customer record. |
| D2 | **5 stages:** `01-intake` / `02-research` / `03a-receptionist-build` / `03b-website-build` / `04-delivery` / `05-writeback` | Linear shared spine, single fork at build-time, single merge at delivery. | 7-stage flat sequence — rejected: forces website-only customers through receptionist-shaped stages. |
| D3 | **Aggregate ratio ≈ 65 / 25 / 10** (deterministic / rule-based / AI) | Inside the 60 / 30 / 10 ICM composing default (`icm-workspace-standard.md`). Per-stage ratios in workspace L2 CONTEXTs, not restated here. | Higher-AI mix — rejected: 100%-AI is the anti-pattern the standard names. |
| D4 | **Bundle `new-service-site` skill** into the workspace | Pattern 9 — workspace self-containment for paid-customer builds. Global `~/.claude/skills/new-service-site/` becomes a pointer to the bundled copy; bundled copy authoritative. | Reference global skill only — rejected: global drifts; paid work cannot tolerate skill-version skew between sessions. |
| D5 | **8 critical Pattern-14 reference docs (real content extracted from canonical sources) — written BEFORE first customer; 18 total reference files across stages once auxiliary schemas / pointers / scaffolds are counted** | Docs-over-outputs (Pattern 14). Early customer outputs are the worst outputs; agents must learn from docs, not from prior `output/`. | Learn from samples — rejected: violates Pattern 14. |
| D6 | **Setup-once questionnaire of 12 questions** | Pattern 8 — configure the factory once. Most fields default from `SYSTEM-SOUL`, `PRICING-SSOT.md`, `INFRA.md`. Three are genuinely Adam-only: tier → SLA confirmation, default voice-clone selection, writeback-target blocking list. | Per-customer questionnaire — rejected: configures the product, not the factory. |
| D7 | **Build via `jake-van-clief-icm/workspaces/workspace-builder/`** | `icm-workspace-standard.md` mandate — new repeatable, sequential, human-reviewed workflows are built with the cloned `workspace-builder`, never hand-assembled. | Hand-assemble from `_core/templates/` — rejected: bypasses the convention enforcement the builder bakes in. |

---

## 4. Scope fence

In scope of the workspace (what the workspace produces):
- Customer intake from sale signal (Stripe webhook or manual trigger)
- Per-customer research (vertical context, scope confirmation, brand pull)
- Branch-specific build (receptionist provisioning OR site generation)
- Delivery (handover artefacts, vault, admin URL)
- Writeback (customer record, INFRA registry entry, Anamnesis decision, RUNNING-CONTEXT.md append)

Out of scope of the workspace (handled by surrounding system, not by this PDR either — listed here for the scope fence):
- Lead generation (upstream of intake)
- Billing reconciliation (Stripe + `setup-new-client.py` already cover it)
- Ongoing monthly care (separate cadence; care plans surface via `/owl/care/ticket`)
- Cross-customer fleet operations (owner dashboard at `/owl/owner`)

---

## 5. Composes-with (link only, do not restate)

| Source | Role |
|---|---|
| `PRICING-SSOT.md` | Single source for every tier number quoted above |
| `INFRA.md` | Single source for Hetzner / Coolify / Render / Stripe / Porkbun / vault |
| `DEPLOYMENT-PLAYBOOK.md` | Existing onboarding spine — merges in as the workspace 03a + 04 process backbone |
| `~/.claude/rules/common/icm-workspace-standard.md` | Workspace standard global rule |
| `jake-van-clief-icm/_core/CONVENTIONS.md` | 15 conventions the workspace MUST follow |
| `~/.claude/skills/new-service-site/SKILL.md` | Bundled into workspace (D4) |
| `callmeie-video-pipeline/` | Sibling ICM workspace; link from workspace L3 if video deliverable is requested |
| `jake-van-clief-icm/workspaces/client-fulfillment/CLAUDE.md` | Workspace L0 (once written by the sibling builder agent) |

---

## 6. Out-of-workspace gaps

The workspace alone does not close every fulfillment gap. Each gap below has an owner and a rough effort. Each becomes an entry in `NEW-REPOS-NEXT-STEPS.md`. Priority order = highest customer risk first.

| # | Gap | Why not in workspace | Owner | Effort |
|---|---|---|---|---|
| 1 | **D5 Manual Delivery Runbook** (HIGHEST RISK — sold 2026-05-19, no automation tomorrow) | Workspace 03b is days away; first managed customer may arrive sooner | Write as `owl-studio-website-directions/D5-MANUAL-DELIVERY-RUNBOOK.md` — Adam-facing checklist receipt → site live | ~1h |
| 2 | **Local SEO Stripe products** (€245 / €495 / €99 — currently mailto-only, blocks sale) | Stripe provisioning is `setup-new-client.py` job, not a fulfillment-workspace job | Adam at Stripe dashboard + `scripts/provision-stripe.py` | ~30min Adam-keyboard |
| 3 | **Care plans on-site surfacing** (6 Stripe links exist, not advertised) | Marketing-site copy edit, not a fulfillment-workspace job | Copy edit `callmeie-hub/websites/index.html` or `callmeie-hub/care/index.html` | ~30min |
| 4 | **Edit-budget meter design** (0.5h / 2h / 6h-90d cap promised across Managed + Care; no counter) | Cross-cutting product-feature design needed before code; not a per-customer artefact | PDR-style spec | ~2h design |
| 5 | **SLA timer design** (2-biz-day / 1-biz-day / same-day / 3-biz-day across Managed + Care + Rescue Doc Ops; no timer) | Same as #4 — cross-cutting, design-first | Could be combined doc with #4 | ~2h design |
| 6 | **Cancellation-export script** (7-day export promised across all Managed tiers; no automation) | Scope unknown — design needed before code | Design + scope | unknown |
| 7 | **Receptionist Growth inventory-catalogue sync — VERIFIED 2026-05-21** (`sync_inventory.py` + `/sync-inventory` endpoint live + 200-OK on real IDs; Dockerfile `COPY *.py .` fix landed cm 10964 ~7-8mo ago. Only outstanding work = per-vertical adapter pattern, gated on first paying Growth-tier customer) | Per-customer scoping at intake — no code-fix needed today | per-customer scoping at intake | unknown per-vertical |
| 8 | **Receptionist Growth monthly optimisation call** (promised, no booking cadence) | Calendar + handoff template — simple, but not the workspace's job | Add to handoff template + calendar template | <30min |
| 9 | **Order-form solicitor-review** (Managed-website min-term enforcement) | Adam-keyboard, blocking on solicitor — pre-revenue / Ltd pending | Adam | external |
| 10 | **Stripe meter-event reporting** for receptionist overage (€0.20-0.22 / min promised; live-posting unverified) | Code audit + test in `setup-new-client.py` + receptionist server | Engineer | ~1h |
| 11 | **Onboarding form payment-honesty fix** ("Continue to payment" button promises a collection that never happens — claude-mem 20437) | Copy / UX correction, not a workspace job | Copy edit on `callmeie-hub/onboarding.html` | ~15min |

---

## 7. Merge map (compressed from inventory agent)

### 7.1 Merge IN as workspace spine

| Source | Why |
|---|---|
| `DEPLOYMENT-PLAYBOOK.md` | Existing onboarding spine (needs D5 update) |
| `on-call-kit/*` | Pre-sale stage of the workspace |
| `BUSINESS-PROFILE-SCHEMA.md` | Becomes `brief.json` contract |
| `RESEARCH-VIDEO-STACK.md` + `RESEARCH-WEB-MOTION-STACK.md` | Consolidate into `opensource-tools-ledger.md` |

### 7.2 KEEP as-is, link from workspace L3 (canonical SSoTs)

| Source | Role |
|---|---|
| `PRICING-SSOT.md` | Canonical pricing — link only |
| `INFRA.md` | Canonical infra — link only |
| `~/.claude/skills/new-service-site/` + `/token-author/` + `/site-qa/` + `/style-match-call/` + `/website-clone/` | Skill set referenced by stage 03b |
| `design-hub/` (`INSTALLED-TOOLS.md` + `foundation/` + `section-pattern-library/` + `WEB-DESIGN-INTELLIGENCE.md`) | Design reference; consumed at build time |
| `ADAM-STRIPE-DEPLOY-2026-05-11.md` + `ADAM-P0-RINGTEST-CHECKLIST-2026-05-11.md` + `ADAM-GH-SECRETS-RUNBOOK-2026-05-11.md` | Provisioning runbooks |
| `PDR-BACKEND.md` + `PDR-AI-CHATBOT.md` + `PDR-UNIQUE-CHROME.md` | Architecture references |
| `callmeie-video-pipeline/` | Sibling ICM workspace |

### 7.3 ARCHIVE or supersede

| Source | Reason |
|---|---|
| `samples/industries/*` | Pattern 14 violation — ball-of-clay templates that future agents would learn patterns from |
| `scripts/render-site.py` + `rewire-gallery` scripts | Superseded by Astro + `new-service-site` skill |
| `PDR-INDUSTRY-DENTAL-SWISS.md` | Pattern absorbed into `new-service-site`; keep as historical example, not as live template |

### 7.4 Conflicts to resolve at merge

1. Pricing in 3+ places — only `PRICING-SSOT.md` canonical; others link
2. Dual `INFRA.md` — owl-studio authority, `callmeie-fix/INFRA.md` mirror; mirror rule already documented in INFRA.md
3. Three CMS candidates — Decap canonical for Pro tier, Sanity interim, Payload future (per `PDR-BACKEND.md §15`)
4. Hosting model conflict — client-owned Cloudflare Pages (own-it-outright tier) vs Owl-hosted source-retained (Managed tier)
5. Receptionist vs chatbot mixing in marketing copy — chatbot is a website add-on (`PDR-AI-CHATBOT.md`), not the receptionist
6. Onboarding form trim — `INFRA.md §10` backlog "trim onboard.html to 6 fields"
7. `scripts/render-site.py` vs `new-service-site` skill — skill wins

---

## 8. Approval gate

This PDR is the synthesis of the audit + the decision-record + the gap inventory. Code starts only after Adam press-back.

Once approved:
1. Sibling agent finishes building the workspace at `jake-van-clief-icm/workspaces/client-fulfillment/`
2. The 10 §6 gaps land in `NEW-REPOS-NEXT-STEPS.md` in priority order
3. Status promotes from `draft` to `accepted`; changelog records the move

---

## 9. Change log

- 2026-05-20 — PDR written. Synthesis of four opus audit agents (Stripe-readiness sweep, fulfillment-pipeline audit, merge-inventory pass, gap-owner identification). Status `draft` pending Adam press-back.
