# Owl Studio — Website Directions · Claude Routing Surface

## What this is

Sales-pitch static site for **Owl Studio**, a web design business being
launched from this domain. Purpose: a prospect lands on the site,
browses ten website "directions" (distinct visual/structural styles),
picks one that fits, and emails the studio to start a project.

- **Live (HTTP)**: http://websites.owlzone.trade/
- **Live (HTTPS)**: pending cert issuance — see "HTTPS status" below
- **GitHub**: https://github.com/scruge1/owl-studio-website-directions
- **Deploy model**: GitHub Pages (legacy, `main` branch, `/` root)
- **Domain**: Porkbun — `websites.owlzone.trade` CNAME → `scruge1.github.io`
- **Contact**: callmeie@proton.me

## Mode

Collaborator mode. Same gates as the parent `New repos/CLAUDE.md`:
research · prototype-before-batch · save · live demo · business intent ·
real automation · routed writeback.

## What landed before this handoff (Codex session, 2026-04-20 ~20:48 UTC)

Codex built the entire static site in one commit (`ffd6459`) and stood
up DNS + GitHub Pages. Listed in order of what a fresh reader should
inspect:

- `index.html` — minimal redirect shell; `<meta http-equiv="refresh">`
  to `interactive-gallery.html`. Keeps `/` working if someone types
  the bare domain.
- `interactive-gallery.html` — the actual sales page. Hero, samples
  section placeholder (rendered at runtime), closing CTA. Modal for
  expanded views of any sample.
- `interactive-gallery.{css,js}` — chrome for the gallery, modal
  open/close, overall layout.
- `unique-samples.{css,js}` — the ten website directions rendered as
  cards inside `<section id="samples">`. This is the sales content.
- `renders/` — three hero image PNGs used in the hero stack:
  `02-chrome-commerce.png`, `06-local-growth-engine.png`,
  `10-heritage-story.png`.
- `CNAME` — `websites.owlzone.trade` (committed; this file is how
  GitHub Pages reads the custom domain).

**Typography**: Archivo, DM Sans, Fraunces, JetBrains Mono (Google Fonts).

## HTTPS status (as of handoff)

```
status:                   built
cname:                    websites.owlzone.trade
https_enforced:           false
protected_domain_state:   None      ← cert not yet issued
build_type:               legacy
```

DNS has propagated cleanly (1.1.1.1, 8.8.8.8, 9.9.9.9 all return
GitHub Pages IPv6 addresses). There is no CAA record blocking
Let's Encrypt. GitHub simply hasn't completed Let's Encrypt issuance.

Typical wait: 5 min – several hours after DNS is live. Codex
confirmed DNS at roughly the same time as commit, so the cert should
arrive on its own. If more than ~24h elapses:

1. Remove custom domain via GitHub Pages settings (or via
   `gh api /repos/scruge1/owl-studio-website-directions/pages -X PUT
   --input -` with `{"cname": null}`)
2. Wait ~30s
3. Re-add the CNAME (same endpoint with `{"cname": "websites.owlzone.trade"}`)

This forces GitHub to re-kick the cert flow.

To test when it's ready:
```bash
curl -s -o /dev/null -w "%{http_code}\n" https://websites.owlzone.trade/
# 200 means cert issued
```

Then enable enforcement:
```bash
gh api repos/scruge1/owl-studio-website-directions/pages -X PUT \
  --input - <<<'{"https_enforced": true}'
```

## Working tree

```
owl-studio-website-directions/
├── CNAME                          (websites.owlzone.trade)
├── index.html                     (redirect shell)
├── interactive-gallery.html       (main page)
├── interactive-gallery.css        (page chrome)
├── interactive-gallery.js         (gallery + modal logic)
├── unique-samples.css             (sample-card styles)
├── unique-samples.js              (10 website-direction definitions)
├── renders/                       (hero images)
│   ├── 02-chrome-commerce.png
│   ├── 06-local-growth-engine.png
│   └── 10-heritage-story.png
└── CLAUDE.md                      (this file)
```

