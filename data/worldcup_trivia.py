"""Preguntas de trivia sobre historia del Mundial (no solo jugadores del álbum)."""

from __future__ import annotations

import random

# Campeones: (año, campeón, subcampeón, sede principal)
WORLD_CUP_FINALS = [
    (1930, "Uruguay", "Argentina", "Uruguay"),
    (1934, "Italia", "Checoslovaquia", "Italia"),
    (1938, "Italia", "Hungría", "Francia"),
    (1950, "Uruguay", "Brasil", "Brasil"),
    (1954, "Alemania", "Hungría", "Suiza"),
    (1958, "Brasil", "Suecia", "Suecia"),
    (1962, "Brasil", "Checoslovaquia", "Chile"),
    (1966, "Inglaterra", "Alemania", "Inglaterra"),
    (1970, "Brasil", "Italia", "México"),
    (1974, "Alemania", "Países Bajos", "Alemania"),
    (1978, "Argentina", "Países Bajos", "Argentina"),
    (1982, "Italia", "Alemania", "España"),
    (1986, "Argentina", "Alemania", "México"),
    (1990, "Alemania", "Argentina", "Italia"),
    (1994, "Brasil", "Italia", "Estados Unidos"),
    (1998, "Francia", "Brasil", "Francia"),
    (2002, "Brasil", "Alemania", "Corea del Sur y Japón"),
    (2006, "Alemania", "Francia", "Alemania"),
    (2010, "España", "Países Bajos", "Sudáfrica"),
    (2014, "Alemania", "Argentina", "Brasil"),
    (2018, "Francia", "Croacia", "Rusia"),
    (2022, "Argentina", "Francia", "Catar"),
]

# Mascotas oficiales
MASCOTS = [
    (1966, "World Cup Willie", "Inglaterra"),
    (1970, "Juanito", "México"),
    (1974, "Tip y Tap", "Alemania"),
    (1978, "Gauchito Mundialito", "Argentina"),
    (1982, "Naranjito", "España"),
    (1986, "Pique", "México"),
    (1990, "Ciao", "Italia"),
    (1994, "Striker", "Estados Unidos"),
    (1998, "Footix", "Francia"),
    (2002, "Ato, Kaz y Nik", "Corea/Japón"),
    (2006, "Goleo VI", "Alemania"),
    (2010, "Zakumi", "Sudáfrica"),
    (2014, "Fuleco", "Brasil"),
    (2018, "Zabivaka", "Rusia"),
    (2022, "La'eeb", "Catar"),
    (2026, "Maple", "Canadá"),
]

# Goleadores del torneo (Mundial 1930-2022, selección)
TOP_SCORERS = [
    (1930, "Guillermo Stábile", "Argentina", 8),
    (1958, "Just Fontaine", "Francia", 13),
    (1970, "Gerd Müller", "Alemania", 10),
    (1986, "Gary Lineker", "Inglaterra", 6),
    (1990, "Salvatore Schillaci", "Italia", 6),
    (1994, "Oleg Salenko / Hristo Stoichkov", "varios", 6),
    (1998, "Davor Šuker", "Croacia", 6),
    (2002, "Ronaldo", "Brasil", 8),
    (2006, "Miroslav Klose", "Alemania", 5),
    (2010, "Diego Forlán / Thomas Müller / Wesley Sneijder / David Villa", "varios", 5),
    (2014, "James Rodríguez", "Colombia", 6),
    (2018, "Harry Kane", "Inglaterra", 6),
    (2022, "Kylian Mbappé", "Francia", 8),
]

WC2026_HOST_CITIES = [
    "Ciudad de México", "Guadalajara", "Monterrey", "Los Ágeles", "San Francisco",
    "Dallas", "Houston", "Kansas City", "Miami", "Atlanta", "Boston", "Nueva York/Nueva Jersey",
    "Filadelfia", "Seattle", "Toronto", "Vancouver",
]

WC2026_FACTS = [
    ("¿Cuántos países sede tendrá el Mundial 2026?", "3", ["2", "4", "5"]),
    ("¿Qué países organizan el Mundial 2026?", "Estados Unidos, México y Canadá", [
        "Brasil, Argentina y Chile", "España, Portugal e Italia", "Qatar, EAU y Arabia Saudita",
    ]),
    ("¿Cuántas selecciones participan en el Mundial 2026?", "48", ["32", "40", "36"]),
    ("¿Cuántos partidos se jugarán aproximadamente en el Mundial 2026?", "104", ["64", "80", "96"]),
    ("¿En qué estadio de México se jugará la final del Mundial 2026?", "Estadio Azteca (Ciudad de México)", [
        "Estadio Akron", "Estadio BBVA", "Estadio Olímpico de Montreal",
    ]),
    ("La mascota oficial del Mundial 2026 de Canadá se llama…", "Maple", ["Zabivaka", "Fuleco", "La'eeb"]),
    ("El Mundial 2026 será el primero con este formato de equipos desde…", "1998 (32 equipos)", [
        "1978 (16 equipos)", "1954 (16 equipos)", "1930 (13 equipos)",
    ]),
    ("¿Qué ciudad canadiense es sede del Mundial 2026?", "Toronto", ["Montreal", "Ottawa", "Quebec"]),
    ("¿Qué ciudad estadounidense del oeste es sede del Mundial 2026?", "Seattle", ["Chicago", "Detroit", "Cleveland"]),
]

