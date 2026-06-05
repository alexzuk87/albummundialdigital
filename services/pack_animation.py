"""Animación de apertura de sobre al desbloquear figuritas."""

from services.constants import RARITY_LABELS

_CELEBRATION_MSG = {
    "basica": "¡Nueva figurita en tu álbum!",
    "comun": "¡Buen hallazgo! Nueva figurita.",
    "rara": "¡Figurita rara desbloqueada!",
    "epica": "⭐ ¡FIGURITA ÉPICA! ¡Qué suerte!",
    "legendaria": "👑 ¡LEYENDA! ¡Figurita legendaria!",
}

_CONFETTI = "".join(
    f'<i class="confetti c{i % 6}" style="left:{(i * 17) % 100}%;animation-delay:{i * 0.07:.2f}s"></i>'
    for i in range(24)
)


def build_pack_opening_html(sticker: dict, reveal_card: str) -> str:
    rarity = sticker.get("rarity", "comun")
    label = RARITY_LABELS.get(rarity, rarity)
    msg = _CELEBRATION_MSG.get(rarity, _CELEBRATION_MSG["comun"])
    tier = rarity if rarity in ("epica", "legendaria") else "normal"
    extra = _CONFETTI if rarity in ("epica", "legendaria") else ""
    badge = (
        f'<div class="pack-rarity-banner rarity-{rarity}">{label}</div>'
        if rarity in ("epica", "legendaria")
        else ""
    )

    return f"""
<div class="pack-scene pack-tier-{tier} pack-rarity-{rarity}">
    <div class="pack-stage">
        <div class="pack-envelope">
            <div class="pack-body">
                <div class="pack-shine"></div>
                <span class="pack-brand">MUNDIAL 2026</span>
                <span class="pack-tag">SOBRE OFICIAL</span>
                <span class="pack-foil">★ ★ ★</span>
            </div>
            <div class="pack-flap pack-flap-top"></div>
            <div class="pack-flap pack-flap-bottom"></div>
            <div class="pack-tear"></div>
        </div>
        <div class="pack-flash"></div>
        <div class="pack-paper pack-p1"></div>
        <div class="pack-paper pack-p2"></div>
        <div class="pack-paper pack-p3"></div>
        <div class="pack-paper pack-p4"></div>
        {extra}
    </div>
    <div class="pack-reveal">
        <div class="pack-reveal-glow"></div>
        <div class="sticker-reveal reveal-rarity-{rarity}">
            {reveal_card}
        </div>
    </div>
    {badge}
    <p class="pack-message">{msg}</p>
</div>
"""
