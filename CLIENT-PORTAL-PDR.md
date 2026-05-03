# PDR — Owl Studio / Document Ops Client Portal

Status: `phase-1-approved`
Date: 2026-05-01
Owner: Adam / Owl Studio + Document Ops
Replaces: Hubflo (NAMED-TOOLS-FLAG, sponsored ad SEQ-REV-003)
Source audit: Image Utility Audit 2026-04-30 → IMAGE-UTILITY-AUDIT-FINAL.md §94 destination row

## Decisions Confirmed (Adam press-back 2026-05-01)

1. **Phase 1 build approved** (~12-16 hrs)
2. **Storage**: Postgres on Coolify (single DB, tenant_id column)
3. **Magic-link mailer**: existing CallMeIE SMTP path (re-uses configured sender; no new Mailgun/Resend account)
4. **Deploy target**: Coolify on Hetzner (existing box, persistent volumes — Render `/tmp` wipe avoided)
5. **Tier pricing**: matches `document-ops/PRICING.md` research-anchored vertical matrix (Irish competitor pricing baseline applied 2026-05-01)
6. **Hubflo framing**: "Document Ops Console" client-facing — operational features replicated, no Hubflo SaaS adoption

## 1. Why a portal

Document Ops pilots succeed when:

1. Client uploads docs without emailing back-and-forth
2. Client sees what's in review queue (uncertainty surfaced, not hidden)
3. Client downloads clean export themselves
4. Adam's support burden does not scale linearly with client count

Without a portal, every pilot becomes a manual support job. With a portal each pilot is mostly self-serve, and a single Adam-touch resolves an entire week of one client's queue.

Hubflo (the audited reference) sells this exact stack as a SaaS at €40-90/seat/month per agency. We replace it with a thin FastAPI+SQLite layer that reuses Adam's existing CallMeIE Render service + Stripe + Coolify rails. Zero new infra cost, full data ownership.

## 2. Target users

### Adam (operator)

- Sees all client tenants in a single admin view
- Triggers extraction runs per client
- Resolves review queue items (single-keystroke approve/reject)
- Sees billing state per client
- Suppresses or off-boards a client cleanly

### Document Ops pilot client

- One firm = one tenant
- 1-3 staff seats max in v1 (no team admin complexity)
- Tasks: upload docs, see queue, approve/correct fields, download clean export, see billing/invoice

## 3. Reference: SEQ-REV-003 Hubflo modules

Captured from Hubflo's own product demo carousel. Replicating the **operational** features, not the SaaS branding. Mapped to Adam's Document Ops pipeline:

| Hubflo module | Adam's equivalent (Document Ops) | v1 priority |
|---|---|---:|
| Home / dashboard | Per-client overview: docs in queue / clean ready / month-to-date | P0 |
| Files | Document upload + per-document status + original viewer | P0 |
| Messaging | Skip — email is fine in v1; revisit if churn signal | — |
| Intake forms | Onboarding form: firm name, document type, schema preferences | P0 |
| Contracts | Stripe-attached subscription terms; client signs at signup | P0 |
| Resource center | Skip — public docs link is enough | — |
| Billing | Stripe Customer Portal embed for invoices + payment method | P0 |
| Action-required panel | Review queue: rows needing client approval/correction | P0 |
| Service contract review | Skip — Stripe Checkout Session covers it | — |
| Proposal review | Skip — no quote-stage flow in v1 | — |
| File repository categories | Tag uploads as: `original`, `extracted`, `clean-export`, `report` | P1 |
| Tasks / progress tracker | Document-status states + visible monthly progress chart | P1 |

P0 = MVP. P1 = post-first-paying-client. Modules marked "Skip" stay deferred until a client asks.

## 4. MVP scope

### In scope

