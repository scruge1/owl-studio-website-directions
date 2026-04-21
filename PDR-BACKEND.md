# PDR · Owl Studio unified backend

> Extends the CallMeIE Render/FastAPI stack with Owl Studio routes. One
> process, one deploy, one admin portal. Every tier we sell is backed
> end-to-end by this document — no "we'll figure that out per-project"
> gaps. Client isolation is enforced by service-level account ownership,
> not by our own code.

---

## 1. Goals & non-goals

**Goals**
- Stop using `mailto:` on client sites — forms must POST to a real endpoint
- Back every tier (Starter / Pro / Custom) and every care plan (Essential / Growth / Concierge) with concrete services, not aspirational promises
- Enforce client data isolation without hand-rolling auth/tenancy
- Produce a clean handover where the client can self-edit their site forever after without ever logging into an Owl Studio account

**Non-goals**
- No custom CMS — Sanity does that
- No custom payment processor — Stripe does that
- No analytics engine — Plausible does that
- No uptime service — UptimeRobot does that
- No hosting platform — Cloudflare Pages does that

We run the **glue**, not the tools.

---

## 2. Architecture at a glance

```
Client site (Cloudflare Pages, client-owned account)
       │  POST /owl/submit { site_id, form_data }
       ▼
callmeie.onrender.com  (FastAPI, multi-tenant)
       ├── /owl/submit          leads + contact forms
       ├── /owl/care/ticket     care-plan edit requests
       ├── /owl/health          per-site health pings (for UptimeRobot)
       ├── /owl/admin?token=    client lead/ticket dashboard
       ├── /owl/owner?token=    our internal fleet overview
       └── existing callmeie routes (untouched)
       │
       ▼
SQLite at /tmp/callmeie.db (Render free tier)
       ├── owl_sites            (site_id, client_email, name, token, …)
       ├── owl_leads            (site_id, ts, payload, status)
       ├── owl_tickets          (site_id, ts, subject, body, status)
       └── existing tables

External services used (each with its own account-ownership model):
- Cloudflare Pages          (client account)
- Sanity CMS                (our org, per-project seats)
- Stripe — our billing      (our account, clients as customers)
- Stripe — their billing    (client's own Stripe, we build with scoped access)
- Google Business Profile   (client's Google, we manage during setup)
- Google Analytics          (client's Google, we as Analyst)
- Cal.com                   (our team OR client's own)
- Plausible / Umami         (our org, per-site seats)
- UptimeRobot               (our account, client gets email alerts only)
- Porkbun / domain registrar (always client's account)
```

---

## 3. Account ownership matrix (the core rule)

**Rule in one line:** anything touching their money, their customers, or their search presence lives in **their** account. Tools we run to serve them live in ours, with token-scoped access.

| Service | Owner | Client edit path | Handover action |
|---|---|---|---|
| Our FastAPI backend | Owl Studio | `/owl/admin?token=CLIENT_TOKEN` | Token issued during onboarding; rotatable; never expires unless we end the relationship |
| Cloudflare Pages hosting | **Client** | They own the Pages account; we deploy via invite | Remove our collaborator access (or keep under care plan) |
| Sanity CMS (Pro tier) | Shared org, per-project | Invited as Editor on their project | "Transfer Project" → they become owner; we stay as Admin under care plan |
| Stripe (our invoicing) | Owl Studio | Client pays hosted invoice link, no login | Nothing to hand over |
| Stripe (their e-commerce) | **Client** | Their Stripe account, their dashboard | We remove ourselves as Developer at handover |
| Google Business Profile | **Client** | Their Google account | We leave as Manager after 90 days (or stay under care plan) |
| Google Analytics | **Client** | Property on their Google | We leave as Analyst at handover |
| Cal.com | Our team OR their own | Team invite limits them to their booking calendar | Team-member → they stay under care plan; self-hosted → full handover |
| Plausible / Umami analytics | Shared (site-scoped invite) | Invited to their site's view only | Site export on handover |
| UptimeRobot | Owl Studio | No client login; they get alert emails | Nothing to hand over |
| Domain registrar | **Client** | Their Porkbun/GoDaddy/etc. | We never hold the domain |

