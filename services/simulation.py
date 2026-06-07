"""Simulación de partidos 11 vs 11 con tácticas y rivales reales.

El equipo del usuario son sus figuritas (11 titulares). Los rivales son
**selecciones reales del álbum**: se elige una al azar entre las de fuerza
parecida a la del usuario. La táctica y la formación de cada lado modifican el
ataque/defensa, y el duelo táctico (piedra-papel-tijera) da un bonus extra.
"""

from __future__ import annotations

import math
import random
from datetime import date

from data.album import ALL_STICKERS, STICKER_BY_ID, TEAM_BY_ID, TEAMS
from data.formations import get_formation
from data.tactics import (
    COUNTER_BONUS_ATK,
    COUNTER_MALUS_ATK,
    TACTICS,
    formation_mods,
    get_tactic,
    tactic_edge,
)
from services.constants import MAX_SIM_PER_DAY, RARITY_POWER
from services.database import count_sim_matches_today, get_sim_overall, record_sim_match
from services.inventory import add_sticker_to_user
from services.progress_hooks import after_progress_change
from services.progress_utils import progress_user_id

GOALKEEPER_POSITION = "Arquero"
OPP_FORMATION = "4-3-3"
_MAX_GOALS = 7

# Orden de slots de un 4-3-3 para ubicar a los 11 de una selección rival.
_OPP_SLOTS = ["gk", "rb", "cb1", "cb2", "lb", "cm1", "cm2", "cm3", "rw", "st", "lw"]


# ----------------------------------------------------------------------------
# Fuerza de los planteles
# ----------------------------------------------------------------------------
def squad_strength(sticker_ids: list[str]) -> int:
    total = 0
    for sid in sticker_ids:
        sticker = STICKER_BY_ID.get(sid)
        if sticker:
            total += RARITY_POWER.get(sticker["rarity"], 1)
    return total


def team_lineup_ids(team_id: str) -> list[str]:
    """Los 11 ids de figuritas de una selección, en orden de plantel."""
    return [f"{team_id}_{i:02d}" for i in range(1, 12)]


def team_433_lineup(team_id: str) -> dict[str, str]:
    """Mapea los 11 de una selección a un esquema 4-3-3 para dibujar la cancha."""
    ids = team_lineup_ids(team_id)
    return dict(zip(_OPP_SLOTS, ids))


def team_strength(team_id: str) -> int:
    return squad_strength(team_lineup_ids(team_id))


OPPONENT_STRENGTHS: dict[str, int] = {t["id"]: team_strength(t["id"]) for t in TEAMS}


# ----------------------------------------------------------------------------
# Selección del rival (real, por fuerza similar)
# ----------------------------------------------------------------------------
def pick_opponent_team(
    user_strength: int,
    exclude_ids: set[str] | None = None,
    strength_factor: float = 0.0,
    rng: random.Random | None = None,
) -> str:
    """Elige una selección rival al azar entre las de fuerza parecida.

    `strength_factor` desplaza el objetivo (la Copa lo sube por ronda para que
    el rival sea cada vez más difícil).
    """
    rng = rng or random.Random()
    exclude = set(exclude_ids or [])
    target = max(1, user_strength * (1 + strength_factor))
    candidates = [(tid, s) for tid, s in OPPONENT_STRENGTHS.items() if tid not in exclude]
    if not candidates:
        candidates = list(OPPONENT_STRENGTHS.items())
    candidates.sort(key=lambda item: abs(item[1] - target))
    pool = candidates[: min(6, len(candidates))]
    return rng.choice(pool)[0]


def build_opponent(team_id: str, tactic_id: str | None = None, rng: random.Random | None = None) -> dict:
    rng = rng or random.Random()
    team = TEAM_BY_ID[team_id]
    return {
        "id": team_id,
        "team_id": team_id,
        "name": team["name"],
        "strength": OPPONENT_STRENGTHS[team_id],
        "tactic": tactic_id or rng.choice(list(TACTICS.keys())),
        "formation": OPP_FORMATION,
        "lineup": team_433_lineup(team_id),
    }


def random_opponent(
    user_strength: int,
    exclude_ids: set[str] | None = None,
    strength_factor: float = 0.0,
    rng: random.Random | None = None,
) -> dict:
    rng = rng or random.Random()
    team_id = pick_opponent_team(user_strength, exclude_ids, strength_factor, rng)
    return build_opponent(team_id, rng=rng)


