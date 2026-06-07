"""Tienda de packs: economía de monedas y apertura de sobres.

Las monedas se ganan **desbloqueando logros** (fuente finita, sin inflación) y
se gastan abriendo sobres de figuritas. El saldo se calcula como:

    saldo = monedas_ganadas_por_logros - monedas_gastadas
"""

from __future__ import annotations

import random

from data.album import ALL_STICKERS
from services.achievements import coins_for_unlocked
from services.database import add_coins_spent, get_coins_spent
from services.inventory import add_sticker_to_user
from services.progress_hooks import after_progress_change
from services.progress_utils import progress_user_id

# Sobres disponibles. `weights` son pesos relativos por categoría a la hora de
# sortear cada figurita; `guarantee` exige al menos una figurita de esas
# categorías en el sobre.
PACKS = [
    {
        "id": "bronce",
        "name": "Sobre Bronce",
        "emoji": "🥉",
        "cost": 40,
        "size": 3,
        "desc": "3 figuritas. Ideal para arrancar.",
        "weights": {"basica": 46, "comun": 28, "rara": 14, "epica": 6, "legendaria": 2, "bandera": 4},
    },
    {
        "id": "plata",
        "name": "Sobre Plata",
        "emoji": "🥈",
        "cost": 90,
        "size": 4,
        "desc": "4 figuritas con mejores chances de raras.",
        "weights": {"basica": 30, "comun": 30, "rara": 22, "epica": 11, "legendaria": 4, "bandera": 3},
    },
    {
        "id": "oro",
        "name": "Sobre Oro",
        "emoji": "🥇",
        "cost": 160,
        "size": 5,
        "desc": "5 figuritas. Garantiza al menos 1 épica o legendaria.",
        "weights": {"basica": 18, "comun": 27, "rara": 28, "epica": 18, "legendaria": 7, "bandera": 2},
        "guarantee": ["epica", "legendaria"],
    },
]

PACK_BY_ID = {p["id"]: p for p in PACKS}

# Figuritas agrupadas por categoría (rareza o "bandera").
_BY_RARITY: dict[str, list[dict]] = {}
for _s in ALL_STICKERS:
    _cat = "bandera" if _s.get("kind") == "bandera" else _s["rarity"]
    _BY_RARITY.setdefault(_cat, []).append(_s)


def coins_balance(progress: dict) -> int:
    """Monedas disponibles para gastar (ganadas por logros menos gastadas)."""
    uid = progress_user_id(progress)
    return max(0, coins_for_unlocked(uid) - get_coins_spent(uid))


def _weighted_rarity(weights: dict[str, int]) -> str:
    cats = [c for c in weights if _BY_RARITY.get(c)]
    pesos = [weights[c] for c in cats]
    return random.choices(cats, weights=pesos, k=1)[0]


def _pick_sticker(rarity: str, owned: set[str]) -> dict:
    """Elige una figurita de la categoría, priorizando las que faltan."""
    pool = _BY_RARITY.get(rarity, []) or ALL_STICKERS
    faltantes = [s for s in pool if s["id"] not in owned]
    return random.choice(faltantes if faltantes else pool)


def open_pack(progress: dict, pack_id: str) -> dict:
    """Abre un sobre gastando monedas y entrega figuritas.

    Devuelve un dict con ``ok``. Si no alcanza el saldo: ``{"ok": False,
    "reason": "coins"}``. Si todo va bien incluye ``pack``, ``rewards`` (lista
    de figuritas) y ``achievements`` (logros recién desbloqueados).
    """
    pack = PACK_BY_ID.get(pack_id)
    if not pack:
        return {"ok": False, "reason": "pack"}

    if coins_balance(progress) < pack["cost"]:
        return {"ok": False, "reason": "coins"}

    uid = progress_user_id(progress)
    add_coins_spent(uid, pack["cost"])

    owned = set(progress.get("unlocked_stickers", []))
    rarities: list[str] = [_weighted_rarity(pack["weights"]) for _ in range(pack["size"])]

    guarantee = pack.get("guarantee")
    if guarantee and not any(r in guarantee for r in rarities):
        valid = [g for g in guarantee if _BY_RARITY.get(g)]
        if valid:
            rarities[random.randrange(len(rarities))] = random.choice(valid)

    rewards: list[dict] = []
    for rarity in rarities:
        sticker = _pick_sticker(rarity, owned)
        owned.add(sticker["id"])
        add_sticker_to_user(uid, sticker["id"], progress)
        rewards.append(sticker)

    achievements = after_progress_change(progress, event="pack")

    return {"ok": True, "pack": pack, "rewards": rewards, "achievements": achievements}
