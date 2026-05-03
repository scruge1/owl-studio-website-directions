# PDR · AI Chatbot Add-On for Owl Studio Client Sites

> Research-first planning document. Written 2026-04-23.
> Purpose: evaluate and specify an AI chatbot product add-on for Owl Studio's Irish SME website clients.
> This document feeds into product scoping — nothing is built until the prototype gate is cleared.

---

## Gemini API Free Tier — What You Get

### Current Models and Limits (as of April 2026)

Rate limits are applied **per Google Cloud project**, not per API key. Multiple keys inside one project share the same quota bucket.

| Model | RPM | TPM | RPD | Status |
|---|---|---|---|---|
| Gemini 2.5 Flash | 10 | 250,000 | 250 | Active, free |
| Gemini 2.5 Flash-Lite | 15 | 250,000 | 1,000 | Active, free |
| Gemini 1.5 Flash | 15 | 1,000,000 | 1,500 | Active, free |
| Gemini 2.0 Flash | — | — | — | Retired March 2026 |

> Note: Google cut free tier limits significantly in December 2025 (50–80% reduction across models). Published tables may lag; always verify your actual project quota at [aistudio.google.com/rate-limit](https://aistudio.google.com/rate-limit) before making promises to clients.

### What "Free" Means in Practice

- No credit card required
- Gemini 2.5 Flash: 10 requests/minute, 250 requests/day — sufficient for most SME sites (see cost section)
- Gemini 2.5 Flash-Lite: 15 req/min, 1,000 req/day — better headroom, slightly less capable
- Token limits are per project, not per key — you cannot multiply quota by creating extra keys in the same project
- Free tier data is used by Google to improve their models. Human reviewers may read prompts/responses. **This is a material GDPR issue for Irish clients — see compliance note below.**

### Per-Client Isolation

Each client gets their own Google Cloud project → their own free tier quota → complete isolation.

- You can create up to 10 projects from one Google account
- Beyond 10 projects: use separate Google accounts per client (each SME client can own their own Google account — this is the preferred model)
- Quota is per project, so one busy client cannot exhaust another client's allowance
- Creating separate accounts specifically to pool quota violates Google's ToS — but giving each client their own account is legitimate and clean

### GDPR / Ireland-Specific Warning

**Free tier = Google uses your data.** Under Gemini API terms:
- Free/unpaid usage: prompts and responses may be used to improve Google products
- Human reviewers may read that data
- No EU data residency controls on free tier
- GDPR requires paid tier (Google Workspace with Gemini, or Vertex AI) to get: data processing addendum, EU region locking, no model training on client data

**For Irish SME clients:** The free tier is acceptable for a general FAQ bot that answers questions already publicly available on the website (opening hours, services, location). It is **not** acceptable for any chat that captures visitor names, health information, or anything under special-category GDPR treatment. A dental practice asking about patient symptoms = needs paid tier or an on-device model.

**Practical recommendation:** Free tier chatbot for non-sensitive FAQ only. Document this clearly in the service agreement. Upgrade path to Vertex AI (paid) for medical, legal, or financial clients who handle sensitive queries.

---

## Gemma 3 4B — Capability Assessment for SME Chatbots

### What It Is

Gemma 3 4B is Google's open-weight 4-billion parameter model, released March 2025. It is **free to run** — you provide the compute, Google provides the model weights. No per-token cost, no rate limits, no data sent to Google.

### Capability for SME FAQ Use

| Capability | Gemma 3 4B | Adequate for SME? |
|---|---|---|
| General conversation | Yes | Yes |
| System prompt following | Good | Yes |
| Context window | 128K tokens | Yes (can fit entire business profile) |
| Multimodal (text+image) | Yes | Rarely needed for FAQ |
| Function calling | Yes | Useful for booking integrations |
| Irish English / local phrasing | Reasonable | Mostly yes |
| Hallucination rate | Higher than cloud models | Mitigate with constrained system prompt |

**Verdict:** Gemma 3 4B is capable enough for a tightly-constrained SME FAQ chatbot that only answers from a provided business profile. It will not be as reliable as Gemini Flash for open-ended questions, but if the system prompt says "only answer from the information below, say you don't know otherwise," it performs adequately.

### Hosting Requirements for Self-Hosted Gemma 3 4B

| Spec | Minimum | Recommended |
|---|---|---|
| RAM | 8 GB (CPU inference, INT4 quant) | 16 GB |
| GPU VRAM | None (CPU works) | 8 GB (10-50x faster) |
| VPS cost | ~€20/month (Hetzner CX31 equivalent) | ~€40/month |
| Response latency CPU-only | 3–8 seconds/response | Too slow for good UX |
| Response latency with GPU | 0.3–1 second | Acceptable |

**Conclusion: Gemma 3 4B self-hosted is not viable for the Owl Studio model at this stage.** The compute cost (~€20-40/month per client) eliminates the savings versus paying for Gemini Flash. CPU-only inference is too slow for chat UX. You would need a shared GPU instance to make it economical — that requires more infrastructure complexity than this product warrants in v1.

### Gemma 3 4B vs Gemini Flash Free Tier — Decision

| Factor | Gemma 3 4B (self-hosted) | Gemini Flash (free tier) |
|---|---|---|
| Cost | €20-40/month VPS | €0 |
| Setup complexity | High (Ollama, server, management) | Low (API key) |
| Latency | 3-8s CPU / 0.3s GPU | ~0.5-1s |
| Rate limits | None (your hardware) | 10-15 RPM, 250-1500 RPD |
| Data privacy | Full control | Google trains on free tier |
| Quality | Good (with tight prompt) | Better, more consistent |
| Maintenance | Ongoing | None |

**Use Gemini Flash free tier for v1.** Revisit Gemma self-hosted when: (a) a client needs GDPR-clean on-device inference, or (b) monthly Gemini paid costs exceed ~€30/client/month. Neither applies at SME traffic volumes in 2026.

---

## Architecture Options

### Option A — Client-Side Direct (NO)

The Astro site's JavaScript calls the Gemini API directly from the browser, with the API key embedded in the frontend code.

```
Visitor browser → Gemini API (key in JS bundle)
```

**Why this fails:** The API key is visible to anyone who inspects the page source or network tab. The key can be extracted and used to exhaust the client's quota or run up charges. Google's own documentation explicitly warns against this.

**Do not use.**

### Option B — Serverless Proxy (RECOMMENDED)

A thin serverless function sits between the browser and Gemini. The API key lives in an environment variable on the server, never in the browser.

```
Visitor browser → Serverless function (key in env var) → Gemini API
```

The serverless function:
1. Receives the visitor's message and conversation history
2. Prepends the business system prompt (hardcoded at build time or fetched from profile)
3. Calls Gemini API with the full context
4. Streams the response back to the browser via SSE

**Hosting options for the proxy:**

| Platform | Free tier | Commercial use | Cold start | Best for |
|---|---|---|---|---|
| Cloudflare Workers | 100K req/day | Yes | ~0ms (edge) | Production default |
| Netlify Functions | 125K req/month | Yes | ~500ms | Backup option |
| Vercel Serverless | 1M req/month | No (Hobby) / $20/mo (Pro) | ~250ms | Avoid (commercial restriction) |
| Render FastAPI | Already running (callmeie.onrender.com) | Yes | ~500ms cold | Use existing infra |

**Recommendation:** Use the existing **callmeie.onrender.com FastAPI backend** (already live, already client-aware) and add a `/owl/chat` endpoint. Zero additional hosting cost. Cold start on Render free tier can be mitigated with UptimeRobot pings (already in place per PDR-BACKEND).

If Render is not fast enough for chat streaming: add a Cloudflare Worker as a thin proxy in front. Cloudflare Workers have ~0ms cold start and 100K free requests/day.

### Option C — Third-Party Widget (PARTIAL USE)

Services like Tidio, Crisp, Intercom, or CustomGPT.ai provide drop-in chat widgets with AI built in. You configure the bot's knowledge base and embed a `<script>` tag.

**Pros:** Zero code, fast setup, polished UI.
**Cons:** Monthly cost ($19-49/month per client), no control over data, client is locked into a vendor, doesn't integrate with brief.json / profile system.

**Use case:** Recommend this only as a stopgap for a client who needs a chatbot before the custom solution is built, or for a client on the Concierge care plan who doesn't want any maintenance involvement.

---

## Recommended Architecture for Owl Studio Clients

### The Stack

```
Client site (Cloudflare Pages or GitHub Pages, static HTML)
  └── chat-widget.js (vanilla JS island, ~150 lines)
        │ POST /owl/chat { site_id, messages[] }
        ▼
callmeie.onrender.com/owl/chat   (FastAPI, existing infra)
  └── reads system_prompt from profile DB (or hardcoded per site_id)
  └── calls Gemini API (client's own key, stored in Render env vars per site_id)
  └── streams response back via SSE
        ▼
Gemini API (client-owned Google Cloud project, free tier)
```

### Why This Is the Right Shape

1. **No new infrastructure.** The FastAPI backend at callmeie.onrender.com is already running, already has the `site_id` concept, already has per-client tokens. A new `/owl/chat` endpoint follows the same pattern as `/owl/submit`.

2. **Client owns their API key.** The Gemini key lives in the client's own Google AI Studio project. Owl Studio stores it in Render environment variables per `site_id`, the same way `OWL_OWNER_TOKEN` is already stored. The client's data goes through the client's quota.

3. **Static site compatibility.** The chat widget is plain JS — it works on any HTML page regardless of whether it was built with Astro, the current Jinja renderer, or raw HTML templates. No build step change needed.

4. **Free at SME traffic volumes.** 250 requests/day on Gemini 2.5 Flash free tier = ~8 conversations/day at 30 messages each. A typical Irish SME site at 200-500 monthly visitors generates ~10-50 chatbot interactions/month (5-15% of visitors engage with a chat widget). This is well within free tier limits.

5. **Upgrade path exists.** If a client's usage grows past the free tier, they enable billing on their Google Cloud project. The code doesn't change.

### What Changes per Client

| Item | Where it lives | Who sets it up |
|---|---|---|
| Gemini API key | Render env var (`GEMINI_KEY_<site_id>`) | Owl Studio onboarding step |
| System prompt | Derived from `profiles/<slug>.json` at build time | Automatic |
| Widget embed | One `<script>` tag in template footer | Template default |
| Google Cloud project | Client's own Google account | Client creates (guided by Owl Studio) |

---

## Per-Client Setup Process

### Step 1 — Client Creates Google AI Studio Account

Guide the client through:

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in with a Google account (use existing Gmail or create one for the business)
3. Accept the terms of service
4. Click "Get API key" → "Create API key in new project"
5. Copy the key and send it to Owl Studio via the onboarding form or secure link

Time required: 5 minutes. Most Irish SME owners can do this unassisted with a one-page guide.

**Note on Google account ownership:** The client should own this Google account, not Owl Studio. This ensures:
- The client's chat data stays in their quota, under their Google terms
- If they leave Owl Studio, they still own the chatbot key
- Owl Studio is not responsible for their data

### Step 2 — Owl Studio Stores the Key

Add the key to the Render service as an environment variable:

```bash
# Via Render dashboard or API
GEMINI_KEY_rathborne-dental=AIza...
```

Pattern: `GEMINI_KEY_<slug>` — matches the `site_id` in `profiles/<slug>.json`.

### Step 3 — System Prompt Generated from Profile

At render time, `scripts/render-site.py` (or the `/owl/chat` endpoint at serve time) builds the system prompt from the profile JSON. The prompt is baked in per site — no runtime profile fetch needed.

### Step 4 — Widget Embedded in Site

Add one line to the site template footer:

```html
<script
  src="https://callmeie.onrender.com/owl/chat-widget.js"
  data-site-id="{{ slug }}"
  data-accent="{{ brand.accent }}"
></script>
```

The widget JS is served from Render (or a CDN). It injects the chat bubble into the page on load. The `data-site-id` tells the backend which system prompt to use.

### Step 5 — Test Before Launch

Standard site QA checklist plus:
- [ ] Send 5 test messages covering common questions (hours, location, services, booking, pricing)
- [ ] Confirm the bot refuses to answer out-of-scope questions
- [ ] Confirm the bot gives correct phone number and booking URL
- [ ] Confirm the bot does not hallucinate services not in the profile
- [ ] Test on mobile 375px

---

## System Prompt Template

This is the prompt structure for an Irish SME chatbot. It loads from the profile JSON. Fill `{{ }}` fields from `profiles/<slug>.json`.

```
You are the website assistant for {{ display_name }}, a {{ vertical }} practice located at {{ address.line1 }}, {{ address.city }}.

You help website visitors with questions about the practice. You are friendly, professional, and concise. You write in plain English — no jargon. You never exaggerate or make promises about clinical outcomes.

ABOUT THE PRACTICE
Name: {{ display_name }}
Address: {{ address.line1 }}, {{ address.city }}, {{ address.eircode }}
Phone: {{ phone }}
Email: {{ email }}
Established: {{ established_year }}

OPENING HOURS
{% for row in hours %}
{{ row.label }}: {{ row.value }}
{% endfor %}

SERVICES
{% for service in services %}
{{ service.kicker }}: {{ service.title }}
{{ service.body }}
{% if service.fees %}
Fees:
{% for fee in service.fees %}
  - {{ fee.label }}: {{ fee.price }}
{% endfor %}
{% endif %}

{% endfor %}

TEAM
{% for member in team %}
{{ member.name }} ({{ member.credentials }}) — {{ member.role }}
{% endfor %}

{% if insurance %}
ACCEPTED INSURANCE / PAYMENT SCHEMES
{{ insurance | join(', ') }}
{% endif %}

FREQUENTLY ASKED QUESTIONS
{% for item in faq %}
Q: {{ item.q }}
A: {{ item.a }}

{% endfor %}

RULES YOU MUST FOLLOW
1. Only answer questions using the information above. Do not invent services, fees, or facts not listed.
2. If you do not know the answer, say: "I'm not sure about that — please call us on {{ phone }} or email {{ email }} and we'll be happy to help."
3. Do not offer medical, legal, or financial advice. For health questions, tell visitors to call the practice.
4. Always provide the phone number {{ phone }} when a visitor needs urgent help.
5. Keep responses under 120 words unless a visitor explicitly asks for more detail.
6. Do not discuss competitors.
7. Use Irish spelling conventions (colour, centre, favour). Use "€" for prices, not "$".
8. If a visitor asks to book an appointment, direct them to: {% if booking_url %}{{ booking_url }}{% else %}call {{ phone }} or email {{ email }}{% endif %}

You are not a substitute for professional advice. You are an information assistant only.
```

**Token count estimate:** ~400-600 tokens for a typical Rathborne Dental-sized profile. Well within Gemini's 1M-token context window. This fits in one API call on every message.

**Approach justification — system prompt vs RAG vs fine-tuning:**

| Approach | Complexity | Cost | Right for SME? |
|---|---|---|---|
| System prompt with full business data | Low | Zero extra | Yes — entire profile fits in context window |
| RAG (vector DB + retrieval) | High | $10-50/month infra | No — overkill for < 5 pages of content |
| Fine-tuning | Very high | $100-1000 one-off | No — SME business data changes, model gets stale |

System prompt approach is correct. The SME's entire business profile is typically 500-1,500 tokens — this is exactly what large-context models are designed for.

---

## Implementation Code

### Backend: FastAPI `/owl/chat` Endpoint

Add to `callmeie.onrender.com` (the existing Render FastAPI service):

```python
# mcp-servers or callmeie-fix equivalent
import os
import json
import asyncio
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
import httpx

router = APIRouter()

class Message(BaseModel):
    role: str  # "user" or "model"
    parts: List[dict]

class ChatRequest(BaseModel):
    site_id: str
    messages: List[Message]

def get_system_prompt(site_id: str) -> str:
    """Load pre-built system prompt for a site_id."""
    # In v1: read from a static file generated at deploy time
    # In v2: read from DB keyed by site_id
    prompt_path = f"system_prompts/{site_id}.txt"
    if not os.path.exists(prompt_path):
        raise HTTPException(404, f"No chatbot configured for site {site_id}")
    with open(prompt_path) as f:
        return f.read()

def get_gemini_key(site_id: str) -> str:
    """Fetch per-client Gemini key from env vars."""
    env_key = f"GEMINI_KEY_{site_id.replace('-', '_')}"
    key = os.environ.get(env_key)
    if not key:
        raise HTTPException(500, "Chatbot not configured for this site")
    return key

@router.post("/owl/chat")
async def chat(req: ChatRequest):
    system_prompt = get_system_prompt(req.site_id)
    api_key = get_gemini_key(req.site_id)

    # Gemini API endpoint (streaming)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:streamGenerateContent?key={api_key}&alt=sse"

    payload = {
        "system_instruction": {
            "parts": [{"text": system_prompt}]
        },
        "contents": [m.dict() for m in req.messages],
        "generationConfig": {
            "maxOutputTokens": 300,
            "temperature": 0.3,  # low temp = consistent, factual responses
        }
    }

    async def stream_gemini():
        async with httpx.AsyncClient(timeout=30.0) as client:
            async with client.stream("POST", url, json=payload) as response:
                if response.status_code != 200:
                    error_body = await response.aread()
                    yield f"data: {json.dumps({'error': 'Gemini error'})}\n\n"
                    return
                async for line in response.aiter_lines():
                    if line.startswith("data:"):
                        yield f"{line}\n\n"

    return StreamingResponse(stream_gemini(), media_type="text/event-stream",
                             headers={"Access-Control-Allow-Origin": "*",
                                      "Cache-Control": "no-cache"})
```

### Frontend: Chat Widget (Vanilla JS, ~180 lines)

This is a self-contained script that injects a floating chat bubble into any HTML page. No React, no build step, no dependencies.

```javascript
// owl-chat-widget.js
// Embed: <script src="..." data-site-id="rathborne-dental" data-accent="#B38B6D"></script>

(function() {
  const script = document.currentScript;
  const SITE_ID = script.dataset.siteId;
  const ACCENT  = script.dataset.accent || '#2D5CA8';
  const API_URL = 'https://callmeie.onrender.com/owl/chat';

  if (!SITE_ID) { console.warn('[owl-chat] Missing data-site-id'); return; }

  // -- Inject styles --
  const style = document.createElement('style');
  style.textContent = `
    #owl-chat-btn {
      position: fixed; bottom: 24px; right: 24px; z-index: 9999;
      width: 56px; height: 56px; border-radius: 50%;
      background: ${ACCENT}; border: none; cursor: pointer;
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
      display: flex; align-items: center; justify-content: center;
      transition: transform 0.2s;
    }
    #owl-chat-btn:hover { transform: scale(1.08); }
    #owl-chat-panel {
      display: none; position: fixed; bottom: 90px; right: 24px; z-index: 9999;
      width: min(380px, calc(100vw - 48px)); height: 480px;
      background: #fff; border-radius: 16px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.18);
      flex-direction: column; overflow: hidden;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    #owl-chat-panel.open { display: flex; }
    #owl-chat-header {
      background: ${ACCENT}; color: #fff; padding: 14px 16px;
      font-weight: 600; font-size: 15px; display: flex;
      justify-content: space-between; align-items: center;
    }
    #owl-chat-close { background: none; border: none; color: #fff;
      font-size: 20px; cursor: pointer; line-height: 1; padding: 0; }
    #owl-chat-messages {
      flex: 1; overflow-y: auto; padding: 16px;
      display: flex; flex-direction: column; gap: 10px;
    }
    .owl-msg {
      max-width: 80%; padding: 10px 14px; border-radius: 12px;
      font-size: 14px; line-height: 1.5;
    }
    .owl-msg.bot { background: #f1f3f5; align-self: flex-start; border-bottom-left-radius: 4px; }
    .owl-msg.user { background: ${ACCENT}; color: #fff; align-self: flex-end; border-bottom-right-radius: 4px; }
    .owl-msg.typing { color: #888; font-style: italic; }
    #owl-chat-form { display: flex; padding: 12px; gap: 8px; border-top: 1px solid #eee; }
    #owl-chat-input {
      flex: 1; border: 1px solid #ddd; border-radius: 8px;
      padding: 8px 12px; font-size: 14px; outline: none;
      font-family: inherit;
    }
    #owl-chat-input:focus { border-color: ${ACCENT}; }
    #owl-chat-send {
      background: ${ACCENT}; color: #fff; border: none;
      border-radius: 8px; padding: 8px 14px; cursor: pointer;
      font-size: 14px; font-weight: 600;
    }
    #owl-chat-send:disabled { opacity: 0.5; cursor: not-allowed; }
  `;
  document.head.appendChild(style);

  // -- Inject HTML --
  const btn = document.createElement('button');
  btn.id = 'owl-chat-btn';
  btn.setAttribute('aria-label', 'Open chat');
  btn.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>`;

  const panel = document.createElement('div');
  panel.id = 'owl-chat-panel';
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-label', 'Chat with us');
  panel.innerHTML = `
    <div id="owl-chat-header">
      <span>Chat with us</span>
      <button id="owl-chat-close" aria-label="Close chat">&times;</button>
    </div>
    <div id="owl-chat-messages" aria-live="polite"></div>
    <form id="owl-chat-form">
      <input id="owl-chat-input" type="text" placeholder="Ask a question..." autocomplete="off" maxlength="500" />
      <button id="owl-chat-send" type="submit">Send</button>
    </form>
  `;

  document.body.appendChild(btn);
  document.body.appendChild(panel);

  // -- State --
  const messages = [];
  let isOpen = false;

  // -- Helpers --
  function appendMessage(role, text, isTyping = false) {
    const msgEl = document.createElement('div');
    msgEl.className = `owl-msg ${role}${isTyping ? ' typing' : ''}`;
    msgEl.textContent = text;
    document.getElementById('owl-chat-messages').appendChild(msgEl);
    msgEl.scrollIntoView({ block: 'end' });
    return msgEl;
  }

  function togglePanel() {
    isOpen = !isOpen;
    panel.classList.toggle('open', isOpen);
    if (isOpen && messages.length === 0) {
      appendMessage('bot', 'Hi! I can answer questions about our services, opening hours, and how to get in touch. What would you like to know?');
    }
    if (isOpen) document.getElementById('owl-chat-input').focus();
  }

  // -- Events --
  btn.addEventListener('click', togglePanel);
  document.getElementById('owl-chat-close').addEventListener('click', togglePanel);

  document.getElementById('owl-chat-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const input = document.getElementById('owl-chat-input');
    const text = input.value.trim();
    if (!text) return;

    input.value = '';
    appendMessage('user', text);
    messages.push({ role: 'user', parts: [{ text }] });

    const sendBtn = document.getElementById('owl-chat-send');
    sendBtn.disabled = true;
    const typingEl = appendMessage('bot', 'Typing…', true);

    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ site_id: SITE_ID, messages })
      });

      if (!res.ok) throw new Error('Request failed');

      // SSE streaming
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let botText = '';
      typingEl.textContent = '';
      typingEl.classList.remove('typing');

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');
        for (const line of lines) {
          if (!line.startsWith('data:')) continue;
          const data = line.slice(5).trim();
          if (data === '[DONE]') break;
          try {
            const parsed = JSON.parse(data);
            const text = parsed.candidates?.[0]?.content?.parts?.[0]?.text || '';
            botText += text;
            typingEl.textContent = botText;
            typingEl.scrollIntoView({ block: 'end' });
          } catch (_) {}
        }
      }

      if (botText) {
        messages.push({ role: 'model', parts: [{ text: botText }] });
      }
    } catch (err) {
      typingEl.textContent = "Sorry, I'm having trouble connecting. Please call us directly.";
      typingEl.classList.remove('typing');
    } finally {
      sendBtn.disabled = false;
      document.getElementById('owl-chat-input').focus();
    }
  });

  // Close on Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && isOpen) togglePanel();
  });
})();
```

### System Prompt Generator Script

```python
# scripts/generate_chat_prompts.py
# Run after render-site.py to produce system_prompts/<slug>.txt

