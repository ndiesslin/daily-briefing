import requests
import feedparser
import os
from dotenv import load_dotenv

load_dotenv()

import random
import math

def get_weather():
    location_query = os.getenv("LOCATION") or os.getenv("CITY") or "New York"
    
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location_query}&count=1&language=en&format=json"
        geo_resp = requests.get(geo_url)
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()
        
        if not geo_data.get("results"):
            return {"error": f"Location '{location_query}' not found", "city": location_query}
        
        location = geo_data["results"][0]
        lat, lon = location["latitude"], location["longitude"]
        display_name = location.get("name", location_query)
        if location.get("postcode"):
            display_name = f"{display_name} ({location['postcode']})"
        
        # 2. Get Weather + Sunrise/Sunset
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,weathercode,sunrise,sunset&current_weather=true&temperature_unit=fahrenheit&windspeed_unit=mph&timezone=auto"
        weather_resp = requests.get(weather_url)
        weather_resp.raise_for_status()
        data = weather_resp.json()
        
        current = data["current_weather"]
        daily = data["daily"]
        
        weather_map = {0: ("Clear sky", "☀️"), 1: ("Mainly clear", "🌤️"), 2: ("Partly cloudy", "⛅"), 3: ("Overcast", "☁️"), 45: ("Fog", "🌫️"), 48: ("Fog", "🌫️"), 51: ("Drizzle", "🌦️"), 61: ("Rain", "🌧️"), 71: ("Snow", "❄️"), 95: ("Thunderstorm", "⛈️")}
        desc, emoji = weather_map.get(current["weathercode"], ("Cloudy", "☁️"))
        
        return {
            "temp": f"{current['temperature']}°F",
            "high": f"{daily['temperature_2m_max'][0]}°F",
            "low": f"{daily['temperature_2m_min'][0]}°F",
            "wind": f"{current['windspeed']} mph",
            "sunrise": daily["sunrise"][0].split("T")[1],
            "sunset": daily["sunset"][0].split("T")[1],
            "description": desc,
            "emoji": emoji,
            "city": display_name
        }
    except Exception as e:
        return {"error": str(e), "city": location_query}

def get_brain_food():
    # 1. Quote
    quote = {"text": "Make each day your masterpiece.", "author": "John Wooden"}
    try:
        resp = requests.get("https://zenquotes.io/api/today", timeout=5)
        if resp.status_code == 200:
            data = resp.json()[0]
            quote = {"text": data["q"], "author": data["a"]}
    except: pass

    # 2. History
    history = "Discovery of something amazing happened on this day."
    try:
        from datetime import datetime
        now = datetime.now()
        # Use leading zeros for month and day
        m = f"{now.month:02d}"
        d = f"{now.day:02d}"
        hist_url = f"https://en.wikipedia.org/api/rest_v1/feed/onthisday/selected/{m}/{d}"
        resp = requests.get(hist_url, timeout=5, headers={"User-Agent": "DailyBriefingBot/1.0 (contact: newsbot@example.com)"})
        if resp.status_code == 200:
            events = resp.json().get("selected", [])
            if events:
                event = random.choice(events) # Randomly pick a curated event
                history = f"{event['year']}: {event['text']}"
    except Exception as e:
        history = f"Error fetching history: {str(e)}"

    # 3. Word of the Day (Simple list for stability)
    words = [
        ("Serendipity", "Finding something good without looking for it."),
        ("Resilience", "The capacity to recover quickly from difficulties."),
        ("Ephemeral", "Lasting for a very short time."),
        ("Luminous", "Full of or shedding light; bright or shining, especially in the dark.")
    ]
    word, definition = random.choice(words)

    return {"quote": quote, "history": history, "word": {"term": word, "def": definition}}

