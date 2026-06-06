"""Estilos CSS — cancha verde y diseño responsive."""

ALBUM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Nunito:wght@400;600;700;800&display=swap');

:root {
    --grass-dark: #1b6b34;
    --grass-mid: #2e8f47;
    --grass-light: #3daa5c;
    --line-white: rgba(255, 255, 255, 0.45);
    --gold: #ffd700;
    --card-bg: #ffffff;
    --shadow: 0 4px 20px rgba(0,0,0,0.2);
}

/* Verde liso + líneas de cancha (bordes, medialuna, círculo central) */
.stApp {
    background-color: var(--grass-mid) !important;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 700' preserveAspectRatio='xMidYMid slice'%3E%3Crect x='20' y='20' width='360' height='660' fill='none' stroke='white' stroke-width='3' opacity='0.5'/%3E%3Cline x1='20' y1='350' x2='380' y2='350' stroke='white' stroke-width='2.5' opacity='0.4'/%3E%3Ccircle cx='200' cy='350' r='55' fill='none' stroke='white' stroke-width='2.5' opacity='0.4'/%3E%3Ccircle cx='200' cy='350' r='4' fill='white' opacity='0.5'/%3E%3Crect x='110' y='20' width='180' height='90' fill='none' stroke='white' stroke-width='2' opacity='0.35'/%3E%3Crect x='110' y='590' width='180' height='90' fill='none' stroke='white' stroke-width='2' opacity='0.35'/%3E%3Crect x='155' y='20' width='90' height='35' fill='none' stroke='white' stroke-width='1.5' opacity='0.3'/%3E%3Crect x='155' y='645' width='90' height='35' fill='none' stroke='white' stroke-width='1.5' opacity='0.3'/%3E%3C/svg%3E") !important;
    background-size: cover !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important;
}

.block-container {
    padding-top: 1rem !important;
    max-width: 1100px !important;
    background: rgba(255, 255, 255, 0.94);
    border-radius: 18px;
    padding-bottom: 2rem !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.18);
    margin-top: 0.5rem;
}

.main-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(2rem, 6vw, 3.5rem);
    color: var(--grass-dark);
    text-align: center;
    text-shadow: none;
    letter-spacing: 2px;
    margin-bottom: 0;
}

.sub-header {
    text-align: center;
    color: #555;
    font-family: 'Nunito', sans-serif;
    font-size: clamp(0.85rem, 2.5vw, 1rem);
    margin-bottom: 1rem;
}

.progress-wrap {
    background: var(--card-bg);
    border-radius: 16px;
    padding: 1rem 1.25rem;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
}

.progress-label {
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    color: var(--grass-dark);
    font-size: 0.95rem;
}

.progress-bar-outer {
    background: #e0e0e0;
    border-radius: 12px;
    height: 22px;
    overflow: hidden;
    margin-top: 0.4rem;
}

.progress-bar-inner {
    height: 100%;
    background: linear-gradient(90deg, var(--grass-dark), var(--grass-light));
    border-radius: 12px;
    transition: width 0.6s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-weight: 700;
    font-size: 0.75rem;
    font-family: 'Nunito', sans-serif;
    min-width: 2.5rem;
}

/* Álbum — hojas que se voltean */
.album-spread {
    background: linear-gradient(180deg, #6b5344 0%, #4a3829 100%);
    padding: 20px 16px 24px;
    border-radius: 14px;
    margin: 1rem 0;
    box-shadow: 0 12px 32px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.08);
    position: relative;
}

.album-edge-hint {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    font-size: 2.8rem;
    color: rgba(255,255,255,0.55);
    font-weight: 700;
    line-height: 1;
    pointer-events: none;
    text-shadow: 0 2px 8px rgba(0,0,0,0.4);
    z-index: 5;
}

.album-edge-left { left: 6px; }
.album-edge-right { right: 6px; }

.album-nav-rail {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 300px;
    gap: 6px;
}

.album-nav-rail-label {
    font-family: 'Nunito', sans-serif;
    font-size: 0.65rem;
    color: #555;
    font-weight: 700;
    text-align: center;
}

/* Botones Anterior / Siguiente — una sola línea, sin cortar palabras */
div[data-testid="stHorizontalBlock"] div[data-testid="column"] .stButton > button {
    white-space: nowrap !important;
    word-break: keep-all !important;
    hyphens: none !important;
    line-height: 1.25 !important;
    min-height: 2.6rem;
}

.album-book {
    position: relative;
    max-width: 920px;
    margin: 0 auto;
    perspective: 1600px;
    padding-left: 14px;
}

.album-binding {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 14px;
    background: repeating-linear-gradient(
        180deg,
        #5c4a3a 0px,
        #5c4a3a 4px,
        #7a6350 4px,
        #7a6350 8px
    );
    border-radius: 4px 0 0 4px;
    box-shadow: inset -3px 0 8px rgba(0,0,0,0.35);
    z-index: 3;
}

