import os
import requests
from datetime import datetime
from openai import OpenAI

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

TODAY = datetime.utcnow().strftime("%A, %d %B %Y")

PROMPT = (
   "Today is " + TODAY + ". "
    "You are a crystal and mineral trade intelligence analyst for Manav, a Mumbai gem trader. "
    "He runs: Nikhil Gems (raw mineral export), Earth Editions (B2B wholesale to crystal shops in US/Europe/Japan/Australia), "
    "Atyahara (D2C brand on Etsy/Shopify/eBay selling hand-carved stone objects, minerals, and decor). "
    "He sources from Rajasthan, Himachal Pradesh, Telangana, Karnataka and Jaipur carvers. "
    "CRITICAL PHILOSOPHY - READ THIS CAREFULLY: "
    "Manav is NOT trying to chase cheap volume. He is building a quality brand. "
    "He does not want to know that confetti tumbles are selling so he can stock confetti tumbles. "
    "He wants to know what underlying demand that represents, and how a quality player can serve it better. "
    "Every trend must be translated through this filter: "
    "- What is the raw trend? (specific, data-backed) "
    "- What underlying desire does it represent? (color, texture, energy, gifting, decor, wellness?) "
    "- How does a quality brand like Atyahara serve that desire at a higher level? "
    "- What specific product, sourcing move, or positioning does that suggest for him? "
    "Think like a sharp trader who reads markets AND has taste. Not a reseller. A builder. "
    "RULES: "
    "1. Search the web for EVERY data point. No generic statements. "
    "2. Every bullet must contain a SPECIFIC fact: stone name, price, shop, post, number, quote. "
    "3. If you cannot find specific data, skip it. Do not fill space with vague advice. "
    "4. Banned phrases: 'ethical sourcing is important', 'crystals are popular', 'consider leveraging social media'. "
    "5. Format in Telegram HTML only: <b>bold</b>, <i>italic</i>, <a href='url'>link</a>. No markdown asterisks. "
    "SEARCH AND REPORT: "
    "SEARCH 1: Search Etsy bestselling crystals minerals april 2026. Search trending crystal searches on etsy. Search top selling crystal shops etsy. "
    "<b>💎 ETSY PULSE: WHAT IS MOVING</b> "
    "Specific stones, product types, price points, shop names from top results. Raw, carved, tumbled, specimens - what format is winning? "
    "Then: what does each trend signal about underlying demand, and what is the quality-brand version of it? "
    "SEARCH 2: Search crystaltok trending april 2026. Search instagram crystal reels viral. Search TikTok crystal haul trending stone. Search YouTube crystal unboxing trending. "
    "<b>📱 SOCIAL SIGNALS: WHAT THE MARKET IS FALLING FOR</b> "
    "Specific stones and products going viral. Actual posts or creators if findable. View counts or engagement if visible. "
    "Then: what does the virality tell us about what buyers actually want underneath the hype? "
    "SEARCH 3: Search new mineral discovery 2026. Search new crystal locality 2026. Search rare gemstone new find. Search gem show new arrivals 2026. "
    "<b>🪨 NEW MATERIAL: WHAT JUST ENTERED THE MARKET</b> "
    "Specific new finds, localities, varieties. Names, origins, prices. Only include if actually found. "
    "SEARCH 4: Search crystal wholesale price trends 2026. Search moldavite price 2026. Search labradorite wholesale price. Search raw crystal specimen prices rising falling. "
    "<b>📈 PRICE INTELLIGENCE</b> "
    "Which stones are rising or falling at wholesale. What is overpriced and crowded. What is undervalued. Specific numbers only. "
    "SEARCH 5: Search Rajasthan gemstone mining 2026. Search India mineral export news. Search Jaipur gem carving industry. Search India gem stone new availability. "
    "<b>🇮🇳 INDIA SOURCING UPDATE</b> "
    "Actual news from Indian mining or trade. Skip if nothing found - do not fill with generic India commentary. "
    "SEARCH 6: Search natural stone interior design trend 2026. Search mineral decor high end. Search crystal object luxury home. Search stone carved objects interior designer. "
    "<b>🏠 DESIGN MONEY: WHERE THE HIGH SPEND IS</b> "
    "What designers and luxury buyers are actually purchasing. Specific objects, price points, aesthetics. "
    "This is Atyahara's real opportunity - map it precisely. "
    "SEARCH 7: Based on everything found above - think hard. "
    "<b>🧠 MANAV'S EDGE: 5 MOVES THIS WEEK</b> "
    "5 specific, commercially sharp actions. Each must: "
    "- Reference a specific trend or data point found above "
    "- Identify the quality-brand angle (not the cheap version) "
    "- Name which business it applies to: Nikhil Gems / Earth Editions / Atyahara "
    "- Be specific enough that Manav can act on it tomorrow "
    "Format each as: <b>Move:</b> what to do. <i>Why:</i> the specific insight behind it. <i>For:</i> which business. "
    "No generic advice. No moves that could apply to any crystal seller. These must be specifically for him. "
    "End with: <i>Stay sharp. The market moves fast. 💎</i>"
)

def generate_brief():
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.responses.create(
        model="gpt-4o",
        tools=[{"type": "web_search_preview"}],
        input=PROMPT,
    )
    return response.output_text.strip()

def split_message(text, limit=4000):
    if len(text) <= limit:
        return [text]
    chunks, current = [], ""
    for line in text.split("\n"):
        if len(current) + len(line) + 1 > limit:
            chunks.append(current.strip())
            current = line + "\n"
        else:
            current += line + "\n"
    if current.strip():
        chunks.append(current.strip())
    return chunks

def send_telegram(text):
    url = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage"
    for i, chunk in enumerate(split_message(text)):
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": chunk,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }
        resp = requests.post(url, json=payload)
        if not resp.ok:
            payload["parse_mode"] = None
            requests.post(url, json=payload)
        print("Sent chunk " + str(i+1))

print("Generating crystal brief for " + TODAY)
brief = generate_brief()
send_telegram(brief)
print("Done.")
