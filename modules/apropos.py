import streamlit as st

def show():
    st.markdown('<div class="sec-title">ℹ️ À propos d\'AgroSuivi Cameroun</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown("""
        ### 🌱 Mission
        **AgroSuivi Cameroun** est une plateforme numérique dédiée à la **collecte, gestion et analyse**
        des données agricoles des 10 régions du Cameroun.

        Elle a été développée dans le cadre du **Projet TP 232 – Statistiques** et vise à fournir
        aux étudiants, entrepreneurs agricoles, superviseurs régionaux et décideurs un outil moderne
        de suivi des exploitations agricoles à l'échelle nationale.

        ---

        ### 🎯 Objectifs
        - Centraliser la collecte de fiches agricoles terrain
        - Analyser les rendements, superficies et pratiques culturales
        - Visualiser les données sur une carte interactive
        - Générer des recommandations personnalisées par région et culture
        - Exporter les données et produire des rapports PDF professionnels

        ---

        ### 🗂️ Fonctionnalités principales
        - **Saisie des données** — Formulaire complet de collecte agricole (exploitant, culture, intrants, problèmes)
        - **Tableau de bord** — KPIs et graphiques analytiques avec filtres dynamiques
        - **Carte interactive** — Visualisation géographique des exploitations par région
        - **Analyses avancées** — Distributions, corrélations, comparaisons, classements
        - **Statistiques** — Données climatiques et analyses temporelles
        - **Recommandations** — Conseils personnalisés basés sur les performances réelles
        - **Export & Rapports PDF** — Téléchargement CSV et génération de rapports PDF complets

        ---

        ### 🛠️ Technologies utilisées
        - **Streamlit** — Interface web interactive
        - **Supabase** — Base de données PostgreSQL cloud
        - **Plotly** — Visualisations interactives
        - **ReportLab** — Génération de rapports PDF
        - **Pandas / NumPy** — Traitement et analyse des données

        ---

        ### 👨‍💻 Auteur
        **KAMDEM Emmanuel**
        📧 kamdememmanuel10@gmail.com
        🐙 [github.com/kamdememmanuel10-ops](https://github.com/kamdememmanuel10-ops/)

        **Projet TP 232 – Statistiques · Avril 2025**
        """)

    with c2:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#1b5e20,#2e7d32);border-radius:16px;
                    padding:1.5rem;color:white;text-align:center;'>
            <div style='font-size:3rem;'>🌍</div>
            <h3 style='font-family:Playfair Display,serif;margin:0.5rem 0;'>Cameroun</h3>
            <p style='opacity:0.8;font-size:0.85rem;'>10 régions · 475 000 km²</p>
            <hr style='border-color:rgba(255,255,255,0.2);margin:1rem 0;'>
            <div style='font-size:0.82rem;line-height:1.8;'>
                🍫 Cacao · ☕ Café · 🌽 Maïs<br>
                🍠 Manioc · 🍌 Plantain<br>
                🌿 Coton · 🌴 Palmier à huile
            </div>
            <hr style='border-color:rgba(255,255,255,0.2);margin:1rem 0;'>
            <div style='font-size:0.78rem;opacity:0.75;line-height:1.6;'>
                AgroSuivi v2.0 · Avril 2025<br>
                Fait avec ❤️ pour les agriculteurs<br><br>
                <b>TP 232 – Statistiques</b>
            </div>
        </div>

        <br>

        <div style='background:white;border-radius:12px;padding:1.2rem;
                    box-shadow:0 2px 10px rgba(0,0,0,0.07);border-top:3px solid #43a047;'>
            <div style='font-weight:800;color:#1b5e20;margin-bottom:0.8rem;'>📊 Données couvertes</div>
            <div style='font-size:0.83rem;color:#546e7a;line-height:1.9;'>
                ✅ 20 cultures suivies<br>
                ✅ 10 régions du Cameroun<br>
                ✅ Rendements & superficies<br>
                ✅ Intrants & pratiques<br>
                ✅ Données climatiques<br>
                ✅ Rapports PDF générés<br>
                ✅ Export CSV disponible
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='text-align:center;padding:1rem;background:#e8f5e9;border-radius:12px;
                border:1px solid #a5d6a7;'>
        <span style='color:#1b5e20;font-weight:700;'>🌱 AgroSuivi Cameroun</span>
        &nbsp;·&nbsp;
        <span style='color:#546e7a;font-size:0.88rem;'>Application de collecte de données agricoles</span>
        &nbsp;·&nbsp;
        <span style='color:#43a047;font-size:0.85rem;font-weight:700;'>Projet TP 232 – Statistiques</span>
    </div>
    """, unsafe_allow_html=True)