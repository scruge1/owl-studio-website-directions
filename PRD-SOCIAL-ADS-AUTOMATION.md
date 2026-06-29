---
title: PRD — Social + Paid-Ads Automation (close the §4b delivery gaps)
status: draft / research-complete / pre-build (Adam-gated)
owner: Adam
created: 2026-06-12
serves: PRICING-SSOT.md §4b (Social + Paid-Ads Management add-on)
trigger: Irish Roofing & Sealing (lmullins-adjacent lead) asked for an ads/social quote; §4b honest-audit found the "campaigns built/run/optimised" tier is manual labour, not a system capability — same overclaim that withdrew Doc Ops 2026-06-07.
_status_date: 2026-06-12
---

# PRD — Social + Paid-Ads Automation

## 1. Real goal

Make the **§4b Social + Paid-Ads Management** product actually deliverable by our system, so the most-popular €249 tier is not "Adam logs into each client's ad account by hand every week." Close the 🔴 gaps with the **cheapest capable** automation (60/30/10 doctrine: query/rule first, AI only where judgement is irreducible), WITHOUT repeating the Doc Ops integrity miss (advertised capability > real capability → withdrawn).

Non-goal: build a Buffer/Hootsuite competitor. We need exactly enough to deliver §4b to a handful of Irish SMB clients, honestly.

## 2. Current capability (the gap we're closing)

| §4b promise | Today | This PRD |
|---|---|---|
| Ad creative (video/posts) | 🟢 Kling + callmeie-video-pipeline (Remotion) + content-engine + Canva MCP | keep — the edge |
| Landing page / funnel | 🟢 `new-service-site` skill | keep |
| GBP setup | 🟢 `provision_client.py` | keep |
| **Auto-publish 8 posts/mo to FB/IG/GBP** | 🔴 not built (no publishing pipeline) | **Phase 1** |
| **Campaigns built / run / optimised** | 🔴 no Google/Meta ad-API wiring; manual | **Phase 2 (Google), Phase 4 (Meta)** |
| Conversion tracking / pixel | 🔴 Umami ≠ ad-pixels | **Phase 3** |
| Monthly performance report | 🟡 manual pull | **Phase 3** |

## 3. Research findings (2026-06-12, cited §10)

### 3a. Social publishing — BUILD vs BUY

The blocker is NOT code — it's **Meta's app review**. To publish to a client's FB Page / IG professional account via your own Meta app you need **Advanced Access on `instagram_content_publish` + Business Verification**: **2-6 weeks, multiple submission rounds, stricter in 2026** [R4]. That gate sits in front of any DIY or self-host route that uses *our* Meta app.

| Option | What it is | Cost | App-review pain | Verdict |
|---|---|---|---|---|
| **Ayrshare** (unified API) | One API → FB, IG, **Google Business Profile**, LinkedIn, X, TikTok, Threads, YouTube +. **They hold the Meta app review.** MCP server exists. | Business (own use) **$149/mo**; agency multi-profile from **$599/mo / 30 profiles** then $2.49-8.99/extra | **None — removed** | **Phase-1 pick.** Fastest path to "publishing is real" (days). |
| **Mixpost** (self-host OSS) | Laravel self-host, supports FB/IG/Threads/X/Bluesky, has API, central media library | **one-time $269-1199** (perpetual) | **YES — you do the Meta app review** | Phase-1.5 swap once volume justifies killing Ayrshare's recurring + you've cleared one Meta review |
| **Postiz** (self-host OSS) | Agentic scheduler, great n8n/Make/Zapier hooks, strongest on X/Bluesky/Mastodon/Discord | self-host free | weaker FB/IG | orchestration reference, not the FB/IG engine |
| DIY Meta Graph API | raw `instagram_content_publish` | free | full 2-6wk review + verification | **No** — friction not worth it at this scale |

**Decision lever:** Ayrshare $149/mo is covered by **one** €249 client. Below ~5 clients, Ayrshare's removed-app-review beats Mixpost's one-time cost + your review labour. Re-evaluate Mixpost swap at ~6+ clients.

### 3b. Paid ads

| Platform | API reality | Gate | Verdict |
|---|---|---|---|
| **Google Ads** | Python client lib; **PMax + Search creatable**; needs **MCC manager account**; campaign create/budget/report all API | **Developer token**: Test→**Basic** (15,000 ops/day — plenty)→Standard. Basic approval = days-weeks. RMF only hits Standard. | **Phase 2.** Google-first matches the trade-routing tip (roofing = high-intent search, Google > Meta). |
| **Meta Marketing API** | campaign create/run via Marketing API | same Meta app-review + Marketing API access friction | **Phase 4 (defer).** Meta = brand/retargeting, second priority for trades. |

