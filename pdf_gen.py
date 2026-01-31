from weasyprint import HTML
from jinja2 import Template
import os
from datetime import datetime

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        @page { size: 8.5in 11in; margin: 0.3in; }
        body { font-family: 'Helvetica', 'Arial', sans-serif; color: #000; line-height: 1.25; font-size: 10.5px; margin: 0; }
        .header { border-bottom: 3px solid #000; padding-bottom: 2px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: baseline; }
        .header h1 { font-size: 22px; margin: 0; text-transform: uppercase; font-weight: 900; letter-spacing: -1px; }
        .date { font-size: 12px; font-weight: bold; }
        
        .container { display: flex; gap: 20px; }
        .left-col { width: 33%; border-right: 1.5px solid #000; padding-right: 12px; }
        .right-col { width: 67%; }

        .section { margin-bottom: 12px; page-break-inside: avoid; }
        .section-title { font-size: 10px; font-weight: bold; text-transform: uppercase; color: #000; border-bottom: 2px solid #000; margin-bottom: 6px; padding-bottom: 1px; }

        /* Weather Box */
        .weather-box { background: #fff; border: 1.5px solid #000; padding: 8px; border-radius: 0; }
        .weather-main { display: flex; justify-content: space-between; align-items: center; }
        .weather-temp { font-size: 20px; font-weight: bold; }
        .weather-emoji { font-size: 22px; }
        .weather-details { font-size: 9.5px; color: #000; margin-top: 3px; line-height: 1.3; }

        /* Market Box */
        .market-item { display: flex; justify-content: space-between; margin-bottom: 2px; border-bottom: 1px solid #eee; }
        .market-label { font-weight: bold; }

        /* News Box */
        .news-item { margin-bottom: 8px; border-bottom: 0.5px solid #eee; padding-bottom: 5px; }
        .news-item:last-child { border-bottom: none; }
        .news-source { font-size: 7.5px; color: #000; text-transform: uppercase; font-weight: bold; margin-bottom: 2px; border-left: 3px solid #000; padding-left: 5px; }
        .news-title { font-size: 11px; font-weight: bold; margin-bottom: 1px; line-height: 1.15; }
        .news-summary { font-size: 9.5px; color: #333; line-height: 1.25; }

        /* Brain Food Box */
        .quote { font-style: italic; font-family: 'Georgia', serif; font-size: 11.5px; margin-bottom: 8px; padding: 10px; background: #f0f0f0; border-left: 5px solid #000; }
        .author { font-style: normal; font-size: 9.5px; text-align: right; margin-top: 4px; color: #000; font-weight: bold; }
        .word-box b { color: #000; font-size: 10.5px; }
        .history-box { font-size: 9.5px; border-top: 1.5px solid #000; padding-top: 8px; margin-top: 10px; }

        /* Sudoku */
        .sudoku { display: grid; grid-template-columns: repeat(9, 1fr); width: 155px; border: 1.5px solid #000; margin: 0 auto; }
        .sudoku div { border: 0.5px solid #000; height: 16px; text-align: center; font-size: 9px; line-height: 16px; font-weight: bold; }
        .sudoku div:nth-child(3n) { border-right: 1.5px solid #000; }
        .sudoku div:nth-child(9n) { border-right: none; }
        .row-third:nth-child(n+19):nth-child(-n+27), .row-third:nth-child(n+46):nth-child(-n+54) { border-bottom: 1.5px solid #000; }

        /* Task List */
        .tasks { list-style: none; padding: 0; }
        .tasks li { margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
        .checkbox { width: 12px; height: 12px; border: 1px solid #000; display: inline-block; }

        /* Comic Section */
        .comic-box { margin-top: 10px; text-align: left; padding-top: 0; }
        .comic-img { max-width: 100%; max-height: 180px; filter: grayscale(100%) contrast(1.2); display: block; margin: 0 auto; }
        .comic-title { font-size: 7.5px; font-weight: bold; margin-top: 3px; text-transform: uppercase; color: #555; text-align: center; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Daily Briefing</h1>
        <div class="date">{{ date }}</div>
    </div>

    <div class="container">
        <!-- Sidebar -->
        <div class="left-col">
            <div class="section">
                <div class="section-title">Local Weather</div>
                <div class="weather-box">
                    <div class="weather-main">
                        <div class="weather-temp">{{ data.weather.temp }}</div>
                        <div class="weather-emoji">{{ data.weather.emoji }}</div>
                    </div>
                    <div class="weather-details">
                        <b>{{ data.weather.description }}</b><br>
                        High: {{ data.weather.high }} | Low: {{ data.weather.low }}<br>
                        Wind: {{ data.weather.wind }}<br>
                        ☀️ {{ data.weather.sunrise }} | 🌙 {{ data.weather.sunset }}
                    </div>
                </div>
            </div>

            <div class="section">
                <div class="section-title">Markets & Environment</div>
                <div class="market-item"><span class="market-label">Gold (XAU)</span> <span>{{ data.markets.gold }}</span></div>
                <div class="market-item"><span class="market-label">Ethereum</span> <span>{{ data.markets.eth }}</span></div>
                <div style="margin-top: 10px; font-size: 10px;">{{ data.moon }}</div>
            </div>

            <div class="section">
                <div class="section-title">Analog Goals</div>
                <ul class="tasks">
                    <li><span class="checkbox"></span> <span style="border-bottom: 1px solid #eee; flex-grow: 1;">&nbsp;</span></li>
                    <li><span class="checkbox"></span> <span style="border-bottom: 1px solid #eee; flex-grow: 1;">&nbsp;</span></li>
                    <li><span class="checkbox"></span> <span style="border-bottom: 1px solid #eee; flex-grow: 1;">&nbsp;</span></li>
                </ul>
            </div>

            <div class="section">
                <div class="section-title">Morning Puzzle</div>
                <div class="sudoku">
                    {% for row in data.sudoku %}
                        {% for cell in row %}
                            <div class="row-third">{{ cell }}</div>
                        {% endfor %}
                    {% endfor %}
                </div>
            </div>

            {% if data.comic %}
            <div class="comic-box">
                <div class="section-title">Daily Comic (xkcd)</div>
                <img src="{{ data.comic.img }}" class="comic-img">
                <div class="comic-title">{{ data.comic.title }}</div>
            </div>
            {% endif %}
            
            <div style="font-size: 8px; color: #999; margin-top: 15px; border-top: 1px solid #eee; padding-top: 5px;">
                Generated: {{ date_full }}<br>
                System Status: All systems nominal
            </div>
        </div>

        <!-- Main Content -->
        <div class="right-col">
            <div class="section">
                <div class="section-title">Quote of the Day</div>
                <div class="quote">
                    "{{ data.brain.quote.text }}"
                    <div class="author">— {{ data.brain.quote.author }}</div>
                </div>
            </div>

            <div class="section">
                <div class="section-title">Daily Headlines</div>
                {% for item in data.news %}
                <div class="news-item">
                    <div class="news-source">{{ item.source }}</div>
                    <div class="news-title">{{ item.title }}</div>
                    <div class="news-summary">{{ item.summary }}</div>
                </div>
                {% endfor %}
            </div>

            <div class="section">
                <div class="section-title">Brain Food</div>
                <div class="word-box">
                    <b>Word of the Day:</b> {{ data.brain.word.term }}<br>
                    <span style="font-size: 10px; color: #555;">{{ data.brain.word.def }}</span>
                </div>
                <div class="history-box" style="margin-top: 10px;">
                    <b>On This Day:</b><br>
                    {{ data.brain.history }}
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

def generate_pdf(data, output_path="daily_briefing.pdf"):
    now = datetime.now().strftime("%A, %B %d")
    now_full = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    template = Template(HTML_TEMPLATE)
    html_out = template.render(date=now, date_full=now_full, data=data)
    
    HTML(string=html_out).write_pdf(output_path)
    return output_path