import json
import os
from pathlib import Path
from jinja2 import Template

PROMPT_TEMPLATE = """You are the website assistant for {{ display_name }}, 
a {{ vertical }} practice located at {{ address.line1 }}, {{ address.city }}.
... (full template from System Prompt Template section above)
"""

def generate_prompt(profile_path: str) -> str:
    with open(profile_path) as f:
        profile = json.load(f)
    template = Template(PROMPT_TEMPLATE)
    return template.render(**profile)

if __name__ == '__main__':
    profiles_dir = Path('profiles')
    prompts_dir = Path('system_prompts')
    prompts_dir.mkdir(exist_ok=True)

    for profile_file in profiles_dir.glob('*.json'):
        slug = profile_file.stem
        prompt = generate_prompt(str(profile_file))
        out_path = prompts_dir / f"{slug}.txt"
        out_path.write_text(prompt)
        print(f"Generated {out_path} ({len(prompt)} chars)")
```

---

## Cost Reality Check

### Free Tier Capacity vs SME Traffic

A typical Owl Studio client has:
- 100-500 monthly website visitors (local Irish SME, no paid ads yet)
- 5-15% chatbot engagement rate (industry benchmark for embedded widgets)
- Average 3-5 messages per conversation

Monthly chatbot calls = 500 visitors × 10% engagement × 4 messages = **200 API calls/month**

Gemini 2.5 Flash-Lite free tier gives **1,000 requests/day** = 30,000 requests/month. A typical SME client uses less than 1% of the free daily allowance.

**The free tier is more than sufficient for any Owl Studio client at current traffic levels.** Even a site with 5,000 monthly visitors at 15% engagement = 3,000 messages/month — still within free limits.

### When Free Tier Breaks

The free tier becomes a problem at:
- 15+ messages per minute sustained (a chatbot going viral, or being spammed)
- 250+ conversations/day on Gemini 2.5 Flash (lower limit model)
- Any point where Google decides to cut limits again (happened Dec 2025)

Mitigation: use Gemini 2.5 Flash-Lite (1,000 req/day) instead of Flash (250 req/day) for the default model. Slightly less capable but the difference is imperceptible for constrained FAQ use.

### Paid Tier Costs if Free Tier is Exhausted

Gemini 2.5 Flash-Lite paid pricing:
- Input: $0.10 per 1M tokens
- Output: $0.40 per 1M tokens

At 500 monthly conversations × 4 messages × 200 tokens average:
= 400,000 tokens/month
= $0.04 input + $0.16 output
= **$0.20/month**

Even at 10x that traffic: $2/month. This will never be a material cost at SME scale. The free tier is a nice bonus; the paid tier is a rounding error.

### Hosting Cost (Render FastAPI backend)

Existing callmeie.onrender.com service. The `/owl/chat` endpoint is one additional route on an already-running service. No incremental hosting cost.

Render free tier sleeps after 15 minutes of inactivity — cold start is 500ms-2s. For chat this is noticeable on the first message after a quiet period. **Solutions:**
- UptimeRobot pings every 10 minutes (already planned per PDR-BACKEND) — keeps it warm at zero cost
- Or serve the chat widget JS from Render but proxy actual Gemini calls through a Cloudflare Worker (instant response, free)

### Cloudflare Worker as Optional Proxy Layer

If Render cold starts are unacceptable for chat UX:

```
Browser → Cloudflare Worker (0ms cold start, free 100K req/day)
              → Render FastAPI (for system prompt lookup, first call only)
              → Gemini API (direct from Worker for streaming)
