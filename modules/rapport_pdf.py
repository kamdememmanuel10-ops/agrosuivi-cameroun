"""
modules/rapport_pdf.py — Génération de rapport PDF agriculteur
Utilise reportlab pour créer un PDF professionnel téléchargeable.
"""
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# ── Couleurs AgroSuivi ────────────────────────────────────────
VERT_FONCE  = colors.HexColor("#1b5e20")
VERT_MOY    = colors.HexColor("#2e7d32")
VERT_CLAIR  = colors.HexColor("#a5d6a7")
VERT_PALE   = colors.HexColor("#e8f5e9")
GRIS        = colors.HexColor("#546e7a")
GRIS_CLAIR  = colors.HexColor("#eceff1")
ORANGE      = colors.HexColor("#e65100")
BLANC       = colors.white


def _styles():
    base = getSampleStyleSheet()
    custom = {}

    custom["titre_principal"] = ParagraphStyle(
        "titre_principal", parent=base["Title"],
        fontSize=20, textColor=BLANC, alignment=TA_CENTER,
        fontName="Helvetica-Bold", spaceAfter=4
    )
    custom["sous_titre"] = ParagraphStyle(
        "sous_titre", parent=base["Normal"],
        fontSize=10, textColor=BLANC, alignment=TA_CENTER,
        fontName="Helvetica"
    )
    custom["section"] = ParagraphStyle(
        "section", parent=base["Heading2"],
        fontSize=12, textColor=BLANC, fontName="Helvetica-Bold",
        spaceAfter=6, spaceBefore=4, alignment=TA_LEFT,
        leftIndent=6
    )
    custom["label"] = ParagraphStyle(
        "label", parent=base["Normal"],
        fontSize=9, textColor=GRIS, fontName="Helvetica-Bold"
    )
    custom["valeur"] = ParagraphStyle(
        "valeur", parent=base["Normal"],
        fontSize=10, textColor=VERT_FONCE, fontName="Helvetica"
    )
    custom["note"] = ParagraphStyle(
        "note", parent=base["Normal"],
        fontSize=8, textColor=GRIS, fontName="Helvetica-Oblique"
    )
    custom["footer"] = ParagraphStyle(
        "footer", parent=base["Normal"],
        fontSize=8, textColor=GRIS, alignment=TA_CENTER
    )
    custom["kpi_val"] = ParagraphStyle(
        "kpi_val", parent=base["Normal"],
        fontSize=16, textColor=VERT_FONCE, fontName="Helvetica-Bold",
        alignment=TA_CENTER
    )
    custom["kpi_lab"] = ParagraphStyle(
        "kpi_lab", parent=base["Normal"],
        fontSize=8, textColor=GRIS, fontName="Helvetica",
        alignment=TA_CENTER
    )
    return custom


def _section_header(title: str, styles):
    """Barre de section verte avec titre blanc."""
    tbl = Table([[Paragraph(title, styles["section"])]], colWidths=[17.5 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), VERT_MOY),
        ("ROUNDEDCORNERS", [6]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    return tbl


def _info_table(rows_data, styles, col_widths=None):
    """Tableau de données label / valeur en 2 colonnes."""
    if col_widths is None:
        col_widths = [5 * cm, 7.5 * cm, 5 * cm] if len(rows_data[0]) == 3 else [5.5 * cm, 12 * cm]

    table_data = []
    for row in rows_data:
        formatted = []
        for i, cell in enumerate(row):
            if i % 2 == 0:  # labels (pair)
                formatted.append(Paragraph(str(cell), styles["label"]))
            else:            # valeurs (impair)
                formatted.append(Paragraph(str(cell) if cell else "—", styles["valeur"]))
        table_data.append(formatted)

    tbl = Table(table_data, colWidths=col_widths)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BLANC),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [BLANC, VERT_PALE]),
        ("GRID", (0, 0), (-1, -1), 0.3, VERT_CLAIR),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return tbl


