"""Distribución global de rarezas del álbum (no usa Transfermarkt en vivo).

Las categorías se asignan por «nivel de estrella» curado (fama, club top, rol en
la selección), con cupos fijos para más exclusividad arriba:
  5 % legendaria · 10 % épica · 20 % rara · 25 % común · 30 % básica
(pesos 5:10:20:25:30 sobre 528 figuritas).
"""

from __future__ import annotations

RARITY_ORDER_ASSIGN = ["legendaria", "epica", "rara", "comun", "basica"]
RARITY_WEIGHTS_PCT = {
    "legendaria": 5,
    "epica": 10,
    "rara": 20,
    "comun": 25,
    "basica": 30,
}

# Puntuación manual aproximada (mercado / fama / rendimiento internacional)
STAR_SCORES: dict[str, int] = {
    "Lionel Messi": 100, "Cristiano Ronaldo": 99, "Kylian Mbappé": 98, "Erling Haaland": 97,
    "Neymar": 96, "Kevin De Bruyne": 95, "Mohamed Salah": 94, "Harry Kane": 93,
    "Vinícius Júnior": 92, "Jude Bellingham": 92, "Rodri": 91, "Jamal Musiala": 91,
    "Florian Wirtz": 90, "Lautaro Martínez": 89, "Virgil van Dijk": 89, "Alisson Becker": 88,
    "Manuel Neuer": 88, "Son Heung-min": 87, "Luka Modrić": 87, "Frenkie de Jong": 86,
    "Bruno Fernandes": 86, "Bernardo Silva": 85, "Pedri": 85, "Gavi": 84, "Lamine Yamal": 84,
    "Federico Valverde": 84, "Antoine Griezmann": 83, "Harry Maguire": 70, "Phil Foden": 88,
    "Bukayo Saka": 85, "Declan Rice": 84, "Christian Pulisic": 82, "Alphonso Davies": 83,
    "Jonathan David": 80, "Edson Álvarez": 78, "Hirving Lozano": 77, "Raúl Jiménez": 76,
    "Kim Min-jae": 86, "Lee Kang-in": 82, "Patrik Schick": 79, "Tomáš Souček": 78,
    "Achraf Hakimi": 85, "Youssef En-Nesyri": 78, "Hakim Ziyech": 77, "Andrew Robertson": 82,
    "Scott McTominay": 80, "Miguel Almirón": 79, "Julio Enciso": 78, "Gustavo Gómez": 80,
    "Moisés Caicedo": 84, "Enner Valencia": 79, "Piero Hincapié": 81, "Kendry Páez": 80,
    "Memphis Depay": 81, "Cody Gakpo": 82, "Kaoru Mitoma": 83, "Takefusa Kubo": 82,
    "Alexander Isak": 84, "Viktor Gyökeres": 83, "Romelu Lukaku": 84, "Jérémy Doku": 82,
    "Omar Marmoush": 81, "Rodrygo": 86, "Marquinhos": 87, "Casemiro": 84, "Bruno Guimarães": 83,
    "Richarlison": 78, "Danilo": 76, "Granit Xhaka": 80, "Xherdan Shaqiri": 77, "Yann Sommer": 82,
    "Edin Džeko": 78, "Miralem Pjanić": 77, "Akram Afif": 79, "Hakan Çalhanoğlu": 83,
    "Arda Güler": 82, "Kenan Yıldız": 81, "Emiliano Martínez": 87, "Cristian Romero": 83,
    "Enzo Fernández": 85, "Alexis Mac Allister": 84, "Ángel Di María": 86, "Julián Álvarez": 88,
    "Luis Suárez": 85, "Darwin Núñez": 82, "Darwin Núñez": 82, "James Rodríguez": 80,
    "Luis Díaz": 84, "João Félix": 80, "Pedro Neto": 81, "Rúben Dias": 86, "João Cancelo": 83,
    "Mateo Kovačić": 84, "Joško Gvardiol": 85, "Thomas Partey": 80, "Mohammed Kudus": 82,
    "Inaki Williams": 79, "İlkay Gündoğan": 83, "Joshua Kimmich": 87, "Leroy Sané": 84,
    "Nicolas Pépé": 78, "Wilfried Zaha": 79, "Sadio Mané": 86, "Nicolas Jackson": 78,
    "Breel Embolo": 77, "Manuel Akanji": 80, "Remo Freuler": 76, "Denzel Dumfries": 81,
    "Matthijs de Ligt": 82, "Wataru Endo": 76, "Emil Forsberg": 77, "Youri Tielemans": 79,
    "Amadou Onana": 78, "Loïs Openda": 80, "Serge Aurier": 74, "Simon Adingra": 77,
    "Pervis Estupiñán": 78, "Willian Pacho": 80, "Jeremy Sarmiento": 76, "Carlos Gruezo": 72,
    "Hernán Galíndez": 70, "Guillermo Ochoa": 75, "Santiago Giménez": 80, "César Montes": 74,
    "Jorge Sánchez": 72, "Orbelín Pineda": 73, "Lyle Foster": 72, "Percy Tau": 71,
    "Hwang Hee-chan": 78, "Cho Gue-sung": 74, "Antonín Barák": 73, "Michal Sadílek": 70,
    "Stephen Eustáquio": 76, "Tajon Buchanan": 77, "Cyle Larin": 74, "Liam Millar": 70,
    "Sead Kolašinac": 72, "Asmir Begović": 71, "Almoez Ali": 76, "Hassan Al-Haydos": 72,
    "Sofyan Amrabat": 77, "Brahim Díaz": 82, "John McGinn": 78, "Che Adams": 74,
    "Lawrence Shankland": 72, "Tyler Adams": 76, "Giovanni Reyna": 77, "Weston McKennie": 76,
    "Sergiño Dest": 75, "Antonio Sanabria": 73, "Adam Bareiro": 70, "Matías Rojas": 74,
    "Diego Gómez": 75, "Jackson Irvine": 73, "Craig Goodwin": 72, "Merih Demiral": 76,
    "Ferdi Kadıoğlu": 77, "Orkun Kökçü": 75, "Barış Alper Yılmaz": 72, "Antonio Rüdiger": 85,
    "Kai Havertz": 82, "Niclas Füllkrug": 76, "Jonathan Tah": 80, "David Raum": 76,
    "Sébastien Haller": 77, "Franck Kessié": 78, "Ousmane Dembélé": 88, "Aurélien Tchouaméni": 86,
    "N'Golo Kanté": 85, "Ousmane Dembélé": 88, "Kalidou Koulibaly": 82, "Rafael Leão": 86,
    "David Alaba": 84, "Marko Arnautović": 74, "Martin Ødegaard": 88, "Cristiano Ronaldo": 99,
    "Jordan Pickford": 82, "Kyle Walker": 80, "John Stones": 81, "Luke Shaw": 78,
    "Marcus Rashford": 82, "Dominik Livaković": 80, "Ivan Perišić": 81, "Marcelo Brozović": 79,
    "Bruno Petković": 74, "Marko Livaja": 72, "Lawrence Ati-Zigi": 68, "Jordan Ayew": 74,
    "Ernest Nuamah": 72, "Alberto Quintero": 68, "Ismael Díaz": 67,
}

