# 🤖 Project Context for Gemini / AI Assistants

This document provides a technical overview of the **Daily Itinerary Briefing** project to help an AI assistant understand the codebase for maintenance, debugging, or feature extensions.

## 📝 Project Overview
A containerized Python application that aggregates data from various APIs and RSS feeds to generate a single-page, black-and-white 8.5" x 11" PDF briefing for morning printing.

## 🛠️ Tech Stack
- **Language**: Python 3.11-slim
- **PDF Engine**: [WeasyPrint](https://weasyprint.org/) (converts HTML/CSS to PDF)
- **Templating**: Jinja2
- **Containerization**: Docker & Docker Compose
- **Scheduling**: Cron (on host machine)
- **APIs**: Open-Meteo (Weather), CoinGecko (ETH), Gold-API (Gold), Wikipedia (History), ZenQuotes (Quotes).

## 📂 Core Architecture
1. **`fetchers.py`**: Contains all data retrieval logic.
   - `get_weather()`: Uses Geocoding + Forecast APIs. Includes wind/sunrise/sunset.
   - `get_news()`: Parses RSS feeds using `feedparser`. Strips HTML and "Comments" links.
   - `get_brain_food()`: Fetches quotes, history, and word of the day.
   - `generate_sudoku()`: Generates a lightweight puzzle grid.
2. **`pdf_gen.py`**: Contains the HTML/CSS template and generation logic.
   - **Constraint**: Designed strictly for a single 8.5" x 11" page.
   - **Aesthetic**: Minimalist Black & White "Journal" style.
3. **`main.py`**: The orchestrator. Loads environment variables, calls fetchers, and triggers the PDF generation.
4. **`run_daily.sh`**: A portable shell script designed for `cron`. It navigates to the project dir, runs the Docker container, and sends the output to the Mac system printer (`lp`).

## 🧱 Key Constraints & Patterns
- **Portability**: The shell script uses `cd "$(dirname "$0")"` to resolve paths relative to itself.
- **Environment**: Configuration is handled via a `.env` file (see `.env.example`).
- **Space Efficiency**: News items are capped and summaries are truncated to ensure a 1-page layout.
- **B&W Optimization**: CSS uses grayscale filters and high-contrast borders for clear printing on laser printers.

## 🚀 Common Maintenance Tasks
- **Adding News Sources**: Update `RSS_FEED_URL` in `.env` or the default list in `fetchers.py`.
- **Adjusting Layout**: Modify CSS in `pdf_gen.py`. Use `@page` margins and `.section` spacing to manage page overflow.
- **API Troubleshooting**: Check `cron_log.txt` for any failures in the automated run.
