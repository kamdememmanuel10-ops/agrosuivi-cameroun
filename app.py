# ============================================================
#                 🌱 AgroSuivi Cameroun
#  Application de collecte de données agricoles
#  Version Supabase — Streamlit Cloud
# ============================================================

import streamlit as st
from utils.db import init_db
from utils.auth import is_logged_in
from supabase import create_client

# ── Configuration globale ─────────────────────────────────────
st.set_page_config(
    page_title="AgroSuivi Cameroun",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Enrregistrements des données
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
OPENWEATHER_KEY = st.secrets["OPENWEATHER_KEY"]

# ── Initialisation DB ─────────────────────────────────────────
init_db()

# ── CSS global ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Playfair+Display:wght@700;900&display=swap');

html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a3a1a 0%, #2d5a1b 50%, #1b5e20 100%);
    border-right: 2px solid #43a047;
}
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p { color: #e8f5e9 !important; }

[data-testid="stSidebar"] .stButton button {
    background: rgba(255,255,255,0.08) !important;
    color: #e8f5e9 !important;
    border: 1px solid rgba(165,214,167,0.35) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
    text-align: left !important;
    width: 100% !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(67,160,71,0.4) !important;
    border-color: #81c784 !important;
}

.main-header {
    background: linear-gradient(135deg, #1b5e20, #2e7d32, #388e3c);
    border-radius: 16px; padding: 1.8rem 2.5rem;
    margin-bottom: 1.5rem; color: white;
    box-shadow: 0 8px 32px rgba(27,94,32,0.4);
    display: flex; align-items: center; justify-content: space-between;
}
.main-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2rem; margin: 0; letter-spacing: -0.5px;
}
.main-header p { margin: 0.3rem 0 0; opacity: 0.85; font-size: 0.9rem; }
.badge-live {
    background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3);
    border-radius: 20px; padding: 0.35rem 1rem; font-size: 0.8rem; font-weight: 700;
}

