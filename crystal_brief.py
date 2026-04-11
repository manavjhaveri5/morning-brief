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
    "Atyahara (D2C carved stone objects on Etsy/Shopify/eBay). "
    "He sources from Rajasthan, Himachal Pradesh, Telangana, Karnataka and Jaipur carvers. "
    "RULES - YOU MUST FOLLOW THESE OR THE REPORT IS USELESS: "
    "1. Search the web for EVERY data point. No generic statements allowed. "
    "2. Every bullet must contain a SPECIFIC fact: a stone name, a price, a shop name, a post, a number, a quote. "
    "3. If you cannot find specific data for something, skip it. Do not fill space with vague advice. "
    "4. No sentences like 'crystals are popular' or 'ethical sourcing is important' - these are banned. "
    "5. Format in Telegram HTML only: <b>bold</b>, <i>italic</i>, <a href='url'>link</a>. No markdown asterisks. "
    "NOW SEARCH AND REPORT: "
    "SEARCH 1: Search Etsy right now for 'crystals' sorted by bestselling. Search 'trending crystals etsy 2026'. Search 'best selling crystal shops etsy april 2026'. "
    "<b>💎 ETSY: WHAT IS ACTUALLY SELLING</b> "
    "List specific stones and products appearing in top Etsy results. Include shop names, listing titles, price ranges. What shapes - spheres, towers, raw, carved? What stones - selenite, obsidian, labradorite, moldavite, what specifically? "
    "SEARCH 2: Search Twitter/X for #crystals #minerals today. Search TikTok crystal trends april 2026. Search Instagram reels crystals trending. Search 'crystaltok trending stone 2026'. "
    "<b>📱 SOCIAL: WHAT IS GOING VIRAL</b> "
    "Name the specific stones and products going viral. Which crystal accounts posted what. Any stone blowing up with view counts or engagement. Specific posts or videos if findable. "
    "SEARCH 3: Search 'new mineral discovery 2026'. Search 'new crystal find april 2026'. Search 'rare gemstone new locality 2026'. Search gem show news and new arrivals. "
    "<b>🪨 NEW AND RARE: WHAT JUST ENTERED THE MARKET</b> "
    "Specific new finds, new localities, new stone varieties. Names, origins, prices if available. "
    "SEARCH 4: Search 'wholesale crystal buying trends 2026'. Search 'crystal shop owner what to stock'. Search crystal market price changes. Search 'moldavite price 2026' and similar for hot stones. "
    "<b>📈 PRICES AND WHOLESALE MOVEMENT</b> "
    "Which stones are rising or falling in price. What wholesale buyers are ordering. Specific price data points. "
    "SEARCH 5: Search 'Rajasthan mining news 2026'. Search 'India gem export news april 2026'. Search 'Jaipur gem industry 2026'. Search 'India mineral stone news today'. "
    "<b>🇮🇳 INDIA: SOURCING AND TRADE NEWS</b> "
    "Specific news from Indian mining regions or gem trade. Only include if you find actual news. Skip if nothing found. "
    "SEARCH 6: Search crystal home decor trending. Search natural stone interior design 2026. Search biophilic design products trending. "
    "<b>🏠 DESIGN WORLD: WHAT DECORATORS ARE BUYING</b> "
    "Specific products, specific designers or brands using stone. What objects - bowls, clusters, slabs? "
    "SEARCH 7: Combine everything you found above. Think like a trading desk analyst. "
    "<b>🧠 ACTION BRIEF FOR MANAV</b> "
    "5 specific actions based only on what you actually found above. "
    "Each point must reference a specific trend, stone, or data point you found. "
    "Format: What to do + Why (citing the specific thing you found) + Which business it applies to (Nikhil Gems / Earth Editions / Atyahara). "
    "No generic advice. If you cannot back it with something from your searches, do not include it. "
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
