"""
modules/export_page.py — Export CSV + Rapports PDF agriculteurs
"""
import streamlit as st
from datetime import datetime
from utils.db import get_all_fiches, get_fiches_user, get_fiche_by_id


def show():
    st.markdown('<div class="sec-title">📥 Export des données & Rapports PDF</div>',
                unsafe_allow_html=True)

    df = get_all_fiches()
    user = st.session_state.get("user", {})
    role = user.get("role", "agent")

    if df.empty:
        st.warning("Aucune donnée à exporter.")
        return

    # ── Onglets ────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["📊 Export CSV", "📄 Rapports PDF", "📋 Statistiques"])

    # ═══════════════════════════════════════════════════════════
    with tab1:
        st.markdown("### Export des données brutes")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{len(df)} fiches** disponibles")
            csv_all = df.to_csv(index=False, encoding="utf-8").encode("utf-8")
            st.download_button(
                "⬇️ Toutes les données (CSV)",
                data=csv_all,
                file_name=f"agrosuivi_complet_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            # Résumé par culture/région
            summary = df.groupby(["culture", "region"]).agg(
                Nb=("rendement_kg_ha", "count"),
                Rdmt_moy=("rendement_kg_ha", "mean"),
                Superficie=("superficie_ha", "sum"),
            ).reset_index().round(1)
            csv2 = summary.to_csv(index=False, encoding="utf-8").encode("utf-8")
            st.download_button(
                "⬇️ Résumé par culture/région (CSV)",
                data=csv2,
                file_name=f"agrosuivi_resume_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col2:
            st.markdown("### Aperçu")
            n = st.slider("Lignes affichées", 5, 50, 10)
            cols_apercu = [c for c in ["code_fiche", "nom_exploitant", "region",
                                        "culture", "rendement_kg_ha", "superficie_ha",
                                        "date_collecte"] if c in df.columns]
            st.dataframe(df[cols_apercu].head(n), use_container_width=True, hide_index=True)

    # ═══════════════════════════════════════════════════════════
    with tab2:
        st.markdown("### 📄 Générer un rapport PDF pour un agriculteur")
        st.markdown("""
        <div class="alert-info">
            Sélectionnez une fiche dans la liste ci-dessous pour générer
            un rapport PDF professionnel téléchargeable.
        </div><br>
        """, unsafe_allow_html=True)

        # Filtre selon le rôle
        if role == "agent":
            df_select = get_fiches_user(user.get("id"))
            if df_select.empty:
                st.info("Vous n'avez pas encore de fiches enregistrées.")
                return
        else:
            df_select = df.copy()

        # Sélection de la fiche
        col_f1, col_f2 = st.columns([2, 1])
        with col_f1:
            # Construire un libellé lisible pour chaque fiche
            if not df_select.empty:
                labels = (
                    df_select["code_fiche"].fillna("N/A") + " | " +
                    df_select["nom_exploitant"].fillna("—") + " | " +
                    df_select["culture"].fillna("—") + " | " +
                    df_select["region"].fillna("—")
                ).tolist()
                choix = st.selectbox("Sélectionner une fiche", labels)
                idx   = labels.index(choix)
                fiche_row = df_select.iloc[idx]
                fiche_id  = int(fiche_row["id"])
                code      = fiche_row.get("code_fiche", "rapport")
        with col_f2:
            st.markdown("<br>", unsafe_allow_html=True)
            generer = st.button("🖨️ Générer le PDF", use_container_width=True)

        if generer and fiche_id:
            with st.spinner("Génération du rapport PDF en cours..."):
                try:
                    from modules.rapport_pdf import generer_rapport_pdf
                    fiche_dict = get_fiche_by_id(fiche_id)
                    agent_nom  = user.get("nom", "Agent")
                    pdf_bytes  = generer_rapport_pdf(fiche_dict, agent_nom=agent_nom)

                    st.success("✅ Rapport PDF généré !")
                    st.download_button(
                        label=f"📥 Télécharger — {code}.pdf",
                        data=pdf_bytes,
                        file_name=f"rapport_{code}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
                    # Aperçu des infos
                    with st.expander("👁️ Aperçu des données du rapport"):
                        import pandas as pd
                        apercu = {
                            "Code fiche":     fiche_dict.get("code_fiche"),
                            "Exploitant":     fiche_dict.get("nom_exploitant"),
                            "Culture":        fiche_dict.get("culture"),
                            "Région":         fiche_dict.get("region"),
                            "Rendement":      f"{fiche_dict.get('rendement_kg_ha', 0):,.0f} kg/ha",
                            "Superficie":     f"{fiche_dict.get('superficie_ha', 0):.2f} ha",
                            "Production":     f"{fiche_dict.get('production_totale_kg', 0):,.0f} kg",
                            "Revenu estimé":  f"{fiche_dict.get('revenu_estime', 0):,.0f} FCFA",
                        }
                        st.table(pd.DataFrame(
                            list(apercu.items()), columns=["Champ", "Valeur"]
                        ))

                except Exception as e:
                    st.error(f"Erreur lors de la génération PDF : {e}")

        # ── Export PDF en lot ─────────────────────────────────
        if role in ("admin", "superviseur"):
            st.markdown("---")
            st.markdown("### 📦 Export PDF en lot")
            st.markdown("Générer les rapports de plusieurs fiches à la fois.")

            nb_max = st.slider("Nombre de fiches à exporter", 1, min(50, len(df)), 5)
            fiches_lot = df.head(nb_max)

            if st.button(f"📥 Générer {nb_max} rapports PDF (ZIP)", use_container_width=True):
                import zipfile, io
                with st.spinner(f"Génération de {nb_max} PDFs..."):
                    try:
                        from modules.rapport_pdf import generer_rapport_pdf
                        zip_buffer = io.BytesIO()
                        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                            for _, row in fiches_lot.iterrows():
                                fiche_d  = get_fiche_by_id(int(row["id"]))
                                pdf_data = generer_rapport_pdf(fiche_d, agent_nom=user.get("nom", "Agent"))
                                zf.writestr(f"rapport_{row['code_fiche']}.pdf", pdf_data)

                        st.success(f"✅ {nb_max} PDFs générés !")
                        st.download_button(
                            "📥 Télécharger tous les rapports (ZIP)",
                            data=zip_buffer.getvalue(),
                            file_name=f"rapports_agrosuivi_{datetime.now().strftime('%Y%m%d')}.zip",
                            mime="application/zip",
                            use_container_width=True,
                        )
                    except Exception as e:
                        st.error(f"Erreur : {e}")

    # ═══════════════════════════════════════════════════════════
    with tab3:
        st.markdown("### 📊 Statistiques descriptives")
        cols_num = [c for c in ["rendement_kg_ha", "superficie_ha",
                                 "production_totale_kg", "prix_vente_fcfa_kg",
                                 "revenu_estime"] if c in df.columns]
        st.dataframe(df[cols_num].describe().round(2), use_container_width=True)
