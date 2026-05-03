# DRAFT — RESEARCH-VIDEO-STACK.md

**Status:** DRAFT — pending Adam press-back per second-thing-protocol
**Proposed destination:** `C:\Users\a33_s\Desktop\claude MCPs\New repos\owl-studio-website-directions\RESEARCH-VIDEO-STACK.md`
**Source audit:** Image Utility Audit Pass 5 (frozen 2026-04-30T19:45:00Z)
**Image source:** 555-record `Image Intelligence Ledger`

---

## Purpose

Owl Studio research file documenting the video / avatar / faceless-media / web-motion / voice stack. **22 P0 video-axis items** + AXIS-01/02/05 dropped tools. Cross-links to existing faceless-media + web-motion + voice-tts axes.

**Constraints traveling with this file:**
- **CONSENT-GATE:** every avatar / face-swap / voice-clone tool requires explicit consent flow before production use. See `~/.claude/rules/common/security.md` extension proposal.
- **AGPL-3.0:** Wan2GP, OpenMontage, ArcReel are AGPL-viral. Reference-only. Do NOT fork.
- **Hardware:** Vega 8 / 2GB APU eliminates GPU-dependent local inference.

---

## Per-Tool One-Pager Blocks

### 1. HeyGen (P0 — RANK 1 single biggest opportunity)
- **Repo:** heygen.com (proprietary SaaS)
- **License:** proprietary (commercial)
- **Image IDs:** IMG-00173, 00174, 00175, 00176, 00177, 00178, 00179 — 7-image full sequence (largest single workflow in dataset)
- **What it does:** AI avatar studio. 200+ avatars, photo-to-talking-head, lipsync, multi-language voice cloning, social automation.
- **Why-Adam-cares:** Only complete avatar studio in the dataset with a verifiable workflow image sequence. CallMeIE explainer videos + owl-studio client demo videos directly addressable.
- **Cost:** Creator $24/mo, Team $89/mo, Enterprise custom.
- **Consent-gate-applicable:** YES (face-cloning + voice-cloning).
- **Next-action:** spec API + consent flow into `~/.claude/skills/heygen/SKILL.md`. **Defer install until CONSENT-GATE Anamnesis decision is in place.**

### 2. Runway (P0 — RANK 2 cheapest unlock)
- **Repo:** runwayml.com (proprietary)
- **License:** proprietary
- **Image IDs:** IMG-00052
- **What it does:** Text-to-video, image-to-video, video-to-video Gen-3 Alpha. Industry-leading SOTA.
- **Why-Adam-cares:** `.mcp.json` partial entry already exists — finishing the wiring is the cheapest video-gen unlock in the entire stack. No CONSENT-GATE (no face-swap mode required).
- **Cost:** Standard $12/mo (60 credits = ~6 sec video), Pro $35/mo, Unlimited $76/mo.
- **Consent-gate-applicable:** NO (general scene generation; face-swap mode is opt-in).
- **Next-action:** research auth + endpoint, finish MCP wiring binding.

### 3. Luma Dream Machine (P1)
- **Repo:** lumalabs.ai (proprietary)
- **License:** proprietary
- **What it does:** Text-to-video with Pro API tier. Lower deepfake risk than HeyGen (no built-in face-swap).
- **Why-Adam-cares:** Backup video-gen if Runway pricing changes. API stable.
- **Cost:** $9.99 Standard, $29.99 Pro, $94.99 Premier.
- **Consent-gate-applicable:** NO.
- **Next-action:** wrap Pro tier API as MCP-Tool after Runway is wired.

### 4. Pika (P1)
- **Repo:** pika.art (proprietary)
- **License:** proprietary
- **What it does:** Text-to-video, image-to-video. Lipsync, sound effects.
- **Why-Adam-cares:** Adjacent option for short-form social video.
- **Cost:** Free tier, Standard $10/mo, Unlimited $35/mo.
- **Consent-gate-applicable:** YES (lipsync mode).
- **Next-action:** quarterly API-availability monitor; preserve as research.

### 5. Sora (P2 — research only)
- **Repo:** OpenAI (proprietary)
- **License:** proprietary
- **What it does:** Top-tier text-to-video.
- **Why-Adam-cares:** Industry benchmark; API not generally available (2026-04).
- **Next-action:** monitor release; no action.

### 6. Kling, Hunyuan, LTX-Video, Higgsfield, InfiniteTalk (P3 — research only)
- All blocked by some combination of: regional access (China), no GA API, GPU requirement (Hunyuan), academic license (InfiniteTalk), or research-stage status.
- **Next-action:** none.

### 7. Wan2GP (DROPPED — AGPL + face-swap)
- **License:** AGPL-3.0 + face-swap primary purpose.
- **Why-blocked:** compound gate (license viral + consent-gate).
- **Next-action:** none. Awareness only.

