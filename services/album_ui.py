"""Vista de álbum con páginas que se voltean por selección."""

from data.album import ALL_STICKERS, STICKER_BY_ID, TEAMS
from services.flags import flag_img_html
from services.sticker_ui import sticker_card_html


def filter_team_pages(
    unlocked: set[str],
    duplicates: list[str],
    team_filter: str | None,
    rarity_filter: str | None,
    show_only: str,
) -> list[tuple[dict, list[dict]]]:
    """Lista de (equipo, figuritas visibles) para cada página del álbum."""
    dupes = set(duplicates)
    pages: list[tuple[dict, list[dict]]] = []

    for team in TEAMS:
        if team_filter and team["id"] != team_filter:
            continue

        team_stickers = [s for s in ALL_STICKERS if s["team_id"] == team["id"]]
        if rarity_filter == "__bandera__":
            team_stickers = [s for s in team_stickers if s.get("kind") == "bandera"]
        elif rarity_filter:
            team_stickers = [s for s in team_stickers if s["rarity"] == rarity_filter]
        if show_only == "Solo desbloqueadas":
            team_stickers = [s for s in team_stickers if s["id"] in unlocked]
        elif show_only == "Solo bloqueadas":
            team_stickers = [s for s in team_stickers if s["id"] not in unlocked]

        if team_stickers:
            pages.append((
                team,
                sorted(team_stickers, key=lambda x: (0 if x.get("kind") == "bandera" else 1, x["number"])),
            ))

    return pages


def album_page_html(
    team: dict,
    stickers: list[dict],
    unlocked: set[str],
    duplicates: list[str],
    page_num: int,
    total_pages: int,
    flip_class: str = "",
) -> str:
    dupes = set(duplicates)
    total_team = len([s for s in ALL_STICKERS if s["team_id"] == team["id"]])
    team_unlocked = sum(1 for s in stickers if s["id"] in unlocked)
    flag = flag_img_html(team["id"], 32)

    cards = "".join(
        sticker_card_html(s, s["id"] in unlocked, s["id"] in dupes)
        for s in stickers
    )

    flip = f" {flip_class}" if flip_class else ""
    return f"""
<div class="album-spread">
  <div class="album-book">
    <div class="album-binding"></div>
    <div class="album-page{flip}">
      <div class="album-page-shadow"></div>
      <div class="album-page-inner">
        <div class="album-page-corner"></div>
        <div class="album-page-header">
          {flag}
          <div class="album-page-titles">
            <span class="album-team-name">{team["name"]}</span>
            <span class="album-team-meta">Grupo {team["group"]} · {team_unlocked}/{total_team} figuritas</span>
          </div>
          <span class="album-page-num">Hoja {page_num} / {total_pages}</span>
        </div>
        <div class="album-page-rule"></div>
        <div class="sticker-grid album-sticker-grid">{cards}</div>
      </div>
    </div>
    <div class="album-page-edge"></div>
  </div>
</div>
"""
