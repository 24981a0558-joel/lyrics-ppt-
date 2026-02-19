import io
import logging
import re
from flask import Flask, render_template, request, send_file, abort, jsonify

from lyrics_ppt_web.generator import generate_pptx, DEFAULT_FONTS, DEFAULT_FONT_SIZE

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.get("/")
def index():
    return render_template(
        "index.html",
        fonts=DEFAULT_FONTS,
        default_size=int(DEFAULT_FONT_SIZE.pt)
    )


@app.post("/generate")
def generate():
    presentation_name = (request.form.get("presentation_name") or "Lyrics").strip()
    # Sanitize: keep only safe filename characters to prevent header injection / path traversal
    presentation_name = re.sub(r'[^\w \-.]', '', presentation_name).strip() or "Lyrics"
    lyrics_text = (request.form.get("lyrics") or "").strip("\ufeff")  # strip BOM if pasted

    # Get font preferences
    fonts = {
        'english': request.form.get("font_english"),
        'hindi': request.form.get("font_hindi"),
        'telugu': request.form.get("font_telugu")
    }

    logger.debug("Font selections: %s", fonts)

    try:
        font_size = int(request.form.get("font_size", str(int(DEFAULT_FONT_SIZE.pt))))
        font_size = max(12, min(96, font_size))  # clamp to safe range matching UI constraints
        logger.debug("Font size: %d", font_size)
    except (ValueError, TypeError):
        font_size = int(DEFAULT_FONT_SIZE.pt)
        logger.debug("Using default font size: %d", font_size)

    if not lyrics_text:
        return abort(400, description="Lyrics text is required.")

    logger.debug("First few lines: %s", lyrics_text.splitlines()[:2])

    pptx_bytes, slide_count, download_name = generate_pptx(
        lyrics_text,
        presentation_name,
        fonts=fonts,
        font_size=font_size
    )

    # Return as downloadable file
    return send_file(
        io.BytesIO(pptx_bytes),
        mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        as_attachment=True,
        download_name=download_name,
        max_age=0,
    )


if __name__ == "__main__":
    # For local development. In production, use a proper WSGI server (e.g., waitress, gunicorn on Linux)
    app.run(host="127.0.0.1", port=5000, debug=True)