RECORDS = [
    ("¿Quién es el máximo goleador histórico en Mundiales?", "Miroslav Klose", [
        "Ronaldo Nazário", "Pelé", "Just Fontaine",
    ]),
    ("¿Cuántos goles marcó Miroslav Klose en Mundiales?", "16", ["15", "14", "13"]),
    ("¿Qué selección tiene más títulos mundiales?", "Brasil", ["Alemania", "Italia", "Argentina"]),
    ("¿Cuántas Copas del Mundo ganó Brasil?", "5", ["4", "6", "3"]),
    ("¿Qué país ganó el primer Mundial en 1930?", "Uruguay", ["Brasil", "Argentina", "Italia"]),
    ("¿En qué Mundial Maradona levantó la Copa?", "México 1986", ["España 1982", "Italia 1990", "Argentina 1978"]),
    ("¿Qué selección ganó el Mundial 2010 en Sudáfrica?", "España", ["Países Bajos", "Alemania", "Brasil"]),
    ("¿Qué selección ganó el Mundial 2022 en Catar?", "Argentina", ["Francia", "Croacia", "Brasil"]),
    ("¿Qué arquero atajó dos penales en la final del 2022?", "Emiliano Martínez", [
        "Hugo Lloris", "Dominik Livaković", "Thibaut Courtois",
    ]),
    ("¿Qué jugador marcó 3 goles en una final de Mundial?", "Kylian Mbappé (2022)", [
        "Pelé (1970)", "Zinedine Zidane (1998)", "Mario Kempes (1978)",
    ]),
    ("¿Qué país fue sede del Mundial conocido por la 'Mano de Dios'?", "México", ["Argentina", "España", "Italia"]),
    ("¿Cuál fue la final con más goles en los 90 minutos (6)?", "Francia 3-3 Brasil (1958)", [
        "Alemania 1-0 Argentina (2014)", "Italia 1-1 Francia (2006)", "España 1-0 Países Bajos (2010)",
    ]),
    ("¿Qué selección ganó el Mundial jugado en su propio país en 1966?", "Inglaterra", [
        "Alemania", "Brasil", "Italia",
    ]),
    ("¿En qué Mundial se usó por primera vez la tarjeta roja?", "México 1970", [
        "Inglaterra 1966", "España 1982", "Alemania 1974",
    ]),
    ("¿Qué país africano llegó más lejos en un Mundial (cuartos en 1990)?", "Camerún", [
        "Senegal", "Ghana", "Marruecos",
    ]),
    ("¿Qué país organizó el Mundial 2014 donde Alemania ganó 7-1 a Brasil?", "Brasil", [
        "Sudáfrica", "Rusia", "Qatar",
    ]),
    ("El 'Gol del Siglo' de Maradona fue contra…", "Inglaterra", ["Alemania", "Bélgica", "Brasil"]),
    ("¿Qué país ganó el Mundial 2002 en Asia?", "Brasil", ["Alemania", "Corea del Sur", "Japón"]),
    ("¿Cuántas veces ganó Alemania el Mundial?", "4", ["3", "5", "2"]),
    ("¿Cuántas veces ganó Italia el Mundial?", "4", ["3", "5", "2"]),
]


def _pick_wrong(answer: str, pool: list[str], count: int, seed: str) -> list[str]:
    candidates = [x for x in pool if x != answer]
    rng = random.Random(seed)
    rng.shuffle(candidates)
    return candidates[:count]


def _options(answer: str, wrong: list[str]) -> list[str]:
    wrong = [w for w in wrong if w != answer]
    seen = {answer}
    unique_wrong: list[str] = []
    for w in wrong:
        if w not in seen:
            unique_wrong.append(w)
            seen.add(w)
    while len(unique_wrong) < 3:
        filler = str(1930 + (len(unique_wrong) + len(answer)) * 4)
        if filler != answer and filler not in seen:
            unique_wrong.append(filler)
            seen.add(filler)
    opts = [answer] + unique_wrong[:3]
    rng = random.Random(answer + "|".join(unique_wrong))
    rng.shuffle(opts)
    return opts


