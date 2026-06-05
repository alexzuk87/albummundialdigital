"""Renderizado HTML seguro para SVG y animaciones (Streamlit sanitiza <svg> en markdown)."""

from pathlib import Path

import streamlit.components.v1 as components

_PACK_CSS_PATH = Path(__file__).parent / "pack_reveal.css"


def _pack_reveal_styles() -> str:
    css = _PACK_CSS_PATH.read_text(encoding="utf-8")
    return (
        "<style>"
        "@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Nunito:wght@400;600;700;800&display=swap');"
        f"{css}"
        "</style>"
    )


def show_pack_opening(html: str, height: int = 600, *, scroll: bool = False) -> None:
    """Muestra la animación del sobre en un iframe (SVG y CSS completos)."""
    doc = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"{_pack_reveal_styles()}"
        "</head><body style='margin:0;padding:20px 24px 48px;background:transparent;"
        "display:flex;justify-content:center;align-items:flex-start;"
        f"min-height:{height - 48}px;overflow:visible;box-sizing:border-box;'>"
        f"{html}</body></html>"
    )
    components.html(doc, height=height, scrolling=scroll)
