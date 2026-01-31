# 🤖 Project Context for Daily Briefing

This document provides a technical overview of the **Daily Briefing** project to help an AI assistant understand the codebase for maintenance, debugging, or feature extensions.

## 📝 Project Overview
A containerized Python application that aggregates data from various APIs and RSS feeds to generate a single-page, black-and-white 8.5" x 11" PDF briefing for morning printing.

## 🛠️ Tech Stack
- **Language**: Python 3.11-slim
- **Scheduling**: Python `schedule` library (internal daemon)
- **PDF Engine**: [WeasyPrint](https://weasyprint.org/)
- **Printing**: CUPS Bridge (via `/var/run/cups/cups.sock`)
- **Containerization**: Docker & Docker Compose

## 📂 Core Architecture
1. **`main.py`**: The orchestrator. Now includes a **Daemon Mode** that uses the `schedule` library to trigger jobs daily. It also handles the `lp` command internally to send PDFs to the host's printer.
2. **`fetchers.py`**: Retrieval logic for weather, news, brain food, and puzzles.
3. **`pdf_gen.py`**: HTML/CSS to PDF generation logic.
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
