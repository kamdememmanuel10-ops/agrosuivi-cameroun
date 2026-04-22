import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.db import get_all_fiches
from utils.const import COULEURS_REGIONS
def show():
     st.markdown('<div class="sec-title"> Analyses avancées</div>', unsafe_allow_html=True)
df = get_all_fiches()

if df.empty or "culture" not in df.columns:
        def show():
              
            st.info("Aucune données a analyser.")
            return


sel = st.selectbox(
    "Culture (histogramme)",
    ["Toutes"] + sorted(df["culture"].dropna().unique().tolist())
)
if df.empty:
        st.warning("Aucune donnée disponible.")
    
tab1, tab2, tab3, tab4 = st.tabs([" Distributions"," Corrélations","Comparaisons"," Classements"])
with tab1:
    c1, c2 = st.columns(2)
    with c1:
            sel = st.selectbox("Culture (histogramme)", ["Toutes"] + sorted(df["culture"].unique().tolist()), key="multiselect_cultures_dashboard")
            df_h = df if sel == "Toutes" else df[df["culture"] == sel]
            fig = px.histogram(df_h, x="rendement_kg_ha", nbins=25, color_discrete_sequence=["#2e7d32"], template="plotly_white",labels={"rendement_kg_ha":"Rendement (kg/ha)"}, 
                               title=f"Distribution rendements — {sel}")
            fig.add_vline(x=df_h["rendement_kg_ha"].mean(), line_dash="dash",
                          line_color="#f57f17", annotation_text="Moy.")
            fig.add_vline(x=df_h["rendement_kg_ha"].median(), line_dash="dot",
                          line_color="#1565c0", annotation_text="Méd.")
            fig.update_layout(height=340, margin=dict(t=50,b=10,l=0,r=0))
            st.plotly_chart(fig, use_container_width=True)
    with c2:
            fig2 = px.histogram(df, x="superficie_ha", nbins=20,
                                color_discrete_sequence=["#43a047"], template="plotly_white",
                                labels={"superficie_ha":"Superficie (ha)"},
                                title="Distribution des superficies")
            fig2.update_layout(height=340, margin=dict(t=50,b=10,l=0,r=0))
            st.plotly_chart(fig2, use_container_width=True)
        # Problèmes fréquents
        
    prob_list = []
    for p in df["problemes"].dropna():
        prob_list.extend([x.strip() for x in str(p).split(",")])
    prob_s = pd.Series(prob_list).value_counts().reset_index()
    prob_s.columns = ["Problème","Fréquence"]
    fig3 = px.bar(prob_s.head(10), x="Fréquence", y="Problème", orientation="h",
                  color="Fréquence", color_continuous_scale="RdYlGn_r",
                  title="Top 10 problèmes agricoles signalés", template="plotly_white")
    fig3.update_layout(height=380, coloraxis_showscale=False, margin=dict(t=50,b=10,l=0,r=0))
    st.plotly_chart(fig3, use_container_width=True)
with tab2:
    c1, c2 = st.columns(2)
    with c1:
        axe_x = st.selectbox("Axe X", ["superficie_ha","dose_engrais_kg_ha","acces_marche_km","prix_vente_fcfa_kg"])
    with c2:
        axe_y = st.selectbox("Axe Y", ["rendement_kg_ha","production_totale_kg","revenu_estime"])
        couleur = st.selectbox("Colorier par", ["culture","region","irrigation","formation_recue"])
        fig_sc = px.scatter(df, x=axe_x, y=axe_y, color=couleur,hover_data=["nom_exploitant","culture","region"],trendline="ols", template="plotly_white",labels={axe_x: axe_x.replace("_"," ").title(), axe_y: axe_y.replace("_"," ").title()})
        fig_sc.update_layout(height=440, margin=dict(t=20,b=10,l=0,r=0))
        st.plotly_chart(fig_sc, use_container_width=True)
with tab3:
        comp = df.groupby("region").agg(
            Nb=("rendement_kg_ha","count"),
            Rdmt_moy=("rendement_kg_ha","mean"),
            Rdmt_med=("rendement_kg_ha","median"),
            Superficie=("superficie_ha","sum"),
            Pct_irr=("irrigation", lambda x: (x=="Oui").mean()*100),
            Pct_eng=("type_engrais", lambda x: (x!="Aucun").mean()*100),
        ).reset_index()
        comp.columns = ["Région","Nb","Rdmt moy.","Rdmt méd.","Superficie (ha)","% Irrigation","% Engrais"]
        comp = comp.sort_values("Rdmt moy.", ascending=False)
        for c in comp.columns[2:]:
            comp[c] = pd.to_numeric(comp[c], errors='coerce').round(1)
        st.dataframe(comp, hide_index=True, use_container_width=True)
        # Radar
        fig_radar = go.Figure()
        max_rdmt = comp["Rdmt moy."].max() or 1
        for _, row in comp.head(5).iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=[row["Rdmt moy."]/max_rdmt*100, row["% Irrigation"], row["% Engrais"],
                   min(row["Superficie (ha)"]/comp["Superficie (ha)"].max()*100,100),
                   row["Nb"]/comp["Nb"].max()*100],
                theta=["Rendement","Irrigation","Engrais","Superficie","Couverture"],
                fill="toself", name=row["Région"], opacity=0.6,
            ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(range=[0,100])),
                                height=420, title="Radar de performance régionale", template="plotly_white")
        st.plotly_chart(fig_radar, use_container_width=True)
with tab4:
        n = st.slider("Nombre d'exploitants", 5, 30, 10)
        df["rendement_kg_ha"] = pd.to_numeric(df["rendement_kg_ha"], errors="coerce")
        top = df.nlargest(n,"rendement_kg_ha")[
            ["nom_exploitant","region","culture","superficie_ha","rendement_kg_ha","type_engrais","irrigation"]
        ].copy()
        top.index = range(1, len(top)+1)
        top.columns = ["Exploitant","Région","Culture","Superficie (ha)","Rendement (kg/ha)","Engrais","Irrigation"]
        st.dataframe(top, use_container_width=True)
