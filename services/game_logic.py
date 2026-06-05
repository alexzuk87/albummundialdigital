"""Lógica de juego: trivias, desbloqueos e intercambios."""



import random

from datetime import date



from data.album import ALL_STICKERS, STICKER_BY_ID, TOTAL_STICKERS

from services.achievements import check_and_unlock

from services.constants import MAX_TRIVIA_PER_DAY, RARITY_LABELS, RARITY_ORDER

from services.database import add_sticker, get_user_stickers, remove_sticker

from services.inventory import add_sticker_to_user, remove_sticker_from_user, user_owns_sticker

from services.progress_utils import progress_user_id

from services.storage import load_progress, reset_daily_trivia, save_progress



# Re-exportar constantes para compatibilidad

RARITY_COLORS = __import__("services.constants", fromlist=["RARITY_COLORS"]).RARITY_COLORS





def _uid(progress: dict | None = None) -> int:

    return progress_user_id(progress)





def get_progress(user_id: int | None = None) -> dict:

    uid = user_id or progress_user_id()

    progress = load_progress(uid)

    progress["user_id"] = uid

    return reset_daily_trivia(progress)





def persist(progress: dict) -> None:

    save_progress(_uid(progress), progress)





def trivia_remaining(progress: dict) -> int:

    reset_daily_trivia(progress)

    return max(0, MAX_TRIVIA_PER_DAY - progress["trivia_today"]["count"])





def trivia_status_label(progress: dict) -> str:

    remaining = max(0, MAX_TRIVIA_PER_DAY - progress["trivia_today"]["count"])

    return f"{remaining}/6"





def can_play_trivia(progress: dict) -> bool:

    return trivia_remaining(progress) > 0





def pick_random_locked_sticker(progress: dict) -> dict | None:

    unlocked = set(progress["unlocked_stickers"])

    locked = [s for s in ALL_STICKERS if s["id"] not in unlocked]

    if locked:

        return random.choice(locked)

    return None





def unlock_sticker(progress: dict, sticker_id: str) -> tuple[dict, bool]:

    uid = _uid(progress)

    sticker = STICKER_BY_ID[sticker_id]

    was_owned = user_owns_sticker(progress, sticker_id)

    add_sticker_to_user(uid, sticker_id, progress)

    return sticker, was_owned





def _consume_trivia_turn(progress: dict, trivia_id: str) -> bool:

    reset_daily_trivia(progress)

    trivia = progress["trivia_today"]

    if trivia["count"] >= MAX_TRIVIA_PER_DAY:

        return False

    if trivia_id in trivia["answered_ids"]:

        return False

    trivia["count"] += 1

    trivia["answered_ids"].append(trivia_id)

    return True





def process_trivia_wrong(progress: dict, trivia_id: str) -> bool:

    if not _consume_trivia_turn(progress, trivia_id):

        return False

    persist(progress)

    return True





from services.progress_hooks import after_progress_change as _after_progress_change





def process_trivia_correct(progress: dict, trivia_id: str) -> dict | None:

    if not _consume_trivia_turn(progress, trivia_id):

        return None



    sticker = pick_random_locked_sticker(progress)

    if not sticker:

        persist(progress)

        return None



    unlock_sticker(progress, sticker["id"])

    progress["last_unlock_animation"] = {

        "sticker_id": sticker["id"],

        "timestamp": date.today().isoformat(),

    }

    newly = _after_progress_change(progress)

    return {"sticker": sticker, "achievements": newly}





def progress_stats(progress: dict) -> dict:

    unlocked = len(progress["unlocked_stickers"])

    duplicates = len(progress.get("duplicates", []))

    by_rarity = {r: 0 for r in RARITY_ORDER}

    for sid in progress["unlocked_stickers"]:

        sticker = STICKER_BY_ID.get(sid)

        if not sticker or sticker.get("kind") == "bandera":

            continue

        rarity = sticker["rarity"]

        by_rarity[rarity] = by_rarity.get(rarity, 0) + 1

    return {

        "total": TOTAL_STICKERS,

        "unlocked": unlocked,

        "percent": round(unlocked / TOTAL_STICKERS * 100, 1) if TOTAL_STICKERS else 0,

        "duplicates": duplicates,

        "by_rarity": by_rarity,

    }





def clear_animation(progress: dict) -> None:

    progress["last_unlock_animation"] = None

    persist(progress)





# Compatibilidad: re-exportar funciones de intercambio

from services.exchange import (  # noqa: E402

    accept_exchange,

    cancel_my_offer,

    create_exchange_offer,

    get_market_offers,

    get_my_offers,

)


