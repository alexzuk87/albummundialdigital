"""Utilidades para banderas de selecciones."""

FLAG_CDN = "https://flagcdn.com/w80/{code}.png"

# Código ISO / flagcdn para las 48 selecciones del Mundial 2026
TEAM_FLAG_CODES: dict[str, str] = {
    "mex": "mx",
    "rsa": "za",
    "kor": "kr",
    "cze": "cz",
    "can": "ca",
    "bih": "ba",
    "qat": "qa",
    "sui": "ch",
    "bra": "br",
    "mar": "ma",
    "hai": "ht",
    "sco": "gb-sct",
    "usa": "us",
    "par": "py",
    "aus": "au",
    "tur": "tr",
    "ger": "de",
    "cuw": "cw",
    "civ": "ci",
    "ecu": "ec",
    "ned": "nl",
    "jpn": "jp",
    "swe": "se",
    "tun": "tn",
    "bel": "be",
    "egy": "eg",
    "irn": "ir",
    "nzl": "nz",
    "esp": "es",
    "cpv": "cv",
    "ksa": "sa",
    "uru": "uy",
    "fra": "fr",
    "sen": "sn",
    "irq": "iq",
    "nor": "no",
    "arg": "ar",
    "alg": "dz",
    "aut": "at",
    "jor": "jo",
    "por": "pt",
    "cod": "cd",
    "uzb": "uz",
    "col": "co",
    "eng": "gb-eng",
    "cro": "hr",
    "gha": "gh",
    "pan": "pa",
}


def flag_url(team_id: str) -> str:
    code = TEAM_FLAG_CODES.get(team_id, "un")
    return FLAG_CDN.format(code=code.lower())


def flag_img_html(team_id: str, size: int = 32) -> str:
    url = flag_url(team_id)
    return (
        f'<img src="{url}" alt="bandera" '
        f'style="width:{size}px;height:auto;border-radius:4px;'
        f'box-shadow:0 1px 3px rgba(0,0,0,.3);vertical-align:middle;">'
    )