.album-page {
    position: relative;
    transform-origin: left center;
    transform-style: preserve-3d;
    animation: albumPageTurnIn 0.65s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
}

.album-page-flip-next {
    animation: albumPageTurnNext 0.7s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
}

.album-page-flip-prev {
    transform-origin: right center;
    animation: albumPageTurnPrev 0.7s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
}

@keyframes albumPageTurnIn {
    0% {
        transform: rotateY(-72deg) translateX(-8px);
        opacity: 0.4;
        box-shadow: -20px 8px 40px rgba(0,0,0,0.25);
    }
    100% {
        transform: rotateY(0deg) translateX(0);
        opacity: 1;
        box-shadow: 4px 8px 28px rgba(0,0,0,0.2);
    }
}

@keyframes albumPageTurnNext {
    0% {
        transform: rotateY(88deg);
        opacity: 0;
        filter: brightness(0.85);
    }
    45% {
        transform: rotateY(42deg);
        opacity: 0.85;
    }
    100% {
        transform: rotateY(0deg);
        opacity: 1;
        filter: brightness(1);
    }
}

@keyframes albumPageTurnPrev {
    0% {
        transform: rotateY(-88deg);
        opacity: 0;
        filter: brightness(0.85);
    }
    45% {
        transform: rotateY(-42deg);
        opacity: 0.85;
    }
    100% {
        transform: rotateY(0deg);
        opacity: 1;
        filter: brightness(1);
    }
}

.album-page-shadow {
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, rgba(0,0,0,0.12) 0%, transparent 18%);
    border-radius: 2px 14px 14px 2px;
    pointer-events: none;
    z-index: 1;
}

.album-page-inner {
    position: relative;
    background: linear-gradient(
        135deg,
        #faf6ee 0%,
        #fffdf7 12%,
        #fffef9 88%,
        #f0ebe0 100%
    );
    border-radius: 2px 14px 14px 2px;
    padding: 14px 16px 18px;
    min-height: 320px;
    border: 1px solid #d8ccb8;
    box-shadow:
        4px 6px 24px rgba(0,0,0,0.18),
        inset 0 0 60px rgba(139,115,85,0.06);
    z-index: 2;
}

.album-page-corner {
    position: absolute;
    bottom: 0;
    right: 0;
    width: 48px;
    height: 48px;
    background: linear-gradient(
        225deg,
        transparent 48%,
        rgba(0,0,0,0.04) 48%,
        rgba(0,0,0,0.08) 100%
    );
    border-radius: 0 0 12px 0;
    pointer-events: none;
}

.album-page-edge {
    position: absolute;
    right: -4px;
    top: 6px;
    bottom: 6px;
    width: 6px;
    background: linear-gradient(90deg, #e8e0d0, #fff8);
    border-radius: 0 3px 3px 0;
    box-shadow: 2px 0 6px rgba(0,0,0,0.1);
}

.album-page-header {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 8px;
}

.album-page-titles {
    flex: 1;
    min-width: 140px;
    display: flex;
    flex-direction: column;
}

.album-team-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    color: #2c4a35;
    letter-spacing: 1px;
    line-height: 1.1;
}

.album-team-meta {
    font-family: 'Nunito', sans-serif;
    font-size: 0.78rem;
    color: #666;
    font-weight: 600;
}

.album-page-num {
    font-family: 'Nunito', sans-serif;
    font-size: 0.72rem;
    color: #8b7355;
    background: rgba(139,115,85,0.12);
    padding: 4px 10px;
    border-radius: 20px;
    font-weight: 700;
    white-space: nowrap;
}

.album-page-rule {
    height: 3px;
    background: linear-gradient(90deg, var(--grass-dark), var(--grass-light), var(--grass-dark));
    border-radius: 2px;
    margin-bottom: 12px;
    opacity: 0.75;
}

.album-sticker-grid {
    background: rgba(255,255,255,0.35);
    border-radius: 10px;
    padding: 10px;
    border: 1px dashed #d4c4a8;
}

.sticker-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
    gap: 12px;
}

@media (max-width: 480px) {
    .sticker-grid {
        grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
        gap: 8px;
    }
}

.sticker-card {
    border-radius: 12px;
    padding: 8px 6px 10px;
    text-align: center;
    font-family: 'Nunito', sans-serif;
    box-shadow: var(--shadow);
    transition: transform 0.2s;
    position: relative;
    overflow: hidden;
    min-height: 180px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3px;
}

.sticker-card:hover {
    transform: scale(1.04);
}

