"""Simulación de partidos de fútbol 5 y recompensas en figuritas."""

from __future__ import annotations

import math
import random
from datetime import date

from data.album import ALL_STICKERS, STICKER_BY_ID
from data.sim_teams import SIM_TEAM_BY_ID
from services.constants import MAX_SIM_PER_DAY, RARITY_POWER
from services.database import (
    count_sim_matches_today,
    get_sim_overall,
    record_sim_match,
)
from services.inventory import add_sticker_to_user
from services.progress_hooks import after_progress_change
from services.progress_utils import progress_user_id

GOALKEEPER_POSITION = "Arquero"
_MAX_GOALS = 6


def squad_strength(sticker_ids: list[str]) -> int:
    total = 0
    for sid in sticker_ids:
        sticker = STICKER_BY_ID.get(sid)
        if sticker:
            total += RARITY_POWER.get(sticker["rarity"], 1)
    return total


def available_goalkeepers(progress: dict) -> list[dict]:
    return [
        STICKER_BY_ID[sid]
        for sid in progress.get("unlocked_stickers", [])
        if STICKER_BY_ID.get(sid)
        and STICKER_BY_ID[sid].get("position") == GOALKEEPER_POSITION
    ]


def available_outfielders(progress: dict) -> list[dict]:
    return [
        STICKER_BY_ID[sid]
        for sid in progress.get("unlocked_stickers", [])
        if STICKER_BY_ID.get(sid)
        and STICKER_BY_ID[sid].get("kind") == "player"
        and STICKER_BY_ID[sid].get("position") != GOALKEEPER_POSITION
    ]


def _expected_goals(attack: int, defense: int) -> float:
    """Goles esperados según la relación de fuerzas (resultado futbolístico)."""
    ratio = attack / (attack + defense) if (attack + defense) else 0.5
    return 0.35 + 2.8 * ratio


def _sample_poisson(lam: float, rng: random.Random) -> int:
    """Muestra un Poisson (goles realistas, mayormente 0-4)."""
    limit = math.exp(-lam)
    k = 0
    p = 1.0
    while True:
        k += 1
        p *= rng.random()
        if p <= limit:
            return min(k - 1, _MAX_GOALS)


def simulate_score(user_strength: int, opponent_rating: int) -> tuple[int, int]:
    rng = random.Random()
    user_goals = _sample_poisson(_expected_goals(user_strength, opponent_rating), rng)
    opp_goals = _sample_poisson(_expected_goals(opponent_rating, user_strength), rng)
    return user_goals, opp_goals


def _result_of(user_goals: int, opp_goals: int) -> str:
    if user_goals > opp_goals:
        return "win"
    if user_goals < opp_goals:
        return "loss"
    return "draw"


def _award_random_sticker(uid: int, progress: dict) -> dict:
    unlocked = set(progress.get("unlocked_stickers", []))
    locked = [s for s in ALL_STICKERS if s["id"] not in unlocked]
    pool = locked if locked else ALL_STICKERS
    sticker = random.choice(pool)
    add_sticker_to_user(uid, sticker["id"], progress)
    return sticker


def sim_matches_remaining(progress: dict) -> int:
    uid = progress_user_id(progress)
    played = count_sim_matches_today(uid, date.today().isoformat())
    return max(0, MAX_SIM_PER_DAY - played)


def play_match(progress: dict, sticker_ids: list[str], opponent_id: str) -> dict | None:
    """Juega un partido contra `opponent_id` con las 5 figuritas elegidas.

    Devuelve el resultado con goles, recompensas y logros, o None si no quedan
    partidos disponibles hoy.
    """
    opponent = SIM_TEAM_BY_ID.get(opponent_id)
    if not opponent:
        return None

    uid = progress_user_id(progress)
    today = date.today().isoformat()
    if count_sim_matches_today(uid, today) >= MAX_SIM_PER_DAY:
        return None

    user_strength = squad_strength(sticker_ids)
    user_goals, opp_goals = simulate_score(user_strength, opponent["rating"])
    result = _result_of(user_goals, opp_goals)

    record_sim_match(uid, opponent["id"], opponent["name"], user_goals, opp_goals, result, today)

    rewards = [_award_random_sticker(uid, progress)]
    if result == "win":
        rewards.append(_award_random_sticker(uid, progress))

    achievements = after_progress_change(progress, event="sim")

    return {
        "opponent": opponent,
        "user_strength": user_strength,
        "user_goals": user_goals,
        "opp_goals": opp_goals,
        "result": result,
        "rewards": rewards,
        "achievements": achievements,
    }


def user_sim_overall(progress: dict) -> dict:
    return get_sim_overall(progress_user_id(progress))
