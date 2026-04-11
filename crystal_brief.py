import os
import requests
from datetime import datetime
from openai import OpenAI

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

TODAY = datetime.utcnow().strftime("%A, %d %B %Y")

PROMPT = (
    "You are an elite crystal and mineral industry intelligence analyst. "
    "Your client is Manav, a Mumbai-based gem and mineral trader who runs Nikhil Gems (export since 1976), "
    "Earth Editions (B2B wholesale to crystal shops in US, Europe, Japan, Australia), "
    "and Atyahara (D2C Shopify/Etsy/eBay brand selling hand-carved natural stone objects and minerals). "
    "He sources from Indian mines (Rajasthan, Himachal Pradesh, Telangana, Karnataka) and Jaipur artisans. "
    "He sells minerals, raw specimens, hand-carved stone bowls, figurines, and decor. "
    "He attends Tucson and Denver gem shows. "
    "Today is " + TODAY + ". "
    "CRITICAL: Use web search aggressively for EVERY section. Search Etsy, Instagram posts, TikTok trends, "
    "Reddit crystal communities, YouTube, gem show announcements, trade publications, seller forums, "
    "Google Trends, and news sites. Find what happened in the last 24-48 hours in the crystal and mineral world. "
    "Format ONLY in Telegram HTML. Use <b>text</b> for bold, <i>text</i> for italic, <a href='url'>link</a> for links. "
    "Never use markdown asterisks. Only HTML tags. "
    ""
    "Write the following sections: "
    ""
    "Section 1 - Search: site:etsy.com crystal minerals trending + Etsy bestseller crystal lists + what crystals are selling on etsy 2026. "
    "<b>💎 WHAT IS SELLING ON ETSY RIGHT NOW</b> "
    "Which specific stones, shapes, carvings, and products are trending. "
    "Search for bestselling crystal listings, trending searches, what shops are promoting. "
    "Be specific: stone names, product types, price points if visible. "
    ""
    "Section 2 - Search: crystal tiktok trending + tiktok crystals viral + instagram crystal reels trending + #crystaltok + crystal influencer posts. "
    "<b>📱 TRENDING ON SOCIAL MEDIA</b> "
    "What stones and products are going viral on TikTok and Instagram right now. "
    "Which crystals are being featured by influencers. What aesthetics and formats are getting engagement. "
    "Search for recent viral crystal posts, trending hashtags, what crystal creators are posting. "
    ""
    "Section 3 - Search: new crystal find 2026 + new mineral discovery + rare gemstone news + gem show new arrivals + Tucson Denver gem show 2026. "
    "<b>🪨 NEW FINDS AND HOT STONES</b> "
    "Any newly discovered minerals, new localities, new cuts or shapes entering the market. "
    "What stones are being talked about as the next big thing. Any new arrivals from gem shows. "
    ""
    "Section 4 - Search: crystal market trend 2026 + wholesale crystal buying trends + crystal shop owner what to buy + gemstone trend forecast. "
    "<b>📈 MARKET TRENDS AND BUYER INTELLIGENCE</b> "
    "What are crystal shop owners buying and stocking. What is moving fast vs sitting on shelves. "
    "Price movements on key stones. What categories (raw, carved, tumbled, specimens) are growing. "
    ""
    "Section 5 - Search: India gemstone mining news 2026 + Rajasthan mining + India mineral export news + Jaipur gem industry news. "
    "<b>🇮🇳 INDIA SOURCING INTELLIGENCE</b> "
    "Any news from Indian mining districts - Rajasthan, HP, Telangana, Karnataka. "
    "Price changes at source. New material available. Export regulation changes. "
    "Jaipur carving industry updates. Any trade show or buyer activity in India. "
    ""
    "Section 6 - Search: interior design crystals decor trend 2026 + natural stone home decor trending + crystal home styling + biophilic design stone. "
    "<b>🏠 DESIGN AND DECOR CROSSOVER</b> "
    "How is the interior design world using crystals and minerals. "
    "Which stones are appearing in design editorials, home decor shops, architect projects. "
    "What carved objects and display pieces are trending for gifting and home styling. "
    ""
    "Section 7 - Search: crystal industry news today + gemstone business news + rock and mineral show news + crystal wholesale news. "
    "<b>📰 INDUSTRY NEWS</b> "
    "Any significant news from the crystal and mineral industry in the last 24-48 hours. "
    "Trade show announcements, major seller news, platform changes affecting crystal sellers, "
    "any business or regulatory news relevant to the gem trade. "
    ""
    "Section 8 - Based on all the above research: "
    "<b>🧠 MANAV'S ACTION BRIEF</b> "
    "This is the most important section. Based on everything you found, give Manav 4-6 specific, actionable recommendations. "
    "What should he be sourcing right now. Which stones or products should Atyahara list immediately. "
    "What should Earth Editions be pitching to wholesale buyers. What trend should he get ahead of. "
    "What should he avoid or reduce. Be direct, specific, and commercially sharp. "
    "Think like a ruthless, well-informed business advisor who knows the crystal trade deeply. "
    ""
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
