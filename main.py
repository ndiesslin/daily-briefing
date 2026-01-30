import os
from dotenv import load_dotenv
from pdf_gen import generate_pdf
from fetchers import get_weather, get_news, get_brain_food, get_markets, get_moon_phase, generate_sudoku

def main():
    print("Fetching data...")
    load_dotenv()
    
    weather = get_weather()
    news = get_news()
    brain_food = get_brain_food()
    markets = get_markets()
    moon = get_moon_phase()
    sudoku = generate_sudoku()
    
    data = {
        "weather": weather,
        "news": news,
        "brain": brain_food,
        "markets": markets,
        "moon": moon,
        "sudoku": sudoku
    }
    
    print("Generating PDF...")
    output_path = "/output/daily_briefing.pdf" if os.path.exists("/output") else "daily_briefing.pdf"
    
    path = generate_pdf(data, output_path)
    print(f"Success! Daily briefing saved to: {path}")

if __name__ == "__main__":
    main()
