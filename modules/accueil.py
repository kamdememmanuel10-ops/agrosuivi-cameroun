import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.db import get_all_fiches, get_stats_rapides
from utils.const import COULEURS_REGIONS
def show():
      st.markdown("""
    <div class="main-header">
        <div>
            <h1>
 AgroSuivi Cameroun</h1>
            <p>Application de collecte de données agricoles</p>
        </div>
        <div style='text-align:right;'>
            <div class="badge-live">
 Système actif</div>
            <div style='font-size:0.78rem; opacity:0.8; margin-top:0.5rem;'>
        </div>
    </div>
    """, unsafe_allow_html=True)
df = get_all_fiches()
c1, c2, c3, c4, c5 = st.columns(5)
metrics = [
        (c1, " ", f"{len(df):,}", "Fiches collectées", "+5 cette semaine"),
        (c2, " ", f"{df['rendement_kg_ha'].mean():,.0f}" if not df.empty else "—", "Rendement moyen (kg/ha)", ""),
        (c3, " ", f"{df['superficie_ha'].sum():,.1f}" if not df.empty else "—", "Superficie totale (ha)", ""),
        (c4, " ", f"{df['culture'].nunique()}" if not df.empty else "0", "Cultures suivies", "/ 20 cultures"),
        (c5, " ", f"{df['region'].nunique()}" if not df.empty else "0", "Régions couvertes", "/ 10 régions"),
    ]
for col, icon, val, label, delta in metrics:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div style='font-size:1.6rem;'>{icon}</div>
            <div class="kpi-value">{val}</div>
            <div class="kpi-label">{label}</div>
            {'<div class="kpi-delta">' + delta + '</div>' if delta else ''}
        </div>
        """, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
col_l, col_r = st.columns([3, 2])
with col_l:
    st.markdown('<div class="sec-title"> Rendement moyen par région</div>', unsafe_allow_html=True)
    if not df.empty:
        rdmt_reg = df.groupby("region")["rendement_kg_ha"].mean().reset_index()
        rdmt_reg.columns = ["Région", "Rendement moyen (kg/ha)"]
        rdmt_reg = rdmt_reg.sort_values("Rendement moyen (kg/ha)", ascending=False)
        fig = px.bar(
            rdmt_reg, x="Région", y="Rendement moyen (kg/ha)",
            color="Région", color_discrete_map=COULEURS_REGIONS,
            text="Rendement moyen (kg/ha)",
            template="plotly_white",
        )
        fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
        fig.update_layout(height=320, showlegend=False, margin=dict(t=10,b=10,l=0,r=0),
                          xaxis=dict(tickangle=-30))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée disponible.")
with col_r:
    st.markdown('<div class="sec-title"> Répartition des cultures</div>', unsafe_allow_html=True)
    if not df.empty:
        cult_c = df["culture"].value_counts().head(8)
        fig2 = px.pie(values=cult_c.values, names=cult_c.index,
                      color_discrete_sequence=px.colors.sequential.Greens_r,
                      hole=0.45, template="plotly_white")
        fig2.update_layout(height=320, margin=dict(t=10,b=10,l=0,r=0),
                           legend=dict(font=dict(size=11)))
        fig2.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig2, use_container_width=True)
st.markdown('<div class="sec-title"> Dernières fiches collectées</div>', unsafe_allow_html=True)
if not df.empty:
    recent = df.head(8)[["code_fiche","date_collecte","region","culture",
                          "rendement_kg_ha","superficie_ha","nom_exploitant"]].copy()
    recent.columns = ["Code","Date","Région","Culture","Rdmt (kg/ha)","Superficie (ha)","Exploitant"]
    st.dataframe(recent, use_container_width=True, hide_index=True)
else:
    st.info("Aucune donnée pour le moment.")
st.markdown('<div class="sec-title"> Guide de démarrage rapide</div>', unsafe_allow_html=True)
g1, g2, g3, g4 = st.columns(4)
guides = [
    (g1, "1", "Saisir une fiche", "Cliquez sur Saisie des données pour enregistrer une nouvelle exploitation agricole."),
    (g2, "2 ", "Explorer la carte", "Visualisez les cultures et le climat de chaque région sur."),
    (g3, "3 ", "Analyser", "Consultez les graphiques et statistiques dans."),
    (g4, "4 ", "Recommandations", "Obtenez des conseils personnalisés par région et culture dans."),

 
]
for col, num, titre, desc in guides:
    with col:
        st.markdown(f"""
        <div style='background:white;border-radius:12px;padding:1.2rem;
                    box-shadow:0 2px 10px rgba(0,0,0,0.06);border-top:3px solid #43a047;
                    height:170px;'>
            <div style='font-size:1.5rem;'>{num}</div>
            <div style='font-weight:800;color:#1b5e20;margin:.4rem 0 .3rem;'>{titre}</div>
            <div style='font-size:0.82rem;color:#546e7a;line-height:1.5;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)