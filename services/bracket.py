"""Simulación de fase de grupos y cuadro eliminatorio (Mundial 48 equipos)."""

from __future__ import annotations

from data.album import TEAMS

GROUP_ORDER = list("ABCDEFGHIJKL")
THIRD_PLACES_NEEDED = 8


def teams_by_group() -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    for team in TEAMS:
        groups.setdefault(team["group"], []).append(team)
    for g in groups:
        groups[g] = sorted(groups[g], key=lambda t: t["name"])
    return groups


def default_group_picks() -> dict[str, dict[str, str]]:
    groups = teams_by_group()
    picks: dict[str, dict[str, str]] = {}
    for g, teams in groups.items():
        names = [t["name"] for t in teams]
        picks[g] = {"first": names[0], "second": names[1], "third": names[2]}
    return picks


def collect_third_places(group_picks: dict[str, dict[str, str]]) -> list[str]:
    return [group_picks[g]["third"] for g in GROUP_ORDER if g in group_picks]


def _name_to_group(group_picks: dict[str, dict[str, str]]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for g, picks in group_picks.items():
        for key in ("first", "second", "third"):
            name = picks.get(key)
            if name:
                mapping[name] = g
    return mapping


def _pair_avoid_same_group(
    items: list[str], name_to_group: dict[str, str]
) -> list[tuple[str, str]]:
    """Empareja una lista evitando, en lo posible, cruces del mismo grupo."""
    remaining = list(items)
    pairs: list[tuple[str, str]] = []
    while len(remaining) >= 2:
        a = remaining.pop(0)
        idx = next(
            (i for i, x in enumerate(remaining) if name_to_group.get(x) != name_to_group.get(a)),
            0,
        )
        pairs.append((a, remaining.pop(idx)))
    if remaining:
        pairs.append((remaining[0], "BYE"))
    return pairs


def _repair_same_group(
    pairs: list[tuple[str, str]], name_to_group: dict[str, str]
) -> list[tuple[str, str]]:
    """Intercambia rivales para deshacer cruces del mismo grupo cuando es posible."""
    work = [list(p) for p in pairs]

    def same_group(pair: list[str]) -> bool:
        a, b = pair
        if "BYE" in (a, b):
            return False
        ga = name_to_group.get(a)
        return ga is not None and ga == name_to_group.get(b)

    for i, pair in enumerate(work):
        if not same_group(pair):
            continue
        a, b = pair
        for j, other in enumerate(work):
            if i == j or "BYE" in other:
                continue
            c, d = other
            if name_to_group.get(a) != name_to_group.get(d) and name_to_group.get(c) != name_to_group.get(b):
                work[i], work[j] = [a, d], [c, b]
                break
            if name_to_group.get(a) != name_to_group.get(c) and name_to_group.get(d) != name_to_group.get(b):
                work[i], work[j] = [a, c], [d, b]
                break
    return [tuple(p) for p in work]


def seed_knockout_pairs(
    group_picks: dict[str, dict[str, str]],
    best_thirds: list[str],
) -> list[tuple[str, str]]:
    """Cruces de dieciseisavos: cada 1° contra un 2°/3° de otro grupo."""
    name_to_group = _name_to_group(group_picks)
    firsts = [group_picks[g]["first"] for g in GROUP_ORDER if g in group_picks]
    seconds = [group_picks[g]["second"] for g in GROUP_ORDER if g in group_picks]
    pool = seconds + list(best_thirds)

    pairs: list[tuple[str, str]] = []
    for winner in firsts:
        if not pool:
            break
        idx = next(
            (i for i, rival in enumerate(pool) if name_to_group.get(rival) != name_to_group.get(winner)),
            0,
        )
        pairs.append((winner, pool.pop(idx)))
    pairs.extend(_pair_avoid_same_group(pool, name_to_group))
    return _repair_same_group(pairs, name_to_group)


def build_qualified_32(
    group_picks: dict[str, dict[str, str]],
    best_thirds: list[str],
) -> tuple[list[str] | None, str | None]:
    """Arma la lista de 32 clasificados (12+12+8) ya sembrada para el cruce."""
    if len(best_thirds) != THIRD_PLACES_NEEDED:
        return None, f"Elegí exactamente {THIRD_PLACES_NEEDED} mejores terceros (llevas {len(best_thirds)})."

    thirds_pool = set(collect_third_places(group_picks))
    invalid = [t for t in best_thirds if t not in thirds_pool]
    if invalid:
        return None, f"Terceros inválidos: {', '.join(invalid)}"

    pairs = seed_knockout_pairs(group_picks, best_thirds)
    qualified = [team for pair in pairs for team in pair]
    if len(qualified) != 32:
        return None, "Error al armar los 32 clasificados."
    return qualified, None


def pair_round(teams: list[str]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for i in range(0, len(teams) - 1, 2):
        pairs.append((teams[i], teams[i + 1]))
    if len(teams) % 2 == 1:
        pairs.append((teams[-1], "BYE"))
    return pairs


def winners_from_pairs(
    pairs: list[tuple[str, str]],
    picks: dict[str, str],
    prefix: str,
) -> tuple[list[str] | None, str | None]:
    winners: list[str] = []
    for i, (a, b) in enumerate(pairs):
        key = f"{prefix}_{i}"
        if b == "BYE":
            winners.append(a)
            continue
        w = picks.get(key)
        if not w:
            return None, f"Falta elegir ganador: {a} vs {b}"
        if w not in (a, b):
            return None, f"Ganador inválido en {a} vs {b}"
        winners.append(w)
    return winners, None


def flag_name_row_html(team: dict, size: int = 26) -> str:
    from services.flags import flag_img_html

    return (
        f'<div class="group-flag-row">'
        f'{flag_img_html(team["id"], size)}'
        f'<span class="group-flag-name">{team["name"]}</span></div>'
    )


def group_podium_html(picks: dict[str, str], name_to_team: dict[str, dict]) -> str:
    rows = []
    for pos, key in (("1°", "first"), ("2°", "second"), ("3°", "third")):
        name = picks.get(key)
        if name and name in name_to_team:
            inner = flag_name_row_html(name_to_team[name], 24)
        else:
            inner = '<span class="group-flag-name">—</span>'
        rows.append(
            f'<div class="group-rank-row">'
            f'<span class="group-rank-badge">{pos}</span>{inner}</div>'
        )
    return f'<div class="group-podium">{"".join(rows)}</div>'


def assign_group_position(
    picks: dict[str, str],
    team_names: list[str],
    team_name: str,
    slot: str,
) -> dict[str, str]:
    """Asigna 1°, 2° o 3° tocando la bandera (slot: first|second|third)."""
    p = dict(picks)
    for key in ("first", "second", "third"):
        if p.get(key) == team_name:
            p[key] = ""
    p[slot] = team_name
    used = {p.get("first"), p.get("second"), p.get("third")} - {""}
    for key in ("first", "second", "third"):
        if not p.get(key):
            for n in team_names:
                if n not in used:
                    p[key] = n
                    used.add(n)
                    break
    return p


def toggle_best_third(best_thirds: list[str], name: str, max_n: int = THIRD_PLACES_NEEDED) -> list[str]:
    """Agrega o quita un tercero de la lista de clasificados."""
    selected = list(best_thirds)
    if name in selected:
        selected.remove(name)
    elif len(selected) < max_n:
        selected.append(name)
    return selected


TEAM_BY_NAME = {t["name"]: t for t in TEAMS}


def bracket_round_labels(size: int) -> str:
    labels = {32: "Dieciseisavos de final", 16: "Octavos de final", 8: "Cuartos de final", 4: "Semifinales", 2: "Final"}
    return labels.get(size, f"Ronda de {size}")
