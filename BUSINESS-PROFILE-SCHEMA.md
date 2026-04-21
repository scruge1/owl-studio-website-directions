# Business Profile Schema · Owl Studio

> One client → one `profiles/<slug>.json` → templates render ALL pages
> with their actual data baked in. No hand-editing per client.
>
> This is the normalised-data pattern Family Tree used
> (`data/normalized/people.json` → React → UI) applied to client websites:
> onboarding form → profile JSON → template → deployed site.
>
> **Rule**: every field a template uses must live here. If a template
> hardcodes a value that should be per-client, move it to this schema
> and back-populate every existing profile.

---

## 1 · Schema (v1, 2026-04-21)

The profile is a single JSON object. Keys marked `*` are required; all
others optional-but-templates-should-handle-missing. Comments are shown
here only; remove them when writing the JSON file.

```jsonc
{
  // === Identity ===
  "slug*":            "rathborne-dental",           // kebab-case, used as site_id + file name
  "display_name*":    "Rathborne Dental",           // appears in headlines, emails, footers
  "vertical*":        "dental",                     // dental | solicitor | accountant | physio | opticians |
                                                    // audiologist | vet | financial | architect | aesthetic
  "template*":        "01-dental-swiss",            // which industry sample to render from
  "tagline*":         "General, cosmetic and implant dentistry in Ashtown, Dublin 15",

  // === Location ===
  "address*": {
    "line1":          "Rathborne Village",
    "line2":          "Ashtown",
    "city":           "Dublin 15",
    "eircode":        "D15 P2C3",
    "country":        "Ireland"
  },
  "map_link":         "https://maps.google.com/?q=Rathborne+Village+Ashtown+Dublin+15",

  // === Contact ===
  "phone*":           "01 555 0148",               // display format — Ireland conventions
  "phone_tel*":       "+35315550148",              // E.164 for tel: links
  "email*":           "hello@rathbornedental.ie",
  "whatsapp":         null,                        // string or null
  "booking_url":      null,                        // external booking system (Calendly etc.)

  // === Hours ===
  "hours": [                                        // list of rows, free-form second column
    { "label": "Mon-Fri",    "value": "08:30-17:30" },
    { "label": "Sat",        "value": "09:00-13:00" },
    { "label": "Sun",        "value": "closed" },
    { "label": "Emergency",  "value": "triage by phone, same day" }
  ],

  // === Key facts shown above the fold ===
  "status_pill*":     "Accepting new patients · next available Tue 29 Apr 2026",
  "established_year*": 2014,
  "kicker*":          "RATHBORNE VILLAGE · ASHTOWN · DUBLIN 15",
  "issue_label":      "EST. 2014 · ISSUE NO. 12",  // editorial accent text (Swiss template uses this)

  // === Hero ===
  "hero*": {
    "headline_prefix":  "Careful dentistry,",      // first line
    "headline_emphasis": "quietly practised.",      // italic second line (renders in serif italic for Swiss)
    "body":             "General, cosmetic and implant dentistry in Ashtown, Dublin 15. Three dentists, one hygiene team, published fees, and a waiting room that isn't trying to sell you anything.",
    "primary_cta":      { "label": "Book first appointment", "href": "#book" },
    "secondary_cta":    { "label": "Call the practice",      "href": "tel:+35315550148" }
  },

  // === Team ===
  "team*": [
    {
      "name":            "Dr. Aoife Ní Dhálaigh",
      "credentials":     "BDS (NUI), MFDS RCSI",
      "qualified_year":  2009,
      "role":            "Principal dentist",
      "interest":        "implantology & full-mouth rehabilitation",
      "bio":             "Aoife opened Rathborne Dental in 2014 after seven years in practices in Galway and south Dublin. She places every implant in the practice and leads on full-mouth rehabilitation cases."
    }
    // ... more team members, same shape
  ],

  // === Services with fees ===
  "services*": [                                    // each row renders as an editorial article
    {
      "kicker":         "GENERAL DENTISTRY",
      "title":          "Exams, fillings, hygiene",
      "body":           "Standard six-monthly care. Two-film intraoral X-rays at the first visit...",
      "fees": [                                     // dot-leader price list
        { "label": "Examination & two X-rays",  "price": "€60" },
        { "label": "Hygiene (scale & polish)",  "price": "from €95" }
      ]
    }
    // ... more services
  ],

  // === Insurance / payment ===
  "insurance": [                                    // simple list of display strings
    "VHI",
    "Laya Healthcare",
    "Irish Life Health",
    "PRSI Treatment Benefit"
  ],

  // === Testimonials (first-name-only per GDPR) ===
  "testimonials": [
    {
      "quote":   "Aoife rebuilt three molars I'd been hiding for a decade. She quoted the whole thing on the first visit, to the euro, and it didn't move.",
      "author":  "Cian",
      "town":    "Ashtown"
    }
  ],

  // === FAQ ===
  "faq": [
    { "q": "Do you take medical cards?",    "a": "Yes — bring your card to the first visit..." },
    { "q": "How long is a check-up?",       "a": "30 minutes for an existing patient, 45 minutes on a first visit." }
  ],

  // === Footer / regulatory ===
  "registration*": {
    "body":   "Dental Council of Ireland",
    "number": "DC-12345",
    "url":    "https://dentalcouncil.ie"
  },
  "gdpr": {
    "contact_email": "privacy@rathbornedental.ie",
    "retention":     "We retain clinical records for 8 years per DPC guidance."
  },
  "policies": [
    { "label": "Privacy policy",       "href": "/privacy" },
    { "label": "Appointment policy",   "href": "/appointments" },
    { "label": "Cancellation policy",  "href": "/cancellation" }
  ],

  // === Brand (per-vertical defaults — rarely overridden) ===
  "brand": {
    "style_tokens": "01-dental-swiss",              // matches template CSS tokens
    "accent":        "#B38B6D",                     // optional per-client accent override
    "logo_svg":      null,                          // inline SVG if supplied by client, else null (wordmark fallback)
    "og_image":      null
  },

  // === Deploy metadata (filled by build pipeline, not by onboarding) ===
  "owl_studio": {
    "site_id":         "rathborne-dental-demo",     // matches owl_sites.site_id in DB
    "tier":            "pro",                       // starter | pro | custom
    "care_tier":       "growth",                    // essential | growth | concierge | null
    "live_url":        "https://rathbornedental.ie",
    "hosted_at":       "cloudflare-pages",          // cloudflare-pages | coolify | etc.
    "launched_date":   "2026-04-21"
  }
}
```

