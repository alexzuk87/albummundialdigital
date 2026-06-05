"""Hooks post-cambio de progreso (evita importaciones circulares)."""

from services.achievements import check_and_unlock
from services.progress_utils import progress_user_id
from services.storage import save_progress


def after_progress_change(progress: dict, event: str | None = None) -> list[dict]:
    user_id = progress_user_id(progress)
    newly = check_and_unlock(user_id, progress, event=event)
    save_progress(user_id, progress)
    return newly