Every client gets a **1Password (or Bitwarden) shared vault** named `OwlStudio · <ClientName>` at the start of their project. Every credential we generate for them lives in that vault. Vault is transferred to them at handover; if they cancel early we export a PDF to their email and delete.

---

## 4. Route catalogue (new Owl Studio routes on the Render process)

### 4.1 `POST /owl/submit`

Replaces every `mailto:` on every client site.

**Request body (JSON):**
```json
{
  "site_id": "rathborne-dental",
  "form_data": {
    "name": "Cian Murphy",
    "email": "cian@gmail.com",
    "phone": "+353 87 555 0129",
    "message": "Looking for a first appointment for my child."
  },
  "form_type": "contact",
  "submitted_from": "https://rathbornedental.ie/#book"
}
```

**Behaviour:**
1. Validate `site_id` exists in `owl_sites` table
2. Insert row into `owl_leads`
3. Email the submission to the client's `lead_email` address via Resend/Postmark
4. Reply with `{"ok": true, "message": "We'll reply within 24 hours."}`
5. Rate limit: 10 per minute per IP (abuse protection)

**Failure modes:**
- Unknown site_id → 404 (never leak list of clients)
- Email provider down → log + queue, return success to user (their form "worked")
- Honeypot field `nickname` populated → silently drop (bot filter)

### 4.2 `POST /owl/care/ticket`

Care-plan intake for content edits.

**Request body (JSON):**
```json
{
  "site_id": "rathborne-dental",
  "submitter_email": "aoife@rathbornedental.ie",
  "subject": "Swap header photo",
  "body": "Please swap the hero image for the attached PDF — new practice photo.",
  "priority": "normal",
  "attachments": ["https://signed-upload-url-from-r2"]
}
```

**Behaviour:**
1. Verify submitter_email matches a registered email on `owl_sites.edit_emails`
2. Create ticket, SLA based on care tier:
   - Essential: 5 working days
   - Growth: 2 working days
   - Concierge: 1 working day
3. Email owner (`callmeie@proton.me`) + client acknowledgement
4. Log for weekly care-plan report

### 4.3 `GET /owl/admin?token=CLIENT_TOKEN`

Per-client dashboard. Only sees their own site's leads + tickets + uptime.

**Token generation:** 32-char URL-safe random, stored hashed. Rotatable via `POST /owl/admin/rotate` with email verification.

**Shows:**
- Last 100 leads (name, email, phone, message, timestamp, status open/contacted)
- Open + closed tickets (ticket ID, subject, status, our reply thread)
- Last 30 days uptime (from UptimeRobot public-status integration)
- Monthly report download link (PDF)

**Doesn't show:** anything belonging to any other site. SQL queries always scope by `site_id`. No admin superuser on this URL.

### 4.4 `GET /owl/owner?token=OWNER_TOKEN`

Our internal fleet overview. One token, hard-coded env var, rotatable.

**Shows:**
- All active clients (table: name, tier, care plan, MRR, last lead, last uptime check, PDF export)
- Any ticket overdue vs SLA (red flag row)
- Stripe subscription status per client (paid / past-due / cancelled)
- Weekly report runner (cron trigger button)

### 4.5 `GET /owl/health/:site_id`

Simple 200-OK endpoint returning `{"ok": true, "site_id": "…", "last_deploy": "…"}`. UptimeRobot polls this to verify the Render backend AND the client site reachability.

### 4.6 Stripe webhook: `POST /owl/stripe/webhook`

Handles care-plan subscriptions.

**Events:**
- `customer.subscription.created` → upgrade `owl_sites.care_tier`, start billing
- `customer.subscription.updated` → tier change mid-plan
- `invoice.payment_failed` → email client, flag in owner dashboard
- `customer.subscription.deleted` → downgrade to `none`, flag for downgrade-pass-2 workflow

---

## 5. Database schema (SQLite at /tmp, portable to Postgres later)

