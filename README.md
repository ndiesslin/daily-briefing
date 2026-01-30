# 🗞️ Daily Itinerary Briefing

A containerized Python application that generates a beautiful, single-page 8.5" x 11" daily briefing including news, weather, markets, and more. Perfect for printing out every morning!

## ✨ Features
- **🌦️ Local Weather**: Current temp, high/low, wind speed, and sunrise/sunset.
- **📰 Curated News**: Headlines from Hacker News, NASA, 3D Printing, and Pinball news.
- **📈 Market Snapshot**: Live prices for **Gold (XAU)** and **Ethereum (ETH)**.
- **🧠 Brain Food**: Daily Quote, Word of the Day, and "On This Day" historical events.
- **🧩 Morning Fun**: A fresh Sudoku puzzle every morning and an analog task list.
- **🖨️ Auto-Print**: Shell scripts included to send directly to your Mac printer on a schedule.

---

## 🚀 Getting Started

### 1. Prerequisites
- [Docker & Docker Compose](https://www.docker.com/products/docker-desktop/) installed.
- A Mac (if using the automatic printing features).

### 2. Configuration
Copy the example environment file and edit it:
```bash
cp .env.example .env
```

Open `.env` and configure:
- `LOCATION`: Your city or Zip Code (e.g., `90210`).
- `RSS_FEED_URL`: (Optional) Comma-separated list of RSS feeds.
- `PRINTER_NAME`: (Optional) Your Mac printer name for auto-printing.

### 3. Run Manually
To generate the PDF on demand:
```bash
docker-compose up --build
```
The resulting PDF will be saved in the `output/` directory as `daily_briefing.pdf`.

---

## ⏰ Automatic Morning Printing (Mac)

To have your briefing waiting for you at the printer every morning at 7:00 AM:

### 1. Find your Printer Name
Run this in your terminal:
```bash
lpstat -p
```
Copy the name (e.g., `HP_LaserJet_Pro`) and add it to `PRINTER_NAME=` in your `.env` file.

### 2. Set Execute Permissions
```bash
chmod +x run_daily.sh
```

### 3. Schedule the Cron Job
1. Open your cron editor:
   ```bash
   crontab -e
   ```
2. Add the following line (replaces the path with your actual project location):
   ```text
   0 7 * * * "/absolute/path/to/daily-itinerary/run_daily.sh" >> "/absolute/path/to/daily-itinerary/cron_log.txt" 2>&1
   ```
   *Tip: Use `pwd` in the project folder to get the absolute path.*

---

## 🛠️ Project Structure
- `fetchers.py`: Data fetching logic (APIs and RSS).
- `pdf_gen.py`: HTML/CSS template and PDF generation (WeasyPrint).
- `main.py`: Application orchestration.
- `run_daily.sh`: Automation script for Docker + Printing.
- `Dockerfile` & `docker-compose.yml`: Containerization environment.
