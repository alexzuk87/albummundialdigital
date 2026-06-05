"""Datos del álbum: 48 selecciones × 11 jugadores."""

from data.player_meta import get_club, get_shirt_number
from data.rarity import assign_rarities

# Plantilla por defecto (se reasigna globalmente en _build_stickers)
RARITY_WEIGHTS = ["basica"] * 4 + ["comun"] * 3 + ["rara"] * 2 + ["epica"] + ["legendaria"]

POSITIONS = ["Arquero", "Defensor", "Defensor", "Defensor", "Defensor", "Mediocampista",
             "Mediocampista", "Mediocampista", "Delantero", "Delantero", "Delantero"]


def _players(names: list[str], rarities: list[str] | None = None) -> list[dict]:
    r = rarities or RARITY_WEIGHTS
    return [
        {"name": n, "position": POSITIONS[i], "rarity": r[i]}
        for i, n in enumerate(names)
    ]


TEAMS = [
    {"id": "mex", "name": "México", "group": "A", "players": _players(
        ["Guillermo Ochoa", "Jorge Sánchez", "César Montes", "Johan Vásquez", "Gerardo Arteaga",
         "Edson Álvarez", "Luis Chaves", "Orbelín Pineda", "Santiago Giménez", "Raúl Jiménez", "Hirving Lozano"],
        ["comun", "basica", "comun", "rara", "basica", "epica", "basica", "comun", "rara", "legendaria", "epica"])},
    {"id": "rsa", "name": "Sudáfrica", "group": "A", "players": _players(
        ["Ronwen Williams", "Khuliso Mudau", "Grant Kekana", "Teboho Mokoena", "Bongani Zulu",
         "Sphephelo Sithole", "Themba Zwane", "Percy Tau", "Evidence Makgopa", "Zakhele Lepasa", "Lyle Foster"])},
    {"id": "kor", "name": "Corea del Sur", "group": "A", "players": _players(
        ["Jo Hyeon-woo", "Kim Min-jae", "Kim Young-gwon", "Kim Jin-su", "Jung Seung-hyun",
         "Lee Kang-in", "Hwang In-beom", "Paik Seung-ho", "Son Heung-min", "Hwang Hee-chan", "Cho Gue-sung"],
        ["basica", "epica", "comun", "basica", "basica", "rara", "comun", "basica", "legendaria", "epica", "rara"])},
    {"id": "cze", "name": "República Checa", "group": "A", "players": _players(
        ["Tomáš Vaclík", "Vladimír Coufal", "David Hovorka", "Ondřej Kúdela", "Tomáš Holeš",
         "Antonín Barák", "Michal Sadílek", "Lukáš Provod", "Patrik Schick", "Jan Kuchta", "Tomáš Souček"],
        ["comun", "basica", "basica", "comun", "rara", "comun", "basica", "rara", "epica", "basica", "legendaria"])},
    {"id": "can", "name": "Canadá", "group": "B", "players": _players(
        ["Milan Borjan", "Alphonso Davies", "Steven Vitória", "Derek Cornelius", "Sam Adekugbe",
         "Stephen Eustáquio", "Samuel Piette", "Jonathan David", "Cyle Larin", "Tajon Buchanan", "Liam Millar"],
        ["basica", "legendaria", "comun", "basica", "basica", "epica", "comun", "rara", "rara", "epica", "basica"])},
    {"id": "bih", "name": "Bosnia y Herzegovina", "group": "B", "players": _players(
        ["Asmir Begović", "Sead Kolašinac", "Ervin Zukanović", "Dennis Hadžikadunić", "Admir Ljevaković",
         "Miralem Pjanić", "Amir Hadžiahmetović", "Edin Džeko", "Miroslav Stevanović", "Ermedin Demirović", "Benjamin Tahirović"])},
    {"id": "qat", "name": "Catar", "group": "B", "players": _players(
        ["Saad Al-Sheeb", "Abdelkarim Hassan", "Bassam Al-Rawi", "Tarek Salman", "Homam Ahmed",
         "Hassan Al-Haydos", "Akram Afif", "Almoez Ali", "Mohammed Muntari", "Yousuf Abdurisag", "Pedro"])},
    {"id": "sui", "name": "Suiza", "group": "B", "players": _players(
        ["Yann Sommer", "Manuel Akanji", "Nico Elvedi", "Ricardo Rodríguez", "Silvan Widmer",
         "Granit Xhaka", "Remo Freuler", "Xherdan Shaqiri", "Breel Embolo", "Dan Ndoye", "Noah Okafor"],
        ["epica", "rara", "comun", "comun", "basica", "legendaria", "comun", "epica", "rara", "basica", "basica"])},
    {"id": "bra", "name": "Brasil", "group": "C", "players": _players(
        ["Alisson Becker", "Danilo", "Marquinhos", "Gabriel Magalhães", "Guilherme Arana",
         "Casemiro", "Bruno Guimarães", "Rodrygo", "Vinícius Júnior", "Richarlison", "Neymar"],
        ["epica", "comun", "rara", "comun", "basica", "epica", "rara", "rara", "legendaria", "comun", "legendaria"])},
    {"id": "mar", "name": "Marruecos", "group": "C", "players": _players(
        ["Yassine Bounou", "Achraf Hakimi", "Romain Saïss", "Nayef Aguerd", "Noussair Mazraoui",
         "Sofyan Amrabat", "Azzedine Ounahi", "Hakim Ziyech", "Youssef En-Nesyri", "Sofiane Boufal", "Brahim Díaz"],
        ["comun", "legendaria", "comun", "rara", "epica", "rara", "comun", "epica", "rara", "basica", "basica"])},
    {"id": "hai", "name": "Haití", "group": "C", "players": _players(
        ["Johny Placide", "Derrick Etienne", "Ricardo Adé", "Martinique Joseph", "Carlens Arcus",
         "Derrick Luckassen", "Zachary Herivaux", "Bryan Alceus", "Mondy Prunier", "Frantzdy Pierrot", "Duckens Nazon"])},
    {"id": "sco", "name": "Escocia", "group": "C", "players": _players(
        ["Angus Gunn", "Andrew Robertson", "Grant Hanley", "Jack Hendry", "Kieran Tierney",
         "John McGinn", "Scott McTominay", "Billy Gilmour", "Lyndon Dykes", "Che Adams", "Lawrence Shankland"],
        ["basica", "legendaria", "comun", "basica", "rara", "epica", "rara", "comun", "comun", "basica", "epica"])},
    {"id": "usa", "name": "Estados Unidos", "group": "D", "players": _players(
        ["Matt Turner", "Sergiño Dest", "Chris Richards", "Walker Zimmerman", "Antonee Robinson",
         "Tyler Adams", "Weston McKennie", "Giovanni Reyna", "Christian Pulisic", "Folarin Balogun", "Ricardo Pepi"],
        ["comun", "rara", "basica", "comun", "epica", "rara", "comun", "epica", "legendaria", "rara", "basica"])},
    {"id": "par", "name": "Paraguay", "group": "D", "players": _players(
        ["Anthony Silva", "Omar Alderete", "Gustavo Gómez", "Júnior Alonso", "Blas Riveros",
         "Matías Rojas", "Diego Gómez", "Miguel Almirón", "Antonio Sanabria", "Adam Bareiro", "Julio Enciso"],
        ["basica", "comun", "legendaria", "rara", "basica", "comun", "rara", "epica", "comun", "basica", "epica"])},
    {"id": "aus", "name": "Australia", "group": "D", "players": _players(
        ["Mathew Ryan", "Fran Karačić", "Bailey Wright", "Harry Souttar", "Aziz Behich",
         "Jackson Irvine", "Riley McGree", "Craig Goodwin", "Mitchell Duke", "Martin Boyle", "Kusini Yengi"])},
    {"id": "tur", "name": "Turquía", "group": "D", "players": _players(
        ["Uğurcan Çakır", "Zeki Çelik", "Merih Demiral", "Çağlar Söyüncü", "Ferdi Kadıoğlu",
         "Hakan Çalhanoğlu", "Orkun Kökçü", "Arda Güler", "Cenk Tosun", "Barış Alper Yılmaz", "Kenan Yıldız"],
        ["comun", "basica", "rara", "comun", "epica", "legendaria", "comun", "epica", "basica", "basica", "rara"])},
    {"id": "ger", "name": "Alemania", "group": "E", "players": _players(
        ["Manuel Neuer", "Joshua Kimmich", "Antonio Rüdiger", "Jonathan Tah", "David Raum",
         "İlkay Gündoğan", "Florian Wirtz", "Jamal Musiala", "Kai Havertz", "Niclas Füllkrug", "Leroy Sané"],
        ["legendaria", "epica", "rara", "comun", "basica", "epica", "legendaria", "legendaria", "rara", "comun", "rara"])},
    {"id": "cuw", "name": "Curazao", "group": "E", "players": _players(
        ["Eloy Room", "Cuca Martina", "Juriën Gaari", "Rangelo Janga", "Brandley Kuwas",
         "Leandro Bacuna", "Elson Hooi", "Gervane Kastaneer", "Roly Bonevacia", "Jarchinio Antonia", "Shanon Carmelia"])},
    {"id": "civ", "name": "Costa de Marfil", "group": "E", "players": _players(
        ["Badra Ali Sangaré", "Serge Aurier", "Wilfried Bony", "Ousmane Diomande", "Ghislain Konan",
         "Franck Kessié", "Sébastien Haller", "Nicolas Pépé", "Simon Adingra", "Evann Guessand", "Wilfried Zaha"],
        ["basica", "rara", "comun", "epica", "basica", "rara", "comun", "legendaria", "comun", "basica", "epica"])},
    {"id": "ecu", "name": "Ecuador", "group": "E", "players": _players(
        ["Hernán Galíndez", "Pervis Estupiñán", "Piero Hincapié", "Felix Torres", "Angelo Preciado",
         "Moisés Caicedo", "Carlos Gruezo", "Kendry Páez", "Enner Valencia", "Willian Pacho", "Jeremy Sarmiento"],
        ["basica", "epica", "rara", "comun", "basica", "legendaria", "comun", "epica", "rara", "rara", "basica"])},
    {"id": "ned", "name": "Países Bajos", "group": "F", "players": _players(
        ["Bart Verbruggen", "Virgil van Dijk", "Matthijs de Ligt", "Nathan Aké", "Denzel Dumfries",
         "Frenkie de Jong", "Georginio Wijnaldum", "Cody Gakpo", "Memphis Depay", "Brian Brobbey", "Xavi Simons"],
        ["basica", "legendaria", "rara", "comun", "epica", "legendaria", "comun", "rara", "epica", "basica", "rara"])},
    {"id": "jpn", "name": "Japón", "group": "F", "players": _players(
        ["Keisuke Osako", "Hiroki Ito", "Ko Itakura", "Yukinari Sugawara", "Takehiro Tomiyasu",
         "Wataru Endo", "Kaoru Mitoma", "Ritsu Doan", "Daizen Maeda", "Ayase Ueda", "Takefusa Kubo"],
        ["basica", "comun", "rara", "basica", "comun", "epica", "legendaria", "rara", "comun", "basica", "epica"])},
    {"id": "swe", "name": "Suecia", "group": "F", "players": _players(
        ["Robin Olsen", "Victor Lindelöf", "Isak Hien", "Ludwig Augustinsson", "Emil Holm",
         "Kristoffer Olsson", "Emil Forsberg", "Dejan Kulusevski", "Alexander Isak", "Viktor Gyökeres", "Jesper Karlsson"],
        ["comun", "rara", "basica", "basica", "comun", "comun", "epica", "rara", "legendaria", "epica", "basica"])},
    {"id": "tun", "name": "Túnez", "group": "F", "players": _players(
        ["Aymen Dahmen", "Yassine Meriah", "Montassar Talbi", "Ali Maâloul", "Wajdi Kechrida",
         "Aïssa Laïdouni", "Ellyes Skhiri", "Hamza Rafia", "Youssef Msakni", "Issam Jebali", "Taha Yassine Khenissi"])},
    {"id": "bel", "name": "Bélgica", "group": "G", "players": _players(
        ["Koen Casteels", "Timothy Castagne", "Wout Faes", "Arthur Theate", "Zeno Debast",
         "Youri Tielemans", "Amadou Onana", "Kevin De Bruyne", "Romelu Lukaku", "Jérémy Doku", "Loïs Openda"],
        ["comun", "basica", "comun", "basica", "rara", "rara", "comun", "legendaria", "epica", "epica", "rara"])},
    {"id": "egy", "name": "Egipto", "group": "G", "players": _players(
        ["Mohamed El Shenawy", "Ahmed Hegazi", "Mohamed Hany", "Mohamed Abdelmonem", "Ahmed Fatouh",
         "Mohamed Elneny", "Emam Ashour", "Mohamed Salah", "Omar Marmoush", "Mostafa Mohamed", "Trézéguet"],
        ["basica", "comun", "basica", "comun", "basica", "rara", "comun", "legendaria", "epica", "basica", "rara"])},
    {"id": "irn", "name": "Irán", "group": "G", "players": _players(
        ["Alireza Beiranvand", "Shojae Khalilzadeh", "Hossein Kanani", "Milad Mohammadi", "Ramin Rezaeian",
         "Saeid Ezatolahi", "Mehdi Taremi", "Sardar Azmoun", "Alireza Jahanbakhsh", "Omid Noorafkan", "Saman Ghoddos"])},
    {"id": "nzl", "name": "Nueva Zelanda", "group": "G", "players": _players(
        ["Max Crocombe", "Bill Tuiloma", "Michael Boxall", "Nando Pijker", "Liberato Cacace",
         "Joe Bell", "Marko Stamenić", "Marco Rojas", "Chris Wood", "Ben Waine", "Elijah Just"])},
    {"id": "esp", "name": "España", "group": "H", "players": _players(
        ["Unai Simón", "Aymeric Laporte", "Robin Le Normand", "Jules Koundé", "Marc Cucurella",
         "Rodri", "Pedri", "Gavi", "Álvaro Morata", "Nico Williams", "Lamine Yamal"],
        ["comun", "rara", "comun", "rara", "basica", "legendaria", "legendaria", "epica", "comun", "epica", "legendaria"])},
    {"id": "cpv", "name": "Cabo Verde", "group": "H", "players": _players(
        ["Vozinha", "Stopira", "Jójó", "Dylan Tavares", "Patrick Andrade",
         "Nuno Rocha", "Ryan Mendes", "Bebé", "Júlio Tavares", "Garés", "Djaniny"])},
    {"id": "ksa", "name": "Arabia Saudita", "group": "H", "players": _players(
        ["Mohammed Al-Owais", "Yasser Al-Shahrani", "Ali Al-Bulaihi", "Sultan Al-Ghamdi", "Mohammed Al-Breik",
         "Salem Al-Dawsari", "Salman Al-Faraj", "Sami Al-Najei", "Saleh Al-Shehri", "Firas Al-Buraikan", "Abdullah Radif"])},
    {"id": "uru", "name": "Uruguay", "group": "H", "players": _players(
        ["Sergio Rochet", "José Giménez", "Ronald Araújo", "Sebastián Coates", "Matías Viña",
         "Federico Valverde", "Rodrigo Bentancur", "Giorgian De Arrascaeta", "Darwin Núñez", "Luis Suárez", "Facundo Pellistri"],
        ["comun", "rara", "epica", "comun", "basica", "legendaria", "rara", "epica", "rara", "legendaria", "basica"])},
    {"id": "fra", "name": "Francia", "group": "I", "players": _players(
        ["Mike Maignan", "Jules Koundé", "Dayot Upamecano", "Ibrahima Konaté", "Théo Hernandez",
         "N'Golo Kanté", "Aurélien Tchouaméni", "Ousmane Dembélé", "Kylian Mbappé", "Olivier Giroud", "Antoine Griezmann"],
        ["epica", "rara", "comun", "rara", "epica", "legendaria", "rara", "epica", "legendaria", "comun", "legendaria"])},
    {"id": "sen", "name": "Senegal", "group": "I", "players": _players(
        ["Édouard Mendy", "Kalidou Koulibaly", "Abdou Diallo", "Moussa Wagué", "Youssouf Sabaly",
         "Idrissa Gueye", "Pape Matar Sarr", "Sadio Mané", "Nicolas Jackson", "Boulaye Dia", "Ismaïla Sarr"],
        ["comun", "legendaria", "comun", "basica", "basica", "rara", "comun", "legendaria", "epica", "basica", "rara"])},
    {"id": "irq", "name": "Irak", "group": "I", "players": _players(
        ["Jalal Hassan", "Ali Adnan", "Saad Natiq", "Manaf Younis", "Hussein Ali",
         "Amir Al-Ammari", "Zidane Iqbal", "Aymen Hussein", "Mohammed Ali Qasim", "Aso Rostam", "Bashar Resan"])},
    {"id": "nor", "name": "Noruega", "group": "I", "players": _players(
        ["Bernd Leno", "Nicolai Østigård", "Stefan Strandberg", "Marcus Pedersen", "Felix Myhre",
         "Martin Ødegaard", "Sander Berge", "Erling Haaland", "Alexander Sørloth", "Antonio Nusa", "Aron Dønnum"],
        ["comun", "basica", "basica", "comun", "basica", "legendaria", "rara", "legendaria", "epica", "rara", "comun"])},
    {"id": "arg", "name": "Argentina", "group": "J", "players": _players(
        ["Emiliano Martínez", "Nahuel Molina", "Cristian Romero", "Nicolás Otamendi", "Marcos Acuña",
         "Enzo Fernández", "Alexis Mac Allister", "Ángel Di María", "Lionel Messi", "Lautaro Martínez", "Julián Álvarez"],
        ["epica", "comun", "rara", "comun", "basica", "legendaria", "epica", "legendaria", "legendaria", "legendaria", "epica"])},
    {"id": "alg", "name": "Argelia", "group": "J", "players": _players(
        ["Raïs M'Bolhi", "Ramy Bensebaini", "Aissa Mandi", "Youcef Atal", "Houssam Eddine Aouar",
         "Ismaël Bennacer", "Ramiz Zerrouki", "Riyad Mahrez", "Youcef Belaïli", "Amine Gouiri", "Baghdad Bounedjah"])},
    {"id": "aut", "name": "Austria", "group": "J", "players": _players(
        ["Patrick Pentz", "David Alaba", "Philipp Lienhart", "Kevin Danso", "Philipp Mwene",
         "Marcel Sabitzer", "Florian Grillitsch", "Christoph Baumgartner", "Marko Arnautović", "Michael Gregoritsch", "Romano Schmid"],
        ["basica", "legendaria", "comun", "rara", "basica", "epica", "comun", "rara", "epica", "comun", "basica"])},
    {"id": "jor", "name": "Jordania", "group": "J", "players": _players(
        ["Yazeed Abulaila", "Yazan Al-Naimat", "Husam Al-Barqawi", "Salem Al-Ajalin", "Musa Al-Taamari",
         "Nizar Al-Rashdan", "Mahmoud Al-Mardi", "Ali Olwan", "Yaseen Al-Bakheet", "Abdullah Nahar", "Ehsan Haddad"])},
    {"id": "por", "name": "Portugal", "group": "K", "players": _players(
        ["Diogo Costa", "João Cancelo", "Rúben Dias", "Pepe", "Nuno Mendes",
         "Bruno Fernandes", "Bernardo Silva", "Rafael Leão", "Cristiano Ronaldo", "Pedro Neto", "João Félix"],
        ["comun", "rara", "epica", "legendaria", "comun", "legendaria", "legendaria", "epica", "legendaria", "rara", "rara"])},
    {"id": "cod", "name": "Rep. Dem. del Congo", "group": "K", "players": _players(
        ["Joël Kiassumbua", "Chancel Mbemba", "Marcel Tisserand", "Arthur Masuaku", "Issama Mpeko",
         "Gaël Kakuta", "Edo Kayombo", "Théo Bongonda", "Cédric Bakambu", "Yoane Wissa", "Meschack Elia"])},
    {"id": "uzb", "name": "Uzbekistán", "group": "K", "players": _players(
        ["Utkir Yusupov", "Egor Sorokin", "Jaloliddin Masharipov", "Odil Khamdamov", "Abdulla Abdullayev",
         "Jasurbek Yakhshiboyev", "Otabek Shukurov", "Eldor Shomurodov", "Igor Sergeev", "Khozhimurat Akbarov", "Sherzod Nasriddinov"])},
    {"id": "col", "name": "Colombia", "group": "K", "players": _players(
        ["Camilo Vargas", "Davinson Sánchez", "Yerry Mina", "Jhon Lucumí", "Johan Mojica",
         "Wilmar Barrios", "Jefferson Lerma", "James Rodríguez", "Luis Díaz", "Rafael Santos Borré", "Jhon Durán"],
        ["comun", "rara", "comun", "basica", "basica", "comun", "rara", "legendaria", "legendaria", "epica", "rara"])},
    {"id": "eng", "name": "Inglaterra", "group": "L", "players": _players(
        ["Jordan Pickford", "Kyle Walker", "John Stones", "Harry Maguire", "Luke Shaw",
         "Declan Rice", "Jude Bellingham", "Phil Foden", "Harry Kane", "Bukayo Saka", "Marcus Rashford"],
        ["comun", "rara", "comun", "basica", "comun", "epica", "legendaria", "legendaria", "legendaria", "epica", "rara"])},
    {"id": "cro", "name": "Croacia", "group": "L", "players": _players(
        ["Dominik Livaković", "Joško Gvardiol", "Dejan Lovren", "Borna Sosa", "Josip Juranović",
         "Luka Modrić", "Mateo Kovačić", "Marcelo Brozović", "Marko Livaja", "Bruno Petković", "Ivan Perišić"],
        ["comun", "epica", "comun", "basica", "basica", "legendaria", "legendaria", "epica", "rara", "comun", "rara"])},
    {"id": "gha", "name": "Ghana", "group": "L", "players": _players(
        ["Lawrence Ati-Zigi", "Daniel Amartey", "Alexander Djiku", "Gideon Mensah", "Tariq Lamptey",
         "Thomas Partey", "Mohammed Kudus", "Inaki Williams", "Jordan Ayew", "Antoine Semenyo", "Ernest Nuamah"],
        ["basica", "comun", "rara", "basica", "comun", "epica", "legendaria", "rara", "comun", "basica", "rara"])},
    {"id": "pan", "name": "Panamá", "group": "L", "players": _players(
        ["Orlando Mosquera", "Michael Murillo", "Fidel Escobar", "Harold Cummings", "Eric Davis",
         "Aníbal Godoy", "Adalberto Carrasquilla", "José Fajardo", "Ismael Díaz", "Alberto Quintero", "Jorge Hernández"])},
]