def _first_world_cup_win() -> dict[str, int]:
    first: dict[str, int] = {}
    for year, champ, _, _ in WORLD_CUP_FINALS:
        if champ not in first:
            first[champ] = year
    return first


FIRST_WORLD_CUP_WIN = _first_world_cup_win()


def _q(question: str, answer: str, wrong: list[str], qid: str) -> dict:
    return {
        "id": qid,
        "question": question,
        "options": _options(answer, wrong),
        "answer": answer,
    }


def build_worldcup_trivia(count: int) -> list[dict]:
    """Genera preguntas variadas sobre Mundiales (hasta `count`)."""
    questions: list[dict] = []
    n = 0
    years = [y for y, _, _, _ in WORLD_CUP_FINALS]
    champions = [c for _, c, _, _ in WORLD_CUP_FINALS]
    runners = [r for _, _, r, _ in WORLD_CUP_FINALS]
    hosts = [h for _, _, _, h in WORLD_CUP_FINALS]

    def add(q: str, a: str, wrong: list[str]) -> None:
        nonlocal n
        if len(questions) >= count:
            return
        n += 1
        questions.append(_q(q, a, wrong, f"w{n:04d}"))

    for year, champ, runner, host in WORLD_CUP_FINALS:
        add(
            f"¿Quién ganó el Mundial de {year}?",
            champ,
            _pick_wrong(champ, champions, 3, f"win-{year}"),
        )
        add(
            f"¿Quién fue subcampeón en el Mundial de {year}?",
            runner,
            _pick_wrong(runner, runners, 3, f"run-{year}"),
        )
        add(
            f"¿Dónde se jugó principalmente el Mundial de {year}?",
            host,
            _pick_wrong(host, hosts, 3, f"host-{year}"),
        )
        if len(questions) >= count:
            break

    for year, name, country in MASCOTS:
        add(
            f"¿Cómo se llamaba la mascota del Mundial de {year}?",
            name,
            _pick_wrong(name, [m[1] for m in MASCOTS], 3, f"masc-{year}"),
        )
        if len(questions) >= count:
            break

    for year, scorer, country, goals in TOP_SCORERS:
        add(
            f"¿Quién fue uno de los goleadores del Mundial de {year}?",
            scorer.split(" / ")[0],
            _pick_wrong(scorer.split(" / ")[0], [s[1].split(" / ")[0] for s in TOP_SCORERS], 3, f"sc-{year}"),
        )
        add(
            f"¿Cuántos goles marcó el goleador del Mundial {year} (referencia: {scorer})?",
            str(goals),
            _pick_wrong(str(goals), ["4", "5", "7", "8", "10", "13"], 3, f"sg-{year}"),
        )
        if len(questions) >= count:
            break

    for q, a, wrong in WC2026_FACTS:
        add(q, a, wrong)
        if len(questions) >= count:
            break

    for city in WC2026_HOST_CITIES:
        add(
            f"¿{city} es ciudad sede del Mundial 2026?",
            "Sí",
            ["No", "Solo en 2030", "Solo amistosos FIFA"],
        )
        if len(questions) >= count:
            break

    for q, a, wrong in RECORDS:
        add(q, a, wrong)
        if len(questions) >= count:
            break

    year_strs = [str(y) for y in years]
    for team, first_year in sorted(FIRST_WORLD_CUP_WIN.items()):
        add(
            f"¿En qué año ganó {team} su primer título mundial?",
            str(first_year),
            _pick_wrong(str(first_year), year_strs, 3, f"first-{team}"),
        )
        if len(questions) >= count:
            break

    templates = [
        ("¿Qué selección levantó la Copa en {year}?", "{champ}", "champs"),
        ("El Mundial de {year} se disputó en…", "{host}", "hosts"),
    ]
    ti = 0
    while len(questions) < count:
        year, champ, runner, host = WORLD_CUP_FINALS[ti % len(WORLD_CUP_FINALS)]
        tpl = templates[ti % len(templates)]
        if tpl[2] == "champs":
            wrong = _pick_wrong(champ, champions, 3, f"fill-c-{ti}")
            add(tpl[0].format(year=year), champ, wrong)
        else:
            wrong = _pick_wrong(host, hosts, 3, f"fill-h-{ti}")
            add(tpl[0].format(year=year), host, wrong)
        ti += 1

    result = questions[:count]
    for q in result:
        if q["answer"] not in q["options"]:
            raise ValueError(f"Trivia inválida {q['id']}: respuesta fuera de opciones — {q}")
    return result