```

Cloudflare Worker free tier: 100K requests/day. An SME chatbot uses ~10-50 requests/day. Headroom is enormous.

### Summary Cost Table

| Component | Cost |
|---|---|
| Gemini API (free tier) | €0 |
| Gemini API (if free exhausted) | <€2/month at SME scale |
| Render FastAPI hosting | €0 (existing service) |
| Cloudflare Worker (optional) | €0 (free tier) |
| Client Google account | €0 |
| **Total per client (typical)** | **€0** |
| **Total per client (high traffic)** | **<€5/month** |

### Product Pricing Recommendation

Given zero marginal cost, the chatbot add-on can be:

- **Included free** in Growth and Concierge care plans (conversion tool, not cost centre)
- **€20-30/month add-on** for Essential plan clients who want it
- **Setup fee** of €100-150 to cover the onboarding, system prompt writing, testing, and per-client Google AI Studio setup

The value proposition to the client: "an AI assistant that answers your most common questions 24/7, so you stop getting phone calls asking for your opening hours."

---

## Constraints and Decisions Not Made

Things left for the next session:

- [ ] Decide whether system prompt is baked into widget JS at build time, or fetched from Render at widget-init time (build-time is simpler and faster; fetch-at-init allows live edits)
- [ ] Decide on conversation history depth (storing last N messages in browser sessionStorage — no server-side session needed)
- [ ] Decide on rate limiting on the `/owl/chat` endpoint (prevent abuse / prompt injection from public sites)
- [ ] GDPR disclosure text in the chat widget ("By using this chat, you agree to our privacy policy. Do not share sensitive personal information.")
- [ ] System prompt injection attack mitigation (tell Gemini to ignore instructions that override its rules)
- [ ] Mobile keyboard behaviour (chat input pushing content up on iOS)
- [ ] Build the prototype on one live site before rolling out to all clients

---

## Build Sequence (Next Steps)

This follows the prototype-before-batch gate from the collaborator behavior contract.

1. **Prototype on Rathborne Dental demo** — one site, full end-to-end
   - Generate `system_prompts/rathborne-dental.txt` from existing profile
   - Add `/owl/chat` endpoint to callmeie FastAPI with Render env var key
   - Ship `chat-widget.js` as standalone file on Render static files
   - Embed in `client-builds/rathborne-dental/index.html`
   - Test 20+ real conversations

2. **Review + iterate** — what does the bot get wrong? Fix system prompt.

3. **Add to template** — wire `{{ slug }}` into chat widget embed in `render-site.py`

4. **Document per-client setup** — one-page guide for clients + Owl Studio runbook

5. **Ship to first real client** — only after prototype proves quality

---

*Sources for rate limit data: [Google AI for Developers — Rate Limits](https://ai.google.dev/gemini-api/docs/rate-limits) · [AI Free API — Gemini Free Tier Guide](https://www.aifreeapi.com/en/posts/gemini-api-free-tier-complete-guide) · [Google AI for Developers — Pricing](https://ai.google.dev/gemini-api/docs/pricing) · [LaoZhang AI Blog — Free Tier 2026](https://blog.laozhang.ai/en/posts/gemini-api-free-tier) · [BSWEN — AI Studio Free Tier Limits 2026](https://docs.bswen.com/blog/2026-03-23-google-ai-studio-free-tier-limits/) · [DataStudios — Gemini GDPR](https://www.datastudios.org/post/google-gemini-gdpr-hipaa-and-enterprise-compliance-standards-explained) · [Cloudflare Workers Pricing](https://developers.cloudflare.com/workers/platform/pricing/) · [Agent Deals — Free Tier Comparison 2026](https://agentdeals.dev/hosting-free-tier-comparison-2026) · [ProfileTree — AI Chatbots for Irish SME Websites](https://profiletree.com/ai-chatbots-in-sme-websites-a-practical-integration-guide-for-businesses-in-ireland-and-the-uk/)*
