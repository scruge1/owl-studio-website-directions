# CLIENT-PORTAL — Phase 1 Build Spec

Status: `ready-to-execute`
Date: 2026-05-01
PRD: `CLIENT-PORTAL-PDR.md` (decisions confirmed)
Scope: Skeleton — single tenant signs up via Stripe → magic-link login → empty dashboard
Time estimate: 12-16 hrs
Acceptance: First paying client onboarded end-to-end via portal flow (no manual intervention)

## Architecture decisions (locked)

| Layer | Decision | Why |
|---|---|---|
| Repo | New repo `document-ops-portal` (sibling to `callmeie-fix`) | Clean separation; Document Ops is a separate product line from CallMeIE receptionist; both deploy to Coolify independently |
| Framework | FastAPI + Jinja templates + HTMX | Same engineering taste as CallMeIE; no SPA build step; HTMX gives partial-page updates without React |
| DB | Postgres on Coolify (single DB, `tenant_id` column) | Audit-recommended over SQLite-per-tenant; persistent volume avoids Render `/tmp` wipe |
| Auth | Magic link via existing CallMeIE SMTP | No new mailer account; reuse callmeie@proton.me sender |
| Billing | Stripe Customer Portal embed + 3 new Payment Links | Reuse existing Stripe live account; webhook reuses CallMeIE pattern |
| File storage | Coolify persistent volume (`/data/uploads/<tenant_id>/<doc_id>`) | Free; matches doc-ops single-tenant scale; can migrate to R2 later |
| Deploy | Coolify on Hetzner box (existing) | Persistent volumes; alongside owltradezone, vaultwarden |
| Domain | **`portal.owlzone.trade`** (locked) | Sub of existing zone in Porkbun; matches client-portal framing |
| Stripe mode | **live** (locked) — Adam first paying client | Real receipt + flow validation; test mode added Phase 1.5 |
| Repo visibility | **private** (locked) — `github.com/scruge1/document-ops-portal` | Public review only after first paying client + auditable PR |
| Front-end taste | Plain Owl Studio brand (no purple gradients, no Inter font) | Match `websites.owlzone.trade` + `callmeie.ie` look |

## Repo structure

```text
document-ops-portal/
  README.md
  pyproject.toml                  (FastAPI, sqlmodel, jinja2, htmx, stripe, python-jose)
  app/
    __init__.py
    main.py                       (FastAPI app, route mounts)
    config.py                     (env vars, no hardcoded secrets)
    db.py                         (Postgres connection, sqlmodel session)
    models.py                     (tenants, users, magic_links, documents, ...)
    auth/
      __init__.py
      magic_link.py               (token generation, verify, send via SMTP)
      middleware.py               (require_tenant_user dependency)
      smtp.py                     (CallMeIE SMTP wrapper)
    routes/
      __init__.py
      public.py                   (/portal/login, /portal/auth/callback)
      tenant.py                   (/portal/<slug>/...)
      admin.py                    (/admin/tenants, /admin/tenants/<id>)
      stripe_webhook.py           (/webhooks/stripe)
    templates/
      base.html
      login.html
      magic_link_sent.html
      dashboard.html
      admin_tenants.html
    static/
      portal.css                  (Owl Studio brand, no purple gradients)
      htmx.min.js
  alembic/                         (Postgres migrations)
    versions/
      0001_init.py
  tests/
    test_tenant_isolation.py      (load-bearing; must pass)
    test_magic_link.py
    test_stripe_webhook.py
  Dockerfile                      (Coolify build target)
  .env.example                    (DATABASE_URL, SMTP_*, STRIPE_*, BASE_URL)
```

## Database schema (initial migration)

```sql
-- 0001_init.py — Postgres
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug TEXT UNIQUE NOT NULL,
    firm_name TEXT NOT NULL,
    niche TEXT,
    primary_contact_email TEXT NOT NULL,
    stripe_customer_id TEXT UNIQUE,
    plan TEXT NOT NULL DEFAULT 'pilot_entry',
    status TEXT NOT NULL DEFAULT 'active',
    suppressed BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ON tenants(slug);
CREATE INDEX ON tenants(stripe_customer_id);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'member',           -- member | admin | adam_super
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_login_at TIMESTAMPTZ
);
CREATE UNIQUE INDEX ON users(tenant_id, lower(email));
CREATE INDEX ON users(email);

CREATE TABLE magic_links (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash TEXT NOT NULL,                       -- sha256 of token
    expires_at TIMESTAMPTZ NOT NULL,                -- 15 min from creation
    used_at TIMESTAMPTZ
);
CREATE INDEX ON magic_links(token_hash);

CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id) ON DELETE SET NULL,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action TEXT NOT NULL,
    target_type TEXT,
    target_id TEXT,
    payload_json JSONB,
    at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ON audit_log(tenant_id, at DESC);

-- documents / extractions / review_items / exports tables added in Phase 2
```