### 8. ArcReel, OpenMontage (DROPPED — AGPL viral)
- **License:** AGPL-3.0
- **Why-blocked:** integrating source triggers GPL obligations on Adam's entire codebase.
- **Next-action:** read public README only; do NOT fork.

---

## AVATAR Sub-stack (AXIS-02)

### 9. Synthesia (P0)
- **Cost:** $22/mo Personal, custom Enterprise.
- **Why-Adam-cares:** Multi-language avatars with auto-translation. Enterprise consent gate built into onboarding.
- **Consent-gate-applicable:** YES.
- **Next-action:** enterprise eval, defer behind CONSENT-GATE Anamnesis decision.

### 10. D-ID (P1 — CONSENT-GATE high)
- **What it does:** Photo-to-talking-head; face-swap.
- **Consent-gate-applicable:** YES (deepfake/face-swap primary purpose).
- **Next-action:** research-direction only.

### 11. Tavus (P1 — enterprise CONSENT-GATE)
- **What it does:** Custom avatar training, real-time streaming, personalized video at scale.
- **Cost:** Enterprise custom (~$75-$1000+/mo).
- **Consent-gate-applicable:** YES.
- **Next-action:** enterprise eval.

### 12. Argil (P2)
- **What it does:** Batch avatar generation, no consent rule visible at signup.
- **Consent-gate-applicable:** YES — Adam must add consent flow.
- **Next-action:** research only.

### 13. Hedra (P2)
- **What it does:** Animation + music lipsync.
- **Consent-gate-applicable:** YES.
- **Next-action:** research only.

---

## VOICE Sub-stack (AXIS-05)

### 14. Whisper local (P0 — RANK 3 cheapest cross-axis unlock)
- **Repo:** github.com/openai/whisper (MIT)
- **License:** MIT
- **Image IDs:** IMG-00052, 00058, 00168, 00219, 00224 (5 hits)
- **What it does:** State-of-art speech-to-text (medium/large.v3 models). CPU-only viable on Vega 8.
- **Why-Adam-cares:** Foundation primitive for faceless-media + ASR + diarization + viral-video discovery. 5 image hits = high signal.
- **Cost:** Free.
- **Consent-gate-applicable:** NO (transcription).
- **Next-action:** `pip install openai-whisper` + `_dep_notes/whisper.md` per dep-ingest skill. Skill route into faceless-media + last30days.

### 15. VoxCPM2 (P1)
- **Repo:** github.com/OpenBMB/VoxCPM-2 (Apache-2.0)
- **License:** Apache-2.0
- **Image IDs:** IMG-00100
- **What it does:** Local TTS, 2B params, 30 langs, one-shot speaker cloning.
- **Why-Adam-cares:** Cost savings vs ElevenLabs for non-cloned narration. Privacy gate for sensitive content.
- **Cost:** Free (local compute bound).
- **Consent-gate-applicable:** YES (cloning mode only — narration mode safe).
- **Next-action:** local-inference test + `_dep_notes/voxcpm2.md`.

### 16. ElevenLabs (INSTALLED — extension only)
- **Status:** INSTALLED via gateway MCP.
- **Consent-gate-applicable:** YES for cloning mode.
- **Next-action:** extension to add cloning gate; narration mode unchanged.

### 17. Descript (P0 workflow-doc — CONSENT-GATE)
- **Repo:** descript.com (proprietary SaaS)
- **License:** proprietary
- **Image IDs:** IMG-00358
- **What it does:** Faceless YouTube workflow anchor. Voice cloning + video editing + transcript-based editing.
- **Cost:** Creator $24/mo, Pro $50/mo.
- **Consent-gate-applicable:** YES (voice cloning subset).
- **Next-action:** document workflow; defer voice-clone behind consent flow.

### 18. Izwi (P3 — research only)
- **Repo:** izwiai.com (proprietary)
- **What it does:** On-device voice runtime with cloning + design.
- **Image IDs:** IMG-00507
- **Consent-gate-applicable:** YES.
- **Next-action:** research only; transcription/diarization safe to spike on non-sensitive samples.

### 19. Edge TTS, Kokoro (P3)
- **Edge TTS:** Microsoft enterprise TTS — research only; ElevenLabs covers.
- **Kokoro:** Mentioned in AXIS spec; zero image hits → GAP-RESEARCH; web-research before any routing.

---

## FACELESS-MEDIA Sub-stack (AXIS-03 — assembly skills)

