"""Autenticación: registro, login y Google OAuth."""

import re
import secrets
from urllib.parse import urlencode

import bcrypt
import streamlit as st

from services.database import (
    create_user,
    get_user_by_email,
    get_user_by_google_id,
    get_user_by_id,
    get_user_by_username,
    init_db,
    link_google_account,
)

init_db()

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), password_hash.encode())
    except ValueError:
        return False


def validate_registration(email: str, username: str, password: str) -> str | None:
    if not EMAIL_RE.match(email):
        return "Email inválido."
    if len(username.strip()) < 3:
        return "El usuario debe tener al menos 3 caracteres."
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return "El usuario solo puede contener letras, números y guión bajo."
    if len(password) < 6:
        return "La contraseña debe tener al menos 6 caracteres."
    if get_user_by_email(email):
        return "Ese email ya está registrado."
    if get_user_by_username(username):
        return "Ese nombre de usuario ya existe."
    return None


def register_user(email: str, username: str, password: str) -> tuple[dict | None, str | None]:
    err = validate_registration(email, username, password)
    if err:
        return None, err
    user_id = create_user(email, username, hash_password(password))
    user = get_user_by_id(user_id)
    return user, None


def login_user(identifier: str, password: str) -> tuple[dict | None, str | None]:
    identifier = identifier.strip()
    user = get_user_by_email(identifier) if "@" in identifier else get_user_by_username(identifier)
    if not user or not user.get("password_hash"):
        return None, "Usuario o contraseña incorrectos."
    if not verify_password(password, user["password_hash"]):
        return None, "Usuario o contraseña incorrectos."
    return user, None


def login_session(user: dict) -> None:
    st.session_state.user = {
        "id": user["id"],
        "email": user["email"],
        "username": user["username"],
        "avatar_url": user.get("avatar_url"),
    }
    st.session_state.pop("progress", None)


def logout_user() -> None:
    for key in ("user", "progress", "show_animation", "current_trivia_id", "trivia_round", "trivia_flash"):
        st.session_state.pop(key, None)


def is_logged_in() -> bool:
    return st.session_state.get("user") is not None


def current_user() -> dict | None:
    return st.session_state.get("user")


def google_oauth_configured() -> bool:
    try:
        return bool(st.secrets.get("google", {}).get("client_id"))
    except Exception:
        return False


def get_google_auth_url() -> str | None:
    if not google_oauth_configured():
        return None
    g = st.secrets["google"]
    state = secrets.token_urlsafe(16)
    st.session_state.oauth_state = state
    params = {
        "client_id": g["client_id"],
        "redirect_uri": g["redirect_uri"],
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "online",
        "prompt": "select_account",
        "state": state,
    }
    return "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)


def handle_google_callback() -> tuple[dict | None, str | None]:
    params = st.query_params
    code = params.get("code")
    state = params.get("state")
    error = params.get("error")

    if error:
        return None, f"Google OAuth: {error}"
    if not code:
        return None, None

    expected = st.session_state.pop("oauth_state", None)
    if expected and state != expected:
        return None, "Estado OAuth inválido. Intentá de nuevo."

    try:
        from google_auth_oauthlib.flow import Flow

        g = st.secrets["google"]
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": g["client_id"],
                    "client_secret": g["client_secret"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [g["redirect_uri"]],
                }
            },
            scopes=["openid", "https://www.googleapis.com/auth/userinfo.email",
                    "https://www.googleapis.com/auth/userinfo.profile"],
        )
        flow.redirect_uri = g["redirect_uri"]
        flow.fetch_token(code=code)
        creds = flow.credentials
        import requests

        resp = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {creds.token}"},
            timeout=10,
        )
        resp.raise_for_status()
        info = resp.json()
    except Exception as exc:
        return None, f"No se pudo completar el login con Google: {exc}"

    google_id = info["id"]
    email = info["email"]
    name = info.get("name", email.split("@")[0])
    avatar = info.get("picture")

    user = get_user_by_google_id(google_id)
    if not user:
        existing = get_user_by_email(email)
        if existing:
            link_google_account(existing["id"], google_id, avatar)
            user = get_user_by_id(existing["id"])
        else:
            base_username = re.sub(r"[^a-zA-Z0-9_]", "", name.lower())[:20] or "user"
            username = base_username
            n = 1
            while get_user_by_username(username):
                username = f"{base_username}{n}"
                n += 1
            uid = create_user(email, username, password_hash=None, google_id=google_id, avatar_url=avatar)
            user = get_user_by_id(uid)

    st.query_params.clear()
    return user, None
