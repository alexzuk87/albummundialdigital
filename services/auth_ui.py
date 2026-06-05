"""Pantallas de autenticación."""

import streamlit as st

from services.auth import (
    get_google_auth_url,
    google_oauth_configured,
    handle_google_callback,
    login_session,
    login_user,
    register_user,
)


def try_google_login() -> bool:
    user, err = handle_google_callback()
    if err:
        st.error(err)
        return False
    if user:
        login_session(user)
        st.rerun()
        return True
    return False


def render_auth_page() -> None:
    st.markdown(
        '<p class="main-header">⚽ ÁLBUM MUNDIAL DIGITAL 2026</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="sub-header">Iniciá sesión para guardar tu álbum en la nube</p>',
        unsafe_allow_html=True,
    )

    tab_login, tab_register = st.tabs(["Iniciar sesión", "Registrarse"])

    with tab_login:
        with st.form("login_form"):
            identifier = st.text_input("Usuario o email")
            password = st.text_input("Contraseña", type="password")
            submitted = st.form_submit_button("Entrar", type="primary", use_container_width=True)
            if submitted:
                user, err = login_user(identifier, password)
                if err:
                    st.error(err)
                else:
                    login_session(user)
                    st.rerun()

    with tab_register:
        with st.form("register_form"):
            email = st.text_input("Email")
            username = st.text_input("Nombre de usuario")
            password = st.text_input("Contraseña", type="password")
            password2 = st.text_input("Confirmar contraseña", type="password")
            submitted = st.form_submit_button("Crear cuenta", type="primary", use_container_width=True)
            if submitted:
                if password != password2:
                    st.error("Las contraseñas no coinciden.")
                else:
                    user, err = register_user(email, username, password)
                    if err:
                        st.error(err)
                    else:
                        login_session(user)
                        st.success("¡Cuenta creada! Bienvenido al álbum.")
                        st.rerun()

    st.divider()
    st.markdown("#### O continuá con Google")
    if google_oauth_configured():
        url = get_google_auth_url()
        if url:
            st.link_button("🔐 Iniciar sesión con Gmail", url, use_container_width=True)
    else:
        st.info(
            "Para habilitar login con Gmail, configurá `.streamlit/secrets.toml` "
            "usando el archivo `secrets.toml.example`."
        )