These are the **missing assembly skills** Adam needs to combine Whisper + Scrapling + content-engine + last30days into a faceless-video pipeline. None require CONSENT-GATE on their own (they're glue).

### 20. Reddit→video pipeline skill (P0)
- **Surface:** Skill
- **Image IDs:** IMG-00020, 00021
- **What it does:** Reddit thread → script → TTS → video composition → upload.
- **Cost:** low (Adam has Scrapling + content-engine; this is glue).
- **Next-action:** `~/.claude/skills/reddit-to-video/SKILL.md`.

### 21. Word-level caption sync skill (P0)
- **Surface:** Skill
- **What it does:** Per-word caption alignment for short-form video. Whisper word-timestamps + caption renderer.
- **Cost:** low.
- **Next-action:** `~/.claude/skills/caption-sync/SKILL.md`.

### 22. Character consistency skill (P0)
- **Surface:** Skill
- **What it does:** Prompt-engineering primitive for keeping character consistent across image-gen runs (face/body/clothing).
- **Cost:** medium.
- **Next-action:** `~/.claude/skills/visual-consistency/SKILL.md`.

### 23. Music ducking + beat detection (P0)
- **Surface:** Skill + Prototype
- **What it does:** Audio-engineering primitive — duck music under voice, detect beats for cut timing.
- **Cost:** medium (librosa + ffmpeg).
- **Next-action:** `~/.claude/skills/audio-engineering/SKILL.md` + dep-ingest librosa.

### 24. Platform encoding profiles (P0)
- **Surface:** Skill (extend content-engine)
- **What it does:** Per-platform output profiles (1:1 IG, 9:16 TT/Shorts/Reels, 16:9 YT, 4:5 IG feed) + bitrate / codec / max-length per platform.
- **Cost:** low.
- **Next-action:** `content-engine/encoding-profiles.md`.

### 25. Novelty gate (P1)
- **Surface:** Skill + Memory
- **What it does:** Anti-duplicate / competition-shadowing scan against last30days output before publishing.
- **Cost:** low.
- **Next-action:** `~/.claude/skills/novelty-gate/SKILL.md` + Hermes pattern.

### 26. TikTok pattern primitive (P1)
- **Surface:** Skill (extend last30days)
- **Image IDs:** IMG-00133, 00137
- **What it does:** TikTok-specific pattern extraction (hook structure, sound usage, hashtag clustering).
- **Cost:** low.
- **Next-action:** extend last30days skill.

### 27. Viral video discovery + transcribe (P1)
- **Surface:** Skill
- **Image IDs:** IMG-00170, 00171
- **What it does:** last30days + Whisper compose — discover viral video, transcribe, extract structure.
- **Cost:** medium (depends on Whisper local).
- **Next-action:** `~/.claude/skills/viral-discovery/SKILL.md` (after Whisper).

---

## WEB-MOTION Sub-stack (AXIS-04 — links to RESEARCH-WEB-MOTION-STACK.md)

(Detail in companion file `DRAFTS/DRAFT-RESEARCH-WEB-MOTION-STACK.md`. Quick references here:)

- **Remotion (P0):** declarative React video → `_dep_notes/remotion.md`
- **GSAP toolkit routing (P1):** 23 sub-skills in toolkit not routed → `rules-deferred/skill-triggers.md` §13 update
- **framer-motion (P1):** dep-ingest
- **Lottie (P1):** GraphQL dep-ingest

---

## Cross-axis links

- **Faceless-media** ↔ AXIS-03 — see assembly skills above.
- **Web-motion** ↔ AXIS-04 — see DRAFT-RESEARCH-WEB-MOTION-STACK.md.
- **Voice-tts** ↔ AXIS-05 — see Whisper / VoxCPM2 / ElevenLabs entries above.
- **Local-first-edge** ↔ AXIS-13 — Whisper CPU-only crosses axes 5+13.
- **Content-engine** existing skill — encoding profiles + novelty-gate extend it.
- **last30days** existing skill — TikTok pattern primitive + viral-discovery extend it.

---

## Open questions for Adam

1. **CONSENT-GATE workflow:** spec verbiage + record-keeping + revocation now (covers 11 tools at once)?
2. **HeyGen vs Synthesia primary:** which becomes the active avatar surface?
3. **Runway wiring:** finish now? (Cheapest unlock; ~30 min work.)
4. **Whisper CPU install:** OK to proceed without further press-back? No GPU dep, no network call after install.
5. **Reddit→video skill scope:** assembly only, or include upload? Upload requires per-platform API auth.

---

## Provenance

Every claim in this file traces to:
- An image_id in `Image Intelligence Ledger/records/`
- An axis report in `Image Intelligence Ledger/axis/AXIS-NN-*.md`
- A confirmation report in `Image Intelligence Ledger/axis/CONFIRM-NN-*.md`
- A routing row in `Image Intelligence Ledger/GAP-ROUTING.md`

**No claim is promoted from carousel/marketing/profit narrative without the source-context flag traveling with it.**

---

**DRAFT END**
