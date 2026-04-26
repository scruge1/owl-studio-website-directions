# Owl Studio — Running Context

## Status (2026-04-26)

Active client agency project. Gallery + 7 demo sites live.

## Live surfaces

| URL | Status | Notes |
|---|---|---|
| https://websites.owlzone.trade | Live, HTTPS | Gallery + 10 directions. Cert expires 2026-07-20 (auto-renew). |
| /demos/vetcare-limerick | Live | Fraunces Variable font. Mobile fix shipped 2026-04-25. |
| /demos/curtin-electrical | Live | tokens.css fix shipped 2026-04-26 |
| /demos/slaney-dental-wexford | Live | |
| /demos/aran-vets-galway | Live | |
| /demos/murphy-plumbing-cork | Live | |
| /demos/strand-road-dental | Live | |
| /demos/clancys-restaurant-cork | Live | HeroFullBleed + ScrollNarrative |

## Recent work (last 5 commits)

- `aa6bb87` fix(curtin-electrical): add missing tokens.css, fix broken path
- `54de7a8` fix(demos): self-host GSAP to fix animations in DuckDuckGo browser
- `f227329` fix: 3 audit bugs — duplicate ID, fetch error handling, focus trap
- `94f173b` feat: Lab samples open in overlay too
- `191933b` feat: full-screen demo preview overlay

## Pipeline

Build: design-hub `clients/[slug]/dist/` → copy to `demos/[slug]/` → commit → push main → GitHub Pages rebuilds ~30s.

Image pipeline: Tier 3 Pollinations `model=turbo` (free, 35s delays). JPEG magic-byte check `ffd8ff` required.

## Read on any infra session

`INFRA.md` in this repo — sole source of truth for Hetzner VPS, Coolify, Stripe, Porkbun DNS, CallMeIE routes.
