# DRAFT — RESEARCH-WEB-MOTION-STACK.md

**Status:** DRAFT — pending Adam press-back per second-thing-protocol
**Proposed destination:** `C:\Users\a33_s\Desktop\claude MCPs\New repos\owl-studio-website-directions\RESEARCH-WEB-MOTION-STACK.md`
**Source audit:** Image Utility Audit Pass 5 (frozen 2026-04-30T19:45:00Z)
**Image source:** AXIS-04 (web-motion) + AXIS-06 (web-design)

---

## Purpose

Owl Studio research file documenting the web-motion + design-system primitives stack. Covers:
- 17 motion tools from AXIS-04
- Design-system primitives from AXIS-06 (token-author, taste-skill, design-hub already INSTALLED)
- Paste-into-Claude flow — how Adam routes motion needs into existing skills
- Cross-links to existing taste-skill / style-match-call / design-hub

**Constraints traveling with this file:**
- **No CONSENT-GATE** required — pure motion design has no deepfake/voice/face issue.
- **No AGPL-3.0** in this stack.
- **GSAP DrawSVG** is commercial paid plugin tier ($99–$499/yr) — flag separately.

---

## Existing INSTALLED motion stack (cross-reference)

Adam already has these — extension via dep-ingest only:

| Tool/Skill | Status | Path |
|---|---|---|
| **`web-motion` skill** | INSTALLED | `~/.claude/skills/web-motion/SKILL.md` (master motion design vocabulary) |
| **`scroll-animation` skill** | INSTALLED | `~/.claude/skills/scroll-animation/SKILL.md` (Astro+GSAP scroll-driven animation) |
| **`css-motion-design` skill** | INSTALLED | `~/.claude/skills/css-motion-design/SKILL.md` (CSS-only modern techniques) |
| **`taste-skill`** | INSTALLED | anti-slop frontend guardrails |
| **`token-author`** | INSTALLED | client design tokens (brand.json + Style Dictionary) |
| **`new-service-site`** | INSTALLED | orchestrator that wires motion into client sites |
| **`site-qa`** | INSTALLED | quality gate (motion guards, breakpoints, GSAP pin conflicts) |

**Topology gap:** the `web-motion` skill is NOT yet ingested into Hermes. One-line `hermes_ingest skill-web-motion` fixes this (Rank 4 in top-25 stack-rank).

**Toolkit gap:** 23 GSAP sub-skills exist in `awesome-claude-code-toolkit` but are not routed in `rules-deferred/skill-triggers.md`. Workflow update unlocks them (Rank 11).

---

## Tools to dep-ingest (P0–P1 unlocks)

### 1. Remotion (P0 — RANK 16)
- **Repo:** github.com/remotion-dev/remotion (Remotion License — free for individuals + small teams)
- **License:** Remotion (custom; commercial OK for small companies, paid for ≥4 employees on commercial use)
- **What it does:** Declarative React-based video composition. Render frame-by-frame from React components.
- **Why-Adam-cares:** Bridges web-motion ↔ video-gen. Programmatic video from same React idioms used in client sites. Slot fits between `web-motion` skill and HeyGen/Runway video-gen.
- **Cost:** free for Adam (≤3 employees).
- **Next-action:** `_dep_notes/remotion.md` per dep-ingest skill + skill route into `web-motion` skill §5.

### 2. framer-motion (P1 — RANK 22)
- **Repo:** github.com/framer/motion (MIT)
- **License:** MIT
- **What it does:** Declarative spring physics animation library for React. The default for React-based UI motion.
- **Why-Adam-cares:** Already used in many `new-service-site` outputs implicitly; explicit dep-ingest pins API surface.
- **Cost:** free (npm).
- **Next-action:** `_dep_notes/framer-motion.md`.

### 3. GSAP (P1 — RANK 11 toolkit routing)
- **Repo:** github.com/greensock/GSAP (Standard "no charge" license; paid for some plugins)
- **License:** GreenSock standard (free for most uses; commercial paid for plugins like DrawSVG, MorphSVG, SplitText)
- **What it does:** Industry-standard JavaScript animation library. Timeline, ScrollTrigger, Observer.
- **Why-Adam-cares:** Already implicit via `scroll-animation` skill. 23 GSAP sub-skills exist in `awesome-claude-code-toolkit`. Routing them via `skill-triggers.md` §13 unlocks them without any new code.
- **Cost:** core free; paid plugins $99–$499/yr.
- **Next-action:** update `rules-deferred/skill-triggers.md` §13 with GSAP toolkit row + alias `aw:gsap-*`.

### 4. Lottie + LottieFiles GraphQL (P1 — RANK 23)
- **Repo:** github.com/airbnb/lottie-web (MIT) + lottiefiles.com (proprietary asset library)
- **License:** MIT (player) / commercial (asset library)
- **What it does:** Vector animation player for After Effects → JSON. LottieFiles GraphQL = programmatic asset access.
- **Why-Adam-cares:** Already in `scroll-animation` skill. Explicit dep-ingest captures API surface.
- **Cost:** player free; LottieFiles Pro $25/mo for asset library.
- **Next-action:** `_dep_notes/lottie.md`.

