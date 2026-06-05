"""UI de fase de grupos y cuadro eliminatorio (banderas + botones)."""

from __future__ import annotations

import html

import streamlit as st

from data.album import TEAMS
from services.bracket import (
    THIRD_PLACES_NEEDED,
    assign_group_position,
    flag_name_row_html,
    group_podium_html,
    toggle_best_third,
)

TEAM_BY_NAME = {t["name"]: t for t in TEAMS}


def _rank_button(label: str, selected: bool, key: str, rank: str) -> bool:
    """Botón de posición con estilo según 1°/2°/3°."""
    css_class = f"rank-btn-{rank}" if selected else "rank-btn-off"
    st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
    clicked = st.button(
        label,
        type="primary" if selected else "secondary",
        use_container_width=True,
        key=key,
    )
    st.markdown("</div>", unsafe_allow_html=True)
    return clicked


def render_group_column(
    col,
    letter: str,
    team_list: list[dict],
    picks: dict[str, str],
    group_picks: dict,
    state: dict,
) -> None:
    team_names = [t["name"] for t in team_list]
    name_to_team = {t["name"]: t for t in team_list}
    picks = dict(picks)

    with col:
        st.markdown(
            f'<div class="group-pick-card">'
            f'<div class="group-pick-title">Grupo {letter}</div>'
            f"{group_podium_html(picks, name_to_team)}</div>",
            unsafe_allow_html=True,
        )
        for team in team_list:
            n = team["name"]
            is_first = picks.get("first") == n
            is_second = picks.get("second") == n
            is_third = picks.get("third") == n
            rank_cls = ""
            if is_first:
                rank_cls = "is-first"
            elif is_second:
                rank_cls = "is-second"
            elif is_third:
                rank_cls = "is-third"
            st.markdown(
                f'<div class="group-team-pick {rank_cls}">'
                f"{flag_name_row_html(team, 22)}</div>",
                unsafe_allow_html=True,
            )
            b1, b2, b3 = st.columns(3)
            with b1:
                if _rank_button(
                    "🥇 1°" if is_first else "1°",
                    is_first,
                    f"grp_{letter}_{team['id']}_1",
                    "gold",
                ):
                    group_picks[letter] = assign_group_position(
                        picks, team_names, n, "first"
                    )
                    state["group_picks"][letter] = group_picks[letter]
                    st.rerun()
            with b2:
                if _rank_button(
                    "🥈 2°" if is_second else "2°",
                    is_second,
                    f"grp_{letter}_{team['id']}_2",
                    "silver",
                ):
                    group_picks[letter] = assign_group_position(
                        picks, team_names, n, "second"
                    )
                    state["group_picks"][letter] = group_picks[letter]
                    st.rerun()
            with b3:
                if _rank_button(
                    "🥉 3°" if is_third else "3°",
                    is_third,
                    f"grp_{letter}_{team['id']}_3",
                    "bronze",
                ):
                    group_picks[letter] = assign_group_position(
                        picks, team_names, n, "third"
                    )
                    state["group_picks"][letter] = group_picks[letter]
                    st.rerun()

    if letter not in group_picks:
        group_picks[letter] = picks


def render_best_thirds_picker(
    all_thirds: list[str],
    selected: list[str],
    state: dict,
) -> list[str]:
    """Elige 8 mejores terceros con bandera (toggle por equipo)."""
    sel = list(selected)
    st.caption(
        f"Tocá **Clasifica** en cada bandera · **{len(sel)} / {THIRD_PLACES_NEEDED}** elegidos"
    )
    cols = st.columns(4)
    for i, name in enumerate(all_thirds):
        team = TEAM_BY_NAME.get(name)
        if not team:
            continue
        is_on = name in sel
        with cols[i % 4]:
            cls = "third-pick-card is-selected" if is_on else "third-pick-card"
            st.markdown(
                f'<div class="{cls}">{flag_name_row_html(team, 28)}</div>',
                unsafe_allow_html=True,
            )
            btn_label = "✓ Clasifica" if not is_on else "✕ Quitar"
            btn_type = "primary" if is_on else "secondary"
            if st.button(
                btn_label,
                key=f"third_pick_{team['id']}",
                use_container_width=True,
                type=btn_type,
            ):
                new_sel = toggle_best_third(sel, name, THIRD_PLACES_NEEDED)
                state["best_thirds"] = new_sel
                st.rerun()
    return sel