.sticker-locked {
    background: linear-gradient(145deg, #555, #333);
    color: #aaa;
}

.sticker-locked::after {
    content: '🔒';
    font-size: 1.5rem;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.sticker-unlocked {
    background: var(--card-bg);
    color: #222;
}

.sticker-unlocked.rarity-bg-default {
    background: #ffffff;
    border: 1px solid #e0e0e0;
}

.sticker-unlocked.rarity-bg-rara,
.reveal-card.rarity-bg-rara {
    background: linear-gradient(160deg, #fdf6e8 0%, #e8b86d 35%, #cd7f32 70%, #a5651e 100%);
    border: 2px solid #b87333;
    color: #2a1a08;
}

.sticker-unlocked.rarity-bg-epica,
.reveal-card.rarity-bg-epica {
    background: linear-gradient(160deg, #ffffff 0%, #e8e8e8 30%, #c0c0c0 55%, #9e9e9e 100%);
    border: 2px solid #9c27b0;
    color: #1a1a1a;
    box-shadow: 0 0 14px rgba(156, 39, 176, 0.35);
}

.sticker-unlocked.rarity-bg-legendaria,
.reveal-card.rarity-bg-legendaria {
    background: linear-gradient(160deg, #fffde7 0%, #ffd700 40%, #daa520 75%, #b8860b 100%);
    border: 2px solid #ff9800;
    color: #3e2723;
    box-shadow: 0 0 16px rgba(255, 193, 7, 0.45);
}

.sticker-bandera {
    background: linear-gradient(160deg, #f8f9fa 0%, #e8ecf0 50%, #dde4ea 100%) !important;
    border: 2px solid #90a4ae !important;
    color: #263238;
}

.sticker-bandera .sticker-bandera-label,
.sticker-bandera-tag {
    font-size: 0.55rem;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: #455a64;
    margin-top: 4px;
}

.sticker-bandera img {
    margin: 8px auto;
    display: block;
    border-radius: 6px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.reveal-bandera img {
    margin: 10px auto;
}

/* Cuadro eliminatorio */
.knockout-tree {
    display: flex;
    flex-direction: row;
    gap: 12px;
    overflow-x: auto;
    padding: 12px 4px 20px;
    margin: 8px 0 16px;
}

.knockout-tree-col {
    flex: 1;
    min-width: 140px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.knockout-col-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 0.95rem;
    letter-spacing: 1px;
    text-align: center;
    color: #1b5e20;
    padding: 4px 6px;
    background: rgba(46, 143, 71, 0.15);
    border-radius: 6px;
}

.knockout-col-matches {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    gap: 10px;
    flex: 1;
}

.bracket-match {
    background: #fff;
    border: 2px solid #c5cae9;
    border-radius: 8px;
    padding: 8px 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    position: relative;
}

.bracket-match::after {
    content: '';
    position: absolute;
    right: -14px;
    top: 50%;
    width: 12px;
    height: 2px;
    background: #9fa8da;
}

.knockout-tree-col:last-child .bracket-match::after {
    display: none;
}

.bracket-team {
    font-size: 0.72rem;
    font-weight: 700;
    padding: 4px 6px;
    border-radius: 4px;
    background: #f5f5f5;
    margin: 2px 0;
    line-height: 1.2;
}

.bracket-team.winner {
    background: linear-gradient(90deg, #e8f5e9, #c8e6c9);
    border-left: 3px solid #2e7d32;
}

.bracket-vs {
    font-size: 0.6rem;
    color: #888;
    text-align: center;
    margin: 2px 0;
}

.bracket-bye-label {
    font-size: 0.65rem;
    color: #2e7d32;
    font-weight: 700;
    text-align: center;
}

.bracket-pick-box {
    background: rgba(255,255,255,0.85);
    border: 1px dashed #90a4ae;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 8px;
}

.knockout-bracket-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 10px;
}

/* Fase de grupos — 6 columnas por fila, banderas apiladas */
.groups-grid-row {
    margin-bottom: 0.5rem;
}

.group-pick-card {
    background: rgba(255,255,255,0.92);
    border-radius: 10px;
    padding: 8px 6px 10px;
    border: 1px solid #c8e6c9;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    min-height: 200px;
}

.group-pick-title {
    text-align: center;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    color: #1b5e20;
    letter-spacing: 1px;
    margin-bottom: 6px;
}

.group-podium {
    margin: 0 0 10px;
    padding: 6px 4px;
    background: rgba(46, 143, 71, 0.08);
    border-radius: 8px;
    min-height: 88px;
}

.group-rank-row {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 4px 2px;
    border-bottom: 1px solid rgba(0,0,0,0.06);
}

.group-rank-row:last-child {
    border-bottom: none;
}

.group-rank-badge {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 0.85rem;
    color: #1b5e20;
    min-width: 1.4rem;
    text-align: center;
}

.group-flag-row {
    display: flex;
    align-items: center;
    gap: 6px;
    flex: 1;
    min-width: 0;
}

.group-flag-row img {
    flex-shrink: 0;
    border-radius: 3px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}

.group-flag-name {
    font-family: 'Nunito', sans-serif;
    font-size: 0.62rem;
    font-weight: 700;
    color: #333;
    line-height: 1.15;
    word-break: break-word;
}

.group-team-pick {
    display: flex;
    align-items: center;
    gap: 4px;
    margin: 4px 0;
    padding: 3px 2px;
    border-radius: 6px;
    background: rgba(255,255,255,0.6);
}

.group-team-pick.is-first { outline: 2px solid #ffd700; background: rgba(255, 215, 0, 0.12); }
.group-team-pick.is-second { outline: 2px solid #9e9e9e; background: rgba(192, 192, 192, 0.15); }
.group-team-pick.is-third { outline: 2px solid #cd7f32; background: rgba(205, 127, 50, 0.12); }

/* Botones 1° 2° 3° coloreados (marcador + hermano del botón en Streamlit) */
div:has(> .rank-btn-gold) + div button[kind="primary"],
div:has(> .rank-btn-gold) + div button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(180deg, #ffe082, #ffc107) !important;
    color: #3e2723 !important;
    border: 2px solid #ff8f00 !important;
    font-weight: 800 !important;
}
div:has(> .rank-btn-gold) + div button[kind="secondary"],
div:has(> .rank-btn-gold) + div button[data-testid="stBaseButton-secondary"] {
    background: #fffde7 !important;
    color: #795548 !important;
    border: 1px solid #ffe082 !important;
}

div:has(> .rank-btn-silver) + div button[kind="primary"],
div:has(> .rank-btn-silver) + div button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(180deg, #eeeeee, #bdbdbd) !important;
    color: #212121 !important;
    border: 2px solid #757575 !important;
    font-weight: 800 !important;
}
div:has(> .rank-btn-silver) + div button[kind="secondary"],
div:has(> .rank-btn-silver) + div button[data-testid="stBaseButton-secondary"] {
    background: #fafafa !important;
    color: #616161 !important;
    border: 1px solid #bdbdbd !important;
}

div:has(> .rank-btn-bronze) + div button[kind="primary"],
div:has(> .rank-btn-bronze) + div button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(180deg, #ffcc80, #cd7f32) !important;
    color: #3e2723 !important;
    border: 2px solid #8d5524 !important;
    font-weight: 800 !important;
}
div:has(> .rank-btn-bronze) + div button[kind="secondary"],
div:has(> .rank-btn-bronze) + div button[data-testid="stBaseButton-secondary"] {
    background: #fff8e1 !important;
    color: #6d4c41 !important;
    border: 1px solid #ffcc80 !important;
}

div:has(> .rank-btn-off) + div button[kind="secondary"],
div:has(> .rank-btn-off) + div button[data-testid="stBaseButton-secondary"] {
    background: #fafafa !important;
    color: #666 !important;
    border: 1px solid #ddd !important;
}

/* Mejores terceros */
.third-pick-card {
    background: rgba(255,255,255,0.9);
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    padding: 8px 6px;
    margin-bottom: 6px;
    text-align: center;
}

.third-pick-card.is-selected {
    border-color: #2e7d32;
    background: rgba(46, 125, 50, 0.1);
    box-shadow: 0 0 0 2px rgba(46, 125, 50, 0.25);
}

/* Llaves eliminatorias */
.knockout-match-card {
    background: #fff;
    border: 2px solid #c5cae9;
    border-radius: 12px;
    padding: 10px 8px;
    margin-bottom: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.knockout-team-row {
    padding: 4px 2px;
    border-radius: 6px;
    margin: 2px 0;
}

.knockout-team-row.is-winner {
    background: linear-gradient(90deg, rgba(232,245,233,0.95), rgba(200,230,201,0.85));
    outline: 2px solid #43a047;
}

.knockout-vs {
    text-align: center;
    font-size: 0.7rem;
    font-weight: 700;
    color: #888;
    margin: 4px 0;
}

.bracket-team-row-html {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 3px 4px;
    border-radius: 4px;
    background: #f5f5f5;
    margin: 2px 0;
}

.bracket-team-row-html.winner {
    background: linear-gradient(90deg, #e8f5e9, #c8e6c9);
    outline: 2px solid #2e7d32;
}

.bracket-team-row-html .group-flag-row {
    flex: 1;
}

.bracket-team-row-html .group-flag-name {
    font-size: 0.58rem;
}

.sticker-name {
    font-size: 0.68rem;
    font-weight: 800;
    line-height: 1.2;
    margin-top: 2px;
    color: #222;
}

.sticker-meta {
    display: flex;
    flex-direction: column;
    gap: 1px;
    width: 100%;
}

.sticker-pos {
    font-size: 0.58rem;
    font-weight: 700;
    color: var(--grass-dark);
    background: #e8f5e9;
    border-radius: 4px;
    padding: 1px 4px;
}

.sticker-club {
    font-size: 0.55rem;
    color: #666;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
}

.sticker-avatar {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #ddd;
    margin-top: 2px;
}

.jersey-svg {
    display: block;
    margin: 2px auto 0;
    flex-shrink: 0;
}

.jersey-lg {
    margin: 6px auto 4px;
}

.reveal-card-full .jersey-svg {
    filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));
}

.dupe-badge {
    position: absolute;
    top: 4px;
    right: 4px;
    font-size: 0.75rem;
}

.dupe-count-badge {
    background: var(--grass-dark);
    color: #fff;
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 0.62rem;
    padding: 2px 7px;
    border-radius: 20px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    border: 1.5px solid #fff;
}

.inventory-cat-header {
    display: flex;
    align-items: baseline;
    gap: 10px;
    flex-wrap: wrap;
    margin: 1rem 0 0.4rem;
    padding-bottom: 4px;
    border-bottom: 2px solid var(--grass-light);
}

.inventory-cat-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    letter-spacing: 1px;
    color: var(--grass-dark);
}

.inventory-cat-meta {
    font-family: 'Nunito', sans-serif;
    font-size: 0.78rem;
    font-weight: 700;
    color: #666;
}

.sticker-rarity {
    font-size: 0.55rem;
    font-weight: 800;
    text-transform: uppercase;
    padding: 2px 4px;
    border-radius: 4px;
    display: inline-block;
    margin-top: 2px;
}

.rarity-basica { background: #9e9e9e; color: #fff; }
.rarity-comun { background: #4caf50; color: #fff; }
.rarity-rara { background: #2196f3; color: #fff; }
.rarity-epica { background: #9c27b0; color: #fff; }
.rarity-legendaria {
    background: linear-gradient(135deg, #ff9800, #ffd700);
    color: #333;
}

/* Animación apertura de sobre (todas las rarezas) */
.pack-scene {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1.75rem 1.25rem 2.25rem;
    background: radial-gradient(ellipse at center, rgba(0,0,0,0.45) 0%, rgba(0,0,0,0.25) 100%);
    border-radius: 20px;
    margin: 1rem 0;
    animation: packSceneIn 0.4s ease;
    overflow: visible;
    position: relative;
}

@keyframes packSceneIn {
    from { opacity: 0; transform: scale(0.92); }
    to { opacity: 1; transform: scale(1); }
}

.pack-stage {
    position: relative;
    width: 200px;
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.pack-envelope {
    position: relative;
    width: 130px;
    height: 168px;
    animation: packShake 0.55s ease-in-out 0.15s 2;
    z-index: 3;
}

.pack-body {
    position: absolute;
    inset: 0;
    background: linear-gradient(155deg, #d32f2f 0%, #8e0000 55%, #5d0000 100%);
    border-radius: 10px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.45), inset 0 2px 0 rgba(255,255,255,0.15);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
    overflow: hidden;
    animation: packBodyHide 0.35s ease 1.35s forwards;
}

.pack-shine {
    position: absolute;
    top: -40%;
    left: -30%;
    width: 60%;
    height: 180%;
    background: linear-gradient(105deg, transparent, rgba(255,255,255,0.22), transparent);
    animation: packShine 1.1s ease 0.2s;
}

@keyframes packShine {
    0% { transform: translateX(-120%) rotate(18deg); }
    100% { transform: translateX(280%) rotate(18deg); }
}

.pack-brand {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.15rem;
    color: var(--gold);
    letter-spacing: 2px;
    z-index: 1;
}

.pack-tag {
    font-family: 'Nunito', sans-serif;
    font-size: 0.55rem;
    color: rgba(255,255,255,0.85);
    letter-spacing: 1px;
    z-index: 1;
}

.pack-foil {
    font-size: 0.7rem;
    color: rgba(255,215,0,0.7);
    z-index: 1;
}

.pack-flap {
    position: absolute;
    left: 4px;
    right: 4px;
    height: 50%;
    background: linear-gradient(155deg, #e53935, #9a0007);
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.35);
    z-index: 4;
}

.pack-flap-top {
    top: 4px;
    transform-origin: top center;
    animation: packRipTop 0.55s cubic-bezier(0.4, 0, 0.2, 1) 1.05s forwards;
}

.pack-flap-bottom {
    bottom: 4px;
    transform-origin: bottom center;
    animation: packRipBottom 0.55s cubic-bezier(0.4, 0, 0.2, 1) 1.05s forwards;
}

.pack-tear {
    position: absolute;
    left: 8%;
    right: 8%;
    top: 48%;
    height: 4px;
    background: linear-gradient(90deg, transparent, #fff8, #ffd700, #fff8, transparent);
    border-radius: 2px;
    opacity: 0;
    z-index: 5;
    animation: packTearFlash 0.4s ease 0.95s forwards;
}

@keyframes packShake {
    0%, 100% { transform: rotate(0deg) scale(1); }
    15% { transform: rotate(-7deg) scale(1.02); }
    30% { transform: rotate(7deg) scale(1.02); }
    45% { transform: rotate(-5deg); }
    60% { transform: rotate(5deg); }
}

@keyframes packTearFlash {
    0% { opacity: 0; transform: scaleX(0.2); }
    40% { opacity: 1; transform: scaleX(1.1); }
    100% { opacity: 0; transform: scaleX(1); }
}

@keyframes packRipTop {
    0% { transform: rotateX(0deg) translateY(0); opacity: 1; }
    100% { transform: rotateX(-75deg) translateY(-55px) translateX(-12px); opacity: 0; }
}

@keyframes packRipBottom {
    0% { transform: rotateX(0deg) translateY(0); opacity: 1; }
    100% { transform: rotateX(75deg) translateY(55px) translateX(12px); opacity: 0; }
}

@keyframes packBodyHide {
    to { opacity: 0; transform: scale(0.85); visibility: hidden; }
}

.pack-flash {
    position: absolute;
    inset: 0;
    background: radial-gradient(circle, rgba(255,255,255,0.9) 0%, transparent 65%);
    opacity: 0;
    pointer-events: none;
    z-index: 6;
    animation: packFlashPop 0.45s ease 1.15s forwards;
}

@keyframes packFlashPop {
    0% { opacity: 0; transform: scale(0.5); }
    35% { opacity: 0.85; transform: scale(1.1); }
    100% { opacity: 0; transform: scale(1.4); }
}

.pack-paper {
    position: absolute;
    width: 18px;
    height: 24px;
    background: linear-gradient(135deg, #ffcdd2, #ef9a9a);
    border-radius: 2px;
    opacity: 0;
    z-index: 2;
}

.pack-p1 { animation: paperFly1 0.7s ease 1.2s forwards; left: 42%; top: 38%; }
.pack-p2 { animation: paperFly2 0.7s ease 1.22s forwards; left: 48%; top: 42%; }
.pack-p3 { animation: paperFly3 0.7s ease 1.18s forwards; left: 52%; top: 36%; }
.pack-p4 { animation: paperFly4 0.7s ease 1.25s forwards; left: 46%; top: 44%; }

@keyframes paperFly1 {
    0% { opacity: 1; transform: translate(0,0) rotate(0deg); }
    100% { opacity: 0; transform: translate(-45px,-60px) rotate(-40deg); }
}
@keyframes paperFly2 {
    0% { opacity: 1; transform: translate(0,0) rotate(0deg); }
    100% { opacity: 0; transform: translate(50px,-55px) rotate(35deg); }
}
@keyframes paperFly3 {
    0% { opacity: 1; transform: translate(0,0) rotate(0deg); }
    100% { opacity: 0; transform: translate(-35px,50px) rotate(25deg); }
}
@keyframes paperFly4 {
    0% { opacity: 1; transform: translate(0,0) rotate(0deg); }
    100% { opacity: 0; transform: translate(40px,45px) rotate(-30deg); }
}

.pack-reveal {
    position: relative;
    margin-top: -95px;
    z-index: 8;
}

.pack-reveal-glow {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 220px;
    height: 220px;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,215,0,0.35) 0%, transparent 70%);
    opacity: 0;
    animation: revealGlow 1.2s ease 1.35s forwards;
    pointer-events: none;
}

@keyframes revealGlow {
    0% { opacity: 0; transform: translate(-50%, -50%) scale(0.4); }
    50% { opacity: 1; }
    100% { opacity: 0.35; transform: translate(-50%, -50%) scale(1); }
}

.sticker-reveal {
    animation: stickerPop 0.85s cubic-bezier(0.34, 1.4, 0.64, 1) 1.35s both;
    position: relative;
    z-index: 2;
}

@keyframes stickerPop {
    0% { transform: scale(0) rotate(-18deg); opacity: 0; filter: blur(4px); }
    55% { transform: scale(1.12) rotate(4deg); opacity: 1; filter: blur(0); }
    100% { transform: scale(1) rotate(0deg); opacity: 1; }
}

.pack-message {
    color: #ffd700;
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    margin-top: 0.75rem;
    text-align: center;
    animation: packMsgIn 0.5s ease 1.7s both;
}

@keyframes packMsgIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

.pack-rarity-banner {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.35rem;
    letter-spacing: 2px;
    padding: 6px 18px;
    border-radius: 8px;
    margin-top: 0.5rem;
    animation: bannerPulse 1.2s ease 1.6s infinite;
}

@keyframes bannerPulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

/* Festejo épico / legendario */
.pack-tier-epica .pack-stage,
.pack-tier-legendaria .pack-stage {
    height: 230px;
}

.pack-tier-epica .pack-reveal-glow,
.pack-tier-legendaria .pack-reveal-glow {
    width: 280px;
    height: 280px;
}

.pack-tier-epica .pack-scene,
.pack-tier-legendaria .pack-scene {
    padding-bottom: 3rem;
    min-height: 520px;
}

.pack-tier-epica .pack-scene {
    background: radial-gradient(ellipse at center, rgba(156,39,176,0.35) 0%, rgba(0,0,0,0.4) 70%);
    box-shadow: 0 0 40px rgba(156,39,176,0.4);
}

.pack-tier-legendaria .pack-scene {
    background: radial-gradient(ellipse at center, rgba(255,152,0,0.4) 0%, rgba(0,0,0,0.45) 70%);
    box-shadow: 0 0 50px rgba(255,193,7,0.5);
    animation: packSceneIn 0.4s ease, legendaryBg 2s ease 1.2s infinite alternate;
    min-height: 560px;
}

.pack-tier-epica .pack-message,
.pack-tier-legendaria .pack-message {
    margin-bottom: 0.5rem;
    line-height: 1.35;
}

.pack-tier-epica .pack-rarity-banner,
.pack-tier-legendaria .pack-rarity-banner {
    margin-bottom: 0.75rem;
}

@keyframes legendaryBg {
    from { box-shadow: 0 0 40px rgba(255,193,7,0.4); }
    to { box-shadow: 0 0 65px rgba(255,215,0,0.75); }
}

.pack-tier-epica .sticker-reveal,
.pack-tier-legendaria .sticker-reveal {
    animation-duration: 1s;
}

.pack-tier-legendaria .sticker-reveal {
    animation: stickerPopLegend 1.1s cubic-bezier(0.34, 1.5, 0.64, 1) 1.35s both;
}

@keyframes stickerPopLegend {
    0% { transform: scale(0) rotate(-25deg); opacity: 0; }
    40% { transform: scale(1.25) rotate(8deg); opacity: 1; }
    70% { transform: scale(0.95) rotate(-3deg); }
    100% { transform: scale(1) rotate(0deg); opacity: 1; }
}

.pack-tier-epica .pack-message,
.pack-tier-legendaria .pack-message {
    font-size: 1.25rem;
    text-shadow: 0 0 12px rgba(255,215,0,0.6);
}

.pack-tier-legendaria .pack-message {
    font-size: 1.45rem;
    color: #fff;
    text-shadow: 0 0 18px gold, 0 0 8px #ff9800;
}

.reveal-rarity-epica .reveal-card-full {
    border-color: #9c27b0;
    box-shadow: 0 0 30px rgba(156,39,176,0.55), 0 12px 40px rgba(0,0,0,0.35);
}

.reveal-rarity-legendaria .reveal-card-full {
    border: 4px solid #ffd700;
    box-shadow: 0 0 40px rgba(255,193,7,0.7), 0 0 80px rgba(255,152,0,0.35);
    animation: legendCardShine 1.5s ease 1.8s infinite alternate;
}

@keyframes legendCardShine {
    from { filter: brightness(1); }
    to { filter: brightness(1.12); }
}

.confetti {
    position: absolute;
    top: -10px;
    width: 8px;
    height: 14px;
    border-radius: 2px;
    opacity: 0;
    animation: confettiFall 1.8s ease 1.1s forwards;
    z-index: 7;
}

.confetti.c0 { background: #ff4081; }
.confetti.c1 { background: #ffd700; }
.confetti.c2 { background: #7c4dff; }
.confetti.c3 { background: #00e676; }
.confetti.c4 { background: #ff6d00; }
.confetti.c5 { background: #00b0ff; }

@keyframes confettiFall {
    0% { opacity: 1; transform: translateY(0) rotate(0deg); }
    100% { opacity: 0; transform: translateY(220px) rotate(540deg); }
}

.reveal-card {
    width: 200px;
    padding: 16px;
    background: linear-gradient(160deg, #fff, #f5f5f5);
    border-radius: 14px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.35);
    text-align: center;
    font-family: 'Nunito', sans-serif;
    border: 3px solid var(--gold);
}

.reveal-card-full .reveal-avatar {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid var(--gold);
    margin: 8px auto;
    display: block;
}

.reveal-meta {
    font-size: 0.78rem;
    color: #555;
    margin: 4px 0 8px;
}

.reveal-card .name {
    font-weight: 800;
    font-size: 0.9rem;
    color: #222;
}

.reveal-card .team {
    font-size: 0.75rem;
    color: #666;
}

.confetti {
    position: fixed;
    width: 10px;
    height: 10px;
    animation: confettiFall 2s ease forwards;
    pointer-events: none;
    z-index: 9999;
}

@keyframes confettiFall {
    0% { transform: translateY(-20px) rotate(0deg); opacity: 1; }
    100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
}

.team-header {
    display: flex;
    align-items: center;
    gap: 10px;
    background: var(--card-bg);
    padding: 0.6rem 1rem;
    border-radius: 12px;
    margin: 0.75rem 0 0.5rem;
    box-shadow: var(--shadow);
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    color: var(--grass-dark);
}

.historical-card {
    background: var(--card-bg);
    border-radius: 14px;
    padding: 1rem;
    margin-bottom: 0.75rem;
    box-shadow: var(--shadow);
    font-family: 'Nunito', sans-serif;
    border-left: 5px solid var(--gold);
}

.historical-locked {
    opacity: 0.5;
    filter: grayscale(0.8);
    border-left-color: #999;
}

.stat-pill {
    display: inline-block;
    background: var(--grass-dark);
    color: #fff;
    padding: 4px 12px;
    border-radius: 20px;
    font-family: 'Nunito', sans-serif;
    font-size: 0.8rem;
    font-weight: 600;
    margin: 2px 4px;
}

.code-box {
    background: #1a1a2e;
    color: var(--gold);
    font-family: monospace;
    font-size: 1.1rem;
    padding: 0.75rem 1rem;
    border-radius: 10px;
    text-align: center;
    letter-spacing: 2px;
    margin: 0.5rem 0;
}

section[data-testid="stSidebar"] {
    background: var(--grass-dark) !important;
    border-right: 3px solid var(--line-white) !important;
}

section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label {
    color: #fff !important;
}

div[data-testid="stMetric"] {
    background: var(--card-bg);
    padding: 0.5rem;
    border-radius: 10px;
}

.formation-wrap {
    background: linear-gradient(180deg, #2e8f47 0%, #1b6b34 100%);
    border-radius: 16px;
    padding: 1rem;
    margin: 1rem 0;
    box-shadow: var(--shadow);
    border: 3px solid rgba(255,255,255,0.35);
}

.formation-title {
    text-align: center;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    color: #fff;
    letter-spacing: 1px;
    margin-bottom: 0.75rem;
    text-shadow: 1px 1px 4px rgba(0,0,0,0.4);
}

.formation-pitch {
    display: none;
}

.pitch-field {
    position: relative;
    width: 100%;
    max-width: 560px;
    margin: 0 auto;
    aspect-ratio: 2 / 3;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: inset 0 0 40px rgba(0,0,0,0.15);
}

.pitch-grass {
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        #2e9b4a 0px,
        #2e9b4a 28px,
        #268a40 28px,
        #268a40 56px
    );
}

.pitch-center-line {
    position: absolute;
    left: 5%;
    right: 5%;
    top: 50%;
    height: 2px;
    background: rgba(255,255,255,0.55);
}

.pitch-center-circle {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 22%;
    aspect-ratio: 1;
    transform: translate(-50%, -50%);
    border: 2px solid rgba(255,255,255,0.55);
    border-radius: 50%;
}

.pitch-box {
    position: absolute;
    left: 22%;
    right: 22%;
    height: 16%;
    border: 2px solid rgba(255,255,255,0.45);
}

.pitch-box-top {
    top: 0;
    border-top: none;
}

.pitch-box-bottom {
    bottom: 0;
    border-bottom: none;
}

.pitch-marker {
    position: absolute;
    transform: translate(-50%, -50%);
    z-index: 2;
}

.pitch-player {
    background: rgba(255,255,255,0.94);
    border-radius: 10px;
    padding: 4px 3px 5px;
    text-align: center;
    width: 68px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.28);
    display: flex;
    flex-direction: column;
    align-items: center;
}

.pitch-player.empty {
    background: rgba(255,255,255,0.2);
    border: 2px dashed rgba(255,255,255,0.55);
    color: #fff;
    min-height: 52px;
    justify-content: center;
}

.pitch-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #ddd;
}

.pitch-player .jersey-svg {
    margin: 0 auto;
}

.pitch-player .slot-name {
    font-family: 'Nunito', sans-serif;
    font-size: 0.55rem;
    font-weight: 800;
    color: #222;
    line-height: 1.1;
    margin-top: 1px;
}

.pitch-player .slot-club {
    font-size: 0.48rem;
    color: #555;
}

.pitch-player .slot-pos {
    font-size: 0.5rem;
    font-weight: 700;
}

.pitch-player .slot-empty {
    font-size: 0.6rem;
}

.pitch-line {
    display: flex;
    justify-content: center;
    align-items: flex-end;
    gap: 8px;
    flex-wrap: wrap;
}

.pitch-line-gk { margin-bottom: 4px; }
.pitch-line-def { gap: 6px; }
.pitch-line-fwd { margin-top: 2px; }

.pitch-slot {
    background: rgba(255,255,255,0.92);
    border-radius: 10px;
    padding: 6px 4px;
    text-align: center;
    width: 72px;
    min-height: 95px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
}

.pitch-slot.empty {
    background: rgba(255,255,255,0.25);
    border: 2px dashed rgba(255,255,255,0.5);
    justify-content: center;
    color: #fff;
}

.pitch-slot .slot-name {
    font-family: 'Nunito', sans-serif;
    font-size: 0.6rem;
    font-weight: 800;
    color: #222;
    line-height: 1.1;
    margin-top: 2px;
}

.pitch-slot .slot-club {
    font-size: 0.48rem;
    color: #666;
    line-height: 1.1;
}

.pitch-slot .slot-pos {
    font-size: 0.55rem;
    font-weight: 700;
}

.pitch-slot .slot-empty {
    font-size: 0.65rem;
    opacity: 0.85;
}

.formation-formation {
    text-align: center;
    color: rgba(255,255,255,0.85);
    font-family: 'Nunito', sans-serif;
    font-size: 0.8rem;
    margin-top: 0.5rem;
}

@media (max-width: 480px) {
    .pitch-slot {
        width: 62px;
        min-height: 88px;
        padding: 4px 2px;
    }
    .pitch-line {
        gap: 4px;
    }
}
</style>
"""

