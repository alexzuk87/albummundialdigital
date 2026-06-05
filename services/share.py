"""Generar contenido para compartir el 11 ideal en redes sociales."""

from urllib.parse import quote

from data.album import STICKER_BY_ID
from data.formations import get_formation
from services.constants import RARITY_LABELS


def build_lineup_share_text(team_name: str, formation_id: str, lineup: dict) -> str:
    formation = get_formation(formation_id)
    lines = [f"⚽ Mi 11 ideal — {team_name} ({formation['label']})", "Álbum Mundial Digital 2026", ""]

    for slot in formation["slots"]:
        sid = lineup.get(slot["key"])
        if sid and sid in STICKER_BY_ID:
            s = STICKER_BY_ID[sid]
            if s.get("kind") in ("crest", "bandera"):
                continue
            lines.append(
                f"• {slot['label']}: {s['name']} ({s['team_name']}) — {RARITY_LABELS[s['rarity']]}"
            )
        else:
            lines.append(f"• {slot['label']}: —")

    lines.extend(["", "#AlbumMundial2026 #Mundial2026 #FIFA2026 #Figuritas"])
    return "\n".join(lines)


def share_links(text: str) -> dict[str, str]:
    encoded = quote(text)
    return {
        "twitter": f"https://twitter.com/intent/tweet?text={encoded}",
        "facebook": f"https://www.facebook.com/sharer/sharer.php?quote={encoded}",
        "whatsapp": f"https://wa.me/?text={encoded}",
        "telegram": f"https://t.me/share/url?text={encoded}",
        "instagram": "https://www.instagram.com/",
    }


def get_share_content(team_name: str, formation_id: str, lineup: dict) -> tuple[str, dict[str, str]]:
    text = build_lineup_share_text(team_name, formation_id, lineup)
    return text, share_links(text)