# ----------------------------------------------------------------------------
# Motor de resultado
# ----------------------------------------------------------------------------
def _expected_goals(attack: float, defense: float) -> float:
    ratio = attack / (attack + defense) if (attack + defense) else 0.5
    return 0.35 + 2.8 * ratio


def _sample_poisson(lam: float, rng: random.Random) -> int:
    limit = math.exp(-max(0.0, lam))
    k = 0
    p = 1.0
    while True:
        k += 1
        p *= rng.random()
        if p <= limit:
            return min(k - 1, _MAX_GOALS)


def _effective(strength: float, tactic_id: str, formation: dict, edge: int) -> tuple[float, float]:
    tactic = get_tactic(tactic_id)
    f_atk, f_def = formation_mods(formation)
    atk_mult = 1 + tactic["atk"] + f_atk
    def_mult = 1 + tactic["def"] + f_def
    if edge > 0:
        atk_mult += COUNTER_BONUS_ATK
    elif edge < 0:
        atk_mult -= COUNTER_MALUS_ATK
    return strength * max(0.4, atk_mult), strength * max(0.4, def_mult)


def simulate_match(
    user_strength: int,
    user_tactic: str,
    user_formation_id: str,
    opp_strength: int,
    opp_tactic: str,
    opp_formation_id: str = OPP_FORMATION,
    rng: random.Random | None = None,
) -> tuple[int, int, int]:
    """Devuelve (goles_usuario, goles_rival, edge_táctico)."""
    rng = rng or random.Random()
    edge = tactic_edge(user_tactic, opp_tactic)
    u_form = get_formation(user_formation_id)
    o_form = get_formation(opp_formation_id)
    u_atk, u_def = _effective(user_strength, user_tactic, u_form, edge)
    o_atk, o_def = _effective(opp_strength, opp_tactic, o_form, -edge)
    user_goals = _sample_poisson(_expected_goals(u_atk, o_def), rng)
    opp_goals = _sample_poisson(_expected_goals(o_atk, u_def), rng)
    return user_goals, opp_goals, edge


def result_of(user_goals: int, opp_goals: int) -> str:
    if user_goals > opp_goals:
        return "win"
    if user_goals < opp_goals:
        return "loss"
    return "draw"


# ----------------------------------------------------------------------------
# Recompensas
# ----------------------------------------------------------------------------
def award_random_sticker(uid: int, progress: dict, only_rarity: str | None = None) -> dict:
    unlocked = set(progress.get("unlocked_stickers", []))
    pool = ALL_STICKERS
    if only_rarity:
        pool = [s for s in ALL_STICKERS if s.get("rarity") == only_rarity] or ALL_STICKERS
    locked = [s for s in pool if s["id"] not in unlocked]
    sticker = random.choice(locked if locked else pool)
    add_sticker_to_user(uid, sticker["id"], progress)
    return sticker


# ----------------------------------------------------------------------------
# Partido amistoso (usa el 11 guardado del usuario)
# ----------------------------------------------------------------------------
def sim_matches_remaining(progress: dict) -> int:
    uid = progress_user_id(progress)
    played = count_sim_matches_today(uid, date.today().isoformat())
    return max(0, MAX_SIM_PER_DAY - played)


def play_friendly(
    progress: dict,
    lineup_ids: list[str],
    formation_id: str,
    user_tactic: str,
) -> dict | None:
    """Juega un amistoso contra una selección real al azar de nivel parecido."""
    uid = progress_user_id(progress)
    today = date.today().isoformat()
    if count_sim_matches_today(uid, today) >= MAX_SIM_PER_DAY:
        return None

    user_strength = squad_strength(lineup_ids)
    opponent = random_opponent(user_strength)
    user_goals, opp_goals, edge = simulate_match(
        user_strength, user_tactic, formation_id,
        opponent["strength"], opponent["tactic"],
    )
    result = result_of(user_goals, opp_goals)
    record_sim_match(uid, opponent["id"], opponent["name"], user_goals, opp_goals, result, today)

    rewards = [award_random_sticker(uid, progress)]
    if result == "win":
        rewards.append(award_random_sticker(uid, progress))

    achievements = after_progress_change(progress, event="sim")
    return {
        "opponent": opponent,
        "user_strength": user_strength,
        "user_tactic": user_tactic,
        "user_formation": formation_id,
        "user_goals": user_goals,
        "opp_goals": opp_goals,
        "edge": edge,
        "result": result,
        "rewards": rewards,
        "achievements": achievements,
    }


def user_sim_overall(progress: dict) -> dict:
    return get_sim_overall(progress_user_id(progress))
