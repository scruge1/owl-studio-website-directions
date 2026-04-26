# Owl Studio — Next Steps

## Open punch-list (P1 → P5)

### P1 — Social preview cards (OG + Twitter) — NOT DONE
Current `<head>` has title + description but no OG/Twitter tags. Shared links render as naked URLs.
Add to `interactive-gallery.html`:
- `og:title`, `og:description`, `og:image` (1200×630 from one of the three hero PNGs), `og:url`
- `twitter:card: summary_large_image`

### P2 — 10 samples content review
Read `unique-samples.js` — every direction must have: specific non-generic name, 3–5 concrete section names, named target audience, credible CTA. Nothing generic / AI-filler.

### P3 — Favicon + PWA polish
No `<link rel="icon">` present. Add SVG owl-themed favicon. Optional: `manifest.json` + `apple-touch-icon`.

### P4 — Contact form alternative
Current `mailto:` loses prospects without a mail client. Options: Formspree, Basin, or Cloudflare Pages Function.

### P5 — Analytics
Plausible / Umami / Cloudflare Web Analytics. Track: `#samples` clicks, modal opens, `mailto:` CTA. Three events.

## Agency expansion
- Second client brief: ready when brief arrives. Pipeline: 6 remaining section templates, Dental/Trades presets.
- New-service-site skill: `~/.claude/skills/new-service-site/SKILL.md`
