import io
from flask import Flask, render_template, request, send_file, abort

from lyrics_ppt_web.generator import generate_pptx

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/generate")
def generate():
    presentation_name = (request.form.get("presentation_name") or "Lyrics").strip()
    lyrics_text = (request.form.get("lyrics") or "").strip("\ufeff")  # strip BOM if pasted

    if not lyrics_text:
        return abort(400, description="Lyrics text is required.")

    pptx_bytes, slide_count, download_name = generate_pptx(lyrics_text, presentation_name)

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
