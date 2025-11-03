# Lyrics → PPT Web

A tiny Flask-based web app that turns lyrics (one line per row) into a PowerPoint (.pptx). Two lines per slide, black background, white text. Basic line-by-line font selection supports English (Calibri), Hindi (Noto Sans Devanagari), and Telugu (Noto Sans Telugu).

## Quick start (Windows PowerShell)

```pwsh
# Create and activate a virtual environment (optional but recommended)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Open http://127.0.0.1:5000 in your browser. Paste lyrics, set a name, and click Generate.

## Notes
- Two lines per slide. Empty lines are preserved.
- Fonts must be installed on the machine where you open the PPT in PowerPoint:
  - English: Calibri (usually present on Windows)
  - Hindi: Noto Sans Devanagari
  - Telugu: Noto Sans Telugu
  PowerPoint may substitute if a font isn’t installed. This app does not embed fonts.
- For production hosting, use a WSGI server (e.g., waitress on Windows) and set `debug=False`.

## Project layout
- `app.py` — Flask app with the web routes
- `lyrics_ppt_web/generator.py` — PPT generation logic reused by the web app
- `templates/index.html` — Simple UI
- `static/styles.css` — Minimal styles

## Troubleshooting
- If you see a blank or substituted font, install the appropriate Noto fonts and restart PowerPoint.
- If PowerPoint says the file is corrupted, ensure the full download completes and try a different browser.