def _build_stickers() -> list[dict]:
    stickers = []
    for team in TEAMS:
        stickers.append({
            "id": f"{team['id']}_bandera",
            "kind": "bandera",
            "team_id": team["id"],
            "team_name": team["name"],
            "group": team["group"],
            "number": 0,
            "shirt_number": 0,
            "name": f"Bandera {team['name']}",
            "position": "Bandera",
            "club": team["name"],
            "rarity": "bandera",
        })
        for i, player in enumerate(team["players"], start=1):
            sid = f"{team['id']}_{i:02d}"
            stickers.append({
                "id": sid,
                "kind": "player",
                "team_id": team["id"],
                "team_name": team["name"],
                "group": team["group"],
                "number": i,
                "shirt_number": get_shirt_number(player["name"], i),
                "name": player["name"],
                "position": player["position"],
                "club": get_club(player["name"], team["id"], i - 1),
                "rarity": player["rarity"],
            })
    players = [s for s in stickers if s.get("kind") == "player"]
    assign_rarities(players)
    return stickers


def _register_bandera_aliases(sticker_map: dict) -> None:
    """Compatibilidad con desbloqueos guardados como *_crest."""
    for sid, sticker in list(sticker_map.items()):
        if sid.endswith("_bandera"):
            sticker_map[sid.replace("_bandera", "_crest")] = sticker


ALL_STICKERS = _build_stickers()
STICKER_BY_ID = {s["id"]: s for s in ALL_STICKERS}
_register_bandera_aliases(STICKER_BY_ID)
TEAM_BY_ID = {t["id"]: t for t in TEAMS}
TOTAL_STICKERS = len(ALL_STICKERS)
TOTAL_TEAMS = len(TEAMS)
