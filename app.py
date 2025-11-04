import io
from flask import Flask, render_template, request, send_file, abort, jsonify

from lyrics_ppt_web.generator import generate_pptx, DEFAULT_FONTS

app = Flask(__name__)


@app.get("/")
def index():
    return render_template(
        "index.html",
        fonts=DEFAULT_FONTS,
        default_size=42  # Matches generator.py
    )


@app.post("/generate")
def generate():
    presentation_name = (request.form.get("presentation_name") or "Lyrics").strip()
    lyrics_text = (request.form.get("lyrics") or "").strip("\ufeff")  # strip BOM if pasted
    
    # Get font preferences
    fonts = {
        'english': request.form.get("font_english"),
        'hindi': request.form.get("font_hindi"),
        'telugu': request.form.get("font_telugu")
    }
    
    # Debug print
    print("Font selections:", fonts)
    
    try:
        font_size = int(request.form.get("font_size", "42"))
        print("Font size:", font_size)
    except (ValueError, TypeError):
        font_size = 42
        print("Using default font size:", font_size)

    if not lyrics_text:
        return abort(400, description="Lyrics text is required.")

    # Debug print first few lines
    print("First few lines:", lyrics_text.splitlines()[:2])

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
