# DEPLOYMENT PLAYBOOK · Owl Studio client onboarding

> One page, end-to-end. Every command to wire a new client from a signed
> contract to a fully-live site with forms, monitoring, credentials, and
> a client-accessible admin dashboard. Tested first on our own sites
> (`websites.owlzone.trade` + `callmeie.ie`) so we know it works before
> any paying client sees it.
>
> If any step fails here and you can't recover it in 10 minutes,
> update this playbook with the fix — it's a living document.

> **⚠ HOST MIGRATION (2026-05-30).** The CallMeIE FastAPI moved **off Render onto Hetzner/Coolify** (`178.104.205.255`). Everywhere below that says `callmeie.onrender.com`, the live host is now **`api.callmeie.ie`** (owl/stripe routes) / **`admin.callmeie.ie`** (admin). `callmeie.onrender.com` is **dead/stale** — do not deploy to or curl it. Env vars + redeploy are now done in **Coolify** (not the Render dashboard). DB is Coolify Postgres (persistent). Canonical: `INFRA.md` §3 banner. The onrender URLs in the commands below are retained for the decommission task; swap host before running.

---

## 0 · One-time Owl Studio setup (done once, then every client follows §1-§7)

### 0.1 Env vars on Render (Dashboard → callmeie-receptionist → Environment)

| Key | Value | Notes |
|---|---|---|
| `OWL_OWNER_TOKEN` | `$(python -c "import secrets; print(secrets.token_urlsafe(32))")` | Only person who knows this is the owner. Used to register new sites. |

All other env vars already exist for CallMeIE (Twilio etc.) — `/owl/submit`
reuses them for SMS notifications.

### 0.2 Infra inventory (Owl Studio-owned)

