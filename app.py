"""Álbum Mundial Digital — aplicación Streamlit."""

import random
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.album import STICKER_BY_ID, TEAM_BY_ID, TEAMS, TOTAL_STICKERS
from data.formations import FORMATIONS, get_formation
from data.historical import HISTORICAL_PLAYERS, HISTORICAL_UNLOCK_THRESHOLDS
from data.trivia import TRIVIA_BY_ID, TRIVIA_QUESTIONS
from services.achievements import achievements_summary
from services.auth import current_user, is_logged_in, logout_user
from services.auth_ui import render_auth_page, try_google_login
from services.custom_team import (
    ensure_custom_team,
    formation_pitch_html,
    lineup_filled_count,
    save_custom_team,
    sticker_label,
    unlocked_for_position,
)
from services.share import get_share_content
from services.flags import flag_img_html
from services.constants import RARITY_LABELS, RARITY_ORDER
from services.exchange import (
    accept_exchange,
    cancel_my_offer,
    create_exchange_offer,
    get_market_offers,
    get_my_offers,
)
from services.game_logic import (
    clear_animation,
    get_progress,
    process_trivia_correct,
    process_trivia_wrong,
    progress_stats,
    trivia_remaining,
    trivia_status_label,
)
from services.album_ui import album_page_html, filter_team_pages
from services.sticker_ui import reveal_card_html, sticker_card_html
from services.database import get_achievements, reset_user_progress as reset_user
from services.storage import save_progress
from services.progress_utils import ensure_progress_user, progress_user_id
from services.html_render import show_pack_opening
from services.pack_animation import build_pack_opening_html
from services.styles import ALBUM_CSS

st.set_page_config(
    page_title="Álbum Mundial Digital 2026",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="auto",
)

st.markdown(ALBUM_CSS, unsafe_allow_html=True)


def init_state() -> None:
    if "show_animation" not in st.session_state:
        st.session_state.show_animation = False
    if "current_trivia_id" not in st.session_state:
        st.session_state.current_trivia_id = None
    if "trivia_round" not in st.session_state:
        st.session_state.trivia_round = 0
    if "album_page_index" not in st.session_state:
        st.session_state.album_page_index = 0
    if "album_flip" not in st.session_state:
        st.session_state.album_flip = ""


def refresh_progress() -> dict:
    progress = get_progress()
    ensure_progress_user(progress)
    st.session_state.progress = progress
    return progress


def _album_set_page(new_index: int, direction: str, total: int) -> None:
    new_index = max(0, min(new_index, total - 1))
    st.session_state.album_page_index = new_index
    st.session_state.album_flip = (
        "album-page-flip-next" if direction == "next" else "album-page-flip-prev"
    )


def _album_go_prev() -> None:
    total = st.session_state.get("album_page_count", 1)
    idx = st.session_state.get("album_page_index", 0)
    if idx > 0:
        _album_set_page(idx - 1, "prev", total)


def _album_go_next() -> None:
    total = st.session_state.get("album_page_count", 1)
    idx = st.session_state.get("album_page_index", 0)
    if idx < total - 1:
        _album_set_page(idx + 1, "next", total)


def _on_album_jump() -> None:
    total = st.session_state.get("album_page_count", 1)
    new = st.session_state.album_jump_select
    old = st.session_state.get("album_page_index", 0)
    if new != old:
        direction = "next" if new > old else "prev"
        _album_set_page(new, direction, total)


def show_new_achievements(achievements: list[dict]) -> None:
    for ach in achievements:
        st.toast(f"{ach['icon']} Logro desbloqueado: {ach['title']}", icon="🏆")


def render_header() -> None:
    user = current_user()
    st.markdown('<p class="main-header">⚽ ÁLBUM MUNDIAL DIGITAL 2026</p>', unsafe_allow_html=True)
    if user:
        st.markdown(
            f'<p class="sub-header">Hola, {user["username"]} · 48 selecciones · 576 figuritas (528 jugadores + 48 banderas)</p>',
            unsafe_allow_html=True,
        )


