# PDR · Dental × Swiss Editorial — industry prototype #1

> Protoype-before-batch. This is the single strongest Irish SMB Pro-tier
> archetype (high AOV, compliance-trained, stable services, rarely touches
> the site post-launch). If this sample lands, the other 9 verticals get
> dispatched under the same pattern.

## Pre-Design Gate — installed tools declared

| Tool | Path | Used for |
|---|---|---|
| `ui-ux-pro-max` (Row 1 Minimalism / Swiss) | `~/.claude/skills/ui-ux-pro-max-skill/src/ui-ux-pro-max/data/styles.csv` | Canonical palette, tokens, type spec |
| `frontend-design` (anti-AI-slop) | `~/.claude/plugins/cache/claude-plugins-official/frontend-design/unknown/skills/frontend-design/SKILL.md` | Stop generic AI tells, editorial voice |
| `parallel-skill-dispatch` pattern | `~/.claude/skills/parallel-skill-dispatch/SKILL.md` | Single-agent industry brief template |
| `awesome-design-md` | local clone | Editorial pro-services brand spec reference |

## Real Irish context

| | |
|---|---|
| Practice name | **Rathborne Dental** |
| Location | Rathborne Village, Ashtown, Dublin 15, D15 P2C3 |
| Principal | Dr. Aoife Ní Dhálaigh, BDS (NUI), MFDS RCSI |
| Founded | 2014 |
| Team | 3 dentists · 2 hygienists · 5 support |
| Phone | 01 555 0148 (placeholder but correctly Dublin-formatted) |
| Email | hello@rathbornedental.ie |
| Reg. | Dental Council of Ireland Reg. No. DC-12345 (format placeholder) |
| Insurance | Accepts VHI, Laya, Irish Life Health, PRSI Treatment Benefit |

## Services (6)

1. **General dentistry** — checkups, fillings, hygiene
2. **Cosmetic** — veneers, composite bonding, in-chair whitening
3. **Invisalign / clear aligners**
4. **Dental implants** — single tooth to full arch
5. **Emergency same-day** — same-day triage for acute pain
6. **Children's dentistry** — from 2 years, under the PRSI children's scheme

## Page sections (in order)

1. **Topbar** — small mark · phone · "Book" CTA
2. **Hero** — heavy serif headline with one italicised word · single taupe accent rule · "accepting new patients" status pill · primary + secondary CTA
3. **First-visit strip** (3 columns) — "What to expect" / "Fees & insurance" / "Bring these on the day"
4. **Services grid** — 6 editorial cards (Fraunces serif + JetBrains Mono label + rule divider)
5. **Team** — 3 dentist cards with credentials, year qualified, special interest
6. **Testimonials** — 3 editorial pull-quotes on beige paper, first-name-only attribution (GDPR)
7. **Fees & FAQ** — typographic list with dot-leader pattern for prices (e.g., `Examination · · · · · €60`)
8. **Opening hours + location** — clean grid with the Dublin 15 address
9. **Footer** — Dental Council reg · GDPR · Practice Policies · privacy PDF link

## Anti-patterns (must NOT appear)

- Stock smile photos / toothbrush icons / white-coat cliché
- "Transforming smiles" / "Your smile is our passion" taglines
- Emojis
- Glassmorphism, gradients, neon accents
- Purple → blue hero gradients
- Centered hero with a big round photo
- Inter / Space Grotesk / Poppins fonts
- Frosted cards, floating 3D elements
- Vague "Modern dental care for the whole family" filler
- Any SaaS / tech-startup vocabulary
- Any copy that could apply to any dentist in any country

## Style spec (from ui-ux-pro-max Row 1)

| Token | Value |
|---|---|
| `--ink` | `#000000` |
| `--paper` | `#FFFFFF` |
| `--cream` | `#F5F1E8` |
| `--grey` | `#808080` |
| `--taupe` (single accent) | `#B38B6D` |
| `--rule` | `#000000` 2px or 3px solid |
| `--spacing` | `2rem` |
| `--radius` | `0` |
| `--display` | `"Fraunces", Georgia, serif` |
| `--sans` | `"Inter Tight"` — **NO**. Use `"Archivo", system-ui` |
| `--mono` | `"JetBrains Mono"` |
| Shadows | **none** |

## Responsive

- Desktop first, collapse at 900px then 640px
- Must include the mobile-fit safety net (added automatically via `<!-- mobile-fit-safety -->` — agent should preserve it if generating from scratch, or let `scripts/patch-mobile-fit.py` add it on write)

## File path

`samples/industries/01-dental-swiss.html`

Self-contained single HTML file. Google Fonts only external dep.

## Acceptance criteria (must all be true before user review)

- [ ] Every piece of text is specific to Rathborne Dental — no generic filler
- [ ] "Accepting new patients" status pill visible above the fold
- [ ] Services grid uses editorial typography rhythm, not card-stack sameness
- [ ] Fees section uses dot-leader pattern for real €-denominated prices (Exam €60, Hygiene from €95, Composite filling from €140, Whitening €395, Veneer €850/tooth, Implant from €2,400)
- [ ] Team section names 3 dentists with their year of qualification + one line of interest
- [ ] Dental Council registration + GDPR language in footer (Irish-compliant)
- [ ] Serif display type = Fraunces, **no** Inter/Space Grotesk
- [ ] Single taupe accent #B38B6D, used sparingly
- [ ] No emoji, no gradients, no glass, no centered-hero-with-big-photo
- [ ] Renders cleanly on 375px mobile without horizontal scroll
- [ ] Renders cleanly on 1440px desktop with editorial spacing
- [ ] All CTAs resolve: "Book" → `#book`, phone → `tel:`, email → `mailto:`
- [ ] File loads < 200ms on localhost (no heavy assets)

## What happens after sign-off

If the prototype lands, the other 9 industries dispatch in parallel — each with its own industry PDR block, each with its own paired style from the gallery:

| # | Vertical | Style | PDR |
|---|---|---|---|
| 01 | Dental | Swiss Editorial | **this file** |
| 02 | Solicitor | Swiss Authority (dark-biased) | TBD |
| 03 | Accountant | Minimalism numbers-forward | TBD |
| 04 | Private physio | Neumorphism soft-healing | TBD |
| 05 | Opticians | Glassmorphism lens-clarity | TBD |
| 06 | Audiologist | Aurora UI calm-tech | TBD |
| 07 | Veterinary | Claymorphism pet-friendly | TBD |
| 08 | Insurance/financial | Brutalism editorial (cream+black) | TBD |
| 09 | Architecture | 3D Hyperrealism tactile | TBD |
| 10 | Aesthetic clinic | Aurora UI luxe | TBD |

Each batch agent gets: this template PDR, their vertical's real Irish context, their paired style tokens, their anti-pattern list.