### 3c. Orchestration backbone

**n8n self-hosted** (free, Docker) [R6] = the deterministic spine. Native Google Ads / Meta Ads / social nodes; the community has agency client-reporting + multi-post workflows. Runs on the existing Hetzner box (INFRA.md). This is the 60% deterministic layer — our creative engine and judgement calls are the 10% AI.

### 3d. Conversion tracking

GA4 + Google Ads conversion + Meta Pixel, installed via GTM. Per-client manual-but-scriptable (snippet into the site we host/built — we control the `<head>`, so this is low-friction for OUR-built sites, harder for client-owned sites).

## 4. Recommended architecture

```
[our creative engine]                 [n8n self-host @ Hetzner = spine]
 Kling / Remotion / content-engine ──► n8n workflow ──► Ayrshare API ──► FB / IG / GBP (Phase 1)
 Canva MCP / article-writing                │
                                            ├──► Google Ads API (MCC, Basic token) ──► Search/PMax (Phase 2)
                                            ├──► GA4 + Ads conversion + Pixel (Phase 3)
                                            └──► monthly report builder ──► PDF ──► client (Phase 3)
                                                     ▲
                                       [Meta Marketing API] ──────────────── Phase 4 (deferred)
```

60/30/10: posting schedule + budget pacing + report assembly = **deterministic (n8n + rules)**; campaign structure = **rule-based templates**; only creative + "is this campaign underperforming, change what" = **AI/human judgement**.

## 5. Phased roadmap (each phase independently shippable — finish before next)

### Phase 0 — Accounts & gates (do first, they have lead time)
- [ ] Create **Google Ads MCC** (manager account) + apply **developer token, Basic access** (days-weeks lead — apply NOW even before build).
- [ ] Sign up **Ayrshare Business** ($149/mo) OR decide Mixpost; create Business Profile linkage for first client.
- [ ] Stand up **n8n** via Docker on Hetzner (INFRA.md runbook pattern).
- **AC:** MCC live, dev-token application submitted, Ayrshare key in `~/.claude/routes/.env`, n8n reachable on a subdomain behind CF.

### Phase 1 — Social auto-publish (closes the biggest, easiest gap)
- [ ] n8n workflow: creative-engine output → Ayrshare scheduled post → FB + IG + GBP.
- [ ] Per-client config (which pages, cadence, brand voice).
- [ ] First real client = the roofer: 8 posts/mo, scheduled, no manual upload.
- **AC:** a post authored by our engine appears on a live FB+IG+GBP on schedule with zero manual platform login. Touch gate = the live post.

