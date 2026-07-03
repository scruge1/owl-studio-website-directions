# Twilio support reply — ticket #27259801 (draft, Adam to send)

**Reply within ticket #27259801** (the existing thread — that routes it to the agent already handling it).

---

Subject: Re: #27259801 — CALLMEIE alphanumeric Sender ID (Ireland) now ComReg-approved

Hi,

Following up on ticket #27259801 about our alphanumeric Sender ID **CALLMEIE** on Messaging Service **MG5773dd9d6b3b577d9517361ebcb758d0** ("CallMeIE Ireland Outbound").

**Update:** our Sender ID registration with **ComReg (Ireland) is now APPROVED** — registration name CALLMEIE, registration date **17 June 2026**.

Previously the sender was configured on the Messaging Service but not yet regulatory-registered, so messages to Irish networks were being overstamped as "Likely Scam." Now that ComReg has approved the registration, could you please help with two things:

1. **Confirm what Twilio needs from us** to complete the alphanumeric Sender ID registration on our account (US1). The self-serve REST path (`messaging/v1/AlphaSenderRegistrations`) returns 404 for us, and the Trust Hub console flow for Alphanumeric Sender IDs is not present on this account (Senders shows only Short codes / WhatsApp).
2. **Submit/accept our Sender ID to the Irish networks** (with Twilio acting as Participating Aggregator) so CALLMEIE delivers to Ireland without the "Likely Scam" label.

I can provide our Irish company registration certificate (**CRO 816273**) or any other documentation you require as proof of the registered entity.

Thanks for your help,
Adam — CallMeIE

---

**Notes for Adam:**
- Only send once you can attach/quote the ComReg approval + CRO 816273 cert if they ask.
- Sole blocker to IE SMS is this Twilio-side acceptance; ComReg side is done. Until it clears, keep interim outbound = email via Resend `hello@callmeie.ie` (per INFRA.md §alpha-sender, now updated).
