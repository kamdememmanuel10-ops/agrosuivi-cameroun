import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.db import get_all_fiches
from utils.const import COULEURS_REGIONS, REGIONS, CULTURES, SAISONS
def show():
     st.markdown('<div class="sec-title"> Tableau de bord analytique</div>', unsafe_allow_html=True)
df = get_all_fiches()
if df.empty or "culture" not in df.columns:
        def show():
            st.warning("Aucune fiche disponible pour le moment.")
            return
fc = st.multiselect(
    "Cultures",
    ["Toutes"] + sorted(df["culture"].dropna().unique().tolist()),
    default=["Toutes"]
)
if df.empty:
        st.warning("Aucune donnée disponible. Saisissez d'abord des fiches.")

with st.expander(" Filtres", expanded=True):
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        fc = st.multiselect("Cultures", ["Toutes"] + sorted(df["culture"].unique().tolist()), key="multiselect_cultures_dashboard")
    with f2:
        fr = st.multiselect(" Régions", ["Toutes"] + sorted(df["region"].unique().tolist()), key="multiselect_régions_dashboard")
    with f3:
        fs = st.multiselect("Saisons", ["Toutes"] + sorted(df["saison"].unique().tolist()), key="multiselect_saisons_dashboard")
    with f4:
        fi = st.selectbox("Irrigation", ["Tous", "Oui", "Non"])

 
 
df_f = df.copy()
if fc and "Toutes" not in fc:   df_f = df_f[df_f["culture"].isin(fc)]
if fr and "Toutes" not in fr:   df_f = df_f[df_f["region"].isin(fr)]
if fs and "Toutes" not in fs:   df_f = df_f[df_f["saison"].isin(fs)]
if fi != "Tous":                 df_f = df_f[df_f["irrigation"] == fi]
if df_f.empty:
    st.info("Aucun résultat pour les filtres sélectionnés.")

if df_f.empty:
     st.warning("Aucune données pour les filtres sélectionnées.")
if 'rendement_kg_ha' in df_f.columns and not df_f.empty:
     val = f"{df_f['rendement_kg_ha'].mean():,.0f}"
else:
     val = "N/A"