---

## 2 · Per-vertical variations

Each of the 10 industry templates may require extra fields. Additive only —
never drop from the core. Examples:

- **Dental / Physio / Aesthetic / Audiology / Opticians / Vet** (medical): `insurance[]`, `registration.body + number`, `emergency_contact`, `referrals_welcome: bool`
- **Solicitor / Accountant / Financial / Architect** (professional): `practice_areas[]` (like services but different kicker), `engagement_fee_note`, `professional_body.membership_number`, no `insurance`, no `emergency_contact`
- **Vet** (dual-audience): `farm_calls: { area_km: 30, call_out_fee: "€45" }`, `after_hours_rota: { clinic_name, phone }`
- **Solicitor**: add `confidentiality_statement: string` (replaces testimonials)

The template decides what it renders; the profile supplies all raw fields.
A template renderer silently skips missing optional fields.

---

## 2.5 · Two-stage onboarding (mother's feedback, 2026-04-21)

**Problem:** the schema above has 40+ fields. Asking a prospect to fill
all of them before they commit is a guaranteed bounce. Real B2B
buying behaviour — they'll give you 4-6 fields to start; the rest
comes AFTER they've committed, when the cost of the next 10 minutes
of their time is cheap because they're already invested.

**Pattern:** classic two-stage (signup / discovery), mirrors how phone
menus route callers with minimal friction:

### Stage 1 — Signup (lightweight, gets commitment)

6 fields total. Target completion time: **90 seconds**.

| Field | Why |
|---|---|
| Business name | Only way to greet them by name afterwards |
| Contact name + email + phone | Talk to them |
| Business type (pick vertical from list) | Routes to right template; drives every default |
| Tier (Starter / Pro / Custom) | Drives deposit amount |
| Care plan (none / Essential / Growth / Concierge) | Sets recurring revenue on day 1 |

Copy on the form: _"For now, select the package that most suits your
business. We'll tailor and bespoke it with you on the next call — no
homework before you sign up."_

This is what `callmeie-fix/onboard.html` should be trimmed to.

### Stage 2 — Bespoke tailoring (after commitment)

The full Business Profile JSON. Captured across one or more touches
**after** the deposit is paid / the Stripe subscription is active:

- Short discovery call (20 min) populates ~70% of the profile
- Owner writes the remaining fields from the client's existing
  website / email / published fees
- Follow-up email asks for photos, logo, testimonial approvals

Each profile gets a `completeness` tracker (added to schema §1):