def _kpi_table(kpis, styles):
    """Ligne de KPI : [(valeur, label), ...]."""
    cells = []
    for val, lab in kpis:
        cell = [
            Paragraph(str(val), styles["kpi_val"]),
            Paragraph(lab, styles["kpi_lab"]),
        ]
        cells.append(cell)

    tbl = Table([cells], colWidths=[17.5 / len(kpis) * cm] * len(kpis))
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), VERT_PALE),
        ("BOX", (0, 0), (-1, -1), 0.5, VERT_CLAIR),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, VERT_CLAIR),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS", [8]),
    ]))
    return tbl


def generer_rapport_pdf(fiche: dict, agent_nom: str = "Agent") -> bytes:
    """
    Génère un rapport PDF professionnel pour une fiche agriculteur.
    Retourne les bytes du PDF.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=1.8 * cm, rightMargin=1.8 * cm,
        topMargin=1.5 * cm, bottomMargin=1.5 * cm
    )
    styles = _styles()
    story = []

    # ── EN-TÊTE ───────────────────────────────────────────────
    header_data = [[
        Paragraph("🌱 AgroSuivi Cameroun", styles["titre_principal"]),
        Paragraph(f"Rapport de collecte agricole<br/>Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
                  styles["sous_titre"]),
    ]]
    header_tbl = Table(header_data, colWidths=[17.5 * cm])
    header_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), VERT_FONCE),
        ("TOPPADDING", (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("ROUNDEDCORNERS", [10]),
        ("SPAN", (0, 0), (-1, 0)),
    ]))
    story.append(header_tbl)
    story.append(Spacer(1, 0.4 * cm))

    # ── CODE FICHE ────────────────────────────────────────────
    code = fiche.get("code_fiche", "N/A")
    date_col = fiche.get("date_collecte", "N/A")
    badge_data = [[
        Paragraph(f"Code fiche : <b>{code}</b>", styles["valeur"]),
        Paragraph(f"Date de collecte : <b>{date_col}</b>", styles["valeur"]),
        Paragraph(f"Agent : <b>{agent_nom}</b>", styles["valeur"]),
    ]]
    badge_tbl = Table(badge_data, colWidths=[6 * cm, 6 * cm, 5.5 * cm])
    badge_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), VERT_PALE),
        ("BOX", (0, 0), (-1, -1), 1, VERT_CLAIR),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, VERT_CLAIR),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(badge_tbl)
    story.append(Spacer(1, 0.5 * cm))

    # ── SECTION 1 : EXPLOITANT ────────────────────────────────
    story.append(_section_header("1. Identification de l'exploitant", styles))
    story.append(Spacer(1, 0.2 * cm))
    story.append(_info_table([
        ["Nom & Prénom",    fiche.get("nom_exploitant", "—"),  "Téléphone",   fiche.get("telephone", "—")],
        ["Région",          fiche.get("region", "—"),           "Département", fiche.get("departement", "—")],
        ["Arrondissement",  fiche.get("arrondissement", "—"),   "Coopérative", fiche.get("membre_cooperative", "—")],
        ["Latitude GPS",    fiche.get("coordonnees_lat", "—"),  "Longitude GPS", fiche.get("coordonnees_lon", "—")],
    ], styles, col_widths=[4 * cm, 4.75 * cm, 4 * cm, 4.75 * cm]))
    story.append(Spacer(1, 0.4 * cm))

    # ── SECTION 2 : CULTURE ───────────────────────────────────
    story.append(_section_header("2. Informations sur la culture", styles))
    story.append(Spacer(1, 0.2 * cm))
    story.append(_info_table([
        ["Culture",        fiche.get("culture", "—"),       "Variété",    fiche.get("variete", "—")],
        ["Saison",         fiche.get("saison", "—"),         "Âge plant.", f"{fiche.get('age_plantation_ans', '—')} ans"],
        ["Superficie",     f"{fiche.get('superficie_ha', '—')} ha", "Type de sol", fiche.get("type_sol", "—")],
        ["Qualité du sol", fiche.get("qualite_sol", "—"),   "Formation",  fiche.get("formation_recue", "—")],
    ], styles, col_widths=[4 * cm, 4.75 * cm, 4 * cm, 4.75 * cm]))
    story.append(Spacer(1, 0.4 * cm))

    # ── KPI PRODUCTION ────────────────────────────────────────
    rendement   = fiche.get("rendement_kg_ha", 0) or 0
    superficie  = fiche.get("superficie_ha", 0) or 0
    production  = fiche.get("production_totale_kg", 0) or round(superficie * rendement, 1)
    prix        = fiche.get("prix_vente_fcfa_kg", 0) or 0
    revenu      = fiche.get("revenu_estime", 0) or round(production * prix, 0)

    story.append(_kpi_table([
        (f"{rendement:,.0f} kg/ha", "Rendement"),
        (f"{superficie:,.2f} ha",   "Superficie"),
        (f"{production:,.0f} kg",   "Production totale"),
        (f"{revenu:,.0f} FCFA",     "Revenu estimé"),
    ], styles))
    story.append(Spacer(1, 0.4 * cm))

    # ── SECTION 3 : INTRANTS ──────────────────────────────────
    story.append(_section_header("3. Intrants et pratiques agricoles", styles))
    story.append(Spacer(1, 0.2 * cm))
    story.append(_info_table([
        ["Type d'engrais",  fiche.get("type_engrais", "—"),      "Dose engrais",  f"{fiche.get('dose_engrais_kg_ha', 0)} kg/ha"],
        ["Irrigation",      fiche.get("irrigation", "—"),         "Source d'eau",  fiche.get("source_eau", "—")],
        ["Main-d'œuvre",    fiche.get("main_oeuvre", "—"),        "Nb actifs",     str(fiche.get("nb_actifs", "—"))],
        ["Dist. marché",    f"{fiche.get('acces_marche_km', '—')} km", "Prix vente", f"{prix:,.0f} FCFA/kg"],
    ], styles, col_widths=[4 * cm, 4.75 * cm, 4 * cm, 4.75 * cm]))
    story.append(Spacer(1, 0.4 * cm))

    # ── SECTION 4 : PROBLÈMES ─────────────────────────────────
    story.append(_section_header("4. Problèmes, solutions et observations", styles))
    story.append(Spacer(1, 0.2 * cm))

    problemes  = fiche.get("problemes", "Aucun") or "Aucun"
    solutions  = fiche.get("solutions_appliquees", "—") or "—"
    obs        = fiche.get("observations", "—") or "—"

    pb_data = [
        ["Problèmes rencontrés", problemes],
        ["Solutions appliquées", solutions],
        ["Observations",         obs],
    ]
    pb_tbl = Table(
        [[Paragraph(r[0], styles["label"]), Paragraph(r[1], styles["valeur"])] for r in pb_data],
        colWidths=[5 * cm, 12.5 * cm]
    )
    pb_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BLANC),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [BLANC, VERT_PALE]),
        ("GRID", (0, 0), (-1, -1), 0.3, VERT_CLAIR),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(pb_tbl)
    story.append(Spacer(1, 0.5 * cm))

    # ── SIGNATURE ─────────────────────────────────────────────
    sig_data = [[
        Paragraph("Signature de l'agent", styles["label"]),
        Paragraph("Signature de l'exploitant", styles["label"]),
        Paragraph("Visa superviseur", styles["label"]),
    ], [
        Paragraph("\n\n\n________________________", styles["note"]),
        Paragraph("\n\n\n________________________", styles["note"]),
        Paragraph("\n\n\n________________________", styles["note"]),
    ]]
    sig_tbl = Table(sig_data, colWidths=[5.8 * cm, 5.8 * cm, 5.9 * cm])
    sig_tbl.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, VERT_CLAIR),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, VERT_CLAIR),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    story.append(sig_tbl)
    story.append(Spacer(1, 0.4 * cm))

    # ── FOOTER ────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=VERT_CLAIR))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        f"AgroSuivi Cameroun · Projet TP 232 – Statistiques · {datetime.now().year} | "
        f"Document généré automatiquement – Ne pas modifier manuellement",
        styles["footer"]
    ))

    doc.build(story)
    return buffer.getvalue()
