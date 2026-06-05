"""Mercado de intercambios entre usuarios."""

from data.album import STICKER_BY_ID
from services.constants import RARITY_LABELS
from services.database import (
    add_sticker,
    create_exchange_offer_db,
    delete_exchange_offer,
    get_exchange_offer,
    get_user_exchange_offers,
    get_user_stickers,
    list_exchange_offers,
    remove_sticker,
)
from services.inventory import remove_sticker_from_user, user_owns_sticker
from services.progress_utils import progress_user_id


def _uid(progress: dict) -> int:
    return progress_user_id(progress)


def create_exchange_offer(progress: dict, offer_sticker_id: str) -> tuple[bool, str]:
    if not user_owns_sticker(progress, offer_sticker_id):
        return False, "No tienes esa figurita."
    sticker = STICKER_BY_ID[offer_sticker_id]
    create_exchange_offer_db(_uid(progress), offer_sticker_id, sticker["rarity"])
    return True, f"Oferta publicada. Buscás figurita **{RARITY_LABELS[sticker['rarity']]}**."


def get_market_offers(progress: dict) -> list[dict]:
    return list_exchange_offers(exclude_user_id=_uid(progress))


def get_my_offers(progress: dict) -> list[dict]:
    return get_user_exchange_offers(_uid(progress))


def cancel_my_offer(progress: dict, offer_id: int) -> bool:
    uid = _uid(progress)
    if not any(o["id"] == offer_id for o in get_user_exchange_offers(uid)):
        return False
    delete_exchange_offer(offer_id)
    return True


def accept_exchange(progress: dict, offer_id: int, give_sticker_id: str) -> tuple[bool, str]:
    from services.progress_hooks import after_progress_change

    uid = _uid(progress)
    offer = get_exchange_offer(offer_id)
    if not offer:
        return False, "Oferta no disponible."
    if offer["user_id"] == uid:
        return False, "No podés aceptar tu propia oferta."

    wanted_rarity = offer["wanted_rarity"]
    give = STICKER_BY_ID.get(give_sticker_id)
    if not give or give["rarity"] != wanted_rarity:
        return False, f"Debés ofrecer una figurita **{RARITY_LABELS[wanted_rarity]}**."

    if not user_owns_sticker(progress, give_sticker_id):
        return False, "No tenés esa figurita."

    seller_id = offer["user_id"]
    if get_user_stickers(seller_id).get(offer["offer_sticker_id"], 0) < 1:
        return False, "El vendedor ya no tiene esa figurita."

    delete_exchange_offer(offer_id)
    remove_sticker_from_user(uid, give_sticker_id, progress)
    add_sticker(uid, offer["offer_sticker_id"], 1)
    progress["sticker_quantities"] = get_user_stickers(uid)
    from services.inventory import sync_progress_stickers
    sync_progress_stickers(uid, progress)

    remove_sticker(seller_id, offer["offer_sticker_id"], 1)
    add_sticker(seller_id, give_sticker_id, 1)

    after_progress_change(progress, event="exchange")
    return True, "¡Intercambio realizado!"