### 5. anime.js (P2)
- **Repo:** github.com/juliangarnier/anime (MIT)
- **License:** MIT
- **What it does:** Lightweight alternative to GSAP. Simpler API, smaller bundle.
- **Why-Adam-cares:** Use case: client sites that need <50KB animation budget.
- **Cost:** free.
- **Next-action:** `_dep_notes/animejs.md`.

### 6. react-spring (P2)
- **Repo:** github.com/pmndrs/react-spring (MIT)
- **License:** MIT
- **What it does:** Spring physics library, lower-level than framer-motion.
- **Cost:** free.
- **Next-action:** `_dep_notes/react-spring.md`.

### 7. Snap.svg (P3)
- **Repo:** github.com/adobe-webplatform/Snap.svg (Apache-2.0)
- **License:** Apache-2.0
- **What it does:** SVG morphing and manipulation.
- **Cost:** free.
- **Next-action:** `_dep_notes/snapsvg.md` (research-only; preserve).

---

## 3D / WebGL stack (toolkit routing only)

### 8. Three.js / Babylon.js / PixiJS (P1 — toolkit routing)
- All three exist as toolkit skills in `awesome-claude-code-toolkit`. Not routed in `skill-triggers.md`.
- **Next-action:** add toolkit row in `rules-deferred/skill-triggers.md` §13.

### 9. WebCodecs / WebGPU (HARDWARE constraint)
- **WebCodecs:** browser-native; documented in `web-motion` §9.
- **WebGPU:** browser-native; **Vega 8 driver does not support** — annotate constraint.

---

## DESIGN-SYSTEM Sub-stack (AXIS-06)

### 10. Figma (P0 — only AXIS-06 GAP that ranks)
- **License:** proprietary (free tier + paid)
- **What it does:** Industry-standard design tool. Design-to-code bridges via plugins / API.
- **Why-Adam-cares:** Closes the design-handoff gap for client work. Currently no MCP wrapper.
- **Cost:** Free Starter, Professional $15/mo per editor.
- **Next-action:** `~/.claude/skills/figma/SKILL.md` + research API → MCP wrapper plan.

### 11. v0.dev (P1)
- **License:** proprietary (Vercel)
- **What it does:** Claude-powered React component generator with instant deploy.
- **Why-Adam-cares:** Adjacent to `new-service-site` orchestrator — could supply candidate components.
- **Next-action:** `~/.claude/skills/v0-dev/SKILL.md` (after Figma).

### 12. 21st.dev (P1)
- **License:** OSS-friendly
- **What it does:** Generative design / component library.
- **Next-action:** `~/.claude/skills/21st-dev/SKILL.md`.

### 13. Stitch, Mockuuups Studio, Lovable, Bolt.new, Framer, Webflow, Wix, Shopify, Builder.io, Relume (research only)
- All drop on architectural fit — `taste-skill` + `token-author` + `new-service-site` cover the chosen design pipeline.
- **Next-action:** preserve as research-direction; no skill creation.

---

## Paste-into-Claude flow (workflow primitive)

The "paste-into-Claude" pattern Adam uses for motion work:

1. Adam pastes a reference URL or screenshot into Claude Code.
2. Claude routes via `~/.claude/skills/website-clone/SKILL.md` (already INSTALLED) → extract visual system.
3. Claude routes via `~/.claude/skills/taste-skill/SKILL.md` to filter AI-slop tells.
4. Claude composes via `web-motion` + `scroll-animation` + `css-motion-design` skills.
5. Output runs through `~/.claude/skills/site-qa/SKILL.md` for breakpoint + motion-guard checks.

**Topology gap:** the `paste-into-Claude` flow is implicit — not documented as a skill. Proposal: NEW `~/.claude/skills/paste-design-reference/SKILL.md` to formalize. (Defer until after Figma skill ships.)

---

## design.md pattern

Adam already uses a `design.md` pattern in client repos. Capture as Anamnesis architecture-reference (proposed): `architecture-reference: client-design-md-pattern`. One-pager describing:
- file location: `<client-repo>/design.md`
- contents: brand hex codes, font choices, motion tier (none/light/medium/heavy), component checklist
- Producer: `token-author` skill writes brand.json → exports tokens.css → captured into design.md
- Consumer: `new-service-site` orchestrator reads design.md to seed section-builder agents

**Next-action:** Anamnesis architecture-reference entry — not a new skill (existing skills already implement the pattern).

---

## Cross-axis links

- **Faceless-media** ↔ AXIS-03 — Remotion bridges into video-gen.
- **Voice-tts** ↔ AXIS-05 — `web-motion` interactions can drive voice-narrated demos.
- **Web-design** ↔ AXIS-06 — Figma + v0.dev + 21st.dev cover design-system tooling.

---

## Open questions for Adam

1. **Remotion install:** OK to dep-ingest now? (Free for Adam at <4 employees.)
2. **GSAP toolkit routing:** add §13 row in `skill-triggers.md`?
3. **Figma skill priority:** P0 design-to-code bridge, or defer behind avatar/video work?
4. **`paste-design-reference` skill:** formalize the implicit pattern, or wait for the next time it shows friction?
5. **`design.md` Anamnesis entry:** capture as architecture-reference?

---

## Provenance

Every claim traces to:
- AXIS-04-web-motion.md / CONFIRM-04-web-motion.md
- AXIS-06-web-design.md / CONFIRM-06-web-design.md
- GAP-ROUTING.md AXIS-04 + AXIS-06 routing rows

---

**DRAFT END**