def render_progress_bar(progress: dict) -> None:
    stats = progress_stats(progress)
    pct = stats["percent"]
    st.markdown(
        f"""
        <div class="progress-wrap">
            <div class="progress-label">
                Progreso del álbum: {stats['unlocked']} / {stats['total']} figuritas ({pct}%)
            </div>
            <div class="progress-bar-outer">
                <div class="progress-bar-inner" style="width:{max(pct, 3)}%;">{pct}%</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns(5)
    for i, rarity in enumerate(RARITY_ORDER):
        with cols[i]:
            st.metric(RARITY_LABELS[rarity], stats["by_rarity"].get(rarity, 0))


def render_unlock_animation(progress: dict) -> None:
    if not st.session_state.get("show_animation"):
        return

    sticker_id = None
    anim = progress.get("last_unlock_animation")
    if anim:
        sticker_id = anim.get("sticker_id")
    if not sticker_id:
        sticker_id = st.session_state.get("pending_unlock_sticker_id")

    if not sticker_id:
        st.session_state.show_animation = False
        return

    sticker = STICKER_BY_ID.get(sticker_id)
    if not sticker:
        st.session_state.show_animation = False
        return

    rarity = sticker["rarity"]
    if rarity == "legendaria":
        st.balloons()
    elif rarity == "epica":
        st.balloons()

    title = "¡Correcto! Desbloqueaste"
    if sticker.get("kind") == "bandera":
        st.markdown(f"### 🏳️ {title} la **BANDERA** de **{sticker['team_name']}**")
    elif rarity == "legendaria":
        st.markdown(f"### 👑 {title} una **LEYENDA**")
    elif rarity == "epica":
        st.markdown(f"### ⭐ {title} una figurita **ÉPICA**")
    else:
        st.success(
            f"{title} a **{sticker['name']}** — "
            f"{sticker['position']}, {sticker['club']}"
        )

    reveal = reveal_card_html(sticker)
    pack_html = build_pack_opening_html(sticker, reveal)
    if rarity == "legendaria":
        show_pack_opening(pack_html, height=920, scroll=True)
    elif rarity == "epica":
        show_pack_opening(pack_html, height=880, scroll=True)
    else:
        show_pack_opening(pack_html, height=580, scroll=False)
    if st.button("¡Genial! Continuar", key="dismiss_anim"):
        clear_animation(progress)
        st.session_state.show_animation = False
        st.session_state.pop("pending_unlock_sticker_id", None)
        refresh_progress()
        st.rerun()


def page_inicio(progress: dict) -> None:
    render_progress_bar(progress)
    dupes = len(progress.get("duplicates", []))
    ach_count = len(get_achievements(progress_user_id(progress)))

    pills = [
        f"🎯 Trivias: {trivia_status_label(progress)}",
        f"🔄 Repetidas: {dupes}",
        f"🏅 Logros: {ach_count}",
    ]
    st.markdown("".join(f'<span class="stat-pill">{p}</span>' for p in pills), unsafe_allow_html=True)
    st.divider()

    st.subheader("🏟️ Cómo jugar")
    st.markdown("""
    1. **Trivias** — 6 intentos por día. Si fallás, perdés ese turno.
    2. **Paquete sorpresa** — Al acertar, se abre un sobre con tu figurita.
    3. **Mi 11 ideal** — Armá tu equipo en distintas formaciones y compartilo.
    4. **Intercambios** — Cambiá figuritas por otra de la **misma categoría**.
    5. **Logros** — Desbloqueá medallas al completar metas del álbum.
    """)
def page_trivia(progress: dict) -> None:
    remaining = trivia_remaining(progress)
    st.subheader("🎯 Trivias del día")
    st.caption(
        f"Banco de **{len(TRIVIA_QUESTIONS)}** preguntas: figuritas del álbum "
        f"y historia del Mundial (sedes, mascotas, récords, goleadores…)."
    )
    st.info(
        f"Te quedan **{remaining}** intentos hoy (máximo 6). "
        "Si fallás, perdés ese turno. Los intentos se renuevan a medianoche."
    )

    if st.session_state.get("show_animation"):
        render_unlock_animation(progress)
        return

    flash = st.session_state.pop("trivia_flash", None)
    if flash:
        if flash[0] == "error":
            st.error(flash[1])
        else:
            st.warning(flash[1])

    if remaining <= 0:
        st.warning("¡Completaste las trivias de hoy! Volvé mañana.")
        return

    available = [
        t for t in TRIVIA_QUESTIONS
        if t["id"] not in progress["trivia_today"].get("answered_ids", [])
    ]
    if not available:
        st.warning("No hay más preguntas disponibles hoy.")
        return

    valid_ids = {t["id"] for t in available}
    if st.session_state.get("current_trivia_id") not in valid_ids:
        st.session_state.current_trivia_id = random.choice(available)["id"]

    question = TRIVIA_BY_ID[st.session_state.current_trivia_id]
    st.markdown(f"**{question['question']}**")
    choice = st.radio("Elige tu respuesta:", question["options"], key=f"trivia_{st.session_state.trivia_round}")

    if st.button("Enviar respuesta", type="primary"):
        if choice == question["answer"]:
            result = process_trivia_correct(progress, question["id"])
            if result:
                st.session_state.show_animation = True
                st.session_state.pending_unlock_sticker_id = result["sticker"]["id"]
                st.session_state.pop("current_trivia_id", None)
                st.session_state.trivia_round += 1
                if result.get("achievements"):
                    st.session_state.pending_achievements = result["achievements"]
                refresh_progress()
                st.rerun()
            else:
                st.warning("No quedan figuritas bloqueadas o agotaste intentos.")
                refresh_progress()
        elif process_trivia_wrong(progress, question["id"]):
            left = trivia_remaining(get_progress())
            st.session_state.pop("current_trivia_id", None)
            st.session_state.trivia_round += 1
            st.session_state.trivia_flash = (
                "error", f"Incorrecto. Era: **{question['answer']}**. Quedan **{left}** intentos."
            )
            refresh_progress()
            st.rerun()
        else:
            st.session_state.trivia_flash = ("error", "Sin intentos restantes hoy.")
            st.rerun()


def page_mi_equipo(progress: dict) -> None:
    st.subheader("⭐ Mi 11 ideal")
    if not progress.get("unlocked_stickers"):
        st.info("Desbloqueá figuritas en **Trivias** para armar tu equipo.")
        return

    team_data = ensure_custom_team(progress)
    formation_id = team_data.get("formation", "4-3-3")
    saved_lineup = team_data["lineup"]
    filled = lineup_filled_count(saved_lineup, formation_id)

    if filled > 0:
        st.markdown("### Tu equipo guardado")
        st.markdown(formation_pitch_html(team_data["name"], formation_id, saved_lineup), unsafe_allow_html=True)
        st.caption(f"Jugadores: **{filled}/11**")

        share_text, links = get_share_content(team_data["name"], formation_id, saved_lineup)
        st.markdown("#### 📣 Compartir en redes")
        st.text_area("Texto para copiar", share_text, height=160, key="share_text")
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.link_button("🐦 X / Twitter", links["twitter"], use_container_width=True)
        c2.link_button("📘 Facebook", links["facebook"], use_container_width=True)
        c3.link_button("💬 WhatsApp", links["whatsapp"], use_container_width=True)
        c4.link_button("✈️ Telegram", links["telegram"], use_container_width=True)
        c5.link_button("📷 Instagram", links["instagram"], use_container_width=True)
        st.divider()

    with st.form("team_form"):
        team_name = st.text_input(
            "Nombre de tu equipo",
            value=team_data.get("name", "Mi Equipo Soñado"),
            max_chars=40,
            key="team_name_input",
        )
        picked_formation = st.selectbox(
            "Formación táctica",
            list(FORMATIONS.keys()),
            index=list(FORMATIONS.keys()).index(formation_id) if formation_id in FORMATIONS else 0,
            format_func=lambda x: FORMATIONS[x]["label"],
            key="team_formation_pick",
        )
        slots = get_formation(picked_formation)["slots"]
        st.caption("Elegí jugadores desbloqueados. Cada uno solo puede estar una vez.")

        draft: dict[str, str | None] = {}
        for slot in slots:
            exclude = {v for v in draft.values() if v}
            candidates = unlocked_for_position(progress, slot["position"], exclude)
            option_ids: list[str | None] = [None] + [c["id"] for c in candidates]
            saved = saved_lineup.get(slot["key"]) if picked_formation == formation_id else None
            idx = option_ids.index(saved) if saved in option_ids and saved not in exclude else 0
            draft[slot["key"]] = st.selectbox(
                f"{slot['label']} ({slot['position']})",
                option_ids,
                index=idx,
                format_func=lambda sid: "— Sin asignar —" if sid is None else sticker_label(STICKER_BY_ID[sid]),
                key=f"team_slot_{picked_formation}_{slot['key']}",
            )

        c1, c2 = st.columns(2)
        save = c1.form_submit_button("💾 Guardar mi 11", type="primary", use_container_width=True)
        clear = c2.form_submit_button("🗑️ Vaciar", use_container_width=True)

    if clear:
        from data.formations import empty_lineup
        save_custom_team(progress, team_data["name"], picked_formation, empty_lineup(picked_formation))
        st.success("Plantilla vaciada.")
        refresh_progress()
        st.rerun()
    if save:
        save_custom_team(progress, team_name, picked_formation, draft)
        st.success(f"¡Equipo **{team_name}** guardado!")
        refresh_progress()
        st.rerun()


def page_album(progress: dict) -> None:
    st.subheader("📖 Mi álbum")
    st.caption(
        "Cada hoja es una selección: **bandera** + 11 jugadores. "
        "Usá el menú «Ir a la hoja» o las flechas laterales."
    )

    unlocked = set(progress["unlocked_stickers"])
    duplicates = progress.get("duplicates", [])

    c1, c2, c3 = st.columns(3)
    with c1:
        filter_team = st.selectbox(
            "Selección",
            ["Todas"] + [f"{t['name']} (Grupo {t['group']})" for t in TEAMS],
            key="album_filter_team",
        )
    with c2:
        filter_rarity = st.selectbox(
            "Categoría",
            ["Todas"] + [RARITY_LABELS[r] for r in RARITY_ORDER] + ["Bandera"],
            key="album_filter_rarity",
        )
    with c3:
        show_only = st.radio(
            "Figuritas",
            ["Todas", "Solo desbloqueadas", "Solo bloqueadas"],
            horizontal=True,
            key="album_show_only",
        )

    if filter_rarity == "Todas":
        rarity_filter = None
    elif filter_rarity == "Bandera":
        rarity_filter = "__bandera__"
    else:
        rarity_filter = next(k for k, v in RARITY_LABELS.items() if v == filter_rarity)
    team_filter = None
    if filter_team != "Todas":
        team_filter = next(t["id"] for t in TEAMS if t["name"] == filter_team.split(" (Grupo")[0])

    pages = filter_team_pages(unlocked, duplicates, team_filter, rarity_filter, show_only)
    if not pages:
        st.warning("No hay figuritas con esos filtros.")
        return

    filter_key = (filter_team, filter_rarity, show_only)
    if st.session_state.get("album_filter_key") != filter_key:
        st.session_state.album_filter_key = filter_key
        st.session_state.album_page_index = 0

    total_pages = len(pages)
    st.session_state.album_page_count = total_pages

    idx = st.session_state.album_page_index
    if idx >= total_pages:
        idx = 0
        st.session_state.album_page_index = 0

    # Sincronizar el selectbox ANTES de dibujarlo (evita error al usar flechas)
    st.session_state.album_jump_select = idx

    team, stickers = pages[idx]
    flip_class = st.session_state.get("album_flip", "")
    st.session_state.album_flip = ""

    can_prev = idx > 0
    can_next = idx < total_pages - 1

    st.selectbox(
        "Ir a la hoja",
        range(total_pages),
        format_func=lambda i: f"Hoja {i + 1} — {pages[i][0]['name']} (Grupo {pages[i][0]['group']})",
        key="album_jump_select",
        on_change=_on_album_jump,
    )
    st.caption(f"**Hoja {idx + 1}** de **{total_pages}** · {team['name']}")

    html = album_page_html(
        team,
        stickers,
        unlocked,
        duplicates,
        idx + 1,
        total_pages,
        flip_class,
    )

    nav_l, nav_page, nav_r = st.columns([1.5, 7, 1.5])
    with nav_l:
        if st.button(
            "◀ Anterior",
            use_container_width=True,
            disabled=not can_prev,
            key="album_arrow_prev",
            help=f"Ir a hoja {idx}" if can_prev else "Primera hoja del álbum",
        ):
            _album_go_prev()
            st.rerun()
    with nav_page:
        st.markdown(html, unsafe_allow_html=True)
    with nav_r:
        if st.button(
            "Siguiente ▶",
            use_container_width=True,
            disabled=not can_next,
            key="album_arrow_next",
            help=f"Ir a hoja {idx + 2}" if can_next else "Última hoja del álbum",
        ):
            _album_go_next()
            st.rerun()


def page_intercambio(progress: dict) -> None:
    st.subheader("🔄 Mercado de intercambios")
    st.info(
        "Podés ofrecer **cualquier figurita** que tengas. "
        "El intercambio exige una figurita de la **misma categoría** (Básica, Común, Rara, etc.)."
    )

    owned = progress.get("unlocked_stickers", [])
    if not owned:
        st.warning("Todavía no tienes figuritas para intercambiar.")
    else:
        st.markdown("**Publicar oferta**")
        offer_id = st.selectbox(
            "Figurita que ofrecés",
            owned,
            format_func=lambda x: sticker_label(STICKER_BY_ID[x]),
        )
        offered = STICKER_BY_ID[offer_id]
        st.caption(f"Buscarás otra figurita **{RARITY_LABELS[offered['rarity']]}** a cambio.")
        if st.button("Publicar oferta", type="primary"):
            ok, msg = create_exchange_offer(progress, offer_id)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

    my_offers = get_my_offers(progress)
    if my_offers:
        st.divider()
        st.markdown("**Tus ofertas activas**")
        for o in my_offers:
            s = STICKER_BY_ID[o["offer_sticker_id"]]
            col1, col2 = st.columns([4, 1])
            col1.markdown(
                f"**{s['name']}** ({RARITY_LABELS[s['rarity']]}) → busca **{RARITY_LABELS[o['wanted_rarity']]}**"
            )
            if col2.button("Cancelar", key=f"cancel_{o['id']}"):
                cancel_my_offer(progress, o["id"])
                st.rerun()

    market = get_market_offers(progress)
    if market:
        st.divider()
        st.subheader("📢 Ofertas de otros coleccionistas")
        for offer in market:
            offered = STICKER_BY_ID[offer["offer_sticker_id"]]
            st.markdown(
                f"**@{offer['username']}** ofrece **{offered['name']}** ({RARITY_LABELS[offered['rarity']]}) "
                f"→ pide **{RARITY_LABELS[offer['wanted_rarity']]}**"
            )
            candidates = [
                sid for sid in owned
                if STICKER_BY_ID[sid]["rarity"] == offer["wanted_rarity"]
            ]
            if candidates:
                give = st.selectbox(
                    "Tu figurita a intercambiar",
                    candidates,
                    format_func=lambda x: sticker_label(STICKER_BY_ID[x]),
                    key=f"give_{offer['id']}",
                )
                if st.button(f"Aceptar intercambio #{offer['id']}", key=f"acc_{offer['id']}"):
                    ok, msg = accept_exchange(progress, offer["id"], give)
                    if ok:
                        st.success(msg)
                        refresh_progress()
                        st.rerun()
                    else:
                        st.error(msg)
            else:
                st.caption(f"No tienes figuritas {RARITY_LABELS[offer['wanted_rarity']]} para intercambiar.")


def page_logros(progress: dict) -> None:
    st.subheader("🏅 Logros")
    summary = achievements_summary(progress_user_id(progress))
    unlocked_n = sum(1 for a in summary if a["unlocked"])
    st.progress(unlocked_n / len(summary), text=f"{unlocked_n} / {len(summary)} logros desbloqueados")

    for ach in summary:
        css = "" if ach["unlocked"] else "historical-locked"
        st.markdown(
            f'<div class="historical-card {css}">'
            f'<strong>{ach["icon"]} {ach["title"]}</strong> '
            f'{"✅" if ach["unlocked"] else "🔒"}<br>'
            f'<small>{ach["desc"]}</small></div>',
            unsafe_allow_html=True,
        )


def page_historicos(progress: dict) -> None:
    st.subheader("🏛️ Jugadores históricos")
    pct = progress_stats(progress)["percent"]
    st.markdown(f"Progreso del álbum: **{pct}%**")
    for player in HISTORICAL_PLAYERS:
        threshold = HISTORICAL_UNLOCK_THRESHOLDS.get(player["id"], 100)
        is_on = pct >= threshold
        flag = f'<img src="https://flagcdn.com/w40/{player["flag_code"]}.png" width="32">'
        st.markdown(
            f'<div class="historical-card {"" if is_on else "historical-locked"}">'
            f'{flag if is_on else "🔒"} <strong>{player["name"] if is_on else "???"}</strong><br>'
            f'<small>{player["achievement"] if is_on else f"Desbloquea al {threshold}%"}</small></div>',
            unsafe_allow_html=True,
        )


def page_selecciones() -> None:
    from services.bracket import (
        THIRD_PLACES_NEEDED,
        bracket_round_labels,
        build_qualified_32,
        collect_third_places,
        default_group_picks,
        flag_name_row_html,
        pair_round,
        teams_by_group,
        winners_from_pairs,
    )
    from services.bracket_ui import (
        bracket_tree_html_flags,
        render_best_thirds_picker,
        render_group_column,
        render_knockout_match,
    )

    st.subheader("🌍 Fase de grupos y cuadro final")
    st.caption(
        "Elegí 1° y 2° de cada grupo, los **8 mejores terceros**, y armá el cuadro eliminatorio "
        "hasta la final (simulación para jugar con el Mundial 2026)."
    )

    if "bracket_state" not in st.session_state:
        st.session_state.bracket_state = {
            "group_picks": default_group_picks(),
            "best_thirds": [],
            "qualified": None,
            "rounds": {},
            "winners": {},
        }
    state = st.session_state.bracket_state
    groups = teams_by_group()

    st.markdown("### Fase de grupos (48 equipos · 12 grupos)")
    st.caption("Tocá **1°**, **2°** o **3°** en cada bandera; el podio de arriba se actualiza al instante.")
    group_picks: dict[str, dict[str, str]] = {}

    def _render_group_column(col, letter: str) -> None:
        if letter not in groups:
            return
        picks = dict(state["group_picks"].get(letter) or default_group_picks()[letter])
        render_group_column(col, letter, groups[letter], picks, group_picks, state)

    row1 = st.columns(6)
    for col, letter in zip(row1, "ABCDEF"):
        _render_group_column(col, letter)

    row2 = st.columns(6)
    for col, letter in zip(row2, "GHIJKL"):
        _render_group_column(col, letter)

    state["group_picks"] = group_picks
    all_thirds = collect_third_places(group_picks)
    thirds_pool_key = tuple(all_thirds)
    if st.session_state.get("bracket_thirds_pool") != thirds_pool_key:
        st.session_state.bracket_thirds_pool = thirds_pool_key
        st.session_state.pop("bracket_best_thirds", None)
        state["best_thirds"] = []
    st.markdown("### Mejores terceros (8 de 12 pasan)")
    prev_thirds = [t for t in state.get("best_thirds", []) if t in all_thirds]
    if not prev_thirds and not state.get("best_thirds"):
        state["best_thirds"] = all_thirds[:THIRD_PLACES_NEEDED]
    state["best_thirds"] = render_best_thirds_picker(
        all_thirds, state.get("best_thirds", []), state
    )

    c_reset, c_build = st.columns(2)
    with c_reset:
        if st.button("🔄 Nueva simulación", help="Reinicia el cuadro eliminatorio"):
            st.session_state.bracket_state = {
                "group_picks": default_group_picks(),
                "best_thirds": [],
                "qualified": None,
                "rounds": {},
                "winners": {},
            }
            st.rerun()
    with c_build:
        build_clicked = st.button("Armar cuadro de 32 equipos", type="primary", key="bracket_build_btn")

    if build_clicked:
        qualified, err = build_qualified_32(group_picks, state["best_thirds"])
        if err:
            st.error(err)
        else:
            state["qualified"] = qualified
            state["rounds"] = {"r32": pair_round(qualified)}
            state["winners"] = {}
            st.success("¡32 clasificados listos! Elegí ganadores en cada llave abajo.")

    qualified = state.get("qualified")
    if not qualified:
        st.info("Completá los grupos y los 8 mejores terceros, luego tocá **Armar cuadro de 32 equipos**.")
        return

    with st.expander("Ver los 32 clasificados", expanded=False):
        from services.bracket_ui import TEAM_BY_NAME

        cols = st.columns(4)
        for i, name in enumerate(qualified):
            team = TEAM_BY_NAME.get(name)
            if team:
                cols[i % 4].markdown(flag_name_row_html(team, 22), unsafe_allow_html=True)
            else:
                cols[i % 4].write(f"· {name}")

    round_keys = ["r32", "r16", "qf", "sf", "final"]
    sizes = [32, 16, 8, 4, 2]
    active_rounds = [
        (bracket_round_labels(sizes[i]), state["rounds"][rk], rk)
        for i, rk in enumerate(round_keys)
        if rk in state["rounds"]
    ]
    if active_rounds:
        st.markdown("### Cuadro eliminatorio")
        st.markdown(
            bracket_tree_html_flags(active_rounds, state["winners"]),
            unsafe_allow_html=True,
        )

    for rkey, size in zip(round_keys, sizes):
        pairs = state["rounds"].get(rkey)
        if not pairs:
            continue
        st.markdown(f"### {bracket_round_labels(size)} — elegí ganadores")
        cols_n = 4 if len(pairs) >= 8 else 2
        for row_start in range(0, len(pairs), cols_n):
            cols = st.columns(cols_n)
            for col_i, col in enumerate(cols):
                i = row_start + col_i
                if i >= len(pairs):
                    break
                a, b = pairs[i]
                render_knockout_match(
                    col, a, b, rkey, i, state["winners"], state
                )

        winners, err = winners_from_pairs(pairs, state["winners"], rkey)
        if err:
            st.warning(err)
            continue
        if rkey == "final" and winners:
            st.balloons()
            st.success(f"🏆 ¡Campeón del Mundial 2026 (tu simulación): **{winners[0]}**!")
            continue
        next_idx = round_keys.index(rkey) + 1
        if next_idx < len(round_keys) and winners:
            next_key = round_keys[next_idx]
            if next_key not in state["rounds"]:
                if st.button(
                    f"Avanzar a {bracket_round_labels(sizes[next_idx])} →",
                    key=f"adv_{rkey}",
                    type="primary",
                ):
                    state["rounds"][next_key] = pair_round(winners)
                    st.rerun()


def main() -> None:
    try_google_login()

    if not is_logged_in():
        render_auth_page()
        return

    init_state()
    progress = refresh_progress()

    pending = st.session_state.pop("pending_achievements", None)
    if pending:
        show_new_achievements(pending)

    with st.sidebar:
        user = current_user()
        st.markdown(f"### 👤 {user['username']}")
        st.caption(user["email"])
        st.divider()
        page = st.radio(
            "Navegación",
            ["🏠 Inicio", "🎯 Trivias", "📖 Álbum", "⭐ Mi 11", "🔄 Intercambio", "🏅 Logros", "🏛️ Históricos", "🌍 Selecciones"],
            label_visibility="collapsed",
        )
        st.divider()
        if st.button("Cerrar sesión", use_container_width=True):
            logout_user()
            st.rerun()
        if st.button("🔄 Reiniciar mi álbum", use_container_width=True):
            reset_user(progress_user_id(progress))
            st.session_state.show_animation = False
            st.session_state.current_trivia_id = None
            st.session_state.pop("pending_unlock_sticker_id", None)
            refresh_progress()
            st.rerun()

    render_header()

    st.session_state.nav_section = page[:2]

    routes = {
        "🏠": page_inicio,
        "🎯": page_trivia,
        "📖": page_album,
        "⭐": page_mi_equipo,
        "🔄": page_intercambio,
        "🏅": page_logros,
        "🏛️": page_historicos,
        "🌍": page_selecciones,
    }
    for prefix, handler in routes.items():
        if page.startswith(prefix):
            if prefix == "🌍":
                handler()
            else:
                handler(progress)
            break


if __name__ == "__main__":
    main()
