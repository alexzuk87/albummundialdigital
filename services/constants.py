"""Constantes compartidas del juego (sin dependencias circulares)."""

RARITY_LABELS = {
    "basica": "Básica",
    "comun": "Común",
    "rara": "Rara",
    "epica": "Épica",
    "legendaria": "Legendaria",
    "bandera": "Bandera",
}

RARITY_COLORS = {
    "basica": "#9e9e9e",
    "comun": "#4caf50",
    "rara": "#2196f3",
    "epica": "#9c27b0",
    "legendaria": "#ff9800",
}

RARITY_ORDER = ["basica", "comun", "rara", "epica", "legendaria"]

# Poder de cada categoría para la simulación de partidos.
RARITY_POWER = {
    "basica": 1,
    "comun": 2,
    "rara": 3,
    "epica": 4,
    "legendaria": 5,
    "bandera": 2,
}

MAX_TRIVIA_PER_DAY = 6
MAX_SIM_PER_DAY = 5
