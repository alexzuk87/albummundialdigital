"""Copa jugable (Modo Torneo).

Un torneo de eliminación directa contra selecciones reales, cada vez más
fuertes. Reglas:

* Se puede jugar **una Copa por día**.
* Se avanza mientras se gana; al perder, quedás **eliminado** y la Copa termina
  por hoy. Si ganás la final, sos **Campeón del Mundo**.
* En eliminación directa no hay empate: si termina igualado, se define por
  **penales** (peso según la fuerza de cada equipo, con bastante azar).
"""

from __future__ import annotations

import random
from datetime import date

from services.database import (
    create_cup_run,
    get_today_cup_run,
    update_cup_run,
)
from services.progress_hooks import after_progress_change
from services.progress_utils import progress_user_id
from services.simulation import (
    award_random_sticker,
    random_opponent,
    result_of,
    simulate_match,
    squad_strength,
)

ROUND_LABELS = ["Octavos de final", "Cuartos de final", "Semifinal", "Final"]
ROUND_FACTORS = [-0.05, 0.06, 0.16, 0.28]
TOTAL_ROUNDS = len(ROUND_LABELS)


def _today() -> str:
    return date.today().isoformat()


def round_label(index: int) -> str:
    return ROUND_LABELS[index] if 0 <= index < TOTAL_ROUNDS else "Final"


def round_factor(index: int) -> float:
    return ROUND_FACTORS[index] if 0 <= index < TOTAL_ROUNDS else ROUND_FACTORS[-1]


def cup_state(progress: dict) -> dict:
    """Estado de la Copa de hoy: idle / active / eliminated / champion."""
    uid = progress_user_id(progress)
    run = get_today_cup_run(uid, _today())
    if run is None:
        return {"state": "idle", "run": None}
    return {"state": run["status"], "run": run}


def start_cup(progress: dict) -> dict:
    uid = progress_user_id(progress)
    run = get_today_cup_run(uid, _today())
    if run is not None:
        return {"ok": False, "reason": "already", "run": run}
    create_cup_run(uid, _today())
    return {"ok": True, "run": get_today_cup_run(uid, _today())}


def make_opponent(lineup_ids: list[str], run: dict, exclude_ids: set[str] | None = None) -> dict:
    """Genera el rival de la ronda actual (fuerza escalada por ronda)."""
    user_strength = squad_strength(lineup_ids)
    return random_opponent(
        user_strength,
        exclude_ids=exclude_ids,
        strength_factor=round_factor(run["round_index"]),
    )


def _penalty_winner(user_strength: int, opp_strength: int, rng: random.Random) -> bool:
    base = user_strength / (user_strength + opp_strength) if (user_strength + opp_strength) else 0.5
    p = 0.5 + (base - 0.5) * 0.4  # los penales achican diferencias: mucho azar
    return rng.random() < p


def play_round(
    progress: dict,
    run: dict,
    lineup_ids: list[str],
    formation_id: str,
    user_tactic: str,
    opponent: dict,
) -> dict | None:
    if run.get("status") != "active":
        return None

    uid = progress_user_id(progress)
    rng = random.Random()
    user_strength = squad_strength(lineup_ids)
    user_goals, opp_goals, edge = simulate_match(
        user_strength, user_tactic, formation_id, opponent["strength"], opponent["tactic"], rng=rng
    )

    result = result_of(user_goals, opp_goals)
    penalties = False
    if result == "draw":
        penalties = True
        result = "win" if _penalty_winner(user_strength, opponent["strength"], rng) else "loss"

    round_index = run["round_index"]
    rewards: list[dict] = []

    if result == "win":
        wins = run["wins"] + 1
        new_index = round_index + 1
        champion = new_index >= TOTAL_ROUNDS
        status = "champion" if champion else "active"
        for _ in range(2 if round_index >= 2 else 1):
            rewards.append(award_random_sticker(uid, progress))
        if champion:
            rewards.append(award_random_sticker(uid, progress, only_rarity="legendaria"))
        update_cup_run(run["id"], new_index, wins, status)
    else:
        status = "eliminated"
        update_cup_run(run["id"], round_index, run["wins"], status)

    achievements = after_progress_change(progress, event="cup")

    return {
        "result": result,
        "user_goals": user_goals,
        "opp_goals": opp_goals,
        "edge": edge,
        "penalties": penalties,
        "opponent": opponent,
        "rewards": rewards,
        "achievements": achievements,
        "run": get_today_cup_run(uid, _today()),
        "round_label": round_label(round_index),
        "champion": status == "champion",
    }
