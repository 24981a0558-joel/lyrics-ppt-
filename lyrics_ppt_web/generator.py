import io
from typing import Tuple

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Fonts and styling
ENGLISH_FONT = 'Calibri'  # Clean sans-serif for English
HINDI_FONT = 'Noto Sans Devanagari'  # For Hindi (Devanagari script)
TELUGU_FONT = 'Noto Sans Telugu'  # For Telugu
DEFAULT_FONT_SIZE = Pt(36)
TEXT_COLOR = RGBColor(255, 255, 255)  # White
BG_COLOR = RGBColor(0, 0, 0)  # Black


def _detect_font(line: str) -> str:
    """Basic language-based font selection per line."""
    if any(0x0900 <= ord(c) <= 0x097F for c in line):
        return HINDI_FONT
    if any(0x0C00 <= ord(c) <= 0x0C7F for c in line):
        return TELUGU_FONT
    return ENGLISH_FONT


def generate_pptx(lyrics_text: str, presentation_name: str) -> Tuple[bytes, int, str]:
    """
    Generate a PPTX file from the given lyrics text.

    Inputs
    - lyrics_text: Full text with lines separated by newlines. Two lines per slide.
    - presentation_name: Name without extension; used for the download filename.

    Returns
    - pptx_bytes: Bytes content of the generated .pptx
    - slide_count: Number of slides generated
    - download_name: Suggested filename for download (with .pptx)
    """
    # Normalize and collect lines (preserve empty lines similarly to original behavior)
    raw_lines = lyrics_text.splitlines()
    lines = [ln.strip() for ln in raw_lines]

    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    blank_slide_layout = prs.slide_layouts[6]

    # Create slides with 2 lines each
    for i in range(0, len(lines), 2):
        slide = prs.slides.add_slide(blank_slide_layout)

        left = Inches(0.665)
        top = Inches(2.5)
        width = Inches(12)
        height = Inches(4)
        textbox = slide.shapes.add_textbox(left, top, width, height)
        tf = textbox.text_frame

        current_lines = lines[i:i + 2]
        tf.text = '\n'.join(current_lines)

        for p in tf.paragraphs:
            p.alignment = PP_ALIGN.CENTER
            p.font.size = DEFAULT_FONT_SIZE
            p.font.color.rgb = TEXT_COLOR
            p.font.name = _detect_font(p.text)

        # Black background
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = BG_COLOR

    # Save to bytes
    bio = io.BytesIO()
    prs.save(bio)
    pptx_bytes = bio.getvalue()
    bio.close()

    slide_count = len(lines) // 2 + (1 if len(lines) % 2 else 0)
    download_name = f"{presentation_name}.pptx" if not presentation_name.lower().endswith('.pptx') else presentation_name

    return pptx_bytes, slide_count, download_name
