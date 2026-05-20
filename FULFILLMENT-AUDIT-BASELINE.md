---
id: callmeie-fulfillment-audit-baseline
title: CallMeIE Fulfillment Audit — Baseline
role: frozen-baseline
temporal_class: data
status: frozen
owner: claude-main
last_verified: 2026-05-20
verified_by: 4 opus agents (audit, ICM workspace design, inventory + merge map, site advertising) — synthesised into PDR-CLIENT-FULFILLMENT.md §2 + §6 (5 post-press-back edits applied 2026-05-20)
refresh_cadence: frozen — DO NOT EDIT IN PLACE. To update: write delta to FULFILLMENT-AUDIT-LOG.md, then overwrite this file with new dated baseline.
enforcement: skill `/audit-fulfillment-gap` reads this file to diff current state; rewriting it without log entry breaks delta-detection
built_from: PDR-CLIENT-FULFILLMENT.md §2 + §6 + claude-mem evidence cited inline
---

# Fulfillment Audit Baseline — 2026-05-20

Frozen snapshot of tier readiness + gap list for the `/audit-fulfillment-gap` skill to diff against. This is the comparator, not the live state. The PDR is the prose-narrative; this file is the machine-readable seed.

## Tier readiness (frozen 2026-05-20)

| Tier (PRICING-SSOT.md anchor) | Sell? | Deliver? | Repeatability | Evidence |
|---|---|---|---|---|
| Receptionist Starter / Professional | yes | semi-auto via `setup-new-client.py` + admin portal | 5 / 10 | INFRA.md §9.1, receptionist/CLAUDE.md |
| Receptionist Growth | yes | partial — inventory sync code EXISTS but flaky (Dockerfile / import bugs); no monthly optimisation call | 5 / 10 | claude-mem 10961-10963; `sync_inventory.py` + `/sync-inventory` endpoint |
| Doc Ops Pilots (€500 / €1500) | yes | yes, via portal | 7 / 10 | claude-mem 19620, 19619, 21833; magic-link onboarding chain |
| Doc Ops Auto subs (€99 / €249 / €499 / €1500) | yes | site says "email us first" — manual gate | 3 / 10 | claude-mem 18576; PRICING-SSOT D5 |
| Own-it-outright websites (€695 / €1595 / from €2950) | yes | `new-service-site` skill works; no Stripe → skill trigger | 3 / 10 | new-service-site SKILL.md; no webhook→skill wiring observed |
| **D5 Managed Websites (€69 / €100 / €149)** — launched 2026-05-19 | **yes** (Stripe links live) | **NO build pipeline, NO SLA timer, NO edit-budget meter, NO order form, NO cancel export** | **0 / 10** | PRICING-SSOT §6a; absent in all scripts |
| Local SEO (€245 / €495 + €99 audit) | mailto only — BLOCKS SALE | n/a — no Stripe product | n/a | claude-mem 21086 (Stripe product list shows only €99 audit, no €245/€495 SEO) |
| Care plans (€45 / €95 / €195 × 2) | not on site — BLOCKS SALE | manual via `/owl/care/ticket` | 2 / 10 | claude-mem 22223 ("preserve... for separate future review"); 17791 (`POST /owl/care/ticket` live) |

## Out-of-workspace gaps (frozen 2026-05-20)

| # | Gap | Owner | Effort |
|---|---|---|---|
| 1 | D5 Manual Delivery Runbook | SUPERSEDED — workspace 03b + 04 cover this | (closed 2026-05-20) |
| 2 | Local SEO Stripe products (mailto only) | Adam + `scripts/provision-stripe.py` | ~30min Adam-keyboard |
| 3 | Care plans on-site surfacing | Copy edit `callmeie-hub/` | ~30min |
| 4 | Edit-budget meter design | PDR-style spec needed | ~2h design |
| 5 | SLA timer design | Could combine with #4 | ~2h design |
| 6 | Cancellation-export script | Scope unknown | unknown |
| 7 | Receptionist Growth inventory sync HARDENING (code exists, fix import) | Engineer + per-customer scoping | ~1h fix + unknown per-vertical |
| 8 | Receptionist Growth monthly optimisation call | Add to handoff template + calendar | <30min |
| 9 | Order form solicitor-review | Adam + solicitor (Ltd pending) | external |
| 10 | Stripe meter-event reporting (€0.20-0.22/min live-posting unverified) | Engineer | ~1h |
| 11 | Onboarding form payment-honesty fix ("Continue to payment" button) | Copy edit `callmeie-hub/onboarding.html` | ~15min |

## Pricing canonical anchors

All numbers above derive from `PRICING-SSOT.md`. Any discrepancy = PRICING-SSOT wins; update this baseline.

D5 launched 2026-05-19 (PRICING-SSOT §8 + commit `e81a692` callmeie-hub). Audit performed 2026-05-20.

## Skill that consumes this file

`~/.claude/skills/audit-fulfillment-gap/SKILL.md` — produces delta-only report against this baseline.

## Update protocol

DO NOT edit in place. To refresh baseline:
1. Run `/audit-fulfillment-gap` first to capture deltas.
2. Append delta + reasons to `FULFILLMENT-AUDIT-LOG.md` (append-only history).
3. Overwrite this file with the new baseline.
4. Update `last_verified` date + `verified_by` field.

Update protocol mirrors `~/.claude/rules/common/work-diary.md` data-intent split — this is data (frozen baseline), not intent (NEXT-STEPS).