def get_markets():
    symbols = os.getenv("MARKET_SYMBOLS", "XAU,ETH").split(",")
    markets = {}
    
    # Mapping for friendly labels and API lookups
    crypto_ids = {"ETH": "ethereum", "BTC": "bitcoin", "SOL": "solana", "DOGE": "dogecoin", "LINK": "chainlink"}
    metal_syms = {"XAU": "Gold", "XAG": "Silver", "XPT": "Platinum", "XPD": "Palladium"}

    for sym in symbols:
        sym = sym.strip().upper()
        try:
            if sym in crypto_ids:
                cid = crypto_ids[sym]
                resp = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={cid}&vs_currencies=usd", timeout=5)
                if resp.status_code == 200:
                    price = resp.json()[cid]['usd']
                    markets[sym] = f"${price:,}" if price >= 1 else f"${price:.4f}"
            elif sym in metal_syms:
                label = metal_syms[sym]
                resp = requests.get(f"https://api.gold-api.com/price/{sym}", timeout=5)
                if resp.status_code == 200:
                    markets[f"{label} ({sym})"] = f"${resp.json()['price']:.2f}"
        except: continue
        
    return markets

def get_moon_phase():
    # Simple moon phase calculation
    from datetime import datetime
    diff = datetime.now() - datetime(2001, 1, 1)
    days = diff.days + diff.seconds / 86400
    lunations = 0.20439731 + (days * 0.03386319269)
    phase_index = int((lunations % 1) * 8)
    phases = ["New 🌑", "Waxing Crescent 🌒", "First Quarter 🌓", "Waxing Gibbous 🌔", "Full 🌕", "Waning Gibbous 🌖", "Last Quarter 🌗", "Waning Crescent 🌘"]
    return phases[phase_index]

def generate_sudoku():
    # Simple placeholder grid
    grid = [["" for _ in range(9)] for _ in range(9)]
    for _ in range(15): # Fill 15 random cells
        r, c = random.randint(0,8), random.randint(0,8)
        grid[r][c] = random.randint(1,9)
    return grid

def get_news():
    rss_urls = os.getenv("RSS_FEED_URL", "https://hnrss.org/frontpage,https://www.nasa.gov/rss/dyn/breaking_news.rss,https://3dprint.com/feed/,https://www.pinballnews.com/site/feed/").split(",")
    news_items = []
    
    import re

    def clean_summary(text, source):
        if not text: return ""
        # Remove common technical links/tags
        text = re.sub(r'<a href=.*?>.*?</a>', '', text)
        text = re.sub(r'<.*?>', '', text)
        text = " ".join(text.split())
        
        # If it's a sparse Hacker News item, provide a better feel
        if not text and "Hacker News" in source:
            return "Latest discussion and links from the Hacker News community."
        return text

    for url in rss_urls:
        url = url.strip()
        if not url: continue
        try:
            feed = feedparser.parse(url)
            source_name = "Hacker News" if "Hacker News" in (feed.feed.title if hasattr(feed.feed, 'title') else "") else (feed.feed.title if hasattr(feed.feed, 'title') else url)
            
            for entry in feed.entries[:2]:
                raw_summary = getattr(entry, 'summary', getattr(entry, 'description', ''))
                summary = clean_summary(raw_summary, source_name)
                
                # If still empty after cleaner, use a snip of the title or a generic line
                if not summary or len(summary) < 5:
                    summary = f"Read the full story from {source_name}."

                news_items.append({
                    "title": entry.title,
                    "summary": summary[:140] + "..." if len(summary) > 140 else summary,
                    "source": source_name
                })
        except: continue
            
    return news_items[:8]

def get_xkcd():
    print("Fetching XKCD comic...")
    try:
        # 1. Get latest comic to find the max ID
        latest_url = "https://xkcd.com/info.0.json"
        resp = requests.get(latest_url, timeout=5)
        if resp.status_code == 200:
            latest_data = resp.json()
            max_id = latest_data.get("num")
            
            # 2. Pick a random comic ID
            random_id = random.randint(1, max_id)
            random_url = f"https://xkcd.com/{random_id}/info.0.json"
            
            # 3. Fetch the random comic
            comic_resp = requests.get(random_url, timeout=5)
            if comic_resp.status_code == 200:
                data = comic_resp.json()
                return {
                    "img": data.get("img"),
                    "title": data.get("title"),
                    "alt": data.get("alt")
                }
    except Exception as e:
        print(f"Error fetching XKCD: {e}")
    return None
