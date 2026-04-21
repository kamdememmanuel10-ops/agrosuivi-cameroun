import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# ─────────────────────────────────────────────
#  CONFIG PAGE
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Statistiques – AGROSUIVI CAMEROUN",
    page_icon="📊",
    layout="wide",
)
# ─────────────────────────────────────────────
#  CSS CUSTOM
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;600;800&display=swap');
html, body, [class*="css"] { font-family: 'Sora', sans-serif; }
.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #16a34a, #84cc16);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}
.hero-sub {
    color: #6b7280;
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
}
.stat-card {
    background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    border: 1px solid #86efac;
    border-radius: 14px;
    padding: 1.1rem 1.4rem;
    text-align: center;
}
.stat-card .label { color: #15803d; font-size: 0.78rem; font-weight: 600; text-transform: 
uppercase; letter-spacing: .05em; }
.stat-card .value { color: #14532d; font-size: 1.8rem; font-weight: 800; }
.stat-card .unit  { color: #4ade80; font-size: 0.75rem; }
.section-title {
    font-size: 1.1rem; font-weight: 700;
    color: #15803d; margin: 1.4rem 0 0.6rem;
    border-left: 4px solid #4ade80;
    padding-left: 0.7rem;
}
</style>
""", unsafe_allow_html=True)
# ─────────────────────────────────────────────
#  IMPORT DB (compatible avec utils/db.py)
# ─────────────────────────────────────────────
try:
    from utils.db import get_connection
    def load_data():
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM fiches", conn)
        conn.close()
        return df
    df_raw = load_data()
    has_real_data = len(df_raw) > 0
except Exception:
    has_real_data = False
    df_raw = pd.DataFrame()
# ─────────────────────────────────────────────
#  DONNÉES DE DÉMO si pas de vraies données
# ─────────────────────────────────────────────
CULTURES = ["Maïs", "Manioc", "Arachide", "Tomate", "Haricot", "Plantain"]
SAISONS  = ["Saison Sèche", "Grande Saison Pluies", "Petite Saison Pluies"]
ANNEES   = [2022, 2023, 2024]
def generate_demo():
    np.random.seed(42)
    rows = []
    for annee in ANNEES:
        for saison in SAISONS:
            for culture in CULTURES:
                rows.append({
                    "culture": culture,
                    "saison": saison,
                    "annee": annee,
                    "superficie_ha": round(np.random.uniform(0.5, 10.0), 2),
                    "rendement_kg_ha": round(np.random.uniform(500, 4000), 1),
                    "production_kg": round(np.random.uniform(300, 12000), 1),
                    "cout_production": round(np.random.uniform(50000, 500000), 0),
                    "revenu": round(np.random.uniform(80000, 800000), 0),
                })
    return pd.DataFrame(rows)
# Normalise colonnes selon la structure réelle ou démo
if has_real_data:
    # Adapter selon tes vraies colonnes ici
    col_map = {
        "nom_culture": "culture",
        "saison": "saison",
        "annee": "annee",
        "superficie": "superficie_ha",
        "rendement": "rendement_kg_ha",
        "production": "production_kg",
    }
    df = df_raw.rename(columns={k: v for k, v in col_map.items() if k in df_raw.columns})
    for col in ["culture","saison","annee","superficie_ha","rendement_kg_ha","production_kg"]:
        if col not in df.columns:
            df[col] = None
else:
    df = generate_demo()
# ─────────────────────────────────────────────
#  EN-TÊTE
# ─────────────────────────────────────────────
st.markdown('<div class="hero-title">📊 Statistiques Agricoles</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Analyse des cultures par saison · Rendements · Moyennes & Médianes</div>', unsafe_allow_html=True)
if not has_real_data:
    st.info("💡Données de démonstration affichées. Saisissez des fiches réelles pour voir vos propres statistiques.")
# ─────────────────────────────────────────────
#  FILTRES
# ─────────────────────────────────────────────
with st.expander("🔽Filtres", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        cultures_dispo = sorted(df["culture"].dropna().unique().tolist())
        sel_cultures = st.multiselect("🌱Cultures", cultures_dispo, default=cultures_dispo)
    with col2:
        saisons_dispo = sorted(df["saison"].dropna().unique().tolist())
        sel_saisons = st.multiselect("🌦 Saisons", saisons_dispo, default=saisons_dispo)
    with col3:
        if "annee" in df.columns:
            annees_dispo = sorted(df["annee"].dropna().unique().tolist())
            sel_annees = st.multiselect("📅 Années", annees_dispo, default=annees_dispo)
        else:
            sel_annees = []
df_f = df[df["culture"].isin(sel_cultures) & df["saison"].isin(sel_saisons)]
if sel_annees and "annee" in df.columns:
    df_f = df_f[df_f["annee"].isin(sel_annees)]
if df_f.empty:
    st.warning("Aucune donnée pour les filtres sélectionnés.")
    st.stop()
# ─────────────────────────────────────────────
#  KPI CARDS
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">Indicateurs clés</div>', unsafe_allow_html=True)
rend_col = "rendement_kg_ha" if "rendement_kg_ha" in df_f.columns else None
prod_col  = "production_kg"  if "production_kg"  in df_f.columns else None
sup_col   = "superficie_ha"  if "superficie_ha"  in df_f.columns else None
k1, k2, k3, k4, k5 = st.columns(5)
def kpi(col, label, value, unit):
    col.markdown(f"""
    <div class="stat-card">
        <div class="label">{label}</div>
        <div class="value">{value}</div>
        <div class="unit">{unit}</div>
    </div>""", unsafe_allow_html=True)
kpi(k1, "Fiches totales", len(df_f), "enregistrements")
kpi(k2, "Cultures", df_f["culture"].nunique(), "types")
kpi(k3, "Saisons", df_f["saison"].nunique(), "périodes")
kpi(k4, "Moy. Rendement",
    f"{df_f[rend_col].mean():.0f}" if rend_col else "—", "kg/ha")
kpi(k5, "Méd. Production",
    f"{df_f[prod_col].median():.0f}" if prod_col else "—", "kg")
# ─────────────────────────────────────────────
#  GRAPHIQUE 1 — Rendement moyen par culture
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">🌾 Rendement moyen par culture</div>', unsafe_allow_html=True)
if rend_col:
    agg1 = df_f.groupby("culture")[rend_col].agg(["mean","median","std"]).reset_index()
    agg1.columns = ["culture","moyenne","médiane","écart_type"]
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=agg1["culture"], y=agg1["moyenne"],
        name="Moyenne", marker_color="#16a34a",
        error_y=dict(type='data', array=agg1["écart_type"].fillna(0), visible=True)
    ))
    fig1.add_trace(go.Scatter(
        x=agg1["culture"], y=agg1["médiane"],
        name="Médiane", mode="markers+lines",
        marker=dict(color="#f59e0b", size=10, symbol="diamond"),
        line=dict(dash="dot", color="#f59e0b")
    ))
    fig1.update_layout(
        plot_bgcolor="#f0fdf4", paper_bgcolor="white",
        xaxis_title="Culture", yaxis_title="Rendement (kg/ha)",
        legend=dict(orientation="h", y=1.1),
        height=380, margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig1, use_container_width=True)
    with st.expander("📋 Tableau — Statistiques par culture"):
        agg1_display = agg1.copy()
        for c in ["moyenne","médiane","écart_type"]:
            agg1_display[c] = agg1_display[c].round(1)
        st.dataframe(agg1_display, use_container_width=True)
# ─────────────────────────────────────────────
#  GRAPHIQUE 2 — Production par saison
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">🌦 Production totale & moyenne par saison</div>', unsafe_allow_html=True)
if prod_col:
    agg2 = df_f.groupby("saison")[prod_col].agg(["sum","mean","median"]).reset_index()
    agg2.columns = ["saison","total","moyenne","médiane"]
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(go.Bar(
        x=agg2["saison"], y=agg2["total"],
        name="Production totale (kg)", marker_color="#4ade80", opacity=0.85
    ), secondary_y=False)
    fig2.add_trace(go.Scatter(
        x=agg2["saison"], y=agg2["moyenne"],
        name="Moyenne", mode="lines+markers",
        marker=dict(color="#16a34a", size=9),
        line=dict(color="#16a34a", width=2.5)
    ), secondary_y=True)
    fig2.add_trace(go.Scatter(
        x=agg2["saison"], y=agg2["médiane"],
        name="Médiane", mode="lines+markers",
        marker=dict(color="#f97316", size=9, symbol="x"),
        line=dict(color="#f97316", width=2, dash="dash")
    ), secondary_y=True)
    fig2.update_layout(
        plot_bgcolor="#f0fdf4", paper_bgcolor="white",
        legend=dict(orientation="h", y=1.12),
        height=380, margin=dict(t=20, b=20)
    )
    fig2.update_yaxes(title_text="Production totale (kg)", secondary_y=False)
    fig2.update_yaxes(title_text="Moy. / Méd. (kg)", secondary_y=True)
    st.plotly_chart(fig2, use_container_width=True)
# ─────────────────────────────────────────────
#  GRAPHIQUE 3 — Heatmap culture × saison
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">🗺 Carte thermique : Rendement moyen (culture × saison)</div>', unsafe_allow_html=True)
if rend_col:
    pivot = df_f.pivot_table(
        index="culture", columns="saison",
        values=rend_col, aggfunc="mean"
    ).fillna(0)
    fig3 = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale="Greens",
        text=np.round(pivot.values, 0).astype(int),
        texttemplate="%{text}",
        hoverongaps=False,
        colorbar=dict(title="kg/ha")
    ))
    fig3.update_layout(
        xaxis_title="Saison", yaxis_title="Culture",
        height=350, margin=dict(t=20, b=20),
        paper_bgcolor="white"
    )
    st.plotly_chart(fig3, use_container_width=True)
# ─────────────────────────────────────────────
#  GRAPHIQUE 4 — Évolution annuelle (si colonne annee)
# ─────────────────────────────────────────────
if "annee" in df_f.columns and rend_col and df_f["annee"].nunique() > 1:
    st.markdown('<div class="section-title">📈 Évolution du rendement par année & culture</div>', unsafe_allow_html=True)
    agg4 = df_f.groupby(["annee","culture"])[rend_col].mean().reset_index()
    agg4.columns = ["annee","culture","rendement_moyen"]
    fig4 = px.line(
        agg4, x="annee", y="rendement_moyen", color="culture",
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Safe,
        labels={"rendement_moyen":"Rendement moyen (kg/ha)", "annee":"Année"}
    )
    fig4.update_layout(
        plot_bgcolor="#f0fdf4", paper_bgcolor="white",
        legend_title="Culture", height=370,
        margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig4, use_container_width=True)
# ─────────────────────────────────────────────
#  GRAPHIQUE 5 — Distribution (box plot)
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📦 Distribution des rendements par culture (Box Plot)</div>', unsafe_allow_html=True)
if rend_col:
    fig5 = px.box(
        df_f, x="culture", y=rend_col, color="saison",
        color_discrete_sequence=["#16a34a","#84cc16","#f59e0b"],
        labels={rend_col: "Rendement (kg/ha)", "culture": "Culture"},
        points="all"
    )
    fig5.update_layout(
        plot_bgcolor="#f0fdf4", paper_bgcolor="white",
        legend_title="Saison", height=400,
        margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig5, use_container_width=True)
# ─────────────────────────────────────────────
#  TABLEAU RÉCAPITULATIF GÉNÉRAL
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📄 Tableau récapitulatif général</div>', unsafe_allow_html=True)
agg_cols = {c: ["mean","median","min","max","count"]
            for c in [rend_col, prod_col, sup_col] if c}
if agg_cols:
    recap = df_f.groupby(["culture","saison"]).agg(agg_cols).round(1)
    recap.columns = [f"{c}_{s}" for c, s in recap.columns]
    recap = recap.reset_index()
    st.dataframe(recap, use_container_width=True, height=280)
# ─────────────────────────────────────────────
#  EXPORT
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">⬇ Exporter les statistiques</div>', unsafe_allow_html=True)
col_e1, col_e2 = st.columns(2)
with col_e1:
    csv = df_f.to_csv(index=False).encode("utf-8")
    st.download_button("📥Télécharger les données filtrées (CSV)",data=csv, file_name="stats_agrosuivi.csv", mime="text/csv",use_container_width=True)
with col_e2:
    if agg_cols:
        csv2 = recap.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Télécharger le récapitulatif (CSV)",data=csv2, file_name="recap_agrosuivi.csv", mime="text/csv",use_container_width=True)
def show():
    generate_demo()