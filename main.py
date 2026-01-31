import os
import time
import schedule
import subprocess
from dotenv import load_dotenv
from pdf_gen import generate_pdf
from fetchers import get_weather, get_news, get_brain_food, get_markets, get_moon_phase, generate_sudoku, get_xkcd

def run_job():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting daily briefing job...")
    
    try:
        weather = get_weather()
        news = get_news()
        brain_food = get_brain_food()
        markets = get_markets()
        moon = get_moon_phase()
        sudoku = generate_sudoku()
        comic = get_xkcd()
        
        data = {
            "weather": weather,
            "news": news,
            "brain": brain_food,
            "markets": markets,
            "moon": moon,
            "sudoku": sudoku,
            "comic": comic
        }
        
        output_path = "/output/daily_briefing.pdf" if os.path.exists("/output") else "daily_briefing.pdf"
        path = generate_pdf(data, output_path)
        print(f"PDF generated: {path}")
        
        # Internal Printing Call
        printer_name = os.getenv("PRINTER_NAME")
        if path:
            print_cmd = ["lp"]
            if printer_name:
                print_cmd.extend(["-d", printer_name])
            print_cmd.append(path)
            
            print(f"Sending to printer: {' '.join(print_cmd)}")
            subprocess.run(print_cmd, check=True)
            print("Job complete!")
            
    except Exception as e:
        print(f"Error during job execution: {e}")

def main():
    load_dotenv()
    schedule_time = os.getenv("SCHEDULE_TIME", "07:00")
    daemon_mode = os.getenv("DAEMON_MODE", "true").lower() == "true"
    
    if daemon_mode:
        print(f"Starting in daemon mode. Briefing scheduled for {schedule_time} daily.")
        schedule.every().day.at(schedule_time).do(run_job)
        
        # Run once on startup if you want immediate feedback
        # run_job() 
        
        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        run_job()

if __name__ == "__main__":
    main()