No build step. Push to `main`, GitHub Pages rebuilds in ~30s.

## Acceptance for "live as a sales pitch"

A shareable link is sales-ready when **all** of:

- [ ] HTTPS works without browser warnings
- [ ] Root `/` redirects to gallery without flicker
- [ ] All ten sample cards render without console errors
- [ ] Modal opens on click, closes on ESC / outside click / X button
- [ ] Hero images load (the three poster cards)
- [ ] `mailto:` CTA opens the email client with the right subject line
- [ ] Mobile viewport 375px renders cleanly
- [ ] `<title>` and `<meta description>` are specific (not generic)
- [ ] OG / Twitter preview cards work (og:image, og:title, og:description)

Untested from here: social preview (`og:image`), Lighthouse score,
SEO sitemap. Worth verifying once HTTPS is live.

## Next punch-list (P0 → P5)

### P0 — HTTPS live + enforcement

Wait for GitHub cert → enable `https_enforced: true` → verify browser
padlock. Poll with the curl check above every ~30 min. If nothing in
24h, do the CNAME re-add dance.

### P1 — Social preview cards (OG + Twitter)

Current `<head>` has `<title>` + `<meta description>` but nothing for
Open Graph or Twitter. A shared link in WhatsApp / Slack / LinkedIn
will render as a naked URL. Add:

- `<meta property="og:title" content="Owl Studio · Website Directions">`
- `<meta property="og:description" content="…">`
- `<meta property="og:image" content="https://websites.owlzone.trade/renders/…">`
- `<meta property="og:url" content="https://websites.owlzone.trade/">`
- `<meta name="twitter:card" content="summary_large_image">`
- Same image should be 1200×630 for best render; repurpose one of
  the three hero PNGs (they're likely 1600×1200 or so — verify).

### P2 — 10 samples content review

Read through `unique-samples.js` — each of the ten directions should:
- Have a specific, non-generic name (no "Modern Business" / "Clean
  Corporate" filler)
- List 3–5 concrete section names (not "About", "Services", "Contact"
  — something distinctive per direction)
- Name a target audience (product · local service · SaaS · clinic
  · finance · trades · AI · story-led)
- Have a credible CTA appropriate to the direction

If any feel generic, rework them. Nothing should read as AI filler —
this is the sales pitch.

### P3 — Favicon + PWA polish

No `<link rel="icon">` currently. Add an owl-themed favicon (SVG ideal
for sharpness). Optional but professional: `manifest.json` +
`apple-touch-icon`.

### P4 — Contact form alternative

`mailto:` is fine for v1 but loses prospects who don't have a mail
client configured. Consider:
- A Formspree / Basin embed that POSTs to callmeie@proton.me
- A simple GitHub Form (Issues backed)
- A Cloudflare Pages Function if we ever migrate off GitHub Pages

Medium effort; adds real lead capture.

### P5 — Analytics + conversion tracking

Once traffic starts: a lightweight analytics setup (Plausible,
Umami self-hosted, or Cloudflare Web Analytics — anything not Google
for ethics). Track only `#samples` clicks, modal opens, and the
`mailto:` CTA click. Three events is enough to measure the funnel.

## Anti-scope (do NOT do)

- No heavy framework migration (Next.js / React) — the site is
  purposely static HTML/CSS/JS for max reliability and zero build step
- No account / auth system — sales pages don't need it
- No premature A/B testing — get it live, advertise, then measure
- No ordering mass runders / new imagery until the existing three
  hero images are confirmed to carry the message
- No switching hosts — GitHub Pages is fine for v1

## Where else to look

- Live URL: http://websites.owlzone.trade/
- GitHub repo: https://github.com/scruge1/owl-studio-website-directions
- Porkbun DNS dashboard: owned by scruge1
- Contact inbox: callmeie@proton.me
- Parent routing: `C:/Users/a33_s/Desktop/claude MCPs/New repos/CLAUDE.md`