def render_knockout_match(
    col,
    team_a: str,
    team_b: str,
    rkey: str,
    match_i: int,
    winners: dict,
    state: dict,
) -> None:
    """Llave con dos banderas y botón para elegir ganador."""
    key = f"{rkey}_{match_i}"
    winner = winners.get(key)
    ta = TEAM_BY_NAME.get(team_a)
    tb = TEAM_BY_NAME.get(team_b)

    with col:
        st.markdown('<div class="knockout-match-card">', unsafe_allow_html=True)
        if team_b == "BYE":
            if ta:
                st.markdown(
                    f'<div class="knockout-team-row is-winner">'
                    f"{flag_name_row_html(ta, 30)}</div>",
                    unsafe_allow_html=True,
                )
            state["winners"][key] = team_a
            st.caption("Pasa directo")
        else:
            a_win = winner == team_a
            b_win = winner == team_b
            if ta:
                st.markdown(
                    f'<div class="knockout-team-row {"is-winner" if a_win else ""}">'
                    f"{flag_name_row_html(ta, 28)}</div>",
                    unsafe_allow_html=True,
                )
            if st.button(
                "🏆 Gana" if not a_win else "✓ Ganador",
                key=f"win_{rkey}_{match_i}_a",
                use_container_width=True,
                type="primary" if a_win else "secondary",
            ):
                state["winners"][key] = team_a
                st.rerun()
            st.markdown(
                '<div class="knockout-vs">vs</div>',
                unsafe_allow_html=True,
            )
            if tb:
                st.markdown(
                    f'<div class="knockout-team-row {"is-winner" if b_win else ""}">'
                    f"{flag_name_row_html(tb, 28)}</div>",
                    unsafe_allow_html=True,
                )
            if st.button(
                "🏆 Gana" if not b_win else "✓ Ganador",
                key=f"win_{rkey}_{match_i}_b",
                use_container_width=True,
                type="primary" if b_win else "secondary",
            ):
                state["winners"][key] = team_b
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def bracket_match_html_flags(
    team_a: str, team_b: str, winner: str | None = None,
) -> str:
    ta = TEAM_BY_NAME.get(team_a)
    tb = TEAM_BY_NAME.get(team_b)
    if team_b == "BYE":
        inner = flag_name_row_html(ta, 22) if ta else html.escape(team_a)
        return (
            f'<div class="bracket-match bye">'
            f'<div class="bracket-team winner">{inner}</div>'
            f'<div class="bracket-bye-label">pasa directo</div></div>'
        )
    a_inner = flag_name_row_html(ta, 20) if ta else html.escape(team_a)
    b_inner = flag_name_row_html(tb, 20) if tb else html.escape(team_b)
    a_cls = "bracket-team-row-html winner" if winner == team_a else "bracket-team-row-html"
    b_cls = "bracket-team-row-html winner" if winner == team_b else "bracket-team-row-html"
    return (
        f'<div class="bracket-match">'
        f'<div class="{a_cls}">{a_inner}</div>'
        f'<div class="bracket-vs">vs</div>'
        f'<div class="{b_cls}">{b_inner}</div></div>'
    )


def bracket_tree_html_flags(
    rounds: list[tuple[str, list[tuple[str, str]], str]],
    winners: dict[str, str],
) -> str:
    cols = []
    for title, pairs, rkey in rounds:
        inner = "".join(
            bracket_match_html_flags(a, b, winners.get(f"{rkey}_{i}"))
            for i, (a, b) in enumerate(pairs)
        )
        cols.append(
            f'<div class="knockout-tree-col">'
            f'<div class="knockout-col-title">{html.escape(title)}</div>'
            f'<div class="knockout-col-matches">{inner}</div></div>'
        )
    return f'<div class="knockout-tree">{"".join(cols)}</div>'
