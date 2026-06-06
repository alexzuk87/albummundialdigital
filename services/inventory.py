"""Inventario de figuritas por usuario (sin dependencias circulares)."""

from collections import Counter

from services.constants import RARITY_ORDER
from services.database import add_sticker, get_user_stickers, remove_sticker


def _stickers_to_lists(stickers: dict[str, int]) -> tuple[list[str], list[str]]:
    unlocked = list(stickers.keys())
    duplicates: list[str] = []
    for sid, qty in stickers.items():
        if qty > 1:
            duplicates.extend([sid] * (qty - 1))
    return unlocked, duplicates


def add_sticker_to_user(user_id: int, sticker_id: str, progress: dict) -> None:
    add_sticker(user_id, sticker_id, 1)
    stickers = get_user_stickers(user_id)
    progress["sticker_quantities"] = stickers
    progress["unlocked_stickers"], progress["duplicates"] = _stickers_to_lists(stickers)


def remove_sticker_from_user(user_id: int, sticker_id: str, progress: dict) -> bool:
    ok = remove_sticker(user_id, sticker_id, 1)
    if ok:
        stickers = get_user_stickers(user_id)
        progress["sticker_quantities"] = stickers
        progress["unlocked_stickers"], progress["duplicates"] = _stickers_to_lists(stickers)
    return ok


def user_owns_sticker(progress: dict, sticker_id: str) -> bool:
    return progress.get("sticker_quantities", {}).get(sticker_id, 0) > 0


def sync_progress_stickers(user_id: int, progress: dict) -> None:
    stickers = get_user_stickers(user_id)
    progress["sticker_quantities"] = stickers
    progress["unlocked_stickers"], progress["duplicates"] = _stickers_to_lists(stickers)


def duplicates_by_category(progress: dict) -> list[tuple[str, list[tuple[dict, int]]]]:
    """Agrupa las figuritas repetidas por categoría.

    Devuelve una lista ordenada de (categoría, [(figurita, cantidad_repetida)]).
    Las banderas se agrupan en su propia categoría al final.
    """
    from data.album import STICKER_BY_ID

    counts = Counter(progress.get("duplicates", []))
    groups: dict[str, list[tuple[dict, int]]] = {}
    for sticker_id, qty in counts.items():
        sticker = STICKER_BY_ID.get(sticker_id)
        if not sticker:
            continue
        category = "bandera" if sticker.get("kind") == "bandera" else sticker["rarity"]
        groups.setdefault(category, []).append((sticker, qty))

    ordered: list[tuple[str, list[tuple[dict, int]]]] = []
    for category in [*RARITY_ORDER, "bandera"]:
        items = groups.get(category)
        if items:
            items.sort(key=lambda pair: pair[0]["name"])
            ordered.append((category, items))
    return ordered
