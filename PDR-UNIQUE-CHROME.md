# PDR · Per-Sample Unique Chrome

**Problem**: The 10 gallery cards share the same `.site-card` +
`.mini-browser` outer frame — identical `border-radius: 34px`,
identical border tint, identical shadow. Readers see "ten variations
of the same rounded card" rather than ten websites. Main-page buttons
(`.pill`, `.button`, `.poster-card`) also use 999px / 34px radius, so
the homepage doesn't visually stand apart from any sample either.

**Goal**: Each of the 10 sample cards should feel like a different
website. Main-page chrome should feel like the Owl Studio brand,
visibly unlike every sample.

**Acceptance**:
- No two samples share their `border-radius` value
- No two samples share their border treatment (style / width / colour
  behaviour)
- No two samples share their shadow style
- Main-page `.button`, `.pill`, `.poster-card` do not use the 999px
  pill radius or the 34px card radius (shared with samples)
- Silhouette test: cover all text / colour and the 10 shapes are still
  identifiable as distinct
- Mobile 375px still works (each style's override holds)

**Reference material** (don't reinvent):
- `~/Desktop/design-hub/advert-web-design-samples/source-longform-sample-pack.html`
  already encodes each direction's aesthetic via CSS variables
  (`.site-1` through `.site-10`) and `::before` decorations. Adapt those.
- `~/Desktop/design-hub/foundation/ANTI-PATTERNS.md` — avoid purple-to-blue
  gradients, glassmorphism-everywhere, Inter as display, pure black,
  generic pill-and-card sameness.
- `~/Desktop/design-hub/CLAUDE.md` — the Reference→Extract→Specify
  →Assemble→Render→Review loop.

## Per-direction chrome

| # | id | layout class | Outer silhouette |
|---|----|---|---|
| 1 | copper | `.layout-product` | Asymmetric rounded: `46px 46px 4px 4px`. No border. Warm amber double shadow. Cream paper page-bg bleed at the top. |
| 2 | chrome | `.layout-commerce` | Sharp `0` corners. Neon-green 1px hairline border + soft lime glow. Inset top highlight stroke. |
| 3 | quiet | `.layout-saas` | Flat `10px` corners. No shadow. Hairline `rgba(130, 119, 255, 0.2)` border. Sits flush. |
| 4 | trust | `.layout-trust` | `2px` corners, stamp-like. `2px solid navy` border + `0 3px 0 navy` offset so it reads as a printed form. |
| 5 | editorial | `.layout-editorial` | Zero corners, −0.5° slight tilt, hard paper shadow `6px 6px 0 rgba(180, 86, 62, 0.25)`. Cream bg. Printed-page feel. |
| 6 | growth | `.layout-growth` | Asymmetric corners `26px 4px 26px 4px` (poster). Deep forest bg. Glow-free dark shadow. |
| 7 | clinic | `.layout-clinic` | Pebble shape: `84px 20px 84px 20px`. Soft warm shadow. No border. Spa-like. |
| 8 | ops | `.layout-ops` | `6px` corners (compact terminal). Cyan hairline. Inset glow from top. Monospace grid feel. |
| 9 | trades | `.layout-trades` | Zero corners. `4px solid ink` border. `8px 8px 0 ink` hard-offset shadow (emergency poster). |
| 10 | heritage | `.layout-heritage` | `2px` corners. Dark brown + gold hairline. Inset vignette. Archive-plate feel. |

## Inner `.mini-browser` treatments

The uniform "browser window chrome" (.mini-browser padding, radial
gradient ::before, standard h3 sizing) also has to vary per layout so
the inside matches the outside:

- copper · rail-padded (32px all-round) with warm soft gradient corner
- chrome · inset neon gradient from bottom, grid dots pattern faint
- quiet · minimal 20px padding, no gradient, hairline divider rail at
  the top
- trust · column-grid inside with 2px rule under the mini-nav
- editorial · serif headline, column-rule, justified body feel
- growth · forest-dark interior, green accent gradient at hero
- clinic · cream-warm, gentle radial, no hard edges inside
- ops · grid of monospace cells visible through the .mini-visual
- trades · yellow interior, diagonal 24HR stamp overlay
- heritage · dark-brown sepia, gold hairlines, centred serif

## Main-page chrome (distinct from every sample)

- `.pill` → small-caps `font-variant`, `2px` corners, cream bg,
  3px-bottom underline in `--accent-ink`. Looks like an old shop
  label. Not a pill.
- `.button` → asymmetric: `10px 2px 10px 2px`. Dark ink bg. Warm amber
  inset top-highlight (`inset 0 1px 0 rgba(...)`). Different from all
  samples.
- `.button.secondary` → hairline 1px outline, squared 2px corners.
- `.poster-card` → no border-radius. Warm amber hard-offset shadow
  `10px 10px 0 rgba(...)`. Looks like pinned paper, not a rounded
  tile.
- `.brand-mark` (owl circle in topbar) — change 50% circle → slightly
  squared (`10px`), feels like a wax seal.

## Impact

- CSS only. No DOM changes. No JS changes.
- Styles are additive via the `.layout-*` selector that Codex already
  emits on `<article>`. All modal behaviour stays untouched.
- Mobile grid collapses 2→1 col; each card's unique silhouette still
  reads.

## Process

1. Prototype site-1 (copper) first → verify locally in Chrome.
2. If silhouette passes the cover-text test and the anti-pattern gate,
   batch the other nine.
3. Finally, update `.pill` / `.button` / `.poster-card` / `.brand-mark`
   so main page reads as its own brand.
4. Push → wait for Pages rebuild → verify at the live URL.

## Anti-scope

- No new illustrations / renders (use what exists in `renders/`).
- No framework migration (still plain HTML/CSS/JS).
- No typography changes to the sample H3 per direction — that already
  differs per layout via `--headline`.
- No new copy or sample content — content review was done last session.
