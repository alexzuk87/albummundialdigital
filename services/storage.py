"""Persistencia por usuario (SQLite)."""

import json
from datetime import date

from services.database import (
    get_progress_row,
    get_user_stickers,
    init_db,
    reset_user_progress,
    save_progress_row,
)
from services.inventory import _stickers_to_lists

init_db()

DEFAULT_TRIVIA = {"date": "", "count": 0, "answered_ids": []}

DEFAULT_CUSTOM_TEAM = {
    "name": "Mi Equipo Soñado",
    "formation": "4-3-3",
    "lineup": {},
}


def load_progress(user_id: int) -> dict:
    row = get_progress_row(user_id)
    stickers = get_user_stickers(user_id)
    unlocked, duplicates = _stickers_to_lists(stickers)

    trivia = json.loads(row.get("trivia_today_json") or "{}")
    if not trivia:
        trivia = dict(DEFAULT_TRIVIA)

    custom = json.loads(row.get("custom_team_json") or "{}")
    if not custom:
        custom = dict(DEFAULT_CUSTOM_TEAM)

    last_unlock = None
    if row.get("last_unlock_json"):
        last_unlock = json.loads(row["last_unlock_json"])

    unlocked = [
        sid.replace("_crest", "_bandera") if sid.endswith("_crest") else sid
        for sid in unlocked
    ]
    duplicates = [
        sid.replace("_crest", "_bandera") if sid.endswith("_crest") else sid
        for sid in duplicates
    ]

    return {
        "user_id": user_id,
        "unlocked_stickers": unlocked,
        "duplicates": duplicates,
        "sticker_quantities": stickers,
        "trivia_today": trivia,
        "exchange_offers": [],
        "historical_unlocked": [],
        "last_unlock_animation": last_unlock,
        "custom_team": custom,
    }


def save_progress(user_id: int, progress: dict) -> None:
    save_progress_row(
        user_id,
        progress.get("trivia_today", DEFAULT_TRIVIA),
        progress.get("last_unlock_animation"),
        progress.get("custom_team", DEFAULT_CUSTOM_TEAM),
    )


def reset_daily_trivia(progress: dict) -> dict:
    today = date.today().isoformat()
    trivia = progress.get("trivia_today", {})
    if trivia.get("date") != today:
        progress["trivia_today"] = {"date": today, "count": 0, "answered_ids": []}
    return progress


def reset_user(user_id: int) -> None:
    reset_user_progress(user_id)


# Re-exportar para compatibilidad con imports antiguos
from services.inventory import (  # noqa: E402
    add_sticker_to_user,
    remove_sticker_from_user,
    user_owns_sticker,
)
