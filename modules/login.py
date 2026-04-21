"""
modules/login.py — Page de connexion AgroSuivi
"""
import streamlit as st
from utils.auth import login


def show_login():
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 50%, #dcedc8 100%); }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style='text-align:center; padding: 2rem 0 1.5rem;'>
            <div style='font-size:4rem;'>🌱</div>
            <div style='font-family:serif; font-size:2rem; color:#1b5e20; font-weight:900;'>AgroSuivi</div>
            <div style='color:#43a047; font-size:1rem; font-weight:700; letter-spacing:0.1em;'>CAMEROUN</div>
            <div style='color:#78909c; font-size:0.85rem; margin-top:0.4rem;'>
                Plateforme nationale de données agricoles
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            st.markdown("#### 🔐 Connexion")
            email     = st.text_input("📧 Email", placeholder="votre@email.cm")
            pwd       = st.text_input("🔑 Mot de passe", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Se connecter →", use_container_width=True)

            if submitted:
                ok, msg = login(email, pwd)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        st.markdown("""
        <div style='text-align:center; margin-top:1rem; padding:1rem;
                    background:rgba(255,255,255,0.7); border-radius:12px;
                    border:1px solid #c8e6c9;'>
            <div style='font-size:0.8rem; color:#546e7a; margin-bottom:0.4rem;'>
                <b>Compte démonstration</b>
            </div>
            <div style='font-family:monospace; font-size:0.85rem; color:#2e7d32;'>
                📧 admin@agrosuivi.cm<br>
                🔑 admin2025
            </div>
        </div>
        <div style='text-align:center; margin-top:1.5rem; font-size:0.75rem; color:#90a4ae;'>
            AgroSuivi Cameroun · Projet TP 232 - Statistiques
        </div>
        """, unsafe_allow_html=True)
