# Call Script — free 20-min style-match call

Minute-by-minute. Adjust tone, don't skip steps.

---

## Before the call (5 min prep)

- Open `on-call-kit/` in Claude Code
- Have `websites.owlzone.trade` open in a browser tab
- Have `INTAKE-TEMPLATE.md` open in another tab
- Check your mic, quit anything noisy

---

## Minute 0 — open

> "Hey <name>, thanks for booking the style-match. Here's how this
> works: I'll ask you about your business for three or four minutes,
> then I'll generate a working preview of your actual website live on
> my screen, and share it with you before we hang up. Sound good?"

---

## Minute 0–3 — intake (fill `intake.md` while they talk)

Walk them through the template questions in `INTAKE-TEMPLATE.md` in
this order (don't read them off — have a conversation):

1. "What's the business called, and where are you based?"
2. "In one sentence, what do you actually sell?"
3. "When someone lands on the site — what's the one thing you want
   them to do?" (book, call, buy, email, visit)
4. "Did one of the ten styles jump out for you, or want me to pick
   one that fits the business?"
5. "Any look you definitely don't want — colours, photos, tone?"

Get their "hard no's" — this is the most common cause of a rejected
preview. "No stock photos of smiling dentists." "No dark mode."
"Nothing that looks like a tech startup."

---

## Minute 3 — tell them you're running it

> "Perfect. I'm generating it now — takes about two minutes. While
> that runs, quick follow-ups..."

Fill the dead air with:
- "Do you have any copy written already, or would we be writing it?"
- "Any photos you want used, or source for you?"
- "What's your hard deadline if you have one?"

---

## Minute 3–5 — dispatch runs

Paste intake block + dispatch line into Claude Code. Keep talking.

When the agent returns a path, open the file locally (Windows:
`start on-call-kit/previews/<file>.html`). Share your screen.

---

## Minute 5–15 — walkthrough

Walk them top-to-bottom of the preview. Point out:

- "That's your hero — your business name, your CTA as the button"
- "These are the sections we'd fill with your actual services"
- "This is where the about block would sit — we'd write it from our
  brief call"
- "The style here is the <Neumorphism / Brutalism / etc> direction
  you picked, adapted so it doesn't look like the sample"

**Ask questions, don't lecture:**
- "What's the first thing that doesn't feel right?"
- "Is that CTA button close to what you'd want, or different wording?"
- "On a scale of 1–10, how close is this to the site you had in your
  head?"

---

## Minute 15–18 — handle the close

Three scripts, pick the one that matches.

### 8+ out of 10 — they're ready to book

> "Great. So — Pro tier is €1,595 all-in, delivered 14 days from when
> you send me your content. I've got a slot opening Monday.
> If you email me now, I'll send you a 1-page brief within 24 hours
> and we lock it in. Want me to send you the email link?"

Drop this mailto in the chat (replace <BIZ> and <TIER>):

```
mailto:callmeie@proton.me?subject=Book%20<TIER>%20-%20<BIZ>&body=From%20style-match%20call%20on%20<DATE>%2C%20<SUMMARY>
```

### 5–7 out of 10 — they're interested but not ready

> "Fair enough. The €99 style-match audit is made for exactly this —
> you pay €99 today, within 48 hours you get a 1-page PDF with the
> full direction locked in, firm quote, and the launch date. If you
> book a project within 30 days the €99 comes off. That way nobody
> rushes a decision."

### Under 5 — not the right fit

> "I don't want to oversell something that's not landing. Let me send
> you the preview file as a link — you can sit with it, come back if
> it grows on you, or if it doesn't, no follow-up from me. Fair?"

Always send the preview regardless of outcome.

---

## Minute 18–20 — close the call

- Confirm the next step (email incoming / audit paid / preview sent)
- Thank them by name
- "If you think of a question in the next day or two, just reply to
  that email thread — I answer within 24 hours."

---

## Right after the call

1. **Append to `leads.md`** (one line — see `CLAUDE.md` for format)
2. **Email them the agreed next step** within 10 minutes
3. **Move preview file** into `previews/archive/` if they didn't book
   (keeps the active folder clean)

---

## Do / don't

| Do | Don't |
|---|---|
| Generate the preview live on the call | Pre-generate before the call |
| Use their real business name in the hero | Let the agent default to "Your Business" |
| Ask "what's the first thing that doesn't feel right" | Ask "do you like it" |
| Quote the tier price and the delivery date | Hedge on price or timeline |
| Log every call in leads.md | Trust memory |
| Send the preview link even to no's | Disappear on a no |