ELITE_CLUBS = {
    "Real Madrid", "Barcelona", "París Saint-Germain", "Manchester City", "Liverpool",
    "Bayern Múnich", "Arsenal", "Chelsea", "Manchester United", "Inter", "Milan",
    "Atlético Madrid", "Borussia Dortmund", "Juventus", "Tottenham", "Nápoles",
    "Newcastle", "Bayer Leverkusen", "Atlético Mineiro",
}

TOP_CLUBS = {
    "Brighton", "Aston Villa", "West Ham", "Sevilla", "Villarreal", "Real Sociedad",
    "Sporting CP", "Benfica", "Porto", "Ajax", "RB Leipzig", "Lille", "Monaco",
    "Olympique de Marsella", "Galatasaray", "Fenerbahçe", "Roma", "Lazio",
    "Wolverhampton", "Fulham", "Bournemouth", "Nottingham Forest", "Crystal Palace",
    "PSV", "Feyenoord", "Braga", "Genoa", "Fiorentina", "Bologna", "Nice",
    "Los Angeles FC", "Inter Miami", "Al Hilal", "Al Nassr",
}


def _target_counts(total: int) -> dict[str, int]:
    keys = RARITY_ORDER_ASSIGN
    wsum = sum(RARITY_WEIGHTS_PCT.values())
    exact = [total * RARITY_WEIGHTS_PCT[k] / wsum for k in keys]
    floors = [int(e) for e in exact]
    remainder = total - sum(floors)
    fracs = sorted(
        ((exact[i] - floors[i], i) for i in range(len(keys))),
        reverse=True,
    )
    for j in range(remainder):
        floors[fracs[j][1]] += 1
    return dict(zip(keys, floors))


def player_star_score(name: str, position: str, club: str) -> int:
    if name in STAR_SCORES:
        return STAR_SCORES[name]
    score = 44
    if club in ELITE_CLUBS:
        score += 22
    elif club in TOP_CLUBS:
        score += 12
    elif club and club not in ("Club internacional",):
        score += 5
    if position == "Delantero":
        score += 8
    elif position == "Mediocampista":
        score += 5
    elif position == "Defensor":
        score += 3
    score += (hash(name) % 13) - 6
    return max(25, min(99, score))


def assign_rarities(stickers: list[dict]) -> None:
    """Asigna rareza global por ranking de estrella (solo jugadores, in-place)."""
    stickers = [s for s in stickers if s.get("kind") not in ("crest", "bandera")]
    total = len(stickers)
    counts = _target_counts(total)
    ranked = sorted(
        stickers,
        key=lambda s: (
            -player_star_score(s["name"], s["position"], s.get("club", "")),
            s["team_id"],
            s["number"],
        ),
    )
    idx = 0
    for rarity in RARITY_ORDER_ASSIGN:
        n = counts[rarity]
        for sticker in ranked[idx : idx + n]:
            sticker["rarity"] = rarity
        idx += n