.kpi-card {
    background: white; border-radius: 14px; padding: 1.3rem 1.5rem;
    box-shadow: 0 2px 16px rgba(0,0,0,0.07); border-left: 5px solid #2e7d32;
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover { transform: translateY(-3px); box-shadow: 0 6px 24px rgba(0,0,0,0.12); }
.kpi-value { font-family: 'Playfair Display', serif; font-size: 2rem; color: #1b5e20; font-weight: 700; }
.kpi-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; color: #78909c; font-weight: 700; }
.kpi-delta { font-size: 0.8rem; color: #43a047; font-weight: 700; margin-top: 0.1rem; }

.sec-title {
    font-family: 'Playfair Display', serif; font-size: 1.4rem; color: #1b5e20;
    padding-bottom: 0.5rem; border-bottom: 3px solid #a5d6a7; margin-bottom: 1.2rem;
}

.alert-success { background: #e8f5e9; border: 1px solid #a5d6a7; border-radius: 10px; padding: 0.9rem 1.2rem; color: #2e7d32; font-weight: 600; }
.alert-info    { background: #e3f2fd; border: 1px solid #90caf9; border-radius: 10px; padding: 0.9rem 1.2rem; color: #1565c0; font-weight: 600; }
.alert-warning { background: #fff8e1; border: 1px solid #ffe082; border-radius: 10px; padding: 0.9rem 1.2rem; color: #e65100; font-weight: 600; }

.stButton button {
    background: linear-gradient(135deg, #2e7d32, #43a047) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    font-weight: 700 !important; padding: 0.55rem 1.8rem !important;
    box-shadow: 0 4px 12px rgba(46,125,50,0.3) !important; transition: all 0.2s !important;
}
.stButton button:hover { transform: translateY(-2px) !important; }
.stDownloadButton button { background: linear-gradient(135deg, #1565c0, #1976d2) !important; }

[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
[data-testid="metric-container"] {
    background: white; border-radius: 12px; padding: 1rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06); border-top: 4px solid #43a047;
}

.footer { text-align: center; padding: 1.5rem; color: #90a4ae; font-size: 0.8rem;
          border-top: 1px solid #e8f5e9; margin-top: 2rem; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #f1f8e9; }
::-webkit-scrollbar-thumb { background: #a5d6a7; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ── Authentification ──────────────────────────────────────────
#if not is_logged_in():
 #   from modules.login import show_login
  #  show_login()
   # st.stop()

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:1.2rem 0 0.5rem;'>
        <div style='font-size:2.8rem;'>🌱</div>
        <div style='font-family:Playfair Display,serif; font-size:1.4rem;
                    color:#e8f5e9; font-weight:700;'>AgroSuivi</div>
        <div style='font-size:0.75rem; color:#a5d6a7; margin-top:0.2rem;'>
            Cameroun · v2.0
        </div>
    </div>
    <hr style='border-color:rgba(165,214,167,0.25); margin:0.8rem 0;'>
    """, unsafe_allow_html=True)

    user = st.session_state.get("user", {})
    st.markdown(f"""
    <div style='background:rgba(255,255,255,0.08); border-radius:10px;
                padding:0.8rem 1rem; margin-bottom:0.8rem;'>
        <div style='font-size:0.75rem; color:#a5d6a7;'>Connecté en tant que</div>
        <div style='color:#e8f5e9; font-weight:700; font-size:0.95rem;'>
            👤 {user.get('nom', 'Utilisateur')}
        </div>
        <div style='font-size:0.72rem; color:#81c784;'>{user.get('role', 'Agent').capitalize()}</div>
    </div>
    """, unsafe_allow_html=True)

    PAGES = {
        "🏠  Accueil":              "accueil",
        "📝  Saisie des données":   "saisie",
        "🗺️  Carte interactive":    "carte",
        "📊  Tableau de bord":      "dashboard",
        "🔬  Analyses":             "analyses",
        "📈  Statistiques":         "statistiques",
        "💡  Recommandations":      "recommandations",
        "📥  Export & Rapports PDF":"export",
        "ℹ️   À propos":            "apropos",
    }

    if "page" not in st.session_state:
        st.session_state["page"] = "accueil"

    for label, key in PAGES.items():
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state["page"] = key
            st.rerun()

    st.markdown("<hr style='border-color:rgba(165,214,167,0.2);'>", unsafe_allow_html=True)

    from utils.db import get_stats_rapides
    stats = get_stats_rapides()
    st.markdown(f"""
    <div style='background:rgba(255,255,255,0.06); border-radius:10px;
                padding:0.9rem; font-size:0.82rem;'>
        <div style='color:#a5d6a7; margin-bottom:0.5rem; font-weight:700;
                    font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em;'>
            Statistiques
        </div>
        <div style='color:#e8f5e9; margin-bottom:0.3rem;'>
            📋 <b>{stats['nb_fiches']}</b> fiches
        </div>
        <div style='color:#e8f5e9; margin-bottom:0.3rem;'>
            🌾 <b>{stats['nb_cultures']}</b> cultures
        </div>
        <div style='color:#e8f5e9;'>
            📍 <b>{stats['nb_regions']}</b> régions
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Se déconnecter", use_container_width=True):
        from utils.auth import logout
        logout()
        st.rerun()

# ── Router ────────────────────────────────────────────────────
page = st.session_state.get("page", "accueil")

if page == "accueil":
    from modules.accueil import show; show()
elif page == "saisie":
    from modules.saisie import show; show()
elif page == "carte":
    from modules.carte import show; show()
elif page == "dashboard":
    from modules.dashboard import show; show()
elif page == "analyses":
    from modules.analyses import show; show()
elif page == "statistiques":
    from modules.statistiques import show; show()
elif page == "recommandations":
    from modules.recommandations import show; show()
elif page == "export":
    from modules.export_page import show; show()
elif page == "apropos":
    from modules.apropos import show; show()

# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🌱 AgroSuivi Cameroun · Application de collecte de données agricoles ·
    Projet TP 232 – Statistiques
</div>
""", unsafe_allow_html=True)