k1, k2, k3, k4, k5, k6 = st.columns(6)
kpis = [
    (k1, " ", f"{len(df_f):,}", "Fiches"),
    (k2, " ", f"{df_f['rendement_kg_ha'].mean():,.0f}", "Rdmt moy. (kg/ha)"),
    (k3, " ", f"{df_f['rendement_kg_ha'].median():,.0f}", "Rdmt médian (kg/ha)"),
    (k4, " ", f"{df_f['rendement_kg_ha'].max():,.0f}", "Rdmt max (kg/ha)"),
    (k5, " ", f"{df_f['superficie_ha'].sum():,.1f}", "Superficie (ha)"),
    (k6, " ", f"{df_f['revenu_estime'].mean():,.0f}", "Revenu moy. (FCFA)"),
]
for col, icon, val, label in kpis:
    with col:
        st.markdown(f"""
            <div class="kpi-card" style="border-left-color:#43a047;">
                <div style="font-size:1.2rem;">{icon}</div>
                <div class="kpi-value" style="font-size:1.5rem;">{val}</div>
                <div class="kpi-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
        st.markdown("** Rendement moyen par culture**")
        rc = df_f.groupby("culture")["rendement_kg_ha"].agg(["mean","median","count"]).reset_index()
        rc.columns = ["culture","moy","med","nb"]
        rc = rc[rc["nb"] >= 1].sort_values("moy", ascending=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(y=rc["culture"], x=rc["moy"], orientation="h", name="Moyenne",
                             marker_color="#2e7d32", text=pd.to_numeric(rc["moy"], errors='coerce').round(0).astype(int), textposition="outside"))
        fig.add_trace(go.Scatter(y=rc["culture"], x=rc["med"], mode="markers", name="Médiane",
                                 marker=dict(size=10, color="#f57f17", symbol="diamond")))
        fig.update_layout(height=380, template="plotly_white",
                          margin=dict(t=10,b=20,l=0,r=40),
                          legend=dict(orientation="h",y=-0.12), xaxis_title="kg/ha")
        st.plotly_chart(fig, use_container_width=True)
with col2:
        st.markdown("* Rendement moyen par région**")
        rr = df_f.groupby("region")["rendement_kg_ha"].mean().reset_index()
        rr.columns = ["region","rdmt"]
        rr = rr.sort_values("rdmt", ascending=False)
        fig2 = px.bar(rr, x="region", y="rdmt", color="region",color_discrete_map=COULEURS_REGIONS, text="rdmt",template="plotly_white",labels={"rdmt": "kg/ha", "region": "Région"})
        fig2.update_traces(texttemplate="%{text:.0f}", textposition="outside")
        fig2.update_layout(height=380, showlegend=False,
                           margin=dict(t=10,b=20,l=0,r=10),
                           xaxis=dict(tickangle=-30))
        st.plotly_chart(fig2, use_container_width=True)
col3, col4 = st.columns(2)
with col3:
        st.markdown("** Boxplots des rendements par culture**")
        top_c = df_f["culture"].value_counts().head(7).index.tolist()
        df_box = df_f[df_f["culture"].isin(top_c)]
        fig3 = px.box(df_box, x="culture", y="rendement_kg_ha", color="culture",
                      color_discrete_sequence=px.colors.qualitative.G10,
                      points="outliers", template="plotly_white",
                      labels={"rendement_kg_ha": "kg/ha", "culture": ""})
        fig3.update_layout(height=360, showlegend=False,
                           margin=dict(t=10,b=20,l=0,r=10),
                           xaxis=dict(tickangle=-25))
        st.plotly_chart(fig3, use_container_width=True)
with col4:
        st.markdown("** Impact de l'engrais sur le rendement**")
        eng_df = df_f.groupby("type_engrais")["rendement_kg_ha"].agg(["mean","count"]).reset_index()
        eng_df.columns = ["engrais","moy","nb"]
        eng_df = eng_df.sort_values("moy", ascending=False)
        colors_e = ["#1b5e20" if e != "Aucun" else "#ef9a9a" for e in eng_df["engrais"]]
        fig4 = go.Figure(go.Bar(
            x=eng_df["engrais"], y=eng_df["moy"],
            text=eng_df["moy"].round(0).astype(int),
            textposition="outside",
            marker_color=colors_e,
        ))
        fig4.update_layout(height=360, template="plotly_white",
                           margin=dict(t=10,b=20,l=0,r=10),
                           yaxis_title="kg/ha", xaxis=dict(tickangle=-20))
        st.plotly_chart(fig4, use_container_width=True)
st.markdown("---")
st.markdown('<div class="sec-title"> Tableau récapitulatif par culture</div>', unsafe_allow_html=True)
summary = df_f.groupby("culture").agg(
        Fiches=("rendement_kg_ha","count"),
        Rdmt_moy=("rendement_kg_ha","mean"),
        Rdmt_med=("rendement_kg_ha","median"),
        Rdmt_max=("rendement_kg_ha","max"),
        Rdmt_min=("rendement_kg_ha","min"),
        Superficie=("superficie_ha","sum"),
        Prix_moy=("prix_vente_fcfa_kg","mean"),
        Revenu_moy=("revenu_estime","mean"),
    ).reset_index()
summary.columns = ["Culture","Nb fiches","Rdmt moy.","Rdmt médian","Max","Min",
                        "Superficie (ha)","Prix moy (FCFA/kg)","Revenu moy (FCFA)"]
for col in ["Rdmt moy.","Rdmt médian","Max","Min","Prix moy (FCFA/kg)","Revenu moy (FCFA)"]:
    summary[col] = summary[col].round(0).astype(int)
summary["Superficie (ha)"] = summary["Superficie (ha)"].round(1)
st.dataframe(summary, use_container_width=True, hide_index=True)
