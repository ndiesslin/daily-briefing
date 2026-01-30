#!/bin/bash

# 1. Navigate to the directory where this script is located
cd "$(dirname "$0")"

# 2. Run Docker to generate the latest PDF
# The --rm flag cleans up the container after it's done
docker-compose run --rm daily-briefing

# 3. Print the PDF using the name in .env (or default)
if [ -f "output/daily_briefing.pdf" ]; then
    # Ensure .env exists, fallback to empty if not
    PRINTER=""
    if [ -f ".env" ]; then
        PRINTER=$(grep "^PRINTER_NAME=" .env | cut -d'=' -f2)
    fi
    
    if [ -n "$PRINTER" ]; then
        echo "Sending to printer: $PRINTER"
        lp -d "$PRINTER" output/daily_briefing.pdf
    else
        echo "Sending to default printer..."
        lp output/daily_briefing.pdf
    fi
else
    echo "Error: PDF not found. Check Docker logs."
fi
