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
from services.inventory import duplicates_by_category
from services.packs import PACKS, coins_balance, open_pack
from services.sticker_ui import legend_card_html, reveal_card_html, sticker_card_html
from services.database import (
    get_achievements,
    get_cup_overall,
    get_sim_by_opponent,
    get_sim_ranking,
    reset_user_progress as reset_user,
)
from data.tactics import TACTICS, get_tactic, tactic_label
from services import cup
from services.simulation import (
    play_friendly,
    sim_matches_remaining,
    squad_strength,
    user_sim_overall,
)
from services.constants import MAX_SIM_PER_DAY
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

NAV_OPTIONS = [
    "🏠 Inicio",
    "🎯 Trivias",
    "🎮 Simular",
    "🏆 Copa",
    "📖 Álbum",
    "🔁 Repetidas",
    "🔄 Intercambio",
    "🛒 Tienda",
    "🏅 Logros",
    "🏛️ Históricos",
]


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


def _go_to_section(target: str) -> None:
    """Callback de navegación: cambia la sección activa de la barra lateral."""
    st.session_state.nav_choice = target


def render_home_shortcuts() -> None:
    st.markdown("#### 🚀 Accesos rápidos")
    shortcuts = [
        ("🎯 Trivias", "Jugá y ganá figuritas"),
        ("🎮 Simular", "Tu equipo y amistosos"),
        ("🏆 Copa", "Torneo del día"),
        ("📖 Álbum", "Mirá tu colección"),
        ("🔁 Repetidas", "Tus duplicadas"),
        ("🔄 Intercambio", "Cambiá figuritas"),
        ("🛒 Tienda", "Canjeá monedas por packs"),
        ("🏅 Logros", "Tus medallas"),
        ("🏛️ Históricos", "Leyendas"),
    ]
    for row_start in range(0, len(shortcuts), 3):
        cols = st.columns(3)
        for col, (label, helptext) in zip(cols, shortcuts[row_start:row_start + 3]):
            col.button(
                label,
                key=f"home_go_{label}",
                help=helptext,
                use_container_width=True,
                on_click=_go_to_section,
                args=(label,),
            )


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

    sim = user_sim_overall(progress)
    pills = [
        f"🎯 Trivias: {trivia_status_label(progress)}",
        f"🎮 Partidos ganados: {sim['won']}",
        f"🪙 Monedas: {coins_balance(progress)}",
        f"🔄 Repetidas: {dupes}",
        f"🏅 Logros: {ach_count}",
    ]
    st.markdown("".join(f'<span class="stat-pill">{p}</span>' for p in pills), unsafe_allow_html=True)
    st.divider()

    render_home_shortcuts()
    st.divider()

    st.subheader("🏟️ Cómo jugar")
    st.markdown(f"""
    1. **Trivias** — 6 intentos por día. Si fallás, perdés ese turno.
    2. **Paquete sorpresa** — Al acertar, se abre un sobre con tu figurita.
    3. **Simular** — Armá tu **11** con formación y **táctica**, y jugá amistosos ({MAX_SIM_PER_DAY}/día) vs selecciones reales.
    4. **Copa** — Un **torneo por día** vs selecciones: avanzás mientras ganás. ¡Ganá la final y sé Campeón del Mundo!
    5. **Intercambios** — Cambiá figuritas por otra de la **misma categoría**.
    6. **Logros** — Desbloqueá medallas y ganá **monedas** 🪙 al completar metas.
    7. **Tienda** — Canjeá tus monedas por **sobres de figuritas**.
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


def _user_team(progress: dict):
    """Devuelve (team, formation_id, tactic_id, lineup_ids, completo)."""
    team = ensure_custom_team(progress)
    formation_id = team.get("formation", "4-3-3")
    tactic_id = team.get("tactic", "equilibrada")
    slots = get_formation(formation_id)["slots"]
    lineup = team.get("lineup", {})
    ids = [lineup.get(s["key"]) for s in slots]
    complete = len(ids) == 11 and all(ids)
    return team, formation_id, tactic_id, [i for i in ids if i], complete


def _mi_equipo_tab(progress: dict) -> None:
    if not progress.get("unlocked_stickers"):
        st.info("Desbloqueá figuritas en **Trivias** para armar tu equipo.")
        return

    team_data = ensure_custom_team(progress)
    formation_id = team_data.get("formation", "4-3-3")
    tactic_id = team_data.get("tactic", "equilibrada")
    saved_lineup = team_data["lineup"]
    filled = lineup_filled_count(saved_lineup, formation_id)

    if filled > 0:
        st.markdown("### Tu equipo guardado")
        st.markdown(formation_pitch_html(team_data["name"], formation_id, saved_lineup), unsafe_allow_html=True)
        t = get_tactic(tactic_id)
        st.caption(f"Jugadores: **{filled}/11** · Táctica: **{t['emoji']} {t['label']}**")
        if filled < 11:
            st.warning("Completá los **11** para poder jugar amistosos y la Copa.")

        share_text, links = get_share_content(team_data["name"], formation_id, saved_lineup)
        with st.expander("📣 Compartir en redes"):
            st.text_area("Texto para copiar", share_text, height=140, key="share_text")
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.link_button("🐦 X", links["twitter"], use_container_width=True)
            c2.link_button("📘 Facebook", links["facebook"], use_container_width=True)
            c3.link_button("💬 WhatsApp", links["whatsapp"], use_container_width=True)
            c4.link_button("✈️ Telegram", links["telegram"], use_container_width=True)
            c5.link_button("📷 Instagram", links["instagram"], use_container_width=True)
        st.divider()

    tactic_ids = list(TACTICS.keys())
    with st.form("team_form"):
        team_name = st.text_input(
            "Nombre de tu equipo",
            value=team_data.get("name", "Mi Equipo Soñado"),
            max_chars=40,
            key="team_name_input",
        )
        cfa, cfb = st.columns(2)
        picked_formation = cfa.selectbox(
            "Formación",
            list(FORMATIONS.keys()),
            index=list(FORMATIONS.keys()).index(formation_id) if formation_id in FORMATIONS else 0,
            format_func=lambda x: FORMATIONS[x]["label"],
            key="team_formation_pick",
        )
        picked_tactic = cfb.selectbox(
            "Táctica",
            tactic_ids,
            index=tactic_ids.index(tactic_id) if tactic_id in TACTICS else 0,
            format_func=tactic_label,
            key="team_tactic_pick",
        )
        st.caption(f"🧠 {get_tactic(picked_tactic)['desc']}")
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
        save = c1.form_submit_button("💾 Guardar equipo", type="primary", use_container_width=True)
        clear = c2.form_submit_button("🗑️ Vaciar", use_container_width=True)

    if clear:
        from data.formations import empty_lineup
        save_custom_team(progress, team_data["name"], picked_formation, empty_lineup(picked_formation), tactic=picked_tactic)
        st.success("Plantilla vaciada.")
        refresh_progress()
        st.rerun()
    if save:
        save_custom_team(progress, team_name, picked_formation, draft, tactic=picked_tactic)
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


def page_inventario(progress: dict) -> None:
    st.subheader("🔁 Inventario de repetidas")
    st.caption(
        "Tus figuritas repetidas, ordenadas por categoría. "
        "Usalas en la sección **Intercambio** para conseguir las que te faltan."
    )

    groups = duplicates_by_category(progress)
    total = len(progress.get("duplicates", []))

    if not groups:
        st.info(
            "Todavía no tenés figuritas repetidas. "
            "Cuando una trivia te dé una figurita que ya tenés, aparecerá acá."
        )
        return

    distintas = sum(len(items) for _, items in groups)
    pills = [
        f"🔁 Repetidas totales: {total}",
        f"🃏 Figuritas distintas: {distintas}",
        f"🗂️ Categorías: {len(groups)}",
    ]
    st.markdown(
        "".join(f'<span class="stat-pill">{p}</span>' for p in pills),
        unsafe_allow_html=True,
    )

    for category, items in groups:
        label = RARITY_LABELS.get(category, category)
        cat_total = sum(qty for _, qty in items)
        st.markdown(
            f'<div class="inventory-cat-header">'
            f'<span class="inventory-cat-title">{label}</span>'
            f'<span class="inventory-cat-meta">{cat_total} repetidas · {len(items)} distintas</span>'
            f"</div>",
            unsafe_allow_html=True,
        )
        cards = "".join(
            sticker_card_html(sticker, True, dupe_count=qty) for sticker, qty in items
        )
        st.markdown(f'<div class="sticker-grid">{cards}</div>', unsafe_allow_html=True)


def _edge_note(edge: int, user_tactic: str, opp_tactic: str) -> str:
    ut, ot = get_tactic(user_tactic), get_tactic(opp_tactic)
    if edge > 0:
        return f"💪 Ventaja táctica: tu {ut['emoji']} {ut['label']} le ganó a {ot['emoji']} {ot['label']}."
    if edge < 0:
        return f"😬 Desventaja táctica: {ot['emoji']} {ot['label']} le ganó a tu {ut['emoji']} {ut['label']}."
    return f"⚖️ Duelo táctico parejo: {ut['emoji']} {ut['label']} vs {ot['emoji']} {ot['label']}."


def _scoreboard_html(headline: str, cls: str, my_strength: int, opp: dict,
                     ug: int, og: int, sub: str = "") -> str:
    flag = flag_img_html(opp["team_id"], 22)
    return (
        f'<div class="sim-scoreboard {cls}">'
        f'<div class="sim-score-headline">{headline}</div>'
        f'<div class="sim-score-line">'
        f'<span class="sim-score-team">Tu equipo</span>'
        f'<span class="sim-score-num">{ug}</span>'
        f'<span class="sim-score-sep">-</span>'
        f'<span class="sim-score-num">{og}</span>'
        f'<span class="sim-score-team">{flag} {opp["name"]}</span>'
        f'</div>'
        f'<div class="sim-score-meta">Tu fuerza: {my_strength} · Rival: {opp["strength"]}{sub}</div>'
        f'</div>'
    )


def _rewards_block(rewards: list[dict], header: str) -> None:
    if not rewards:
        return
    st.markdown(header)
    cards = "".join(sticker_card_html(s, True) for s in rewards)
    st.markdown(f'<div class="sticker-grid">{cards}</div>', unsafe_allow_html=True)


def _opponent_lineup_expander(opp: dict) -> None:
    with st.expander(f"Ver plantel de {opp['name']}"):
        ot = get_tactic(opp["tactic"])
        st.caption(f"Táctica del rival: {ot['emoji']} {ot['label']}")
        st.markdown(formation_pitch_html(opp["name"], "4-3-3", opp["lineup"]), unsafe_allow_html=True)


def _friendly_banner(res: dict) -> None:
    opp = res["opponent"]
    outcome = res["result"]
    if outcome == "win":
        st.balloons()
        headline, cls = "¡Ganaste! 🎉", "sim-score-win"
    elif outcome == "draw":
        headline, cls = "Empate 🤝", "sim-score-draw"
    else:
        headline, cls = "Perdiste 😕", "sim-score-loss"

    st.markdown(
        _scoreboard_html(headline, cls, res["user_strength"], opp, res["user_goals"], res["opp_goals"]),
        unsafe_allow_html=True,
    )
    st.caption(_edge_note(res["edge"], res["user_tactic"], opp["tactic"]))
    n = len(res.get("rewards", []))
    _rewards_block(res.get("rewards", []), f"#### 🎁 Recompensa: {n} figurita{'s' if n != 1 else ''}")
    _opponent_lineup_expander(opp)
    st.divider()


def _amistoso_tab(progress: dict) -> None:
    last = st.session_state.pop("friendly_last", None)
    if last:
        _friendly_banner(last)

    team, formation_id, tactic_id, ids, complete = _user_team(progress)
    remaining = sim_matches_remaining(progress)
    st.caption(
        "Amistoso **11 vs 11** contra una **selección real** de nivel parecido, "
        "con tu equipo y tu táctica. Ganás **1 figurita** (**+1** si ganás)."
    )
    st.info(f"Te quedan **{remaining}** amistosos hoy (máximo {MAX_SIM_PER_DAY}). Se renuevan a medianoche.")

    if not complete:
        st.warning("Necesitás tu **11 completo** para jugar. Armalo en la pestaña **🧠 Mi equipo**.")
        return

    t = get_tactic(tactic_id)
    st.markdown(
        f"**Tu equipo:** {team['name']} · {FORMATIONS[formation_id]['label']} · "
        f"{t['emoji']} {t['label']} · fuerza **{squad_strength(ids)}**"
    )

    can_play = remaining > 0
    if not can_play:
        st.warning("¡Completaste los amistosos de hoy! Volvé mañana.")
    if st.button("⚽ Jugar amistoso", type="primary", use_container_width=True, disabled=not can_play):
        res = play_friendly(progress, ids, formation_id, tactic_id)
        if res is None:
            st.warning("No quedan amistosos disponibles hoy.")
        else:
            st.session_state.friendly_last = res
            if res["achievements"]:
                st.session_state.pending_achievements = res["achievements"]
            refresh_progress()
            st.rerun()


def _sim_ranking(progress: dict) -> None:
    overall = user_sim_overall(progress)
    st.markdown("#### 📊 Tu récord")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Jugados", overall["played"])
    c2.metric("Ganados", overall["won"])
    c3.metric("Empates", overall["drawn"])
    c4.metric("Perdidos", overall["lost"])
    win_rate = round(overall["won"] / overall["played"] * 100) if overall["played"] else 0
    c5.metric("% victorias", f"{win_rate}%")

    st.divider()
    st.markdown("#### 🏆 Ranking de jugadores (por victorias)")
    ranking = get_sim_ranking(20)
    if not ranking:
        st.info("Todavía no hay partidos jugados. ¡Sé el primero en el ranking!")
    else:
        me = current_user()
        my_name = me["username"] if me else None
        rows = []
        for i, r in enumerate(ranking, start=1):
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}")
            name = r["username"] + (" (vos)" if r["username"] == my_name else "")
            rows.append({
                "#": medal,
                "Jugador": name,
                "Ganados": r["won"],
                "Empates": r["drawn"],
                "Perdidos": r["lost"],
                "Jugados": r["played"],
            })
        st.dataframe(rows, hide_index=True, use_container_width=True)

    st.divider()
    st.markdown("#### 🆚 Tu historial por rival")
    by_opp = get_sim_by_opponent(progress_user_id(progress))
    if not by_opp:
        st.caption("Jugá partidos para ver tu historial contra cada equipo.")
    else:
        rows = [
            {
                "Rival": o["opponent_name"],
                "Jugados": o["played"],
                "Ganados": o["won"],
                "Empates": o["drawn"],
                "Perdidos": o["lost"],
            }
            for o in by_opp
        ]
        st.dataframe(rows, hide_index=True, use_container_width=True)


def page_simulacion(progress: dict) -> None:
    st.subheader("🎮 Simular")
    tab_team, tab_friendly, tab_ranking = st.tabs(["🧠 Mi equipo", "⚽ Amistoso", "🏆 Ranking"])
    with tab_team:
        _mi_equipo_tab(progress)
    with tab_friendly:
        _amistoso_tab(progress)
    with tab_ranking:
        _sim_ranking(progress)


def _cup_progress_html(state: dict) -> str:
    run = state.get("run")
    wins = run["wins"] if run else 0
    status = state.get("state")
    steps = []
    for i, label in enumerate(cup.ROUND_LABELS):
        if status == "champion" or i < wins:
            cls, icon = "cup-step-won", "✅"
        elif status == "active" and i == wins:
            cls, icon = "cup-step-now", "▶️"
        elif status == "eliminated" and i == wins:
            cls, icon = "cup-step-out", "❌"
        else:
            cls, icon = "cup-step-todo", "•"
        steps.append(f'<div class="cup-step {cls}">{icon} {label}</div>')
    cls_t = "cup-step-won" if status == "champion" else "cup-step-todo"
    trophy = f'<div class="cup-step {cls_t}">🏆 Campeón</div>'
    return f'<div class="cup-bracket">{"".join(steps)}{trophy}</div>'


def _cup_round_banner(res: dict) -> None:
    opp = res["opponent"]
    if res.get("champion"):
        st.balloons()
        headline, cls = "🏆 ¡CAMPEÓN DEL MUNDO!", "sim-score-win"
    elif res["result"] == "win":
        st.balloons()
        headline, cls = f"¡Ganaste {res['round_label']}! ✅", "sim-score-win"
    else:
        headline, cls = f"Eliminado en {res['round_label']} 😕", "sim-score-loss"

    sub = " · definido por penales 🥅" if res.get("penalties") else ""
    st.markdown(
        _scoreboard_html(headline, cls, squad_strength_safe(res), opp, res["user_goals"], res["opp_goals"], sub),
        unsafe_allow_html=True,
    )
    st.caption(_edge_note(res["edge"], res["user_tactic"], opp["tactic"]))
    n = len(res.get("rewards", []))
    if n:
        header = "#### 🏆 ¡Premio de Campeón!" if res.get("champion") else f"#### 🎁 Premio de ronda: {n} figurita{'s' if n != 1 else ''}"
        _rewards_block(res.get("rewards", []), header)
    _opponent_lineup_expander(opp)
    st.divider()


def squad_strength_safe(res: dict) -> int:
    return res.get("user_strength", 0)


def _cup_active(progress: dict, run: dict, ids: list[str], formation_id: str, tactic_id: str) -> None:
    round_index = run["round_index"]
    label = cup.round_label(round_index)

    opp_key = f"cup_opp_{run['id']}_{round_index}"
    if opp_key not in st.session_state:
        st.session_state[opp_key] = cup.make_opponent(
            ids, run, exclude_ids=set(st.session_state.get("cup_used", []))
        )
    opp = st.session_state[opp_key]
    ot = get_tactic(opp["tactic"])
    flag = flag_img_html(opp["team_id"], 26)

    st.markdown(f"### {label}")
    st.markdown(
        f'<div class="cup-vs">{flag} <strong>{opp["name"]}</strong> · fuerza {opp["strength"]} · '
        f'{ot["emoji"]} {ot["label"]}</div>',
        unsafe_allow_html=True,
    )
    _opponent_lineup_expander(opp)

    if st.button(f"⚔️ Jugar {label}", type="primary", use_container_width=True):
        res = cup.play_round(progress, run, ids, formation_id, tactic_id, opp)
        if res is None:
            st.warning("Esta Copa ya no está activa.")
        else:
            res["user_strength"] = squad_strength(ids)
            res["user_tactic"] = tactic_id
            used = st.session_state.get("cup_used", [])
            used.append(opp["id"])
            st.session_state.cup_used = used
            st.session_state.pop(opp_key, None)
            st.session_state.cup_last = res
            if res["achievements"]:
                st.session_state.pending_achievements = res["achievements"]
            refresh_progress()
            st.rerun()


def page_copa(progress: dict) -> None:
    st.subheader("🏆 Copa del Mundo")
    st.caption(
        "Un **torneo de eliminación por día** contra selecciones reales, cada vez más fuertes. "
        "Avanzás mientras ganás; si perdés, quedás afuera hasta mañana. En la Copa **no hay empate**: "
        "si termina igualado, se define por **penales**."
    )

    team, formation_id, tactic_id, ids, complete = _user_team(progress)
    if not complete:
        st.warning("Necesitás tu **11 completo** para jugar la Copa. Armalo en **🎮 Simular › 🧠 Mi equipo**.")
        return

    t = get_tactic(tactic_id)
    st.markdown(
        f"**Tu equipo:** {team['name']} · {FORMATIONS[formation_id]['label']} · "
        f"{t['emoji']} {t['label']} · fuerza **{squad_strength(ids)}**"
    )
    overall = get_cup_overall(progress_user_id(progress))
    if overall["runs"]:
        st.caption(f"🏆 Copas ganadas: **{overall['champion']}** · finales: **{overall['finals']}** · torneos jugados: **{overall['runs']}**")

    last = st.session_state.pop("cup_last", None)
    if last:
        _cup_round_banner(last)

    state = cup.cup_state(progress)
    st.markdown(_cup_progress_html(state), unsafe_allow_html=True)
    s = state["state"]

    if s == "idle":
        st.info("¡La Copa de hoy te espera! Ganá 4 rondas seguidas para ser Campeón del Mundo.")
        if st.button("🎫 Iniciar Copa", type="primary", use_container_width=True):
            cup.start_cup(progress)
            st.session_state.cup_used = []
            st.rerun()
    elif s == "active":
        _cup_active(progress, state["run"], ids, formation_id, tactic_id)
    elif s == "champion":
        st.success("🏆 ¡Sos **Campeón del Mundo**! Volvé mañana para una nueva Copa.")
    elif s == "eliminated":
        st.info("Quedaste eliminado en esta Copa. 🌙 Volvé mañana para intentarlo de nuevo.")


# Usuario de Cafecito (cambialo por el tuyo en https://cafecito.app).
CAFECITO_USER = "albummundialdigital"


def _pack_odds_text(weights: dict[str, int]) -> str:
    total = sum(weights.values()) or 1
    parts = []
    for cat in ("legendaria", "epica", "rara"):
        if weights.get(cat):
            parts.append(f"{RARITY_LABELS[cat]} {round(weights[cat] / total * 100)}%")
    return " · ".join(parts)


def _pack_reveal(result: dict) -> None:
    pack = result["pack"]
    rewards = result["rewards"]
    n = len(rewards)
    st.markdown(
        f'<div class="sim-scoreboard sim-score-win">'
        f'<div class="sim-score-headline">¡Abriste el {pack["emoji"]} {pack["name"]}!</div>'
        f'<div class="sim-score-meta">Conseguiste {n} figurita{"s" if n != 1 else ""}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )
    cards = "".join(sticker_card_html(s, True) for s in rewards)
    st.markdown(f'<div class="sticker-grid">{cards}</div>', unsafe_allow_html=True)
    st.divider()


def _tienda_packs(progress: dict) -> None:
    last = st.session_state.pop("pack_last_result", None)
    if last:
        _pack_reveal(last)

    balance = coins_balance(progress)
    st.markdown(
        f'<div class="coin-balance">🪙 Tenés <strong>{balance}</strong> monedas</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Ganás monedas desbloqueando **logros**. Canjealas acá por sobres y sumá "
        "figuritas a tu álbum. Los sobres priorizan las figuritas que te faltan."
    )

    cols = st.columns(len(PACKS))
    for col, pack in zip(cols, PACKS):
        with col:
            st.markdown(
                f'<div class="pack-card pack-{pack["id"]}">'
                f'<div class="pack-emoji">{pack["emoji"]}</div>'
                f'<div class="pack-name">{pack["name"]}</div>'
                f'<div class="pack-cost">{pack["cost"]} 🪙</div>'
                f'<div class="pack-desc">{pack["desc"]}</div>'
                f'<div class="pack-odds">{_pack_odds_text(pack["weights"])}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )
            afford = balance >= pack["cost"]
            if st.button(
                f"Abrir por {pack['cost']} 🪙",
                key=f"open_pack_{pack['id']}",
                type="primary",
                use_container_width=True,
                disabled=not afford,
            ):
                res = open_pack(progress, pack["id"])
                if not res["ok"]:
                    st.warning("No te alcanzan las monedas para este sobre.")
                else:
                    st.session_state.pack_last_result = res
                    if res["achievements"]:
                        st.session_state.pending_achievements = res["achievements"]
                    st.rerun()
            if not afford:
                st.caption(f"Te faltan {pack['cost'] - balance} 🪙")


def _tienda_apoyar() -> None:
    st.markdown("#### 💛 Apoyá el proyecto")
    st.markdown(
        "El **Álbum Mundial Digital** es gratis y sin publicidad. "
        "Si te gusta y querés bancar el proyecto, podés invitarme un cafecito. "
        "¡Mil gracias por el aguante! 🙌"
    )
    st.markdown(
        f'<a href="https://cafecito.app/{CAFECITO_USER}" target="_blank" rel="noopener noreferrer">'
        f'<img src="https://cdn.cafecito.app/imgs/buttons/button_3.png" '
        f'alt="Invitame un café en cafecito.app" style="max-width:100%;height:auto;border:0;">'
        f"</a>",
        unsafe_allow_html=True,
    )
    st.caption(
        "Las donaciones son **voluntarias** y no otorgan ventajas dentro del juego. "
        "Las monedas se ganan jugando y desbloqueando logros."
    )


def page_tienda(progress: dict) -> None:
    st.subheader("🛒 Tienda")
    tab_packs, tab_apoyar = st.tabs(["🎁 Packs", "💛 Apoyar"])
    with tab_packs:
        _tienda_packs(progress)
    with tab_apoyar:
        _tienda_apoyar()


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

    st.markdown(
        f'<div class="coin-balance">🪙 Monedas disponibles: <strong>{coins_balance(progress)}</strong></div>',
        unsafe_allow_html=True,
    )
    st.caption("Cada logro te da monedas para canjear por sobres en la **Tienda** 🛒.")

    for ach in summary:
        css = "" if ach["unlocked"] else "historical-locked"
        coins = ach.get("coins", 0)
        st.markdown(
            f'<div class="historical-card {css}">'
            f'<strong>{ach["icon"]} {ach["title"]}</strong> '
            f'{"✅" if ach["unlocked"] else "🔒"} '
            f'<span class="ach-coins">+{coins} 🪙</span><br>'
            f'<small>{ach["desc"]}</small></div>',
            unsafe_allow_html=True,
        )


def page_historicos(progress: dict) -> None:
    st.subheader("🏛️ Álbum de leyendas")
    st.caption(
        "Figuritas especiales de las **leyendas del fútbol**, con un estilo distinto. "
        "Se desbloquean a medida que completás tu álbum."
    )
    pct = progress_stats(progress)["percent"]
    unlocked = [
        p for p in HISTORICAL_PLAYERS
        if pct >= HISTORICAL_UNLOCK_THRESHOLDS.get(p["id"], 100)
    ]
    total = len(HISTORICAL_PLAYERS)
    st.progress(
        min(1.0, len(unlocked) / total) if total else 0.0,
        text=f"{len(unlocked)} / {total} leyendas · álbum al {pct}%",
    )

    cards = "".join(
        legend_card_html(
            player,
            pct >= HISTORICAL_UNLOCK_THRESHOLDS.get(player["id"], 100),
            HISTORICAL_UNLOCK_THRESHOLDS.get(player["id"], 100),
        )
        for player in HISTORICAL_PLAYERS
    )
    st.markdown(f'<div class="legend-grid">{cards}</div>', unsafe_allow_html=True)


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
            NAV_OPTIONS,
            label_visibility="collapsed",
            key="nav_choice",
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
        "🎮": page_simulacion,
        "🏆": page_copa,
        "📖": page_album,
        "🔁": page_inventario,
        "🔄": page_intercambio,
        "🛒": page_tienda,
        "🏅": page_logros,
        "🏛️": page_historicos,
    }
    for prefix, handler in routes.items():
        if page.startswith(prefix):
            handler(progress)
            break


if __name__ == "__main__":
    main()
