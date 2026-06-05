"""Helpers de progreso por usuario (sin imports circulares)."""


def progress_user_id(progress: dict | None = None) -> int:
    if progress is not None and progress.get("user_id"):
        return int(progress["user_id"])
    from services.auth import current_user

    user = current_user()
    if not user:
        raise RuntimeError("Usuario no autenticado")
    if progress is not None:
        progress["user_id"] = user["id"]
    return user["id"]


def ensure_progress_user(progress: dict) -> dict:
    progress_user_id(progress)
    return progress
