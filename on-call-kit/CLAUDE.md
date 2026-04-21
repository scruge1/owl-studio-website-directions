# On-Call Kit — Owl Studio style-match call

Open a Claude Code session in THIS folder when a prospect is on the
phone. Everything you need for a 5-minute live demo during a 20-min
sales call is here.

## The deal

- Prospect is on the phone / Google Meet
- Free 20-min style-match call, booked from websites.owlzone.trade
- They've already picked (or are considering) one of the ten gallery
  styles
- Goal: have a working preview of THEIR website open on screen before
  the call ends

## Workflow during the call

1. **Minute 0–2** — open `INTAKE-TEMPLATE.md`, fill it in while the
   prospect talks. Copy the filled block to the session.
2. **Minute 2–3** — invoke the `style-match-call` skill (it's
   registered globally — just say "run style-match-call with this
   intake" or paste the intake and reference the skill's canonical
   dispatch block).
3. **Minute 3–4** — one Agent tool call, `subagent_type: general-purpose`,
   brief built from the intake per the skill spec. It writes a file to
   `previews/<YYYY-MM-DD>-<business-slug>.html`.
4. **Minute 4–5** — open the file locally (file:// or `start` on
   Windows), share screen, ask the closing question from
   `CALL-SCRIPT.md`.

## After the call

Append one line to `leads.md`:
```
2026-04-DD · <business> · <location> · <style picked> · <tier asked> · booked/audit/no/follow-up
```

If they booked: email them the `mailto:` link in `CALL-SCRIPT.md`
pre-filled with their intake summary. Within 24 h, send a 1-page brief.

If they took the €99 audit path: invoice first, then deliver within 48 h.

If they didn't book: send them the preview as a shareable link, follow
up in 7 days.

## Files in this folder

- `CLAUDE.md` — this file (routing)
- `AGENTS.md` — rules for any sub-agent invoked during a call
- `INTAKE-TEMPLATE.md` — the form you fill during the call
- `CALL-SCRIPT.md` — minute-by-minute script with closing lines
- `leads.md` — lead log (append-only)
- `previews/` — generated preview HTML files, one per prospect

## The skill itself

`~/.claude/skills/style-match-call/SKILL.md` is the canonical spec. It
references this folder's templates and the installed `ui-ux-pro-max`
skill's `styles.csv` for the style catalog. The skill is auto-loaded
by Claude Code on any session inside this folder.

## Dependencies (installed, verified 2026-04-21)

- `~/.claude/skills/ui-ux-pro-max-skill/src/ui-ux-pro-max/data/styles.csv` — 84 styles
- `~/.claude/plugins/cache/claude-plugins-official/frontend-design/unknown/skills/frontend-design/SKILL.md` — anti-AI-slop rules
- `~/.claude/skills/parallel-skill-dispatch/SKILL.md` — general-case pattern (this is the N=1 scaled version)
- `~/Desktop/design-hub/INSTALLED-TOOLS.md` — the full catalog the skill draws from

## Anti-patterns

- **Don't talk past the demo.** Hit "generate", keep talking while it
  runs. Dead air kills the close. The agent takes 2–4 minutes; fill
  that with questions about their business, deadline, content
  readiness.
- **Don't oversell what they can't see yet.** "This is what Day 7 looks
  like" — NOT "this is the final version". It's a preview of the
  direction, not the finished product.
- **Don't skip `leads.md`.** The whole pitch-refinement loop depends on
  seeing what closes and what doesn't. One line per call, always.