- Multi-tenant data isolation (per-client SQLite or Postgres schema)
- Magic-link email auth (no passwords; lowest support burden)
- Per-client dashboard
- Document upload (drag-drop multiple PDFs/images at once)
- OCR/extraction pipeline trigger (existing Document Ops scripts)
- Review queue UI: row-by-row approve / correct / reject
- Clean export download (CSV; per-client filtered)
- Run report download (Markdown)
- Stripe Customer Portal embed (Adam's existing 7 Payment Links + webhook)
- Admin view for Adam: all tenants, all queues, all billing states
- Audit log per row (who approved, when)

### Out of scope (defer until paying)

- Real-time messaging
- Multi-seat per tenant beyond 3 users
- Mobile app
- Direct accounting-software writeback (QuickBooks / Xero / Sage / CargoWise)
- White-label per-client subdomains
- Advanced reporting / charts beyond month-to-date counts
- Automated email notifications beyond magic-link + receipt
- Document-level permissions (everyone in a tenant sees everything)

## 5. Non-goals

- Not a Hubflo competitor
- Not a CRM
- Not a file-share/collaboration platform
- Not a task manager beyond document-status
- Not building any feature without a client asking for it

## 6. Architecture

### 6.1 Reuse, don't rebuild

| Layer | Reuses |
|---|---|
| HTTP framework | CallMeIE FastAPI (Render service); add `/portal/*` route namespace |
| DB | SQLite (file-per-tenant) OR Postgres on Coolify (single DB, tenant_id column) |
| File storage | Local Render disk (free, ephemeral — see §6.4 risk) OR Cloudflare R2 |
| Auth | Magic link via Mailgun / Resend (Adam's existing setup) |
| Billing | Stripe Customer Portal (existing live-mode account, 7 Payment Links) |
| Static UI | Plain HTMX or htmx-server-rendered Jinja templates (no React build) |
| OCR/extraction | Existing `document-ops/scripts/*` invoked as subprocess from FastAPI |
| Deploy | Render redeploy (existing pipeline) OR Coolify (existing Hetzner box) |

### 6.2 Recommended deploy target — Coolify on Hetzner

CallMeIE lives on Render but `/tmp` wipes on restart (per INFRA.md known workaround). Document Ops needs persistent file storage. Coolify on Hetzner has persistent volumes — better fit. Run the portal as new Coolify service alongside owltradezone, vaultwarden, etc.

### 6.3 Data model (Postgres or SQLite)

```text
tenants(
  id, slug, firm_name, niche, primary_contact_name, primary_contact_email,
  stripe_customer_id, plan, status, created_at, suppressed
)

users(
  id, tenant_id, email, role, created_at, last_login_at
)

magic_links(
  id, user_id, token_hash, expires_at, used_at
)

documents(
  id, tenant_id, source_filename, source_hash, storage_path,
  mime_type, status, uploaded_by_user_id, uploaded_at
)
-- status: uploaded -> processing -> review -> approved -> exported -> archived

extractions(
  id, document_id, tenant_id, schema_id,
  ocr_engine, ocr_confidence, ocr_status,
  fields_json, run_at
)

review_items(
  id, extraction_id, tenant_id, field_name, current_value,
  confidence_status, validation_message,
  reviewed_value, reviewed_by_user_id, reviewed_at, status
)
-- status: needs_review -> approved -> rejected

exports(
  id, tenant_id, format, row_count, generated_at, download_url, generated_by_user_id
)

audit_log(
  id, tenant_id, user_id, action, target_type, target_id, payload_json, at
)
```

Per-tenant data isolation: every row carries `tenant_id`. Every query filters by tenant. Adam's admin view bypasses the filter.

### 6.4 Risks + mitigations

| Risk | Mitigation |
|---|---|
| Multi-tenant data leak | All queries filter by `tenant_id`. Code review checklist before merging any portal change. Integration test: tenant A cannot read tenant B docs. |
| Render `/tmp` wipe | Deploy to Coolify with persistent volume, not Render. Tested precedent in INFRA.md §11. |
| Magic-link token leak via shared inbox | Tokens single-use + expire 15 min. Log all uses in audit_log. |
| Stripe webhook misroutes between tenants | Webhook reads `customer_id` → looks up `tenant_id`. Same pattern as existing CallMeIE billing. |
| OCR cost runaway | Per-tenant monthly doc cap (default 200, configurable). Cap blocks new uploads when reached. Surfaces upgrade prompt. |
| File-storage cost | Originals compressed + retained 90 days then archived to cold storage. Configurable per tenant. |
| GDPR data subject request | `tenants/<id>/export-all` admin endpoint. Audit log shows access. |

## 7. User flows

### 7.1 New pilot client onboarding

1. Adam → Stripe Payment Link (existing 7 Payment Links — Document Ops Pilot SKU added to set)
2. Stripe webhook → portal creates `tenants` + `users` row → sends magic-link email
3. Client clicks magic link → lands on dashboard (empty state with "Upload your first document" CTA)
4. Client uploads first 25 docs (Entry Pilot tier)
5. Adam triggers extraction (CLI or admin button)
6. Pipeline runs: ocr_file_to_artifact → prepare_ocr_artifacts → process_text_fixtures → apply_export_gate
7. Review queue populates → email notification to client (one digest, not per-doc)
8. Client logs in via magic link, approves/corrects fields
9. Clean export becomes downloadable
10. Pilot findings call → upgrade to monthly

### 7.2 Monthly recurring run

1. Client uploads docs throughout month (any time, no cron)
2. Adam (or scheduled job) triggers weekly batch extraction
3. Review queue digest emailed once weekly
4. Client logs in, resolves queue
5. Month-end clean export auto-generated + emailed
6. Stripe charges per existing subscription
7. Reports archived; originals retained per retention policy

### 7.3 Off-boarding

1. Client cancels via Stripe Customer Portal
2. Webhook → portal sets `tenants.suppressed = true`
3. Adam runs `tenants/<id>/export-all` → ZIP of all client data
4. Client downloads ZIP within 30 days
5. After 30 days, hard delete (audit-logged)

## 8. UI surfaces (v1 scope)

Plain HTMX + Jinja templates. No SPA. No build step. Same engineering taste as the existing Owl Studio static gallery.

Pages:

- `/portal/login` — email entry → magic-link send
- `/portal/auth/callback?token=...` — magic-link verify
- `/portal/<tenant_slug>/` — dashboard (counts: queue / approved / exported)
- `/portal/<tenant_slug>/upload` — drag-drop multi-file
- `/portal/<tenant_slug>/queue` — row-by-row review with inline edit
- `/portal/<tenant_slug>/exports` — list of clean-export CSVs + download
- `/portal/<tenant_slug>/billing` — Stripe Customer Portal embed
- `/portal/<tenant_slug>/account` — basic settings (firm name, primary contact)
- `/admin/tenants` — Adam-only: all tenants, all states
- `/admin/tenants/<id>` — Adam-only: drill into one tenant's data + run controls

Tone: same plain-direct visual language as `websites.owlzone.trade`. No purple gradients. No Inter font. No glassmorphism. Owl Studio brand consistency.

## 9. Pricing wiring

Three Document Ops tiers from `document-ops/PRICING.md` map to three new Stripe Payment Links:

| Tier | Stripe link | Document cap | Includes |
|---|---|---:|---|
| Entry Pilot | `dops_pilot_entry` | 25 docs one-time | One workflow, CSV export |
| Standard Pilot | `dops_pilot_standard` | 100 docs one-time | One workflow, schema + report |
| Operations Monthly | `dops_ops_monthly` | 600 docs/month | Repeated weekly processing, queue, reporting |

Wiring matches existing CallMeIE pattern in INFRA.md §5: Stripe Payment Link → success URL → portal account creation.

## 10. Build phases

### Phase 1 — Skeleton (one weekend, ~12-16 hrs)

- Coolify deploy of new FastAPI service
- Postgres schema migration
- Magic-link auth working end-to-end
- Tenant isolation tests pass
- Stripe webhook → tenant creation
- Bare dashboard page

### Phase 2 — Document flow (one weekend)

- Upload endpoint + storage
- Pipeline trigger (admin button)
- Review queue page with inline edit
- Clean export download

### Phase 3 — Billing + ops

- Stripe Customer Portal embed
- Admin view for all tenants
- Audit log + GDPR export endpoint

### Phase 4 — Polish (after first paying client signs)

- Email digests (queue ready, export ready)
- Per-tenant doc caps + upgrade prompts
- Run reports formatted for client-facing

## 11. Success metrics

### Build metrics

- One paying client onboarded end-to-end via portal within 14 days of Phase 3
- Portal absorbs all support touches except review queue resolution
- Adam's per-client weekly time drops from ~45 min (manual email back-and-forth) to ~10 min (admin queue glance)

### Revenue metrics

- 3 paying clients within 60 days of portal launch
- Portal lifts pilot → monthly conversion from ~30% to ~50% (operator evidence: self-serve queue increases trust + reduces "did you do this yet?" loop)
- Average MRR per paying client €600-€1,200/month

## 12. Decision required

Adam press-back items:

- Approve Phase 1 build (~12-16 hrs)
- Choose storage: Postgres on Coolify (recommended) vs SQLite-per-tenant
- Choose magic-link sender: Mailgun / Resend / existing CallMeIE SMTP path
- Confirm tier pricing matches `document-ops/PRICING.md`
- Confirm Hubflo replacement is the right framing (alternative: positioned as "Document Ops Console" with no comp)

## 13. Anti-scope (do not build)

- Real-time chat
- Tasks/projects beyond document-status
- Per-tenant subdomain SSL automation
- Visual editor for any document
- AI-suggested corrections in review queue (defer until pilot data shows where it helps)
- Mobile native app
- White-label theming
- Internal workflow builder

## 14. Cross-references

- `document-ops/PRD-DOCUMENT-OPS-REVENUE-ENGINE.md` — pipeline this portal exposes
- `document-ops/PRICING.md` — tier definitions Stripe links must match
- `INFRA.md` — Hetzner / Coolify / Render / Stripe / Porkbun reference
- `INFRA.md §11` — Render `/tmp` wipe workaround (informs Coolify choice)
- `Image Intelligence Ledger/REVENUE-SEQUENCE-VISUAL-REVIEW.md` §SEQ-REV-003 — Hubflo evidence source
- `Image Intelligence Ledger/IMAGE-UTILITY-AUDIT-FINAL.md` §94 — staged destination

## 15. Provenance

This PRD is the press-back-approved version of the audit-staged destination row 7 in `IMAGE-UTILITY-AUDIT-FINAL.md` §94. Audit recommendation: "Build thin FastAPI+Stripe portal instead of adopting Hubflo." This document operationalizes that recommendation.
