# Agent Rules — On-Call Context

Rules for any sub-agent dispatched during a live style-match call.
Time is limited (5 min), the prospect is watching, and a generic or
placeholder output loses the sale.

## Hard rules

1. **Real business info or fail fast.** If the intake block is missing
   business name, location, service, CTA, or picked style — stop and
   ask before generating. A preview for "Your Business Here" is worse
   than no preview.
2. **Use the picked style row, not a guess.** The prospect named a
   gallery style during the call (Neumorphism / Brutalism / Claymorphism
   / etc.). Read that exact row from `ui-ux-pro-max-skill/.../styles.csv`.
   If the intake says "not sure", pick one aloud on the call first and
   only then dispatch.
3. **Every line of copy is about THEIR business.** No "Lorem ipsum", no
   "Modern Business Solutions", no "Empower your growth". Hero CTA, 
   services, testimonial placeholders, about text — all drawn from the
   intake block.
4. **One file, one prospect, one preview.** Output path is always
   `on-call-kit/previews/<YYYY-MM-DD>-<business-slug>.html`. Never
   overwrite a previous prospect's preview.
5. **Return path + line count only.** Don't paste the HTML back into
   the main session. The main session has to keep the call moving.

## What the preview must include

- Hero with: prospect's business name, the CTA from intake, a sub-line
  that reflects their actual service
- Services / features section: 3–6 items drawn from what they described
- Social-proof block: placeholder styled appropriately (e.g.
  "3 upcoming testimonials" callout, or a ready-to-fill quote panel) —
  never fake client names
- About block: 60–80 words written TOWARDS their specifics (location,
  years in business if stated, founder name if stated)
- Footer with: their contact details (if shared), hours (if shared),
  location, plus a clearly-labelled "Preview generated for <business>
  on <date> by Owl Studio" watermark

## What the preview must NOT include

- Fake client logos
- Invented press-quotes
- "Join 500+ happy customers" numbers (unless the prospect has that
  number and said so)
- Stock headset/handshake imagery
- Placeholder names like "John Doe" or "Jane Smith"

## Style guardrails (inherit from frontend-design skill)

- No Inter / Roboto / Arial as the design voice
- No purple-to-blue gradients unless the prospect asked for them
- No glassmorphism on every surface — one use max per page
- Commit to the gallery-picked style's tokens; do not mix two styles

## Fallback if the agent stalls

If the Agent tool call hangs or runs out of quota:
1. Tell the prospect: "My tooling needs another 10 minutes —
   I'll have the preview in your inbox before we hang up the call, 
   or within the next 30 minutes. Can I walk you through another 
   gallery sample meanwhile?"
2. Stay on the call. Walk them through the relevant gallery sample
   on `websites.owlzone.trade`.
3. As soon as the preview file lands, email them the shareable link.
