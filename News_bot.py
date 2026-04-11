import os
import requests
from datetime import datetime
from openai import OpenAI

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

TODAY = datetime.utcnow().strftime("%A, %d %B %Y")

PROMPT = (
    "You are a sharp daily briefing assistant for Manav, a Mumbai-based gem trader and ecommerce entrepreneur. "
    "He runs Nikhil Gems (export), Earth Editions (B2B wholesale), Atyahara (D2C stone objects on Shopify/Etsy/eBay). "
    "He exports to US, Europe, Japan, Australia and attends Tucson and Denver gem shows. "
    "Write a crisp daily brief using web search for every section. Real numbers, real links. "
    "Format in Telegram HTML with bold headers and emoji. "
    "Today is " + TODAY + ". "
    "Cover: "
    "1. Gem and mineral trade news. "
    "2. India export and trade policy, DGFT, RBI, GST. "
    "3. Forex: USD/INR, EUR/INR, JPY/INR, AUD/INR. "
    "4. Etsy, Shopify, eBay platform news. "
    "5. Meta and Instagram ads updates. "
    "6. Luxury and interior design trends. "
    "7. India business and logistics news. "
    "8. One big global story of the day. "
    "Each section: bold emoji header, 2-4 bullet points, include links. "
    "End with: That is your brief. Go make it count."
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

print("Generating brief for " + TODAY)
brief = generate_brief()
send_telegram(brief)
print("Done.")
