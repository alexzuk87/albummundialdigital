"""Equipos rivales para la simulación de partidos (fútbol 5: arquero + 4).

La dificultad se define por la categoría (rareza) de sus jugadores: cuanto más
alta la categoría, mayor el rating del equipo. El rating se usa para simular un
resultado razonable contra el equipo del usuario.
"""

from __future__ import annotations

from services.constants import RARITY_POWER

# Posiciones fijas para un equipo de 5 (1 arquero + 4 de campo).
_SIM_POSITIONS = ["Arquero", "Defensor", "Mediocampista", "Delantero", "Delantero"]

TIER_LABELS = {
    1: "Muy fácil",
    2: "Fácil",
    3: "Media",
    4: "Difícil",
    5: "Elite",
}


def _team(team_id, name, emoji, tier, roster):
    players = [
        {"name": n, "position": _SIM_POSITIONS[i], "rarity": r}
        for i, (n, r) in enumerate(roster)
    ]
    rating = sum(RARITY_POWER.get(p["rarity"], 1) for p in players)
    return {
        "id": team_id,
        "name": name,
        "emoji": emoji,
        "tier": tier,
        "tier_label": TIER_LABELS[tier],
        "stars": "⭐" * tier,
        "players": players,
        "rating": rating,
    }


_b, _c, _r, _e, _l = "basica", "comun", "rara", "epica", "legendaria"


SIM_TEAMS = [
    # ---------------- Tier 1 · Muy fácil ----------------
    _team("potrero", "Los Pibes del Potrero", "🥅", 1, [
        ("Tito Funes", _b), ("Pana Gómez", _b), ("Lalo Ruiz", _b), ("Nano Vera", _b), ("Pipa Suárez", _c),
    ]),
    _team("domingo", "Deportivo Domingo", "⚽", 1, [
        ("Beto Páez", _b), ("Coco Díaz", _b), ("Tincho Ledesma", _b), ("Fefo Ojeda", _c), ("Cacho Rivas", _c),
    ]),
    _team("esquina", "Club Social La Esquina", "🍻", 1, [
        ("Momo Sosa", _b), ("Pichi Acuña", _b), ("Lucho Bravo", _c), ("Tato Mansilla", _c), ("Goyo Paz", _c),
    ]),
    _team("amigos", "Amigos del Fútbol 5", "👟", 1, [
        ("Dani Coria", _b), ("Edu Maidana", _c), ("Fran Toledo", _c), ("Javi Robles", _c), ("Seba Cano", _c),
    ]),
    # ---------------- Tier 2 · Fácil ----------------
    _team("comarca", "Atlético Comarca", "🏟️", 2, [
        ("Marco Vidal", _b), ("Ariel Pons", _c), ("Hugo Salas", _c), ("Diego Lema", _c), ("Brian Costa", _r),
    ]),
    _team("valle", "Unión del Valle", "🌄", 2, [
        ("Iván Roldán", _c), ("Leo Cabrera", _c), ("Nico Funes", _c), ("Pablo Arce", _c), ("Tomás Vega", _r),
    ]),
    _team("norte", "Racing del Norte", "🧭", 2, [
        ("Gastón Ferreyra", _c), ("Emir Daza", _c), ("Raúl Pinto", _c), ("Ciro Bustos", _r), ("Aldo Quiroga", _r),
    ]),
    _team("ribera", "Sporting Ribera", "🌊", 2, [
        ("Kevin Ramos", _c), ("Joel Pereyra", _c), ("Mateo Lira", _r), ("Axel Duarte", _r), ("Bruno Vera", _r),
    ]),
    # ---------------- Tier 3 · Media ----------------
    _team("polar", "Estrella Polar FC", "⭐", 3, [
        ("Marcos Aguilar", _c), ("Lautaro Gil", _r), ("Ezequiel Mora", _r), ("Tobías Rey", _r), ("Franco Ibáñez", _r),
    ]),
    _team("halcones", "Halcones de Acero", "🦅", 3, [
        ("Damián Soto", _c), ("Iker Núñez", _r), ("Brian Maldonado", _r), ("Nahuel Ponce", _r), ("Lisandro Vera", _e),
    ]),
    _team("condores", "Cóndores Unidos", "🦤", 3, [
        ("Ramiro Cáceres", _r), ("Thiago Méndez", _r), ("Gael Ortiz", _r), ("Bautista Roca", _r), ("Valentín Sosa", _e),
    ]),
    _team("tiburones", "Tiburones FC", "🦈", 3, [
        ("Joaquín Real", _r), ("Maxi Luna", _r), ("Santino Bravo", _r), ("Agustín Ferro", _e), ("Ulises Mar", _e),
    ]),
    # ---------------- Tier 4 · Difícil ----------------
    _team("montana", "Real Montaña", "🏔️", 4, [
        ("Adrián Vela", _r), ("Cristian Lobo", _r), ("Emiliano Cruz", _e), ("Gonzalo Prado", _e), ("Rodrigo Sanz", _e),
    ]),
    _team("imperio", "Imperio FC", "👑", 4, [
        ("Facundo Reyes", _r), ("Ignacio Bravo", _e), ("Manuel Sosa", _e), ("Tomás Aguirre", _e), ("Nicolás Vera", _e),
    ]),
    _team("dragones", "Dragones Dorados", "🐉", 4, [
        ("Lucas Moreno", _e), ("Matías Roldán", _e), ("Joaquín Silva", _e), ("Benjamín Castro", _e), ("Felipe Ramos", _e),
    ]),
    _team("galacticos", "Galácticos del Sur", "🌌", 4, [
        ("Álvaro Ruiz", _r), ("Sergio Lema", _e), ("Pablo Navarro", _e), ("Diego Fuentes", _e), ("Marco Pereyra", _l),
    ]),
    # ---------------- Tier 5 · Elite ----------------
    _team("olimpo", "Olimpo FC", "⚡", 5, [
        ("Hernán Ríos", _e), ("Ezequiel Paz", _e), ("Maximiliano Soler", _e), ("Tomás Iglesias", _e), ("Bruno Galán", _l),
    ]),
    _team("titanes", "Titanes Eternos", "🗿", 5, [
        ("Andrés Belmonte", _e), ("Iván Solano", _e), ("Rafael Quiroz", _e), ("Gabriel Montero", _l), ("Lucio Ferrari", _l),
    ]),
    _team("leyendas", "Leyendas Doradas", "🏆", 5, [
        ("Matías Bianchi", _e), ("Esteban Ríos", _e), ("Joaquín Herrera", _l), ("Tomás Aguilar", _l), ("Maximiliano Cruz", _l),
    ]),
    _team("ensueno", "Selección de Ensueño", "💫", 5, [
        ("Bruno Estrada", _e), ("Diego Valente", _l), ("Marco Rinaldi", _l), ("Santiago Ferro", _l), ("Emiliano Costa", _l),
    ]),
]

SIM_TEAM_BY_ID = {t["id"]: t for t in SIM_TEAMS}


def teams_by_tier() -> dict[int, list[dict]]:
    grouped: dict[int, list[dict]] = {}
    for team in SIM_TEAMS:
        grouped.setdefault(team["tier"], []).append(team)
    return grouped
