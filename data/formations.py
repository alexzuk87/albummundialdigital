"""Esquemas tácticos disponibles para el 11 ideal."""

FORMATIONS: dict[str, dict] = {
    "4-3-3": {
        "label": "4-3-3",
        "rows": {
            "gk": ["gk"],
            "def": ["lb", "cb1", "cb2", "rb"],
            "mid": ["cm1", "cm2", "cm3"],
            "fwd": ["lw", "st", "rw"],
        },
        "slots": [
            {"key": "gk", "label": "Arquero", "position": "Arquero", "line": "gk"},
            {"key": "rb", "label": "Lateral derecho", "position": "Defensor", "line": "def"},
            {"key": "cb1", "label": "Defensor central", "position": "Defensor", "line": "def"},
            {"key": "cb2", "label": "Defensor central", "position": "Defensor", "line": "def"},
            {"key": "lb", "label": "Lateral izquierdo", "position": "Defensor", "line": "def"},
            {"key": "cm1", "label": "Mediocampista", "position": "Mediocampista", "line": "mid"},
            {"key": "cm2", "label": "Mediocampista", "position": "Mediocampista", "line": "mid"},
            {"key": "cm3", "label": "Mediocampista", "position": "Mediocampista", "line": "mid"},
            {"key": "rw", "label": "Extremo derecho", "position": "Delantero", "line": "fwd"},
            {"key": "st", "label": "Delantero centro", "position": "Delantero", "line": "fwd"},
            {"key": "lw", "label": "Extremo izquierdo", "position": "Delantero", "line": "fwd"},
        ],
    },
    "4-4-2": {
        "label": "4-4-2",
        "rows": {
            "gk": ["gk"],
            "def": ["lb", "cb1", "cb2", "rb"],
            "mid": ["lm", "cm1", "cm2", "rm"],
            "fwd": ["st1", "st2"],
        },
        "slots": [
            {"key": "gk", "label": "Arquero", "position": "Arquero", "line": "gk"},
            {"key": "rb", "label": "Lateral derecho", "position": "Defensor", "line": "def"},
            {"key": "cb1", "label": "Defensor central", "position": "Defensor", "line": "def"},
            {"key": "cb2", "label": "Defensor central", "position": "Defensor", "line": "def"},
            {"key": "lb", "label": "Lateral izquierdo", "position": "Defensor", "line": "def"},
            {"key": "rm", "label": "Volante derecho", "position": "Mediocampista", "line": "mid"},
            {"key": "cm1", "label": "Mediocampista", "position": "Mediocampista", "line": "mid"},
            {"key": "cm2", "label": "Mediocampista", "position": "Mediocampista", "line": "mid"},
            {"key": "lm", "label": "Volante izquierdo", "position": "Mediocampista", "line": "mid"},
            {"key": "st1", "label": "Delantero", "position": "Delantero", "line": "fwd"},
            {"key": "st2", "label": "Delantero", "position": "Delantero", "line": "fwd"},
        ],
    },
    "3-5-2": {
        "label": "3-5-2",
        "rows": {
            "gk": ["gk"],
            "def": ["cb1", "cb2", "cb3"],
            "mid": ["lwb", "cm1", "cm2", "cm3", "rwb"],
            "fwd": ["st1", "st2"],
        },
        "slots": [
            {"key": "gk", "label": "Arquero", "position": "Arquero", "line": "gk"},
            {"key": "cb1", "label": "Defensor", "position": "Defensor", "line": "def"},
            {"key": "cb2", "label": "Defensor central", "position": "Defensor", "line": "def"},
            {"key": "cb3", "label": "Defensor", "position": "Defensor", "line": "def"},
            {"key": "lwb", "label": "Carrilero izquierdo", "position": "Defensor", "line": "mid"},
            {"key": "cm1", "label": "Mediocampista", "position": "Mediocampista", "line": "mid"},
            {"key": "cm2", "label": "Mediocampista", "position": "Mediocampista", "line": "mid"},
            {"key": "cm3", "label": "Mediocampista", "position": "Mediocampista", "line": "mid"},
            {"key": "rwb", "label": "Carrilero derecho", "position": "Defensor", "line": "mid"},
            {"key": "st1", "label": "Delantero", "position": "Delantero", "line": "fwd"},
            {"key": "st2", "label": "Delantero", "position": "Delantero", "line": "fwd"},
        ],
    },
    "4-2-3-1": {
        "label": "4-2-3-1",
        "rows": {
            "gk": ["gk"],
            "def": ["lb", "cb1", "cb2", "rb"],
            "mid": ["dm1", "dm2", "am1", "am2", "am3"],
            "fwd": ["st"],
        },
        "slots": [
            {"key": "gk", "label": "Arquero", "position": "Arquero", "line": "gk"},
            {"key": "rb", "label": "Lateral derecho", "position": "Defensor", "line": "def"},
            {"key": "cb1", "label": "Defensor central", "position": "Defensor", "line": "def"},
            {"key": "cb2", "label": "Defensor central", "position": "Defensor", "line": "def"},
            {"key": "lb", "label": "Lateral izquierdo", "position": "Defensor", "line": "def"},
            {"key": "dm1", "label": "Mediocampista defensivo", "position": "Mediocampista", "line": "mid"},
            {"key": "dm2", "label": "Mediocampista defensivo", "position": "Mediocampista", "line": "mid"},
            {"key": "am1", "label": "Mediapunta izquierda", "position": "Mediocampista", "line": "mid"},
            {"key": "am2", "label": "Mediapunta", "position": "Mediocampista", "line": "mid"},
            {"key": "am3", "label": "Mediapunta derecha", "position": "Mediocampista", "line": "mid"},
            {"key": "st", "label": "Delantero centro", "position": "Delantero", "line": "fwd"},
        ],
    },
    "5-3-2": {
        "label": "5-3-2",
        "rows": {
            "gk": ["gk"],
            "def": ["lb", "cb1", "cb2", "cb3", "rb"],
            "mid": ["cm1", "cm2", "cm3"],
            "fwd": ["st1", "st2"],
        },
        "slots": [
            {"key": "gk", "label": "Arquero", "position": "Arquero", "line": "gk"},
            {"key": "lb", "label": "Lateral izquierdo", "position": "Defensor", "line": "def"},
            {"key": "cb1", "label": "Defensor central", "position": "Defensor", "line": "def"},
            {"key": "cb2", "label": "Líbero / central", "position": "Defensor", "line": "def"},
            {"key": "cb3", "label": "Defensor central", "position": "Defensor", "line": "def"},
            {"key": "rb", "label": "Lateral derecho", "position": "Defensor", "line": "def"},
            {"key": "cm1", "label": "Mediocampista", "position": "Mediocampista", "line": "mid"},
            {"key": "cm2", "label": "Mediocampista", "position": "Mediocampista", "line": "mid"},
            {"key": "cm3", "label": "Mediocampista", "position": "Mediocampista", "line": "mid"},
            {"key": "st1", "label": "Delantero", "position": "Delantero", "line": "fwd"},
            {"key": "st2", "label": "Delantero", "position": "Delantero", "line": "fwd"},
        ],
    },
    "3-4-3": {
        "label": "3-4-3",
        "rows": {
            "gk": ["gk"],
            "def": ["cb1", "cb2", "cb3"],
            "mid": ["lm", "cm1", "cm2", "rm"],
            "fwd": ["lw", "st", "rw"],
        },
        "slots": [
            {"key": "gk", "label": "Arquero", "position": "Arquero", "line": "gk"},
            {"key": "cb1", "label": "Defensor", "position": "Defensor", "line": "def"},
            {"key": "cb2", "label": "Defensor central", "position": "Defensor", "line": "def"},
            {"key": "cb3", "label": "Defensor", "position": "Defensor", "line": "def"},
            {"key": "rm", "label": "Volante derecho", "position": "Mediocampista", "line": "mid"},
            {"key": "cm1", "label": "Mediocampista", "position": "Mediocampista", "line": "mid"},
            {"key": "cm2", "label": "Mediocampista", "position": "Mediocampista", "line": "mid"},
            {"key": "lm", "label": "Volante izquierdo", "position": "Mediocampista", "line": "mid"},
            {"key": "rw", "label": "Extremo derecho", "position": "Delantero", "line": "fwd"},
            {"key": "st", "label": "Delantero centro", "position": "Delantero", "line": "fwd"},
            {"key": "lw", "label": "Extremo izquierdo", "position": "Delantero", "line": "fwd"},
        ],
    },
}


def get_formation(formation_id: str) -> dict:
    return FORMATIONS.get(formation_id, FORMATIONS["4-3-3"])


def empty_lineup(formation_id: str) -> dict:
    return {s["key"]: None for s in get_formation(formation_id)["slots"]}
