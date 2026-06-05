"""Preguntas de trivia — 1056: 528 del álbum + 528 de historia del Mundial."""

import random

from data.album import ALL_STICKERS, TEAMS, TOTAL_STICKERS
from data.worldcup_trivia import build_worldcup_trivia

_POSITIONS = ["Arquero", "Defensor", "Mediocampista", "Delantero"]
_TEAM_NAMES = [t["name"] for t in TEAMS]
_CLUBS = sorted({s["club"] for s in ALL_STICKERS if s.get("club")})
_GROUPS = sorted({t["group"] for t in TEAMS})


def _pick_wrong(answer: str, pool: list[str], count: int, seed: str) -> list[str]:
    candidates = [x for x in pool if x != answer]
    rng = random.Random(seed)
    rng.shuffle(candidates)
    return candidates[:count]


def _options(answer: str, wrong: list[str]) -> list[str]:
    opts = [answer] + wrong[:3]
    rng = random.Random(answer + "|".join(wrong))
    rng.shuffle(opts)
    return opts


def _build_album_trivia() -> list[dict]:
    """Una pregunta por figurita (equipo, club, posición, grupo o categoría)."""
    from services.constants import RARITY_LABELS

    questions: list[dict] = []
    rpool = list(RARITY_LABELS.values())

    players = [s for s in ALL_STICKERS if s.get("kind") not in ("crest", "bandera")]
    for i, sticker in enumerate(players):
        name = sticker["name"]
        team = sticker["team_name"]
        pos = sticker["position"]
        club = sticker["club"]
        group = sticker["group"]
        variant = i % 5

        if variant == 0:
            q = f"¿De qué selección es la figurita de {name}?"
            ans = team
            wrong = _pick_wrong(team, _TEAM_NAMES, 3, f"{name}-team")
        elif variant == 1:
            q = f"¿Qué posición ocupa {name} en el álbum?"
            ans = pos
            wrong = _pick_wrong(pos, _POSITIONS, 3, f"{name}-pos")
        elif variant == 2:
            q = f"¿En qué club juega {name} según el álbum?"
            ans = club
            wrong = _pick_wrong(club, _CLUBS, 3, f"{name}-club")
        elif variant == 3:
            q = f"¿A qué grupo del Mundial pertenece la selección de {name}?"
            ans = f"Grupo {group}"
            wrong = _pick_wrong(ans, [f"Grupo {g}" for g in _GROUPS], 3, f"{name}-grp")
        else:
            q = f"¿Qué categoría tiene la figurita de {name}?"
            ans = RARITY_LABELS[sticker["rarity"]]
            wrong = _pick_wrong(ans, rpool, 3, f"{name}-rar")

        questions.append({
            "id": f"a{i + 1:04d}",
            "question": q,
            "options": _options(ans, wrong),
            "answer": ans,
        })

    return questions


def build_trivia_questions() -> list[dict]:
    from data.album import ALL_STICKERS as _all

    player_count = sum(1 for s in _all if s.get("kind") not in ("crest", "bandera"))
    album_q = _build_album_trivia()
    wc_q = build_worldcup_trivia(player_count)
    return album_q + wc_q


TRIVIA_QUESTIONS = build_trivia_questions()
TRIVIA_BY_ID = {t["id"]: t for t in TRIVIA_QUESTIONS}