```sql
CREATE TABLE owl_sites (
  site_id            TEXT PRIMARY KEY,          -- slug: rathborne-dental
  display_name       TEXT NOT NULL,              -- Rathborne Dental
  tier               TEXT NOT NULL,              -- starter | pro | custom
  care_tier          TEXT,                       -- essential | growth | concierge | none
  lead_email         TEXT NOT NULL,              -- where form submissions go
  edit_emails        TEXT NOT NULL,              -- JSON array of authorised ticket submitters
  admin_token_hash   TEXT NOT NULL,              -- bcrypt of /owl/admin token
  live_url           TEXT NOT NULL,
  cloudflare_account TEXT,                       -- their CF account email
  sanity_project_id  TEXT,                       -- null unless Pro or Custom
  stripe_sub_id      TEXT,                       -- null unless care plan active
  created_at         DATETIME DEFAULT CURRENT_TIMESTAMP,
  status             TEXT DEFAULT 'active'       -- active | paused | off
);

CREATE TABLE owl_leads (
  id               INTEGER PRIMARY KEY AUTOINCREMENT,
  site_id          TEXT NOT NULL REFERENCES owl_sites(site_id),
  ts               DATETIME DEFAULT CURRENT_TIMESTAMP,
  form_type        TEXT NOT NULL,                -- contact | quote | booking | callback
  payload_json     TEXT NOT NULL,                -- full form body
  submitter_ip     TEXT,
  submitted_from   TEXT,
  status           TEXT DEFAULT 'new'            -- new | contacted | closed | spam
);

CREATE TABLE owl_tickets (
  id               INTEGER PRIMARY KEY AUTOINCREMENT,
  site_id          TEXT NOT NULL REFERENCES owl_sites(site_id),
  submitter_email  TEXT NOT NULL,
  ts               DATETIME DEFAULT CURRENT_TIMESTAMP,
  subject          TEXT NOT NULL,
  body             TEXT NOT NULL,
  attachments_json TEXT,                         -- JSON array of URLs
  priority         TEXT DEFAULT 'normal',        -- low | normal | high
  status           TEXT DEFAULT 'open',          -- open | in_progress | done | wontfix
  sla_due          DATETIME                      -- computed from care_tier
);

CREATE TABLE owl_reports (
  id               INTEGER PRIMARY KEY AUTOINCREMENT,
  site_id          TEXT NOT NULL REFERENCES owl_sites(site_id),
  period_start     DATE NOT NULL,
  period_end       DATE NOT NULL,
  leads_count      INTEGER,
  tickets_closed   INTEGER,
  uptime_pct       REAL,
  pdf_url          TEXT,                         -- R2 signed URL
  created_at       DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Note:** `/tmp` on Render free tier wipes on redeploy. Migration path when a client gets bigger: Render Postgres €7/mo, or Supabase free tier (500MB), or Cloudflare D1 (free up to 100k rows/day). Decision deferred until second paying client.

---

## 6. Client onboarding flow (end-to-end, 3-5 business days)

### Day 0 — Lead comes in
- Prospect submits contact form on `websites.owlzone.trade` or books the style-match call
- Lead hits `/owl/submit` or books the call directly
- We decide: go-ahead or €99 audit

### Day 1 — Kickoff
- Create shared **1Password vault** `OwlStudio · ClientName`
- Client signs up for their own Cloudflare account (free); invites our email as `Pages:Edit`
- Client grants us Google Business Profile manager access via GBP invite
- Client grants us Google Analytics Analyst access (we create the property if they don't have one)
- If Pro tier: we create a Sanity project, invite client as Editor on the project
- We create a `owl_sites` row, generate `admin_token`, email client their admin URL
- Stripe: we create an invoice (one-off project fee) + a subscription product (care plan if selected)
- Client pays the 50% deposit invoice

### Days 2-6 — Build
- We build the site (using the style + content blocks from their PDR)
- Every form on their site POSTs to `/owl/submit` with their `site_id`
- We deploy to their Cloudflare Pages via GitHub integration
- We wire UptimeRobot: 5-minute HEAD check on their live URL, alert to their email + ours

### Day 7 — Handover (Starter) or Day 14 — Handover (Pro)
- Client receives: admin URL + token, 1Password vault access, 15-min walkthrough video
- We remove ourselves from Cloudflare Pages + Google accounts (or keep access under a care plan)
- Stripe: final 50% invoice issued + care plan subscription activates (if chosen)
- Uptime + analytics links added to their admin dashboard
- Ticket queue opens — any post-handover edit is a care-plan ticket

### Ongoing — Care plan cycle
- Monthly: auto-generated PDF report (leads count + uptime + tickets closed)
- Quarterly: SEO + speed pulse review if Growth/Concierge
- Annual: domain + SSL + Google verification refresh check
- If client cancels care plan: we export and delete the 1Password vault, remove our Sanity Admin seat, leave everything in their hands

---

## 7. Handover protocol per service

### Cloudflare Pages
- Client owns the account. We had `Pages:Edit` role during build.
- At handover: we either stay (if on care plan) or remove our email from their Cloudflare Members list.
- GitHub repo: either we transfer to their GitHub org, or we keep ownership and give them a deploy key — their call.

### Sanity CMS (Pro only)
- Project lives under our Sanity org during build.
- At handover: either (a) transfer project to their Sanity org (they have to create one — free), or (b) they stay as Editor under our org and we remain Admin under care plan.
- Most clients pick (b) because they never want to think about Sanity again.

### Stripe (our invoicing)
- Nothing to hand over — they're a customer, not a merchant.
- Invoices hosted on Stripe's URL, they pay via card/SEPA/bank transfer.

### Stripe (their e-commerce — Custom tier only)
- Client creates their own Stripe Standard account (free, few minutes).
- They invite our email as Developer during build.
- At handover: we remove ourselves or stay as Developer on care plan for updates.

### Google Business Profile
- Client owns the listing. We were Manager during build.
- After 90 days of post-launch (or at their request) we leave as Manager.
- On Growth/Concierge care: we stay as Manager and post monthly updates.

### Google Analytics
- Client owns the property. We were Analyst during build.
- At handover we leave as Analyst or stay under care plan.

### Domain
- We never hold it. They own Porkbun/GoDaddy/etc.
- We have DNS-edit access via their registrar's invite system during build; they revoke at handover.

### Cal.com bookings (Custom tier)
- Two paths: our team (they join our workspace, edit their calendar only) or their own self-hosted (we set up, full handover).
- Default recommendation: our team — simpler for them, same isolation, we can help with availability changes under care plan.

### Plausible / Umami analytics
- Our multi-tenant install. They're invited to their site's view only.
- Export CSV on handover if they want to go self-hosted.

### UptimeRobot
- Stays in our account. They get alert emails for their site only.
- No handover — if they leave, we delete their monitor.

---

## 8. Credentials management

One 1Password (or Bitwarden — both have free personal tiers) **shared vault** per client, named `OwlStudio · <ClientName>`.

**Every secret we generate on their behalf goes in there the moment it exists:**
- Cloudflare account credentials (theirs — they set it up, we just note the owner email)
- Google Business Profile owner email + recovery phone
- Sanity project slug + admin seat link
- Stripe customer ID + invoice link
- UptimeRobot monitor ID
- Their admin portal token (rotatable)
- SSH keys for their Cloudflare Pages deployment (if any)
- DNS records snapshot at build time

**At handover:**
- Vault ownership is transferred to them (1Password "Transfer Ownership" flow)
- OR vault content exported as PDF and emailed to them; we delete our copy
- We remove our own access to their Cloudflare/Google/etc. accounts per handover protocol above

**If they breach payment:** we rotate all tokens we issued, email them the new ones, keep the vault intact so they can come back.

**If they cancel care plan:** vault is theirs to keep or delete. We purge our copy 30 days after cancel date.

---

## 9. What gets built — 5-working-day scope

Scope bounded to "enough to back the tiers we already sell." No speculative features.

| Day | Deliverable | Done when |
|---|---|---|
| 1 | `/owl/submit` endpoint + `owl_sites` + `owl_leads` tables + first-party Resend/Postmark email send | Rathborne Dental sample form POST returns 200, email arrives at test inbox |
| 2 | `/owl/admin?token=` dashboard (read-only view of leads) + token issuance script | Hit the URL with a valid token, see the test lead. Wrong token → 401. |
| 3 | Stripe products + `/owl/stripe/webhook` + subscription lifecycle | Test subscription creation in Stripe test mode updates `owl_sites.care_tier` |
| 4 | `/owl/care/ticket` + SLA logic + weekly report cron + PDF generator | Ticket submitted → owner email fires, appears in admin, SLA timer running |
| 5 | UptimeRobot provisioning script + `/owl/health/:site_id` + onboarding wizard CLI | `python onboard.py --site rathborne-dental` creates all accounts, inserts DB row, returns admin URL |

After day 5, any new client onboards via the CLI + 1Password vault template — repeatable, no ad-hoc per-project backend work.

---

## 10. Cost model (Owl Studio's side)

**Fixed monthly costs (regardless of client count):**
- Render Starter: $0 free tier → $7/mo once we pass 750 hours (first paid tier)
- UptimeRobot free tier: $0 for 50 monitors, 5-min interval
- Sanity Cloud: $0 up to 3 seats, 10 projects (enough for 10 Pro clients)
- Postmark: $0 for first 100 emails/month, then $15/mo for 10k
- Cloudflare Pages: $0 for static hosting, generous bandwidth

**Per-client variable costs (none on Starter tier):**
- Stripe transaction: 1.4% + €0.25 per European card
- Plausible Cloud (if we choose cloud over self-hosted): €0.90/site/mo — passed through to client
- Sanity overage: $0 until ~10 projects, then bumps
- Domain: zero (client owns it)

**Estimated monthly infra cost for 10 active clients:** ~€15/mo all-in.
**MRR from 10 care plans at Growth tier:** €950/mo.
**Gross margin on recurring:** >95%.

---

## 11. What this PDR does NOT cover (explicitly out of scope)

- No custom CMS authoring experience — Sanity Studio is the answer
- No custom ecommerce platform — Stripe Payment Links or Shopify for full catalog
- No custom scheduling UI — Cal.com
- No custom analytics dashboard — Plausible's UI is fine
- No custom email marketing — clients use Mailchimp/ConvertKit themselves
- No SEO tool — Google Search Console covers it; our SEO is manual on-page work
- No anti-spam beyond the honeypot field on `/owl/submit` — we add Turnstile if needed later
- No multi-user auth on the admin dashboard — token in URL is sufficient at this scale (clients can email-reset the token if compromised). If we pass 50 clients or a paying client requests it, we add magic-link auth via Resend.

When any of those "nots" become genuinely needed by a real paying client, we write a follow-up PDR.

---

## 12. Risks & honest failure modes

| Risk | Likelihood | Mitigation |
|---|---|---|
| Render free tier wipes `/tmp` on redeploy | Certain — this is documented Render behaviour | Leads + tickets are also emailed; DB is a convenience log, not the source of truth. Migrate to Postgres when second paying client signs. |
| Client forgets their admin token | Likely | Email-reset flow via Resend — verify ownership of `lead_email`, issue new token, hash stored. |
| Sanity project ownership transfer corrupts content | Very unlikely (Sanity does this cleanly) | Snapshot content export nightly to R2 bucket. Restorable. |
| UptimeRobot false positive → client annoyed | Occasional | 2-consecutive-failure rule (10-min downtime threshold before alert) to reduce flapping. |
| Client churns with unpaid invoices | Possible | Stripe handles dunning. After 14 days past-due, we downgrade site to read-only static snapshot + email them. |
| We leak one client's admin URL to another | Impossible if routes always `WHERE site_id = ?` | Code review on every route; integration test with 2 sites + wrong tokens confirms 401 / 404. |
| We lose a 1Password vault | Possible (account deletion, phishing) | 1Password Business has recovery; we enable for the Owl Studio account. |

---

## 13. Decision record

- **Backend runtime**: FastAPI on Render (extends CallMeIE, known stack). No Django/Express — cost is extra mental overhead.
- **Database**: SQLite on free Render → Postgres when revenue justifies. No Firebase / Supabase at day 1 (adds another vendor).
- **CMS for Pro**: Sanity (not Payload). Reason: Sanity is hosted, zero-infra; Payload self-hosted is more control but another thing to own.
- **Subscriptions**: Stripe (not Paddle, not Lemon Squeezy). Reason: Irish/EU bank transfer support + best-in-class API.
- **Analytics**: Plausible over GA4 for client-facing. Reason: 2-line script, no cookie banner needed, privacy-first fits our brand.
- **Multi-tenancy model**: shared backend + per-service account ownership. Reason: low ops cost now, client-owned where it matters (money, brand, SEO).

---

## 14. Approval gate

This PDR is the architecture. Code starts only after sign-off.

Once approved:
1. I write Day 1 (`/owl/submit`) — smallest useful unit
2. We test against the Rathborne Dental sample form
3. Then Day 2-5 proceed in order

Days are real working days, not parallel dispatch. This is our own infrastructure — we build it once, carefully, not via N-agent fan-out.

---

## 15. OSS swaps (approved 2026-04-21 — supersedes service picks in §2, §4, §10, §13)

Every paid service in the original plan that has a genuinely equivalent
OSS alternative has been swapped. The closed services that remain are
kept only where regulation, deliverability, or CDN network make OSS
self-host meaningfully worse for the client — not because of ops laziness.

### 15.1 What changed

| Role | Original pick | New pick | Why OSS wins here |
|---|---|---|---|
| CMS (Pro tier) | Sanity Cloud | **Payload CMS** (MIT) | Same feature bar — admin UI, field types, live preview, roles. Runs on Node + Postgres. No per-seat pricing. Scoped editor accounts per client. |
| Uptime monitoring | UptimeRobot | **Uptime Kuma** (MIT) | Better UI, more integrations (Slack/Discord/Telegram/webhook), unlimited monitors, <100MB RAM. |
| Analytics | Plausible Cloud | **Umami** (MIT) OR **Plausible Community Edition** (AGPL) | Plausible Cloud *is* Plausible CE — only the hosting differs. Umami is the lightest swap; same 1-line script, privacy-first, no cookie banner. |
| Bookings (Custom tier) | Cal.com Cloud | **Cal.com self-hosted** (AGPL) | Cal.com Cloud *is* Cal.com self-hosted — only the hosting differs. Full multi-tenant built-in. |
| Credentials vault | 1Password | **Vaultwarden** (GPL) | Lightweight Rust server fork of Bitwarden. One container. Shared vaults + team features match 1Password. |
| Error monitoring (if/when added) | Sentry | **GlitchTip** (MIT) | Drop-in Sentry-compatible — uses the same Sentry SDK on the client. Self-hosted. |

### 15.2 What stays closed (pragmatic reasons, not ops savings)

| Role | Kept | Why |
|---|---|---|
| Card processing | **Stripe** | Regulated acquirer; no OSS equivalent for real EU card/SEPA payments. Mollie is the alternative if Stripe becomes a blocker — also not OSS. |
| Transactional email | **Resend / Postmark** (or AWS SES) | Self-hosting SMTP *is* possible (Postal is OSS) but deliverability is a multi-month dark art: domain reputation, SPF/DKIM/DMARC, IP warm-up, reverse-DNS. Client forms landing in spam kills the business. Pay for deliverability-as-a-service. |
| CDN + static hosting | **Cloudflare Pages** + **R2** | Free, unlimited bandwidth, free egress, fastest TTFB globally. No self-host matches this without significant spend. |
| Hosting platform (short-term) | **Render** free tier | Keeps ops small while we're <3 paying clients. At 3+ clients or €20+/mo spend, migrate everything to a single **Hetzner CPX11 €4/mo** VPS running **Coolify** (MIT, one-click OSS-Heroku) which hosts every service above. |

### 15.3 Updated architecture (replaces §2 diagram)

```
Hetzner CPX11 €4/mo  (or Render free tier until we outgrow it)
  └── Coolify (OSS Heroku-alike)
       ├── FastAPI (our /owl/* routes — CallMeIE extension)
       ├── Payload CMS        (Pro-tier client content; per-client editor seats)
       ├── Umami              (analytics — one instance, multi-site)
       ├── Cal.com            (self-hosted — Custom-tier bookings)
       ├── Uptime Kuma        (monitoring all client sites + our backend)
       ├── Vaultwarden        (credentials vault, shared per-client)
       ├── GlitchTip          (error monitoring for our backend)
       └── Postgres 16        (one instance, schema-per-service)

External / closed (regulation, deliverability, CDN):
  - Stripe           (card/SEPA payments — required)
  - Resend           (transactional email — deliverability)
  - Cloudflare Pages (client site hosting — free, CDN moat)
  - Cloudflare R2    (backup + attachment storage — free egress)
  - Domain registrar (client-owned — Porkbun, GoDaddy, etc.)
```

### 15.4 Licence caveats

- **Cal.com (AGPL)** — if we modify and offer as a service, we publish modifications. We won't be modifying it. No practical constraint.
- **Plausible CE (AGPL)** — same. Using Umami instead (MIT) avoids this entirely.
- **Vaultwarden (GPL)**, **Uptime Kuma (MIT)**, **Payload (MIT)**, **GlitchTip (MIT)**, **Umami (MIT)** — permissive or copyleft, no practical constraints on how we use them internally.

### 15.5 Updated cost model at 10 clients

| Line item | Monthly |
|---|---|
| Hetzner CPX11 (or Render Starter after free tier) | €4 (Hetzner) / €7 (Render) |
| All 7 OSS services (on the same box) | €0 |
| Stripe transaction fees | 1.4% + €0.25/EU card |
| Resend (first 3,000 emails/mo free, then $20/mo for 50k) | €0 – €18 |
| UptimeRobot → replaced by Uptime Kuma | €0 |
| Sanity → replaced by Payload | €0 |
| Plausible Cloud → replaced by Umami | €0 |
| Cal.com Cloud → replaced by self-hosted | €0 |
| 1Password → replaced by Vaultwarden | €0 |
| **Total fixed monthly infra** | **€4-€25 all-in** (down from ~€15-€30 in original PDR) |
| **MRR from 10 Growth care plans** | **€950** |
| **Gross margin on recurring** | **>97%** |

### 15.6 Deploy order (revised from §9)

The OSS swaps only affect *which* service implements each role — the Day 1 - Day 5 scope in §9 is unchanged. Deploy the stack in this order:

1. **Day 1** — `POST /owl/submit` route on existing Render FastAPI (no new infra yet)
2. **Day 2** — `/owl/admin?token=` client dashboard (HTML template on existing FastAPI)
3. **Day 3** — Stripe products + webhook handler
4. **Day 4** — `/owl/care/ticket` + SLA logic + PDF report generator
5. **Day 5** — Onboarding CLI + first run against Rathborne Dental sample
6. **Day 6 (new, OSS-first)** — Provision Hetzner CPX11 + Coolify; deploy Postgres, Uptime Kuma, Vaultwarden on the box; wire Uptime Kuma to monitor the Render FastAPI + websites.owlzone.trade + callmeie.ie
7. **Day 7 (new)** — Deploy Payload CMS + Umami on the same Coolify box; create the first Payload project for Rathborne Dental as the Pro-tier prototype
8. **Day 8 (new)** — Migrate the Render FastAPI off Render onto the same Coolify box; shut down Render; total infra spend = €4/mo

Days 6-8 only happen if Day 1-5 land cleanly. If Render free tier holds us fine for the first 2 paying clients, the migration can defer months.

### 15.7 Decision record (appended)

- **All infrastructure is OSS-first.** Closed services are used only where regulation, deliverability, or CDN network justifies them.
- **Payload over Sanity** for Pro-tier CMS.
- **Uptime Kuma over UptimeRobot** for monitoring.
- **Umami over Plausible Cloud** for analytics (simpler, MIT).
- **Self-hosted Cal.com** over Cal.com Cloud for Custom-tier bookings.
- **Vaultwarden over 1Password** for credentials vaults.
- **GlitchTip over Sentry** if/when error monitoring is added.
- **Hetzner + Coolify** as the long-term host, migrated to once Render cost/scale makes it sensible.

### 15.8 "Build it on ourselves first, then rinse-and-repeat for clients"

The deployment itself is a tested recipe. We wire every service to
**our own sites first** — websites.owlzone.trade and callmeie.ie — so
the whole pipeline is proven working before any client onboard. The
deployment commands, configs, and gotchas get captured in
`DEPLOYMENT-PLAYBOOK.md` alongside this PDR. That playbook becomes the
one-page onboarding recipe: when client N comes in, we run the same
commands, with their site_id and their lead_email, and 20 minutes later
they're fully wired.