### Phase 2 — Google Ads (makes "campaigns built/run" partly real)
- [ ] Google Ads API client (Python) under MCC; campaign-template module (Search + PMax) seeded with our creative + landing page.
- [ ] Budget guardrails (hard cap = client's stated media budget; never exceed).
- [ ] Start with **Google Smart/PMax** (Google's own optimiser) + conservative rules → de-risks the skill gap (§7).
- **AC:** a Search campaign created via API for the roofer, budget-capped, conversion-tracked, serving. Human-reviewed before live.

### Phase 3 — Conversion tracking + reporting
- [ ] GTM template (GA4 + Ads conversion + Pixel) auto-injected on our-built/hosted sites.
- [ ] n8n monthly report: pull Ads spend/leads + Ayrshare engagement + GA4 → branded PDF → client.
- **AC:** one automated monthly report delivered end-to-end.

### Phase 4 — Meta Ads (deferred) + Mixpost swap (deferred)
- [ ] Meta Marketing API once Meta-paid is justified; own Meta app review (also unlocks Mixpost self-host to kill Ayrshare recurring).
- **AC:** deferred — revisit at ~6 clients.

## 6. Costs (run-rate)

| Item | Cost | Covered by |
|---|---|---|
| Ayrshare Business | $149/mo (~€138) | 1× €249 client |
| n8n self-host | €0 (existing Hetzner) | — |
| Google Ads API | €0 (Basic token free) | — |
| Mixpost (if swapped, Phase 4) | one-time ~$269-349 | — |
| **Client ad spend** | **€0 to us — pass-through** | client (§4b clause) |

Margin at 1 client: €249 − €138 Ayrshare = €111/mo before labour. Improves per extra client until Ayrshare agency tier ($599) — then re-evaluate Mixpost.

## 7. Risks

1. **Skill gap ≠ tooling gap (highest).** Building the Google Ads API does NOT make us good at *buying* ads. **Partial mitigation already true:** Adam has run his own FB ad campaigns (real, not zero from cold) — but own-brand FB ≠ proven client-results across Google Search. So "optimised" stays an overclaim until profitable client campaigns exist. **Mitigations:** start manual (Adam hands-on, learns the client's account before any automation); when Phase 2 lands, lean on Google Smart/PMax + conservative budget caps + human review; §4b copy = "built, run + managed, reported", NOT "optimise/guarantee/ROAS." Honest scope or it's Doc Ops again. **DONE: wording dropped from §4b 2026-06-12.**
2. **App-review timeline** (Meta) — mitigated by Ayrshare in Phase 1 (they own it); only bites if we DIY/Mixpost.
3. **API ToS / token suspension** — Google dev-token + Ayrshare both have ToS; build within RMF, don't scrape.
4. **Cost-at-scale** — Ayrshare per-profile pricing climbs; Mixpost swap is the release valve (Phase 4).
5. **Client-owned sites** — conversion-pixel install is easy on OUR sites, manual on client-owned. Price ad-tier accordingly or require we host.

These tools are **`researched`, NOT `production_ready`** (operator-intelligence-contract). No auto-routing for live client work until each phase's AC passes + failure modes documented.

## 8. Decisions — RESOLVED (Adam 2026-06-12)

1. **Ayrshare vs Mixpost** → **NEITHER yet. Manual-first v0.** No paid tooling subscription bought until (a) a sale is confirmed AND (b) client count makes the tool pay for itself. The first client (likely the roofer = CallMeIE's first customer) — his €249 is margin, NOT spent on a subscription to run his ads. Manage posts + ads **by hand** to start. Adam has already run his own FB ad campaigns → the skill exists. Ayrshare becomes Phase 1b only once volume justifies it.
2. **Apply Google Ads MCC + dev token now** → **YES** (free, days-weeks lead time, no purchase). Adam action — steps in §11.
3. **Drop "optimise/guarantee" wording** → **DONE.** §4b rewritten to "built, run + managed, reported"; copy-rule added to both SSOTs.
4. **Build order** → manual delivery is v0 (no build needed to sell + deliver). Automation phases layer in AFTER the first sale proves the product. Token application is the only "now" action.

## 9. Non-goals
- Not building our own social scheduler from scratch (buy/self-host proven OSS).
- Not Meta paid ads in v1 (Google-first for trades).
- Not promising ROAS/lead guarantees.
- Not auto-running campaigns without human review (budget = client's money).

## 11. Google Ads developer-token application (Adam action, free, do now)

Lead time is days-weeks, so apply before the build. ~10 min of form-filling.

1. **Use the canonical Google account** `swarm.agent.2026@gmail.com` (already holds GSC/GBP/GA — keep ad infra on the same identity, not a new throwaway).
2. **Create a Manager Account (MCC):** ads.google.com → "Tools" → Manager Accounts → create. The MCC is the agency umbrella; client ad accounts get linked under it later. (API Center only appears under a *manager* account, not a normal one.)
3. **Open API Center:** in the MCC → **Admin / Tools & Settings → API Center** → fill the **API Access form** → issues a **developer token** at **Test** access.
4. **Apply for Basic access** (15,000 ops/day — plenty; Standard is unlimited, not needed yet). Use-case to state: *"Internal agency tool to create, manage and report on Google Ads campaigns for our own accounts and our managed clients."* Brand verification = optional faster-approval signal.
5. **Store the token** in `~/.claude/routes/.env` as `GOOGLE_ADS_DEVELOPER_TOKEN=` when issued (grep-extract pattern, never `source`).
6. Approval email arrives in days-weeks. Token works in Test immediately for sandbox dev.

*Account-sensitive web action — Adam drives (or supervises a claude-in-chrome co-drive). Not headless-automatable.*

## 10. Sources
- [Postiz — open-source schedulers roundup](https://postiz.com/blog/open-source-social-media-scheduler) · [postiz-app GitHub](https://github.com/gitroomhq/postiz-app)
- [Mixpost self-host](https://mixpost.app/)
- [Ayrshare pricing](https://www.ayrshare.com/pricing/) · [Ayrshare docs](https://www.ayrshare.com/docs/introduction)
- [R4] [Instagram API pricing / app-review friction 2026 — Blotato](https://www.blotato.com/blog/instagram-api-pricing) · [Meta Instagram content publishing docs](https://developers.facebook.com/docs/instagram-platform/content-publishing/)
- [Google Ads API — create PMax](https://developers.google.com/google-ads/api/performance-max/create-campaign) · [access levels / dev token](https://developers.google.com/google-ads/api/docs/api-policy/access-levels) · [developer token](https://developers.google.com/google-ads/api/docs/api-policy/developer-token)
- [R6] [n8n agency automation 2026](https://robizsolutions.com/automate-digital-marketing-agency-n8n-2026/) · [n8n social workflows](https://n8n.io/workflows/categories/social-media/)
