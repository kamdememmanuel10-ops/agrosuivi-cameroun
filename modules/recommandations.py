import streamlit as st
import pandas as pd
from utils.db import get_recommandations, get_all_fiches
from utils.const import (REGIONS, CULTURES, SAISONS,
 CULTURES_PAR_REGION, RENDEMENTS_REF)
ICONS_TYPE = {
 "culture": "■",
 "intrant": "■",
 "entretien":"■",
 "alerte": "■■",
 "marche": "■",
 "autre": "■",
}
COLORS_TYPE = {
 "culture": "#e8f5e9",
 "intrant": "#e3f2fd",
 "entretien":"#fff8e1",
 "alerte": "#ffebee",
 "marche": "#f3e5f5",
 "autre": "#f5f5f5",
}
BORDER_TYPE = {
 "culture": "#a5d6a7",
 "intrant": "#90caf9",
 "entretien":"#ffe082",
 "alerte": "#ef9a9a",
 "marche": "#ce93d8",
 "autre": "#e0e0e0",
}
def show():
 st.markdown('<div class="sec-title">■ Recommandations agricoles personnalisées</div>', unsafe_allow_html=True)
 st.markdown("""
 <div class="alert-info">
 ■ Le système analyse vos données et les conditions de votre région pour vous fournir
 des recommandations ciblées par culture, région et saison.
 </div><br>
 """, unsafe_allow_html=True)
 # ■■ Filtres de recommandation ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
 col1, col2, col3 = st.columns(3)
 with col1:
    region_sel  = st.selectbox(" Votre région", ["Toutes"] + REGIONS)
 with col2:
    culture_sel = st.selectbox(" Votre culture", ["Toutes"] + CULTURES)
 with col3:
    saison_sel  = st.selectbox("Saison actuelle", ["Toutes"] + SAISONS)
    recs = get_recommandations(
        region=None if region_sel == "Toutes" else region_sel,
        culture=None if culture_sel == "Toutes" else culture_sel,
        saison=None if saison_sel == "Toutes" else saison_sel,
    )
    if not recs.empty:
        st.markdown(f"**{len(recs)} recommandation(s) trouvée(s)**")
        for _, row in recs.iterrows():
            type_r = row.get("type", "autre")
            icon   = ICONS_TYPE.get(type_r, " ")
            bg     = COLORS_TYPE.get(type_r, "#f5f5f5")
            border = BORDER_TYPE.get(type_r, "#e0e0e0")
            prio   = "Urgent" if row.get("priorite",2) == 1 else " Recommandé"
            st.markdown(f"""
            <div style='background:{bg};border:1px solid {border};border-left:5px solid {border};
                        border-radius:12px;padding:1.2rem 1.5rem;margin-bottom:0.8rem;'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                    <div style='font-weight:800;color:#1b5e20;font-size:1rem;'>
                        {icon} {row["titre"]}
                    </div>
                    <div style='display:flex;gap:0.5rem;flex-shrink:0;'>
                        <span style='background:rgba(0,0,0,0.06);border-radius:12px;padding:2px 10px;font-size:0.72rem;font-weight:700;color:#546e7a;'>{row["region"]}</span>
                        <span style='background:rgba(0,0,0,0.06);border-radius:12px;padding:2px 10px;font-size:0.72rem;font-weight:700;color:#546e7a;'>{row["culture"]}</span>
                        <span style='background:rgba(0,0,0,0.06);border-radius:12px;padding:2px 10px;font-size:0.72rem;font-weight:700;color:#e65100;'>{prio}</span>
                    </div>
                </div>
                <div style='color:#37474f;font-size:0.9rem;margin-top:0.6rem;line-height:1.6;'>{row["contenu"]}</div>
                <div style='margin-top:0.5rem;font-size:0.75rem;color:#90a4ae;'>
 {row["saison"]} &nbsp;|&nbsp; Type : {type_r.capitalize()}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Aucune recommandation spécifique pour cette combinaison. Voici les conseils généraux :")
    st.markdown("---")

    st.markdown('<div class="sec-title"> Analyse automatique des performances</div>', unsafe_allow_html=True)
    df = get_all_fiches()
    if not df.empty:
        # Cultures sous-performantes
        rendements_moy = df.groupby("culture")["rendement_kg_ha"].mean()
        sous_perf = []
        sur_perf  = []
        for cult, rdmt in rendements_moy.items():
            ref = RENDEMENTS_REF.get(cult, 1000)
            ecart = (rdmt - ref) / ref * 100
            if ecart < -20:
                sous_perf.append((cult, rdmt, ref, ecart))
            elif ecart > 20:
                sur_perf.append((cult, rdmt, ref, ecart))
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("** Cultures sous-performantes (< -20% de la ref.)**")
            if sous_perf:
                for cult, rdmt, ref, ecart in sorted(sous_perf, key=lambda x: x[3])[:5]:
                    st.markdown(f"""
                    <div style='background:#ffebee;border:1px solid #ef9a9a;border-radius:10px;
                                padding:0.9rem 1.2rem;margin-bottom:0.5rem;'>
                        <b style='color:#c62828;'>
 {cult}</b><br>
                        <span style='font-size:0.85rem;color:#546e7a;'>
                            Rendement actuel: <b>{rdmt:,.0f} kg/ha</b> | Référence: <b>{ref:,} kg/ha</b><br>
                            Écart: <b style='color:#c62828;'>{ecart:.1f}%</b><br>
→ Vérifier les pratiques culturales et l'usage des intrants.
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-success">Toutes les cultures sont dans les normes !</div>', unsafe_allow_html=True)
        with col_b:
            st.markdown("**Cultures sur-performantes (> +20% de la ref.)**")
            if sur_perf:
                for cult, rdmt, ref, ecart in sorted(sur_perf, key=lambda x: -x[3])[:5]:
                    st.markdown(f"""
                    <div style='background:#e8f5e9;border:1px solid #a5d6a7;border-radius:10px;
                                padding:0.9rem 1.2rem;margin-bottom:0.5rem;'>
                        <b style='color:#1b5e20;'>
 {cult}</b><br>
                        <span style='font-size:0.85rem;color:#546e7a;'>
                            Rendement actuel: <b>{rdmt:,.0f} kg/ha</b> | Référence: <b>{ref:,} kg/ha</b><br>
                            Écart: <b style='color:#2e7d32;'>+{ecart:.1f}%</b><br>
→ Documenter et diffuser les bonnes pratiques observées.
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Pas de culture significativement sur-performante.")
        st.markdown("---")
        # Recommandation de culture par région
        st.markdown('<div class="sec-title">Meilleures cultures par région</div>', unsafe_allow_html=True)
        if region_sel != "Toutes":
            cultures_rec = CULTURES_PAR_REGION.get(region_sel, [])
            df_reg = df[df["region"] == region_sel]
            if not df_reg.empty:
                perf_reg = df_reg.groupby("culture")["rendement_kg_ha"].mean().sort_values(ascending=False)
                st.markdown(f"**Classement des cultures en {region_sel} selon vos données :**")
                for i, (cult, rdmt) in enumerate(perf_reg.head(5).items()):
                    ref = RENDEMENTS_REF.get(cult, 1000)
                    pct = (rdmt - ref) / ref * 100
                    medal = [""," "," ","4 ","5 "][i]
                    st.markdown(f"""
                    <div style='background:white;border-radius:10px;padding:0.8rem 1.2rem;
                                margin-bottom:0.4rem;box-shadow:0 1px 6px rgba(0,0,0,0.06);
                                border-left:4px solid {"#f39c12" if i==0 else "#2e7d32"};'>
                        {medal} <b style='color:#1b5e20;'>{cult}</b> —
                        <span style='color:#546e7a;'>{rdmt:,.0f} kg/ha</span>
                        <span style='color:{"#2e7d32" if pct >= 0 else "#c62828"};font-weight:700;margin-left:0.5rem;'>
                            ({("+" if pct>=0 else "")}{pct:.0f}% vs ref.)
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(f"Pas encore de données pour {region_sel}.")
                st.markdown(f"**Cultures recommandées pour {region_sel} (selon référentiels nationaux) :**")
                cultures_rec = CULTURES_PAR_REGION.get(region_sel, [])
                html = '<div style="display:flex;gap:8px;flex-wrap:wrap;">'
                for c in cultures_rec:
                    html += f"""<span style="background:#e8f5e9;color:#1b5e20;border:1px solid #a5d6a7;border-radius:20px;padding:5px 14px;font-size:0.85rem;font-weight:700;">html += "</div>"""
                st.markdown(html, unsafe_allow_html=True)
        else:
            st.markdown("**Sélectionnez une région pour des recommandations ciblées.**")
            # Tableau global top cultures par région
            if not df.empty:
                top_cult_reg = df.groupby(["region","culture"])["rendement_kg_ha"].mean().reset_index()
                top_cult_reg = top_cult_reg.loc[top_cult_reg.groupby("region")["rendement_kg_ha"].idxmax()]
                top_cult_reg.columns = ["Région","Meilleure culture","Rendement moy. (kg/ha)"]
                top_cult_reg["Rendement moy. (kg/ha)"] = top_cult_reg["Rendement moy. (kg/ha)"].round(0).astype(int)
                st.dataframe(top_cult_reg, use_container_width=True, hide_index=True)