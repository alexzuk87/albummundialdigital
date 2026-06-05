"""Logros incrementales del álbum."""

from data.album import STICKER_BY_ID, TOTAL_STICKERS
from data.formations import get_formation
from services.database import get_achievements, unlock_achievement

ACHIEVEMENTS = [
    {"id": "first_sticker", "title": "Primera figurita", "desc": "Desbloquea tu primera figurita", "icon": "🎴", "type": "count", "value": 1},
    {"id": "five_stickers", "title": "Coleccionista novato", "desc": "Consigue 5 figuritas", "icon": "5️⃣", "type": "count", "value": 5},
    {"id": "first_eleven", "title": "Once inicial", "desc": "Completa tu primer 11 ideal", "icon": "⭐", "type": "lineup"},
    {"id": "twenty_five", "title": "Álbum en marcha", "desc": "Consigue 25 figuritas", "icon": "📗", "type": "count", "value": 25},
    {"id": "fifty_stickers", "title": "Medio centenar", "desc": "Consigue 50 figuritas", "icon": "5️⃣0️⃣", "type": "count", "value": 50},
    {"id": "hundred_stickers", "title": "Centenario", "desc": "Consigue 100 figuritas", "icon": "💯", "type": "count", "value": 100},
    {"id": "two_hundred", "title": "Colección seria", "desc": "Consigue 200 figuritas", "icon": "🏅", "type": "count", "value": 200},
    {"id": "first_legendary", "title": "Leyenda viva", "desc": "Desbloquea tu primera figurita legendaria", "icon": "👑", "type": "rarity", "value": "legendaria"},
    {"id": "first_exchange", "title": "Negociador", "desc": "Realiza tu primer intercambio", "icon": "🤝", "type": "exchange"},
    {"id": "album_half", "title": "Mitad del camino", "desc": "Completa el 50% del álbum", "icon": "📊", "type": "percent", "value": 50},
    {"id": "album_complete", "title": "Álbum completo", "desc": "Consigue las 528 figuritas", "icon": "🏆", "type": "count", "value": TOTAL_STICKERS},
]

ACHIEVEMENT_BY_ID = {a["id"]: a for a in ACHIEVEMENTS}


def _unique_count(progress: dict) -> int:
    return len(progress.get("unlocked_stickers", []))


def _lineup_complete(progress: dict) -> bool:
    team = progress.get("custom_team", {})
    formation_id = team.get("formation", "4-3-3")
    slots = get_formation(formation_id)["slots"]
    lineup = team.get("lineup", {})
    return all(lineup.get(s["key"]) for s in slots)


def _has_rarity(progress: dict, rarity: str) -> bool:
    for sid in progress.get("unlocked_stickers", []):
        if STICKER_BY_ID.get(sid, {}).get("rarity") == rarity:
            return True
    return False


def check_and_unlock(user_id: int, progress: dict, event: str | None = None) -> list[dict]:
    """Evalúa logros y desbloquea nuevos. Retorna lista de logros recién obtenidos."""
    already = get_achievements(user_id)
    newly: list[dict] = []
    count = _unique_count(progress)
    pct = round(count / TOTAL_STICKERS * 100, 1) if TOTAL_STICKERS else 0

    for ach in ACHIEVEMENTS:
        if ach["id"] in already:
            continue
        unlocked = False
        t = ach["type"]
        if t == "count" and count >= ach["value"]:
            unlocked = True
        elif t == "lineup" and _lineup_complete(progress):
            unlocked = True
        elif t == "rarity" and _has_rarity(progress, ach["value"]):
            unlocked = True
        elif t == "percent" and pct >= ach["value"]:
            unlocked = True
        elif t == "exchange" and event == "exchange":
            unlocked = True

        if unlocked and unlock_achievement(user_id, ach["id"]):
            newly.append(ach)

    return newly


def achievements_summary(user_id: int) -> list[dict]:
    unlocked = get_achievements(user_id)
    result = []
    for ach in ACHIEVEMENTS:
        result.append({**ach, "unlocked": ach["id"] in unlocked})
    return result
