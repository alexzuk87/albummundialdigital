"""Componentes visuales de figuritas: avatar, camiseta y tarjeta."""



import base64

from urllib.parse import quote



from data.player_meta import get_kit_colors

from services.flags import flag_img_html

from services.constants import RARITY_LABELS





def _hex_luminance(hex_color: str) -> float:

    h = hex_color.lstrip("#")

    if len(h) != 6:

        return 0.5

    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

    return (0.299 * r + 0.587 * g + 0.114 * b) / 255





def avatar_colors_for_team(team_id: str) -> tuple[str, str]:

    """Fondo y texto del avatar con contraste legible (p. ej. Alemania blanco)."""

    primary, secondary, _ = get_kit_colors(team_id)

    lum = _hex_luminance(primary)

    if lum > 0.72:

        return "1a1a2e", "ffffff"

    if lum > 0.55:

        return secondary.lstrip("#") if _hex_luminance(secondary) < 0.5 else "2e4057", "ffffff"

    return primary.lstrip("#"), "ffffff"





def player_avatar_url(name: str, team_id: str) -> str:

    bg, fg = avatar_colors_for_team(team_id)

    safe = quote(name)

    return (

        f"https://ui-avatars.com/api/?name={safe}&size=128"

        f"&background={bg}&color={fg}&bold=true&format=png"

    )





def _jersey_svg_markup(

    team_id: str, number: int, locked: bool, size: str

) -> str:

    uid = f"{team_id}_{number}_{size}_{'lock' if locked else 'ok'}"

    primary, secondary, num_color = get_kit_colors(team_id)

    if locked:

        primary, secondary, num_color = "#666666", "#444444", "#cccccc"

        display = "?"

    else:

        display = str(number)



    return (

        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 110">'

        f"<defs><linearGradient id='jg-{uid}' x1='0%' y1='0%' x2='85%' y2='100%'>"

        f"<stop offset='0%' stop-color='{primary}'/>"

        f"<stop offset='100%' stop-color='{secondary}'/></linearGradient>"

        f"<filter id='sh-{uid}'><feDropShadow dx='0' dy='2' stdDeviation='2' "

        f"flood-opacity='0.25'/></filter></defs>"

        f"<path filter='url(#sh-{uid})' fill='url(#jg-{uid})' stroke='rgba(0,0,0,0.18)' "

        f"stroke-width='1.2' d='M50 11 C43 11 37 15 34 21 L12 30 L18 46 L30 39 L30 98 "

        f"L70 98 L70 39 L82 46 L88 30 L66 21 C63 15 57 11 50 11 Z'/>"

        f"<path fill='none' stroke='rgba(255,255,255,0.55)' stroke-width='2.2' "

        f"stroke-linecap='round' d='M36 13 Q50 23 64 13'/>"

        f"<text x='50' y='76' text-anchor='middle' dominant-baseline='middle' "

        f"fill='{num_color}' font-family='Impact,sans-serif' font-size='"

        f"{'30' if size == 'sm' else '38'}' font-weight='700'>{display}</text></svg>"

    )





def jersey_html(team_id: str, number: int, locked: bool = False, size: str = "sm") -> str:

    """Camiseta como imagen (Streamlit no renderiza SVG inline en markdown)."""

    dims = "58" if size == "sm" else "78"

    h = int(int(dims) * 1.1)

    svg = _jersey_svg_markup(team_id, number, locked, size)

    b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")

    label = "?" if locked else str(number)

    return (

        f'<img class="jersey-svg jersey-{size}" '

        f'src="data:image/svg+xml;base64,{b64}" '

        f'width="{dims}" height="{h}" alt="Camiseta {label}">'

    )





def _rarity_bg_class(rarity: str) -> str:

    if rarity == "legendaria":

        return "rarity-bg-legendaria"

    if rarity == "epica":

        return "rarity-bg-epica"

    if rarity == "rara":

        return "rarity-bg-rara"

    return "rarity-bg-default"





def _dupe_badge_html(is_dupe: bool, dupe_count: int) -> str:

    if dupe_count and dupe_count > 0:

        return f'<span class="dupe-badge dupe-count-badge">x{dupe_count}</span>'

    if is_dupe:

        return '<span class="dupe-badge">🔄</span>'

    return ""




def bandera_card_html(

    sticker: dict, unlocked: bool, is_dupe: bool = False, dupe_count: int = 0

) -> str:

    team_id = sticker["team_id"]

    flag = flag_img_html(team_id, 80 if unlocked else 52)

    dupe = _dupe_badge_html(is_dupe, dupe_count)

    if unlocked:

        return (

            f'<div class="sticker-card sticker-bandera sticker-unlocked" '

            f'title="{sticker["name"]}">'

            f"{dupe}{flag}"

            f'<div class="sticker-bandera-label">BANDERA</div>'

            f'<div class="sticker-name">{sticker["team_name"]}</div></div>'

        )

    return (

        '<div class="sticker-card sticker-bandera sticker-locked" title="Bandera bloqueada">'

        f"{flag_img_html(team_id, 40)}"

        '<div class="sticker-name">???</div></div>'

    )





