"""Equipo personalizado: formaciones y 11 titular."""

from data.album import STICKER_BY_ID
from data.formations import FORMATIONS, empty_lineup, get_formation

DEFAULT_CUSTOM_TEAM = {
    "name": "Mi Equipo Soñado",
    "formation": "4-3-3",
    "tactic": "equilibrada",
    "lineup": {},
}

# Posición vertical en la cancha (% desde arriba)
_PITCH_Y = {"gk": 88, "def": 70, "mid": 50, "fwd": 26}


def _slot_left(keys: list[str], key: str) -> float:
    if len(keys) == 1:
        return 50.0
    idx = keys.index(key)
    return 8.0 + (84.0 / (len(keys) - 1)) * idx


def ensure_custom_team(progress: dict) -> dict:
    if "custom_team" not in progress or not isinstance(progress["custom_team"], dict):
        progress["custom_team"] = {
            "name": DEFAULT_CUSTOM_TEAM["name"],
            "formation": "4-3-3",
            "lineup": empty_lineup("4-3-3"),
        }
    team = progress["custom_team"]
    team.setdefault("name", DEFAULT_CUSTOM_TEAM["name"])
    team.setdefault("tactic", DEFAULT_CUSTOM_TEAM["tactic"])
    formation_id = team.get("formation", "4-3-3")
    if formation_id not in FORMATIONS:
        formation_id = "4-3-3"
        team["formation"] = formation_id
    lineup = team.setdefault("lineup", {})
    for slot in get_formation(formation_id)["slots"]:
        lineup.setdefault(slot["key"], None)
    return team


def unlocked_for_position(progress: dict, position: str, exclude_ids: set[str]) -> list[dict]:
    result = []
    for sid in progress.get("unlocked_stickers", []):
        if sid in exclude_ids:
            continue
        sticker = STICKER_BY_ID.get(sid)
        if sticker and sticker.get("kind") not in ("crest", "bandera") and sticker["position"] == position:
            result.append(sticker)
    return sorted(result, key=lambda s: s["name"])


def unlocked_all(progress: dict, exclude_ids: set[str]) -> list[dict]:
    result = []
    for sid in progress.get("unlocked_stickers", []):
        if sid in exclude_ids:
            continue
        sticker = STICKER_BY_ID.get(sid)
        if sticker and sticker.get("kind") not in ("crest", "bandera"):
            result.append(sticker)
    return sorted(result, key=lambda s: s["name"])


def sticker_label(sticker: dict) -> str:
    from services.constants import RARITY_LABELS
    if sticker.get("kind") == "bandera":
        return f"🏳️ Bandera {sticker['team_name']}"
    return (
        f"#{sticker['shirt_number']} {sticker['name']} ({sticker['club']}) "
        f"— {RARITY_LABELS[sticker['rarity']]}"
    )


def lineup_filled_count(lineup: dict, formation_id: str | None = None) -> int:
    if formation_id:
        slots = get_formation(formation_id)["slots"]
        return sum(1 for s in slots if lineup.get(s["key"]))
    return sum(1 for v in lineup.values() if v)


def save_custom_team(
    progress: dict,
    name: str,
    formation_id: str,
    lineup: dict,
    tactic: str | None = None,
) -> None:
    from services.achievements import check_and_unlock
    from services.progress_utils import progress_user_id
    from services.storage import save_progress

    uid = progress_user_id(progress)
    team = ensure_custom_team(progress)
    team["name"] = name.strip() or DEFAULT_CUSTOM_TEAM["name"]
    team["formation"] = formation_id if formation_id in FORMATIONS else "4-3-3"
    if tactic is not None:
        team["tactic"] = tactic
    slots = get_formation(team["formation"])["slots"]
    owned = set(progress.get("unlocked_stickers", []))
    team["lineup"] = {}
    for slot in slots:
        sid = lineup.get(slot["key"])
        team["lineup"][slot["key"]] = sid if sid in owned else None
    save_progress(uid, progress)
    check_and_unlock(uid, progress)


def _pitch_player_html(sid: str | None, slot: dict) -> str:
    from services.flags import flag_img_html
    from services.sticker_ui import jersey_html, player_avatar_url
    from data.player_meta import get_kit_colors

    if not sid or sid not in STICKER_BY_ID:
        return (
            f'<div class="pitch-player empty" title="{slot["label"]}">'
            f'<span class="slot-pos">{slot["label"]}</span>'
            f'<span class="slot-empty">Vacío</span></div>'
        )
    s = STICKER_BY_ID[sid]
    primary, _, _ = get_kit_colors(s["team_id"])
    avatar = player_avatar_url(s["name"], s["team_id"])
    jersey = jersey_html(s["team_id"], s["shirt_number"], size="sm")
    flag = flag_img_html(s["team_id"], 12)
    return (
        f'<div class="pitch-player filled" title="{s["name"]}">'
        f'<img class="pitch-avatar" src="{avatar}" alt="">'
        f"{jersey}"
        f'<div class="slot-name">{s["name"].split()[-1]}</div>'
        f'<div class="slot-club">{flag} #{s["shirt_number"]}</div></div>'
    )


def formation_pitch_html(team_name: str, formation_id: str, lineup: dict) -> str:
    formation = get_formation(formation_id)
    slot_map = {s["key"]: s for s in formation["slots"]}
    players_html = ""

    for line_key, keys in formation["rows"].items():
        top = _PITCH_Y.get(line_key, 50)
        for key in keys:
            left = _slot_left(keys, key)
            slot = slot_map.get(key, {"key": key, "label": key})
            inner = _pitch_player_html(lineup.get(key), slot)
            players_html += (
                f'<div class="pitch-marker" style="left:{left:.1f}%;top:{top}%;">{inner}</div>'
            )

    label = formation["label"].replace("-", " · ")
    return (
        f'<div class="formation-wrap">'
        f'<div class="formation-title">⚽ {team_name}</div>'
        f'<div class="pitch-field">'
        f'<div class="pitch-grass"></div>'
        f'<div class="pitch-center-line"></div>'
        f'<div class="pitch-center-circle"></div>'
        f'<div class="pitch-box pitch-box-top"></div>'
        f'<div class="pitch-box pitch-box-bottom"></div>'
        f"{players_html}"
        f"</div>"
        f'<div class="formation-formation">Formación {label}</div></div>'
    )