```jsonc
"completeness": {
  "identity":    "full",       // slug, display_name, vertical, tagline, address, phone, email
  "hero":        "full",
  "team":        "stub",       // signup captured principal's name only
  "services":    "partial",    // default service list from template, fees TBD
  "testimonials":"none",
  "insurance":   "stub",
  "faq":         "none",
  "brand":       "default"     // template defaults, no custom logo/colours
}
```

Render script treats any section marked `none` / `stub` as missing
and falls back to template-default copy. Client sees the site looking
complete; owner sees the completeness map and knows what to chase.

### Why this matters for workload reduction

- Prospect fills 6 fields → signs up. Friction near-zero.
- Owner fills 34 fields over 1-2 touches after commitment. Low-stakes.
- Renderer merges: `defaults (from template) + stage1 (signup form) + stage2 (discovery)` → output site.
- Each new client's site gets rendered in seconds with whatever
  completeness level is present. No "blank-template, edit-from-zero"
  iterations.

Future form-extension lives behind the login wall, not at signup.
Real clients see progress bars, not questionnaire fatigue.

---

## 3 · Data flow

```
Onboarding form (callmeie-fix/onboard.html)
  ↓ POST /submit-onboarding                    existing endpoint
  ↓
Admin portal reviews + fills gaps
  ↓ writes/confirms profile JSON
  ↓
profiles/<slug>.json  ──────────┐
                                │
samples/industries/<template>.html
  ↓                             │
scripts/render-site.py          │
  (reads both, merges via ──────┘
   Jinja2 / str.replace for v1)
  ↓
client-builds/<slug>/index.html + any sub-pages
  ↓
Cloudflare Pages deploy (per-client account)
```

---

## 4 · Onboarding form → profile mapping

The existing `callmeie-fix/onboard.html` already collects ~60% of the profile.
Gaps to close (future form-extension task):

| Profile field | In form today? | Action |
|---|---|---|
| slug, display_name, tagline | ✓ (as business_name + service) | keep |
| address.{line1,city,eircode} | ✓ (one freeform field) | split into structured sub-fields |
| phone/email | ✓ | keep |
| hours | ✓ (one textarea) | parse or collect rows |
| team[] | ✗ | add: N team-member repeatable block |
| services[].fees[] | ~ (services textarea only) | add fees repeater |
| insurance[] | ✓ (checkboxes) | keep |
| testimonials[] | ✗ | add optional repeatable |
| faq | ✓ (faq_q/a repeater) | keep |
| registration.* | ✗ | add per-vertical field |
| brand.* | ✗ | default per template; optional upload for logo |

Each onboarding submission → review in `/admin` → manual write to
`profiles/<slug>.json` initially. Full form → profile auto-generation
is §6 of backlog.

---

## 5 · Rendering

v1 (shipped today): `scripts/render-site.py` — light find/replace of
template placeholders `{{dotted.path}}` from the profile. Proves the
pipeline end-to-end without adding a template-engine dependency.

v2 (backlog): swap to Jinja2 for proper loops/conditionals. Same
schema, same profile, same inputs — only the renderer changes.

v3 (backlog): Payload CMS (on Coolify) hosts the profile per-client,
client self-edits, static regen on change. Same schema.

---

## 6 · Backlog (schema-related only)

- [ ] Extend `onboard.html` with team/fees/testimonials/registration repeater blocks
- [ ] Build renderer v2 in Jinja2 once three profiles exist and the
      find/replace approach proves its limit
- [ ] Profile validation via JSON Schema / pydantic at intake
- [ ] Per-vertical profile templates (stubbed JSON with prompts for each field)
- [ ] Auto-convert `onboard.html` submissions → profile JSON in `/submit-onboarding`
- [ ] Deploy Payload CMS, move profile storage there
- [ ] Client self-edit portal (Payload editor role, scoped to one project)
- [ ] Preview-on-change: edit profile → rebuild site → redeploy to preview subdomain
- [ ] Diff view: "what changed between this profile revision and last"

---

## 7 · Why we do this now (not later)

User flagged 2026-04-21: _"first designs we often do don't have
everything wired up ... we can't do that for real customers ... we
need to cut our workload down from so many iterations we can solve it
from the start with the right database."_

Without the schema + renderer, onboarding a new client is: copy
`samples/industries/<template>.html` → find-and-replace 40+ hardcoded
strings → notice you missed the footer reg number three iterations in
→ repeat forever. With it: capture data once, render once, deploy.

This PR ships schema v1 + one seed profile (Rathborne Dental,
reverse-engineered from `samples/industries/01-dental-swiss.html`) +
`scripts/render-site.py` proof. Subsequent clients follow the flow.
