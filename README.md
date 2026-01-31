# 🗞️ Daily Briefing

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
- `SCHEDULE_TIME`: The time you want the briefing generated (e.g., `07:00`).
- `PRINTER_NAME`: (Optional) Your Mac printer name for auto-printing.

**How to find your Printer Name:**
- **Mac**: Run `lpstat -p` in your terminal.
- **Windows**: Run `Get-Printer | Select-Object Name` in PowerShell.

*Note: Internal printing auto-delivery is optimized for Mac/Linux host systems.*

### 3. Run
The container now handles its own scheduling. Simply start it and leave it running:
```bash
docker-compose up -d --build
```
The container will stay active in the background and trigger the briefing every day at your `SCHEDULE_TIME`.

---

## 🏗️ How it Works (Internal Printing)
This project uses a "CUPS Bridge" to print from inside Docker to your Mac.
- The `docker-compose.yml` mounts the host's CUPS socket (`/private/var/run/cupsd` on Mac).
- This allows the container to send print jobs directly to any printer configured on your Mac (USB or Network).

---

## 🪟 Windows Users

The automatic printing feature (the "CUPS Bridge") is designed for Mac and Linux systems. Because Windows does not use the Unix socket standard for CUPS, the container cannot speak directly to your local printer.

**How to use on Windows:**
1.  **PDF Generation**: The container will still run perfectly and generate your `daily_briefing.pdf` into the `output/` folder every day at your scheduled time.
2.  **Manual Print**: Simply open the `output/` folder on your computer and print the PDF manually.
3.  **Logs**: You may see an error in the Docker logs saying `lp: Error - No default destination`—this is expected on Windows and won't stop the PDF from being created.

---

## 🛠️ Project Structure
- `fetchers.py`: Data fetching logic (APIs and RSS).
- `pdf_gen.py`: HTML/CSS template and PDF generation (WeasyPrint).
- `main.py`: Application orchestration.
- `run_daily.sh`: Automation script for Docker + Printing.
- `Dockerfile` & `docker-compose.yml`: Containerization environment.
