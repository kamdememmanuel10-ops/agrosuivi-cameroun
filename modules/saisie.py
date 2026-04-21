import streamlit as st
from datetime import date
from utils.db import insert_fiche, get_stats_rapides, get_fiche_by_id
from utils.const import (CULTURES, REGIONS, SAISONS, TYPES_SOL, ENGRAIS, PROBLEMES, RENDEMENTS_REF)


def show():
    st.markdown('<div class="sec-title">📝 Formulaire de collecte agricole</div>',
                unsafe_allow_html=True)

    # ── Succès après enregistrement ──────────────────────────
    if st.session_state.get("fiche_ok"):
        code    = st.session_state.pop("fiche_ok")
        fiche_id = st.session_state.pop("fiche_id", None)
        st.markdown(f"""
        <div class="alert-success">
            ✅ Fiche <b>{code}</b> enregistrée avec succès !
        </div><br>
        """, unsafe_allow_html=True)

        # Bouton téléchargement PDF immédiat
        if fiche_id:
            _bouton_pdf_direct(fiche_id, code)

    st.markdown("""
    <div class="alert-info">
        ℹ️ Les champs marqués <b>*</b> sont obligatoires.
        La production totale et le revenu estimé sont calculés automatiquement.
    </div><br>
    """, unsafe_allow_html=True)

    # ── Formulaire ────────────────────────────────────────────
    with st.form("saisie_form", clear_on_submit=True):

        # SECTION 1 — Identification
        with st.expander("👤 SECTION 1 — Identification de l'exploitant", expanded=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                nom         = st.text_input("Nom & Prénom *", placeholder="Ex: Jean Mbarga")
                region      = st.selectbox("Région *", ["— Choisir —"] + REGIONS)
            with c2:
                telephone   = st.text_input("Téléphone", placeholder="6XX XXX XXX")
                departement = st.text_input("Département", placeholder="Ex: Mfoundi")
            with c3:
                arrondissement = st.text_input("Arrondissement", placeholder="Ex: Yaoundé 1er")
                date_col    = st.date_input("📅 Date de visite *", value=date.today())

            c4, c5 = st.columns(2)
            with c4:
                lat = st.number_input("Latitude GPS", min_value=-5.0, max_value=13.5,
                                      value=0.0, step=0.0001, format="%.4f")
            with c5:
                lon = st.number_input("Longitude GPS", min_value=8.0, max_value=16.5,
                                      value=8.0, step=0.0001, format="%.4f")
            c6, c7 = st.columns(2)
            with c6:
                membre_coop = st.radio("Membre d'une coopérative ?", ["Non", "Oui"], horizontal=True)
            with c7:
                formation   = st.radio("Formation agricole reçue ?", ["Non", "Oui"], horizontal=True)

        # SECTION 2 — Culture
        with st.expander("🌱 SECTION 2 — Informations sur la culture", expanded=True):
            c8, c9, c10 = st.columns(3)
            with c8:
                culture   = st.selectbox("Culture pratiquée *", ["— Choisir —"] + CULTURES)
                variete   = st.text_input("Variété", placeholder="Ex: CMS 8704")
            with c9:
                saison    = st.selectbox("Saison *", ["— Choisir —"] + SAISONS)
                age_plant = st.number_input("Âge plantation (ans)", 0, 50, 1)
            with c10:
                ref_rdmt  = int(RENDEMENTS_REF.get(
                    culture if culture != "— Choisir —" else "Maïs", 1000))
                superficie = st.number_input("Superficie (ha) *", 0.01, 1000.0,
                                             1.0, 0.1, format="%.2f")
                rendement  = st.number_input(
                    f"📊 Rendement (kg/ha) *\n_Réf: {ref_rdmt:,} kg/ha_",
                    0, 200000, 1000, 50)

            c11, c12 = st.columns(2)
            with c11:
                type_sol    = st.selectbox("🪨 Type de sol", TYPES_SOL)
                qualite_sol = st.select_slider(
                    "Qualité du sol",
                    ["Très peu fertile", "Peu fertile", "Moyennement fertile",
                     "Fertile", "Très fertile"],
                    value="Fertile")
            with c12:
                prix_vente   = st.number_input("💰 Prix de vente (FCFA/kg)", 0, 50000, 200, 10)
                acces_marche = st.number_input("🛣️ Distance au marché (km)", 0, 500, 10)

        # SECTION 3 — Intrants
        with st.expander("🧪 SECTION 3 — Intrants et pratiques", expanded=False):
            c13, c14, c15 = st.columns(3)
            with c13:
                engrais  = st.selectbox("Type d'engrais", ENGRAIS)
                dose_eng = st.number_input("Dose engrais (kg/ha)", 0, 1000, 0, 10,
                                           disabled=(engrais == "Aucun"))
            with c14:
                irrigation = st.radio("Irrigation ?", ["Non", "Oui"], horizontal=True)
                source_eau = st.selectbox("Source d'eau",
                                          ["—", "Pluie", "Cours d'eau", "Forage",
                                           "Barrage", "Puits"])
            with c15:
                main_oeuvre = st.selectbox("Main-d'œuvre",
                                           ["Familiale", "Salariée", "Mixte"])
                nb_actifs   = st.number_input("Nombre d'actifs", 1, 50, 2)

        # SECTION 4 — Problèmes
        with st.expander("⚠️ SECTION 4 — Problèmes et observations", expanded=False):
            problemes_sel = st.multiselect("Problèmes rencontrés", PROBLEMES)
            solutions     = st.text_area("Solutions appliquées",
                                         placeholder="Décrivez les solutions mises en place...",
                                         height=80)
            observations  = st.text_area("Observations libres",
                                         placeholder="Notes, remarques, besoins...",
                                         height=80)

        # ── Récapitulatif calculé ─────────────────────────────
        if superficie > 0 and rendement > 0:
            prod_tot = round(superficie * rendement, 1)
            rev_est  = round(prod_tot * prix_vente, 0)
            ref_cult = RENDEMENTS_REF.get(
                culture if culture != "— Choisir —" else "Maïs", 1000)
            comparaison = "✅ Au-dessus" if rendement >= ref_cult else "⚠️ En dessous"
            couleur_comp = "#43a047" if rendement >= ref_cult else "#e65100"
            st.markdown(f"""
            <div style='background:#e8f5e9;border:1px solid #a5d6a7;border-radius:10px;
                        padding:0.9rem 1.3rem;display:flex;gap:2rem;flex-wrap:wrap;margin:1rem 0;'>
                <div>
                    <span style='color:#78909c;font-size:0.78rem;'>📦 Production totale</span><br>
                    <b style='color:#1b5e20;font-size:1.2rem;'>{prod_tot:,.0f} kg</b>
                </div>
                <div>
                    <span style='color:#78909c;font-size:0.78rem;'>💵 Revenu estimé</span><br>
                    <b style='color:#1b5e20;font-size:1.2rem;'>{rev_est:,.0f} FCFA</b>
                </div>
                <div>
                    <span style='color:#78909c;font-size:0.78rem;'>📈 Réf. nationale ({ref_cult:,} kg/ha)</span><br>
                    <b style='color:{couleur_comp};font-size:1.2rem;'>{comparaison}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            prod_tot = rev_est = 0

        submitted = st.form_submit_button("💾 Enregistrer la fiche", use_container_width=True)

    # ── Traitement soumission ─────────────────────────────────
    if submitted:
        errors = []
        if not nom.strip():           errors.append("Nom de l'exploitant requis")
        if region == "— Choisir —":   errors.append("Région requise")
        if culture == "— Choisir —":  errors.append("Culture requise")
        if saison == "— Choisir —":   errors.append("Saison requise")
        if superficie <= 0:            errors.append("Superficie doit être > 0")
        if rendement <= 0:             errors.append("Rendement doit être > 0")

        if errors:
            for e in errors:
                st.error(f"❌ {e}")
        else:
            stats      = get_stats_rapides()
            code_fiche = f"AGR-{date_col.year}-{stats['nb_fiches'] + 1:04d}"
            data = {
                "code_fiche":           code_fiche,
                "date_collecte":        date_col.isoformat(),
                "user_id":              st.session_state["user"]["id"],
                "nom_exploitant":       nom.strip(),
                "telephone":            telephone.strip(),
                "region":               region,
                "departement":          departement.strip() or f"Dept-{region[:3]}",
                "arrondissement":       arrondissement.strip(),
                "coordonnees_lat":      lat if lat != 0.0 else None,
                "coordonnees_lon":      lon if lon != 0.0 else None,
                "culture":              culture,
                "variete":              variete.strip(),
                "saison":               saison,
                "superficie_ha":        superficie,
                "rendement_kg_ha":      rendement,
                "production_totale_kg": round(superficie * rendement, 1),
                "type_sol":             type_sol,
                "qualite_sol":          qualite_sol,
                "type_engrais":         engrais,
                "dose_engrais_kg_ha":   dose_eng if engrais != "Aucun" else 0,
                "irrigation":           irrigation,
                "source_eau":           source_eau,
                "main_oeuvre":          main_oeuvre,
                "nb_actifs":            nb_actifs,
                "acces_marche_km":      acces_marche,
                "prix_vente_fcfa_kg":   prix_vente,
                "revenu_estime":        rev_est,
                "formation_recue":      formation,
                "membre_cooperative":   membre_coop,
                "problemes":            ", ".join(problemes_sel) if problemes_sel else "Aucun",
                "solutions_appliquees": solutions.strip(),
                "age_plantation_ans":   age_plant,
                "observations":         observations.strip(),
                "valide":               1,
            }
            try:
                new_id = insert_fiche(data)
                st.session_state["fiche_ok"] = code_fiche
                st.session_state["fiche_id"] = new_id
                st.rerun()
            except Exception as e:
                st.error(f"Erreur d'enregistrement : {e}")

    # ── Référentiel rendements ────────────────────────────────
    with st.expander("📋 Référentiel national des rendements (Cameroun)"):
        import pandas as pd
        ref_df = pd.DataFrame([
            {"Culture": k,
             "Rendement de référence (kg/ha)": v,
             "Niveau": "🔴 Élevé" if v > 3000 else "🟡 Moyen" if v > 800 else "🟢 Faible"}
            for k, v in RENDEMENTS_REF.items() if k != "Autre"
        ])
        st.dataframe(ref_df, use_container_width=True, hide_index=True)


def _bouton_pdf_direct(fiche_id: int, code_fiche: str):
    """Génère et affiche un bouton de téléchargement PDF immédiatement après saisie."""
    try:
        from modules.rapport_pdf import generer_rapport_pdf
        fiche = get_fiche_by_id(fiche_id)
        if fiche:
            agent = st.session_state.get("user", {}).get("nom", "Agent")
            pdf_bytes = generer_rapport_pdf(fiche, agent_nom=agent)
            st.download_button(
                label="📄 Télécharger le rapport PDF de cette fiche",
                data=pdf_bytes,
                file_name=f"rapport_{code_fiche}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
    except Exception as e:
        st.warning(f"PDF non disponible : {e}")
