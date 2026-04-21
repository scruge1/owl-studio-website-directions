# Prospect intake — fill during the call

Copy this block into the Claude Code session after filling it in.
Everything below gets fed straight to the dispatch agent.

```
Business name:        ________________________________________________
Location:             ________________________________________________
Service / what they sell:
                      ________________________________________________
                      ________________________________________________

Primary CTA (what the website has to get the visitor to do):
                      ________________________________________________

Audience (who they serve — age, location, B2B / B2C):
                      ________________________________________________

Gallery style they picked (pick ONE):
  [ ] 01 Minimalism / Swiss  (online magazine feel)
  [ ] 02 Neumorphism          (soft, quiet, wellness/meditation)
  [ ] 03 Glassmorphism        (fintech dashboard feel)
  [ ] 04 Brutalism            (bold, raw, design-led)
  [ ] 05 3D / Hyperrealism    (premium product / tactile)
  [ ] 06 Vibrant Block        (startup / creative agency)
  [ ] 07 Dark Mode (OLED)     (tech, gaming, devs)
  [ ] 08 Claymorphism         (playful, education, kids)
  [ ] 09 Aurora UI            (music, lifestyle, streaming)
  [ ] 10 Retro-Futurism       (synthwave, podcast, nostalgia)

Tier they're asking for:
  [ ] Starter €499   — 7 days, single-page, 150–300 words
  [ ] Pro €1,299     — 14 days, 5 pages, CMS + copywriting
  [ ] Custom €2,500+ — quoted, ecommerce / SaaS / integrations

Hard no's (colours / imagery / tones to avoid):
                      ________________________________________________

Business details to weave into copy:
  - Years in business:
  - Founder / owner name (if they want it shown):
  - Phone / email to put on the site:
  - Hours:
  - Any real numbers they want featured (patients / projects / years):

Deadline pressure:
  [ ] Want preview in THIS call
  [ ] OK to get preview within 30 min after call
  [ ] OK to get preview within 24 h

Notes:
                      ________________________________________________
                      ________________________________________________
```

Once filled in, paste the block into the Claude Code session + say:

> "Dispatch style-match-call against the intake above. Write to
> on-call-kit/previews/<today>-<business-slug>.html. Return path +
> line count only."
