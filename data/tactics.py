"""Tácticas de juego y sus interacciones.

Cada táctica modifica el ataque/defensa del equipo y forma un ciclo del estilo
piedra-papel-tijera: cada una le gana a otra (bonus) y pierde contra una tercera
(penalización). La táctica "equilibrada" es neutra (sin ventajas ni desventajas).

Ciclo de duelos (X le gana a Y):
    ofensiva → posesión → presión → defensiva → contragolpe → ofensiva
"""

from __future__ import annotations

TACTICS: dict[str, dict] = {
    "equilibrada": {
        "label": "Equilibrada", "emoji": "⚖️", "atk": 0.00, "def": 0.00,
        "desc": "Sin riesgos ni ventajas. La opción más segura.", "beats": None,
    },
    "ofensiva": {
        "label": "Ofensiva", "emoji": "⚔️", "atk": 0.28, "def": -0.16,
        "desc": "Vas al frente: más gol, pero quedás expuesto atrás.", "beats": "posesion",
    },
    "posesion": {
        "label": "Posesión", "emoji": "🎯", "atk": 0.16, "def": 0.04,
        "desc": "Tenés la pelota y manejás los tiempos del partido.", "beats": "presion",
    },
    "presion": {
        "label": "Presión alta", "emoji": "🔥", "atk": 0.14, "def": -0.04,
        "desc": "Recuperás arriba y ahogás la salida del rival.", "beats": "defensiva",
    },
    "defensiva": {
        "label": "Defensiva", "emoji": "🛡️", "atk": -0.16, "def": 0.28,
        "desc": "Te parás atrás y aguantás el resultado.", "beats": "contragolpe",
    },
    "contragolpe": {
        "label": "Contragolpe", "emoji": "⚡", "atk": 0.12, "def": 0.10,
        "desc": "Cedés la pelota y lastimás en velocidad.", "beats": "ofensiva",
    },
}

DEFAULT_TACTIC = "equilibrada"

# Ajustes de ataque cuando ganás/perdés el duelo táctico.
COUNTER_BONUS_ATK = 0.18
COUNTER_MALUS_ATK = 0.12


def get_tactic(tactic_id: str) -> dict:
    return TACTICS.get(tactic_id, TACTICS[DEFAULT_TACTIC])


def tactic_label(tactic_id: str) -> str:
    t = get_tactic(tactic_id)
    return f"{t['emoji']} {t['label']}"


def tactic_edge(user_tactic: str, opp_tactic: str) -> int:
    """+1 si tu táctica le gana a la rival, -1 si pierde, 0 si es neutra."""
    user = get_tactic(user_tactic)
    opp = get_tactic(opp_tactic)
    if user.get("beats") == opp_tactic:
        return 1
    if opp.get("beats") == user_tactic:
        return -1
    return 0


def formation_mods(formation: dict) -> tuple[float, float]:
    """Modificadores (ataque, defensa) según delanteros/defensores del esquema."""
    rows = formation.get("rows", {}) if formation else {}
    n_fwd = len(rows.get("fwd", []))
    n_def = len(rows.get("def", []))
    return (n_fwd - 3) * 0.06, (n_def - 4) * 0.06