## Phase 1 user journey (must work end-to-end)

1. Adam buys Stripe Payment Link `dops_pilot_entry` (test-mode in dev)
2. Stripe webhook `checkout.session.completed` → creates `tenants` row + first `users` row → sends magic link
3. Client clicks magic link → `/portal/auth/callback?token=...` → verifies + redirects to `/portal/<slug>/`
4. Client lands on dashboard showing: firm name, plan, "Document upload coming in next phase" placeholder
5. Adam logs into `/admin/tenants` (separate magic link with role=adam_super) → sees the new tenant

**Phase 1 is done when steps 1-5 complete without manual DB intervention.**

## Acceptance criteria

- [ ] Repo bootstrapped with FastAPI skeleton + alembic migration
- [ ] Coolify service running at `https://portal.owlzone.trade` (or chosen subdomain)
- [ ] Postgres provisioned on Coolify with initial schema applied
- [ ] Magic-link email sends via CallMeIE SMTP (verified in Adam's inbox)
- [ ] Stripe webhook signature verified + creates tenant on `checkout.session.completed`
- [ ] `/portal/<slug>/` requires valid magic-link session; bare access returns 401
- [ ] **Tenant isolation test passes**: a user authenticated as Tenant A cannot read Tenant B's data via URL probing or session-token swap
- [ ] `/admin/tenants` requires `role='adam_super'` cookie; lists all tenants
- [ ] Audit log writes one row per: tenant created, user created, magic link sent, magic link used, admin login
- [ ] HTTPS enforced (Coolify auto-Let's-Encrypt)
- [ ] First test client (Adam's own email) flow completes end-to-end

## Stripe wiring

3 new Payment Links to create in live mode (in addition to existing 7 CallMeIE links):

| SKU | Price | Mode | Redirects to |
|---|---:|---|---|
| `dops_pilot_entry` | EUR 500 one-time | one-time | `https://portal.owlzone.trade/onboarding?session_id={CHECKOUT_SESSION_ID}` |
| `dops_pilot_standard` | EUR 1,500 one-time | one-time | same |
| `dops_ops_monthly_starter` | EUR 150-300/mo subscription | recurring | same |

Webhook endpoint: `POST /webhooks/stripe` — verifies signature, switches on event type:
- `checkout.session.completed` → create or update tenant + send magic link
- `customer.subscription.created` → set tenant.plan + tenant.status
- `customer.subscription.deleted` → set tenant.status = 'cancelled' (suppress)
- `invoice.payment_failed` → audit log + email Adam

## Magic-link mechanism

- Token = 32 bytes urlsafe random
- Store sha256(token) in `magic_links.token_hash`
- Email contains `https://portal.owlzone.trade/portal/auth/callback?token=<raw_token>`
- Verify: hash incoming token, lookup row, check `expires_at > now()` + `used_at IS NULL`
- On success: set `used_at = now()`, set session cookie (signed JWT containing `user_id` + `tenant_id`)
- Cookie TTL: 7 days; refresh on activity

## Tenant isolation test (load-bearing)

```python
# tests/test_tenant_isolation.py
async def test_tenant_a_cannot_read_tenant_b():
    """Existence test for the most important security property of the entire portal."""
    tenant_a = await create_tenant("alpha-bookkeeping")
    tenant_b = await create_tenant("beta-bookkeeping")
    user_a = await create_user(tenant_a, "alice@alpha.example")
    cookie_a = await magic_link_login(user_a)

    # Direct URL probe to other tenant
    resp = await client.get(f"/portal/{tenant_b.slug}/", cookies=cookie_a)
    assert resp.status_code in {403, 404}, "tenant A reached tenant B namespace"

    # API probe (when Phase 2 adds /api/...)
    resp = await client.get(f"/api/tenants/{tenant_b.id}/documents", cookies=cookie_a)
    assert resp.status_code in {401, 403, 404}

    # Audit log must record the attempt
    log = await fetch_audit_log(tenant_a.id, action="cross_tenant_access_blocked")
    assert len(log) >= 1
```

This test must pass before any code reaches main. Failing it = security incident.

## Deployment

- Coolify project: extend `My first project` (UUID `m100nrzbdx92dn8kxzvrmhpy` per INFRA.md)
- Server UUID: `mihuu5scwb1y3gja1lik7tp9` (existing Hetzner box)
- Persistent volume: `/var/lib/coolify/services/document-ops-portal/data` (or wherever Coolify mounts)
- Port: internal 8000 → Traefik HTTPS
- Domain: `portal.owlzone.trade` (Porkbun CNAME → Hetzner box; Coolify auto-Let's-Encrypt)
- Env vars (Coolify-managed):
  - `DATABASE_URL` — Postgres on same box
  - `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET` — same live-mode account as CallMeIE
  - `SMTP_HOST`, `SMTP_USER`, `SMTP_PASS` — same as CallMeIE callmeie@proton.me sender
  - `SESSION_SIGNING_KEY` — new random 32-byte secret
  - `BASE_URL` — `https://portal.owlzone.trade`

## INFRA.md update (mandatory same-commit)

Add new section to `owl-studio-website-directions/INFRA.md` (and mirror in `callmeie-fix/INFRA.md`):

```markdown
## 14 · Document Ops Portal (Coolify on Hetzner)

| Field | Value |
|---|---|
| Repo | github.com/scruge1/document-ops-portal |
| Coolify UUID | <to be filled at deploy> |
| Public URL | https://portal.owlzone.trade |
| Domain (Porkbun) | portal.owlzone.trade CNAME → 178.104.205.255 |
| Postgres DB name | document_ops_portal |
| Stripe SKUs | dops_pilot_entry, dops_pilot_standard, dops_ops_monthly_starter |
| Magic link sender | callmeie@proton.me (same as CallMeIE) |
| Persistent volume | /var/lib/coolify/services/document-ops-portal/data |
```

## Phase 1 ordering (recommended)

1. **Day 1 (4 hrs)** — repo bootstrap, FastAPI skeleton, models.py, alembic init, local docker-compose with Postgres
2. **Day 1 (4 hrs)** — magic-link auth, SMTP send, login + callback flow, tenant + user creation
3. **Day 2 (4 hrs)** — Stripe Payment Link creation (3 SKUs), webhook handler, end-to-end test from Stripe → tenant
4. **Day 2 (4 hrs)** — tenant isolation test, admin route, dashboard skeleton, Coolify deploy + DNS + HTTPS

## Decisions resolved (Adam press-back 2026-05-01 cont.)

1. **Domain: `portal.owlzone.trade`** (Adam unsure → operator pick).
   Reasoning: matches client-facing framing ("client portal" — what prospects expect from Hubflo replacement narrative). `console` reads developer-y; `docs` reads documentation-site. Portal is the SaaS norm and least ambiguous.

2. **Stripe mode: live** (locked). Adam is first paying client; pays himself via Stripe Payment Link; produces a real receipt for accounting; validates whole flow including invoice email.

3. **Test mode also wired**: recommend YES but defer to Phase 1.5 (after live flow proven). Operator pick.
   Reasoning: tenant-isolation tests benefit from test-mode webhook firing locally without burning live transactions. Build it once live flow is end-to-end-proven, before opening to second paying client. Adds ~2 hrs.

4. **Repo: private** until Phase 3 ships (Adam confirmed).
   `github.com/scruge1/document-ops-portal` (private). Adam-only access. Public review only after first paying client + first auditable PR.

All Phase 1 decisions locked. Build can begin.

## What Phase 1 explicitly does NOT include

- File upload UI (Phase 2)
- OCR pipeline trigger (Phase 2)
- Review queue UI (Phase 2)
- Clean export download (Phase 2)
- Email digests (Phase 4)
- Multi-seat per tenant (Phase 4 if asked)

Anti-scope is load-bearing. Phase 1 ships only what's needed to get a paying client through the door — auth + billing + isolation.