def sticker_card_html(

    sticker: dict, unlocked: bool, is_dupe: bool = False, dupe_count: int = 0

) -> str:

    if sticker.get("kind") == "bandera":

        return bandera_card_html(sticker, unlocked, is_dupe, dupe_count)



    team_id = sticker["team_id"]

    if unlocked:

        avatar = player_avatar_url(sticker["name"], team_id)

        jersey = jersey_html(team_id, sticker["shirt_number"], locked=False)

        meta = (

            f'<div class="sticker-meta">'

            f'<span class="sticker-pos">{sticker["position"]}</span>'

            f'<span class="sticker-club">{sticker["club"]}</span></div>'

        )

        rarity = (

            f'<span class="sticker-rarity rarity-{sticker["rarity"]}">'

            f'{RARITY_LABELS[sticker["rarity"]]}</span>'

        )

        dupe = _dupe_badge_html(is_dupe, dupe_count)

        flag = flag_img_html(team_id, 18)

        bg = _rarity_bg_class(sticker["rarity"])

        return (

            f'<div class="sticker-card sticker-unlocked {bg}" title="{sticker["name"]}">'

            f"{dupe}{flag}"

            f'<img class="sticker-avatar" src="{avatar}" alt="{sticker["name"]}">'

            f"{jersey}{meta}"

            f'<div class="sticker-name">{sticker["name"]}</div>{rarity}</div>'

        )



    return (

        '<div class="sticker-card sticker-locked" title="Bloqueada">'

        f"{jersey_html(team_id, 0, locked=True)}"

        '<div class="sticker-name">???</div></div>'

    )





def legend_avatar_url(name: str) -> str:
    """Avatar caricaturizado y único por jugador (estilo distinto a las figus normales)."""
    seed = quote(name)
    return (
        f"https://api.dicebear.com/9.x/avataaars/svg?seed={seed}"
        f"&radius=12&backgroundType=gradientLinear"
        f"&backgroundColor=b6862c,d4af37,8a6d1b"
    )


def legend_card_html(player: dict, unlocked: bool, threshold: int = 0) -> str:
    """Figurita de leyenda con marco dorado vintage."""
    flag_code = player.get("flag_code", "")
    flag = (
        f'<img class="legend-flag" src="https://flagcdn.com/w40/{flag_code}.png" '
        f'width="30" alt="{player.get("country", "")}">'
        if flag_code else ""
    )

    if not unlocked:
        return (
            '<div class="legend-card legend-locked" title="Leyenda bloqueada">'
            '<div class="legend-avatar-wrap"><span class="legend-lock">🔒</span></div>'
            '<div class="legend-tag">LEYENDA</div>'
            '<div class="legend-name">???</div>'
            f'<div class="legend-era">Se desbloquea al {threshold}% del álbum</div></div>'
        )

    avatar = legend_avatar_url(player["name"])
    return (
        '<div class="legend-card legend-unlocked" title="' + player["name"] + '">'
        f'<div class="legend-avatar-wrap">{flag}'
        f'<img class="legend-avatar" src="{avatar}" alt="{player["name"]}"></div>'
        '<div class="legend-tag">LEYENDA</div>'
        f'<div class="legend-name">{player["name"]}</div>'
        f'<div class="legend-era">{player.get("country", "")} · {player.get("era", "")}</div>'
        f'<div class="legend-ach">{player.get("achievement", "")}</div></div>'
    )


def reveal_card_html(sticker: dict) -> str:

    if sticker.get("kind") == "bandera":

        team_id = sticker["team_id"]

        flag = flag_img_html(team_id, 96)

        return (

            '<div class="reveal-card reveal-card-full reveal-bandera sticker-bandera">'

            f"{flag}"

            '<div class="name">Bandera oficial</div>'

            f'<div class="team">{sticker["team_name"]}</div>'

            '<span class="sticker-bandera-tag">BANDERA</span></div>'

        )



    team_id = sticker["team_id"]

    avatar = player_avatar_url(sticker["name"], team_id)

    flag = flag_img_html(team_id, 40)

    jersey = jersey_html(team_id, sticker["shirt_number"], locked=False, size="lg")

    bg = _rarity_bg_class(sticker["rarity"])

    return (

        f'<div class="reveal-card reveal-card-full reveal-rarity-{sticker["rarity"]} {bg}">'

        f"{flag}"

        f'<img class="reveal-avatar" src="{avatar}" alt="{sticker["name"]}">'

        f"{jersey}"

        f'<div class="name">{sticker["name"]}</div>'

        f'<div class="team">{sticker["team_name"]} · #{sticker["shirt_number"]}</div>'

        f'<div class="reveal-meta">{sticker["position"]} · {sticker["club"]}</div>'

        f'<span class="sticker-rarity rarity-{sticker["rarity"]}">'

        f'{RARITY_LABELS[sticker["rarity"]]}</span></div>'

    )


