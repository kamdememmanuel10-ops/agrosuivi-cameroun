import streamlit as st
from utils.db import verify_user


def login(email: str, pwd: str):
    """Authentifie l'utilisateur et stocke la session."""
    if not email or not pwd:
        return False, "Email et mot de passe requis."
    user = verify_user(email.strip(), pwd)
    if user:
        st.session_state["user"] = user
        st.session_state["logged_in"] = True
        return True, f"Bienvenue, {user['nom']} !"
    return False, "Email ou mot de passe incorrect."


def logout():
    st.session_state.clear()


def is_logged_in():
    return st.session_state.get("logged_in", False)


def get_current_user():
    return st.session_state.get("user", {})
