#!/usr/bin/env python3
“””
Manav’s Daily Morning Brief — Telegram Bot
Runs via GitHub Actions at 10am IST every day.
Powered by OpenAI gpt-4o with web search.
“””

import os
import requests
from datetime import datetime
from openai import OpenAI

# ── Config ──────────────────────────────────────────────────────────────────

TELEGRAM_TOKEN = os.environ[“TELEGRAM_BOT_TOKEN”]
TELEGRAM_CHAT_ID = os.environ[“TELEGRAM_CHAT_ID”]
OPENAI_API_KEY = os.environ[“OPENAI_API_KEY”]

TODAY = datetime.utcnow().strftime(”%A, %d %B %Y”)

# ── Prompt ───────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = “”“You are a sharp, well-informed daily briefing assistant for Manav — a Mumbai-based gem and mineral trader and e-commerce entrepreneur.

He runs:

- Nikhil Gems (gem/mineral export, family business since 1976)
- Earth Editions (B2B wholesale platform for crystal shops globally)
- Atyahara (D2C Shopify/Etsy/eBay brand, hand-carved natural stone objects)

He exports to US, Europe, Japan, Australia. He attends Tucson and Denver gem shows. He is building a Shopify B2B platform and a custom React ERP. He also tracks interior design trends as Atyahara targets design-conscious urban buyers.

Write a crisp, rich daily brief. Use web search extensively — check multiple sources for each section. Be specific: real numbers, real stories, real links. No filler. No generic summaries.

Format in Telegram HTML. Use <b>, <i>, <a href="...">, and emoji. Structure:

<b>☀️ MANAV’S MORNING BRIEF — “”” + TODAY + “””</b>

Then one section at a time, each with a bold emoji header and 2–4 tight bullet points. Each bullet should have a link to read more where relevant.

Sections to cover — search each one:

1. 💎 GEM & MINERAL TRADE — rough/cut stone prices, India mining news (Rajasthan, HP, Telangana), international gem market, Tucson/Denver show news
1. 📦 INDIA EXPORT & TRADE POLICY — DGFT notifications, RBI/FEMA updates, customs/GST changes (HSN 7103, semi-precious stones)
1. 💱 FOREX — USD/INR, EUR/INR, JPY/INR, AUD/INR — today’s rates + direction
1. 🛒 E-COMMERCE PLATFORMS — Etsy, Shopify, eBay policy/algorithm news, seller community updates
1. 📱 META & PAID SOCIAL — Instagram algorithm, Meta Ads, pixel/conversion API changes
1. 🪨 LUXURY & DESIGN — interior design trends, natural materials in décor, luxury gifting market, design world news
1. 🇮🇳 INDIA BUSINESS — SME/startup policy, logistics (FedEx, shipping), Mumbai business, broader macro
1. 🌍 BIG STORY OF THE DAY — one major global story that’s interesting, unusual, or significant — anything Manav should know about

End with:
<i>That’s your brief. Go make it count. 🤙</i>

Be editorial. Sound like a smart, slightly irreverent friend who reads everything — not a press release bot.”””

USER_PROMPT = f”Today is {TODAY}. Search the web thoroughly across all 8 sections and write Manav’s morning brief. Be specific with numbers, names, and links. Keep each bullet punchy — 1–2 lines max. Include real URLs for further reading.”

# ── Call OpenAI with web search ───────────────────────────────────────────────

def generate_brief():
client = OpenAI(api_key=OPENAI_API_KEY)

```
print("Calling OpenAI with web search...")
response = client.responses.create(
    model="gpt-4o",
    tools=[{"type": "web_search_preview"}],
    instructions=SYSTEM_PROMPT,
    input=USER_PROMPT,
)

return response.output_text.strip()
```

# ── Send to Telegram ─────────────────────────────────────────────────────────

def send_telegram(text: str):
url = f”https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage”

```
# Telegram has a 4096 char limit per message — split if needed
chunks = split_message(text, limit=4000)

for i, chunk in enumerate(chunks):
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": chunk,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    resp = requests.post(url, json=payload)
    if not resp.ok:
        print(f"Telegram error on chunk {i+1}: {resp.text}")
        # Retry as plain text if HTML parsing failed
        payload["parse_mode"] = None
        resp = requests.post(url, json=payload)
    else:
        print(f"Sent chunk {i+1}/{len(chunks)} ✓")
```

def split_message(text: str, limit: int = 4000) -> list[str]:
“”“Split long messages at newlines to stay under Telegram’s limit.”””
if len(text) <= limit:
return [text]

```
chunks = []
current = ""
for line in text.split("\n"):
    if len(current) + len(line) + 1 > limit:
        chunks.append(current.strip())
        current = line + "\n"
    else:
        current += line + "\n"
if current.strip():
    chunks.append(current.strip())
return chunks
```

# ── Main ─────────────────────────────────────────────────────────────────────

if **name** == “**main**”:
print(f”Generating brief for {TODAY}…”)
brief = generate_brief()

```
if not brief:
    print("ERROR: Empty brief generated.")
    exit(1)

print(f"Brief generated ({len(brief)} chars). Sending to Telegram...")
send_telegram(brief)
print("Done. ✓")
```
