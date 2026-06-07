"""Logros incrementales del álbum."""

from data.album import STICKER_BY_ID, TOTAL_STICKERS
from data.formations import get_formation
from services.database import (
    get_achievements,
    get_cup_overall,
    get_sim_overall,
    unlock_achievement,
)

ACHIEVEMENTS = [
    {"id": "first_sticker", "title": "Primera figurita", "desc": "Desbloquea tu primera figurita", "icon": "🎴", "type": "count", "value": 1, "coins": 10},
    {"id": "five_stickers", "title": "Coleccionista novato", "desc": "Consigue 5 figuritas", "icon": "5️⃣", "type": "count", "value": 5, "coins": 15},
    {"id": "first_eleven", "title": "Once inicial", "desc": "Completa tu primer 11 ideal", "icon": "⭐", "type": "lineup", "coins": 25},
    {"id": "twenty_five", "title": "Álbum en marcha", "desc": "Consigue 25 figuritas", "icon": "📗", "type": "count", "value": 25, "coins": 25},
    {"id": "fifty_stickers", "title": "Medio centenar", "desc": "Consigue 50 figuritas", "icon": "5️⃣0️⃣", "type": "count", "value": 50, "coins": 40},
    {"id": "hundred_stickers", "title": "Centenario", "desc": "Consigue 100 figuritas", "icon": "💯", "type": "count", "value": 100, "coins": 60},
    {"id": "hundred_fifty", "title": "Coleccionista avanzado", "desc": "Consigue 150 figuritas", "icon": "📚", "type": "count", "value": 150, "coins": 70},
    {"id": "two_hundred", "title": "Colección seria", "desc": "Consigue 200 figuritas", "icon": "🏅", "type": "count", "value": 200, "coins": 90},
    {"id": "three_hundred", "title": "Coleccionista experto", "desc": "Consigue 300 figuritas", "icon": "📦", "type": "count", "value": 300, "coins": 120},
    {"id": "four_hundred", "title": "Maestro del álbum", "desc": "Consigue 400 figuritas", "icon": "🗂️", "type": "count", "value": 400, "coins": 150},
    {"id": "five_hundred", "title": "Casi imparable", "desc": "Consigue 500 figuritas", "icon": "🎯", "type": "count", "value": 500, "coins": 200},
    {"id": "first_legendary", "title": "Leyenda viva", "desc": "Desbloquea tu primera figurita legendaria", "icon": "👑", "type": "rarity", "value": "legendaria", "coins": 30},
    {"id": "first_exchange", "title": "Negociador", "desc": "Realiza tu primer intercambio", "icon": "🤝", "type": "exchange", "coins": 20},
    {"id": "album_half", "title": "Mitad del camino", "desc": "Completa el 50% del álbum", "icon": "📊", "type": "percent", "value": 50, "coins": 100},
    {"id": "album_complete", "title": "Álbum completo", "desc": "Completa todo el álbum", "icon": "🏆", "type": "count", "value": TOTAL_STICKERS, "coins": 300},
    # --- Simulación de partidos ---
    {"id": "sim_debut", "title": "Debut en la cancha", "desc": "Jugá tu primer partido simulado", "icon": "🟢", "type": "sim_played", "value": 1, "coins": 10},
    {"id": "sim_first_win", "title": "Primera victoria", "desc": "Ganá tu primer partido simulado", "icon": "🥅", "type": "sim_wins", "value": 1, "coins": 15},
    {"id": "sim_five_wins", "title": "En racha", "desc": "Ganá 5 partidos simulados", "icon": "🔥", "type": "sim_wins", "value": 5, "coins": 30},
    {"id": "sim_ten_played", "title": "Habitué", "desc": "Jugá 10 partidos simulados", "icon": "🎮", "type": "sim_played", "value": 10, "coins": 25},
    {"id": "sim_fifteen_wins", "title": "Goleador", "desc": "Ganá 15 partidos simulados", "icon": "⚽", "type": "sim_wins", "value": 15, "coins": 50},
    {"id": "sim_thirty_wins", "title": "Campeón de la simulación", "desc": "Ganá 30 partidos simulados", "icon": "🏆", "type": "sim_wins", "value": 30, "coins": 100},
    # --- Copa (Modo Torneo) ---
    {"id": "cup_debut", "title": "Camino a la gloria", "desc": "Jugá tu primera Copa", "icon": "🎟️", "type": "cup_runs", "value": 1, "coins": 20},
    {"id": "cup_finalist", "title": "Finalista", "desc": "Llegá a la final de la Copa", "icon": "🥈", "type": "cup_finals", "value": 1, "coins": 60},
    {"id": "cup_champion", "title": "Campeón del Mundo", "desc": "Ganá la Copa", "icon": "🏆", "type": "cup_champion", "value": 1, "coins": 150},
    {"id": "cup_tricampeon", "title": "Tricampeón", "desc": "Ganá la Copa 3 veces", "icon": "👑", "type": "cup_champion", "value": 3, "coins": 250},
]

ACHIEVEMENT_BY_ID = {a["id"]: a for a in ACHIEVEMENTS}

#: Monedas totales que es posible ganar desbloqueando todos los logros.
TOTAL_COINS_AVAILABLE = sum(a.get("coins", 0) for a in ACHIEVEMENTS)


def coins_for_unlocked(user_id: int) -> int:
    """Monedas acumuladas por los logros que el usuario ya desbloqueó."""
    unlocked = get_achievements(user_id)
    return sum(ACHIEVEMENT_BY_ID.get(aid, {}).get("coins", 0) for aid in unlocked)


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

    needs_sim = any(
        ach["type"] in ("sim_wins", "sim_played") and ach["id"] not in already
        for ach in ACHIEVEMENTS
    )
    sim = get_sim_overall(user_id) if needs_sim else {"played": 0, "won": 0}

    needs_cup = any(
        ach["type"] in ("cup_runs", "cup_finals", "cup_champion") and ach["id"] not in already
        for ach in ACHIEVEMENTS
    )
    cup = get_cup_overall(user_id) if needs_cup else {"runs": 0, "finals": 0, "champion": 0}

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
        elif t == "sim_wins" and sim["won"] >= ach["value"]:
            unlocked = True
        elif t == "sim_played" and sim["played"] >= ach["value"]:
            unlocked = True
        elif t == "cup_runs" and cup["runs"] >= ach["value"]:
            unlocked = True
        elif t == "cup_finals" and cup["finals"] >= ach["value"]:
            unlocked = True
        elif t == "cup_champion" and cup["champion"] >= ach["value"]:
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