| Service | Where | Purpose | Cost |
|---|---|---|---|
| Render (FastAPI) | `callmeie.onrender.com` | `/owl/*` routes | Free tier until 3+ clients |
| Cloudflare account (ours) | `cloudflare.com` | We're invited to clients' accounts — never hold their Pages ourselves | Free |
| Vaultwarden | (planned: Hetzner CPX11 €4/mo) | Per-client credential vaults | €4/mo shared across all clients |
| Uptime Kuma | (planned: same Hetzner box) | Monitor all client sites + Render | Free |
| Payload CMS | (planned: same Hetzner box, per-Pro-client project) | Pro-tier CMS | Free |
| Umami | (planned: same Hetzner box) | Multi-site analytics | Free |
| Stripe (owner account) | `dashboard.stripe.com` | Our invoicing + care-plan subscriptions | Tx fees only |
| Resend | `resend.com` | Transactional email | Free up to 3k/mo |
| Domain registrar | Porkbun (owl studio's own) | `websites.owlzone.trade` | ~€10/yr |

### 0.3 Client-side accounts (client-owned, we never hold the password)

| Service | Who holds login | What we get |
|---|---|---|
| Cloudflare Pages | **Client** | Pages:Edit role via their invite during build |
| Domain registrar | **Client** | DNS edit via their invite; they revoke at handover |
| Google Business Profile | **Client's Google** | Manager role during build; leave after 90 days or stay on care plan |
| Google Analytics | **Client's Google** | Analyst role |
| Stripe (their e-commerce, Custom tier only) | **Client** | Developer role during build; we remove ourselves at handover |

---

## 1 · Pre-onboarding (before client signs the contract)

Not part of the deploy — covered by the sales gallery (`websites.owlzone.trade`),
the style-match call, and the scoping conversation. Go/no-go is made there.

---

## 2 · Signed client · Day 0

**Deliverables by end of day 0:**
- Shared 1Password / Vaultwarden vault `OwlStudio · <Client>` exists
- Client has invited us to their Cloudflare account (Pages:Edit role)
- Client has invited us to their Google Business Profile (Manager) + Google Analytics (Analyst)
- 50% deposit invoice sent via Stripe
- Kickoff call scheduled

Commands:

```bash
# Generate a credentials vault URL to share with the client
# (Vaultwarden once deployed, or a new 1Password shared vault until then)
VAULT_NAME="OwlStudio · Rathborne Dental"
# Manually create the vault with that name in Vaultwarden/1Password
# Share read/write with client's email + owner's email

# Draft the Cloudflare + Google invite request email
cat <<EOF
Hi Aoife,

Three quick setups before I start building:

1. Cloudflare Pages — sign up free at dash.cloudflare.com if you don't
   already have an account, then invite scruge@pm.me as a Member with
   the "Pages:Edit" role (Workers & Pages permissions).
2. Google Business Profile — add scruge@pm.me as a Manager on your
   Rathborne Dental listing.
3. Google Analytics 4 — add scruge@pm.me as Analyst on your property
   (or we create one if you don't have GA set up yet).

I'll confirm once I've accepted all three. Payment invoice attached —
build starts when that clears.

Owl Studio
EOF
```

---

## 3 · Build starts · Days 1-5 (Starter) / Days 1-12 (Pro) / Days 1-21+ (Custom)

### 3.1 Pick the industry sample that's closest + clone it

The 10 industry samples at `samples/industries/0X-<vertical>.html` are the
starting points — you don't build from scratch, you adapt.

```bash
cd owl-studio-website-directions
SLUG="rathborne-dental"              # replace with client slug
cp samples/industries/01-dental-swiss.html client-builds/${SLUG}/index.html
```

### 3.2 Adapt the sample to real client content

Swap these in `client-builds/${SLUG}/index.html`:

- Practice/firm name
- Principal(s) + credentials
- Address + Eircode + phone + email
- Services list (with real fees)
- Registration number (Dental Council / Law Society / etc.)
- Insurance accepted / PRSI language where relevant
- Opening hours
- Testimonials (first-name-only, GDPR) IF client consents to any

The industry sample's 1,000+ lines give you ~80% of the structure. You
only rewrite the content blocks — the design stays.

### 3.3 Wire every form on the client site to `/owl/submit`

Every `<form>` that should capture a lead gets:

```html
<form data-owl>
  <input type="text" name="name" required placeholder="Your name">
  <input type="email" name="email" required placeholder="Email">
  <input type="tel" name="phone" placeholder="Phone">
  <textarea name="message" placeholder="Message"></textarea>
  <!-- honeypot — must be present + empty -->
  <input type="text" name="nickname" style="display:none" tabindex="-1" autocomplete="off">
  <button type="submit">Send</button>
</form>
```

Then drop the embed snippet (one-time, on each page with a `data-owl` form):

```html
<script>
document.querySelectorAll('form[data-owl]').forEach(f =>
  f.addEventListener('submit', async e => {
    e.preventDefault();
    const fd = Object.fromEntries(new FormData(f));
    const r = await fetch('https://callmeie.onrender.com/owl/submit', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({
        site_id: 'rathborne-dental',          // site_id goes here
        form_data: fd,
        submitted_from: location.href
      })
    });
    const j = await r.json();
    f.dispatchEvent(new CustomEvent('owl-result', {detail: j}));
    if (j.ok) { f.reset(); f.querySelector('button').textContent = 'Sent ✓'; }
  })
);
</script>
```

**One snippet per site, pasted once on every page with a form.** The
auto-generated version (via `POST /owl/sites`) already fills in the
site_id for you.

### 3.4 Register the site in the backend

```bash
OWNER_TOKEN="<from Render env var OWL_OWNER_TOKEN>"

curl -X POST "https://callmeie.onrender.com/owl/sites?token=$OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "site_id": "rathborne-dental",
    "display_name": "Rathborne Dental",
    "tier": "pro",
    "care_tier": "growth",
    "lead_email": "aoife@rathbornedental.ie",
    "lead_sms": "+353 87 555 0129",
    "edit_emails": ["aoife@rathbornedental.ie", "reception@rathbornedental.ie"],
    "live_url": "https://rathbornedental.ie"
  }'
```

Response includes the `admin_url` (e.g. `/owl/admin?token=...`) — put
this in the client's vault and email it to them at handover.

### 3.5 Deploy the site to the client's Cloudflare Pages

```bash
# From the client's Cloudflare account (we're invited as Pages:Edit)
cd client-builds/${SLUG}
wrangler pages deploy . --project-name=${SLUG} --branch=main
# Or: push to a GitHub repo and connect Pages to it in the CF UI
```

Set the custom domain in Cloudflare → Pages → ${SLUG} → Custom Domains.
Client adds the CNAME in their registrar (you walk them through it once).

### 3.6 Wire UptimeRobot (free tier, Owl Studio account)

```
dashboard.uptimerobot.com → New Monitor:
  type:     HTTP(s)
  URL:      https://rathbornedental.ie
  name:     rathborne-dental · live
  interval: 5 min
  alert:    owner@owlzone.trade + aoife@rathbornedental.ie

New Monitor:
  URL:      https://callmeie.onrender.com/owl/health/rathborne-dental
  name:     rathborne-dental · backend route
  interval: 5 min
  alert:    owner only
```

Once Uptime Kuma is deployed on our Hetzner box (Phase 2), migrate these
two monitors into Uptime Kuma and shut down UptimeRobot.

### 3.7 Set up the Stripe subscription (if care plan selected)

```
stripe.com → Products:
  Pre-created products (done once):
  - owl-care-essential-monthly  (€45/mo recurring)
  - owl-care-essential-yearly   (€450/yr recurring)
  - owl-care-growth-monthly     (€95/mo)
  - owl-care-growth-yearly      (€950/yr)
  - owl-care-concierge-monthly  (€195/mo)
  - owl-care-concierge-yearly   (€1,950/yr)

For the client:
  1. Customer → new → email aoife@rathbornedental.ie
  2. Subscriptions → create → pick owl-care-growth-monthly
  3. Send hosted invoice URL via email
```

Webhook handler (in `/owl/stripe/webhook`) will auto-update `owl_sites.care_tier` when payment clears.

### 3.8 Pro-tier CMS (if applicable)

Currently Sanity until Payload is deployed. Once Payload is live on our
Hetzner box:

```bash
# Via Payload admin UI (logged in as Owl Studio admin):
# Create project: rathborne-dental
# Create user: aoife@rathbornedental.ie, role: editor, scoped to this project
# Send magic-link via Resend
```

---

## 4 · Handover · Day 7 (Starter) / Day 14 (Pro)

Checklist — don't skip:

- [ ] All forms tested end-to-end (submit → lead appears in `/owl/admin`)
- [ ] Client has admin URL + token in vault + email
- [ ] UptimeRobot monitoring active, client receiving alerts
- [ ] Stripe subscription active (if care plan) OR final invoice paid (if not)
- [ ] Client has been shown the admin dashboard (15-min walkthrough or recorded video)
- [ ] Credentials vault shared with client; we've kept a copy
- [ ] Client has been told: for any edit, email `care@callmeie.ie` (→ opens a ticket)
- [ ] Google Business Profile set up, Google Analytics running
- [ ] We've removed ourselves from Cloudflare Pages collaborator list UNLESS the client is on a care plan
- [ ] Weekly report cron has run at least once (fake if needed for demo)

Email template:

```
Hi Aoife,

Rathborne Dental is live at https://rathbornedental.ie.

Your admin dashboard is here (bookmark it, rotate the token anytime):
https://callmeie.onrender.com/owl/admin?token=<TOKEN>

Every contact form on your site shows up in that dashboard within ~2
seconds of being submitted. Forms also ping my phone via SMS so I see
them too — handy during launch week.

For any content edit you need (new staff photo, holiday hours, a new
service), email care@callmeie.ie with the word "Rathborne" in the
subject. Your Growth care plan is 2 working days turnaround.

Any questions, just ring.
Owl Studio
```

---

## 5 · Ongoing · Care plan cycle (monthly / quarterly)

### 5.1 Monthly (first working day of the month)

```bash
# PDF report per client (auto-generated at month end by cron — TBD)
# Manual for now:
cd scripts
python generate-owl-report.py --site rathborne-dental --month 2026-04

# Attach to email:
# Subject: Rathborne Dental · April 2026 report
# Body: Monthly recap attached. Leads captured: 47.
#       Site uptime: 99.94%. Tickets closed: 3.
```

### 5.2 Quarterly (Growth + Concierge tiers only)

- SEO + page-speed pulse: run PageSpeed Insights, Lighthouse, fix
  regressions.
- Check broken links via `npx linkinator https://rathbornedental.ie`
- Schema markup validation: schema.org validator
- Google Business Profile: photos fresh, Q&A answered, posts up to date

### 5.3 Concierge tier (monthly 20-min call)

- Review the dashboard together
- Plan next month's content / GBP posts / seasonal updates
- Note any ticket themes to proactively solve

---

## 6 · Cancellation / offboarding

When a client cancels:

```bash
# 1. Stripe: cancel subscription at period end (they pay through current period)
# 2. Rotate their admin_token (in case it's been shared widely):
curl -X POST "https://callmeie.onrender.com/owl/sites?token=$OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"site_id":"rathborne-dental","action":"rotate_token"}'
# (action=rotate_token not yet implemented; add in Day 3 of backend build)

# 3. Remove ourselves from Cloudflare Pages collaborator list
# 4. Remove ourselves from Google Business Profile (Manager → Leave)
# 5. Remove ourselves from Google Analytics (Analyst → Remove)
# 6. Export the Vaultwarden vault content as PDF → email to client
# 7. Delete our copy of the vault after 30 days
# 8. Site itself remains on their Cloudflare account — we never owned it
# 9. Update owl_sites.status = 'off' (keeps audit trail, stops new leads)
```

---

## 7 · Rinse-and-repeat cheat sheet (for the Nth client)

For a new client whose build is similar to a past one:

```bash
export SLUG="new-client-slug"
export DISPLAY="New Client Ltd"
export EMAIL="owner@newclient.ie"
export PHONE="+353 XX XXX XXXX"
export URL="https://newclient.ie"
export TIER="pro"                    # starter|pro|custom
export CARE="growth"                 # essential|growth|concierge (or empty for none)

# 1. Clone the closest industry sample
cp samples/industries/0X-<vertical>.html client-builds/$SLUG/index.html

# 2. Adapt content (manual — ~30 minutes for Starter, ~2 hours for Pro)

# 3. Register in backend
curl -X POST "https://callmeie.onrender.com/owl/sites?token=$OWL_OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"site_id\": \"$SLUG\",
    \"display_name\": \"$DISPLAY\",
    \"tier\": \"$TIER\",
    \"care_tier\": \"$CARE\",
    \"lead_email\": \"$EMAIL\",
    \"lead_sms\": \"$PHONE\",
    \"edit_emails\": [\"$EMAIL\"],
    \"live_url\": \"$URL\"
  }"
# → copy the admin_token from the response into Vaultwarden

# 4. Add the embed snippet (auto-generated — just paste into each page
#    with a data-owl form)

# 5. Deploy to client's Cloudflare Pages
wrangler pages deploy client-builds/$SLUG --project-name=$SLUG

# 6. UptimeRobot: add 2 monitors (see §3.6)

# 7. Stripe: create customer + subscription (if care plan)

# 8. Send handover email (template in §4)
```

**Goal: a new client from signed contract to live site in < 1 working day for Starter tier, < 2 working days for Pro.**

---

## 8 · What's still manual (and OK to leave that way)

- GBP + Google Analytics setup — client invites us, no automation saves time here
- Custom-tier integrations — every one is different, playbook per-project
- Domain DNS — client-specific, we walk them through the registrar UI once

---

## 9 · What's automated next (roadmap after first paying client)

- [ ] `python onboard.py --site $SLUG` script (combines steps 3-6 into one command)
- [ ] Stripe webhook → auto-update `owl_sites.care_tier`
- [ ] Monthly PDF report cron (Render scheduled jobs or GitHub Actions)
- [ ] Migrate off Render to Hetzner CPX11 + Coolify (Payload, Umami, Uptime Kuma, Vaultwarden, GlitchTip all on one box)
- [ ] Turnstile anti-spam on `/owl/submit` if we start getting bot traffic

---

## 10 · If something breaks

| Symptom | Check |
|---|---|
| Form shows "Sent ✓" but no lead in dashboard | Render logs — `https://dashboard.render.com/web/...` → Logs. Look for POST /owl/submit 4xx. Common: wrong `site_id`, site paused. |
| Lead arrives but no SMS | `lead_sms` column empty, or Twilio balance hit zero. Check `send_sms` logs. |
| Admin URL returns 401 | Token was rotated or site `status='off'`. Check `SELECT * FROM owl_sites WHERE site_id = ?`. |
| Render process restarted, leads from last hour gone | `/tmp/callmeie.db` wipes on redeploy — Render free-tier limitation. Leads were also SMS'd, so nothing permanently lost. Migrate to Postgres when 2nd paying client signs. |
| UptimeRobot false alarm | Render spin-down after 15min inactivity (free tier). 2-consecutive-failure rule on the monitor. |
| Stripe webhook not firing | Dashboard → Developers → Webhooks → check event delivery log. Secret in env var must match. |

**Escalation:** if nothing in the table above applies, file an issue in
the CallMeIE GitHub repo with the Render log tail attached.

---

## Appendix A · First real-site wiring test (our own sites)

The first two sites we wire to `/owl/submit` are **our own** so the
playbook is tested end-to-end before a paying client sees it:

1. `rathborne-dental` (the industry sample) — as if it were a real
   Dublin 15 practice. `site_id = rathborne-dental-demo`. Proves the
   industry-sample → production flow works.
2. `owl-studio-sales` — the contact form on `websites.owlzone.trade`
   itself. `site_id = owl-studio-sales`. Proves the backend works for
   our OWN lead capture before we use it for clients.

Both are registered via `POST /owl/sites`, both get an admin dashboard
URL, both send SMS to the owner on every lead. If either of these
breaks, stop onboarding real clients until fixed.
