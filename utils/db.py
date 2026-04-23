import hashlib
import streamlit as st
import pandas as pd
from supabase import create_client


# ── Connexion Supabase ────────────────────────────────────────
@st.cache_resource
def get_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


# ── Utilitaire mot de passe ───────────────────────────────────
def _hash_pwd(pwd: str) -> str:
    return hashlib.sha256(pwd.encode()).hexdigest()


# ── Initialisation DB ─────────────────────────────────────────
def init_db():
    """Vérifie la connexion et crée l'admin par défaut si absent."""
    try:
        sb = get_supabase()
        res = sb.table("utilisateurs").select("id").execute()
        if len(res.data) == 0:
            pwd = _hash_pwd("admin2025")
            sb.table("utilisateurs").insert({
                "nom":          "Administrateur",
                "email":        "admin@agrosuivi.cm",
                "mot_de_passe": pwd,
                "role":         "admin",
                "actif":        1,
            }).execute()
    except Exception as e:
        st.error(f"Erreur de connexion Supabase : {e}")
        st.info("Vérifiez vos secrets SUPABASE_URL et SUPABASE_KEY dans .streamlit/secrets.toml")
        st.stop()


# ── Authentification ──────────────────────────────────────────
def verify_user(email: str, pwd: str):
    """Retourne le dict utilisateur si les credentials sont valides, sinon None."""
    sb     = get_supabase()
    hashed = _hash_pwd(pwd)
    res    = (
        sb.table("utilisateurs")
        .select("*")
        .eq("email", email)
        .eq("mot_de_passe", hashed)
        .eq("actif", 1)
        .execute()
    )
    return res.data[0] if res.data else None


# ── Fiches ────────────────────────────────────────────────────
FICHES_COLUMNS = [
    "id", "code_fiche", "date_collecte", "user_id",
    "nom_exploitant", "telephone", "region", "departement", "arrondissement",
    "coordonnees_lat", "coordonnees_lon", "membre_cooperative",
    "culture", "variete", "saison", "age_plantation_ans",
    "superficie_ha", "rendement_kg_ha", "production_totale_kg",
    "type_sol", "qualite_sol", "prix_vente_fcfa_kg", "acces_marche_km", "revenu_estime",
    "type_engrais", "dose_engrais_kg_ha", "irrigation", "source_eau",
    "main_oeuvre", "nb_actifs",
    "problemes", "solutions_appliquees", "observations",
    "valide", "created_at",
]

def insert_fiche(data: dict):
    """Insère une fiche et retourne son id."""
    sb  = get_supabase()
    res = sb.table("fiches").insert(data).execute()
    if res.data:
        return res.data[0].get("id")
    return None

def get_fiche_by_id(fiche_id: int):
    """Retourne une fiche par son id."""
    sb  = get_supabase()
    res = sb.table("fiches").select("*").eq("id", fiche_id).execute()
    return res.data[0] if res.data else None

def get_all_fiches() -> pd.DataFrame:
    """Retourne toutes les fiches valides sous forme de DataFrame."""
    sb  = get_supabase()
    res = (
        sb.table("fiches")
        .select("*")
        .eq("valide", 1)
        .order("date_collecte", desc=True)
        .execute()
    )
    if not res.data:
        return pd.DataFrame(columns=FICHES_COLUMNS)
    return pd.DataFrame(res.data)

def get_fiches_user(user_id: str) -> pd.DataFrame:
    """Retourne les fiches d'un utilisateur donné."""
    sb  = get_supabase()
    res = sb.table("fiches").select("*").eq("user_id", user_id).execute()
    if not res.data:
        return pd.DataFrame(columns=FICHES_COLUMNS)
    return pd.DataFrame(res.data)


# ── Stats rapides ─────────────────────────────────────────────
def get_stats_rapides() -> dict:
    """Retourne les statistiques globales de la base."""
    sb    = get_supabase()
    res   = sb.table("fiches").select("id, culture, region, superficie_ha, rendement_kg_ha").eq("valide", 1).execute()
    rows  = res.data or []
    nb_f  = len(rows)
    nb_cu = len(set(r["culture"] for r in rows if r.get("culture")))
    nb_re = len(set(r["region"]  for r in rows if r.get("region")))
    sup_t = round(sum(r.get("superficie_ha", 0) or 0 for r in rows), 1)
    return {
        "nb_fiches":     nb_f,
        "nb_cultures":   nb_cu,
        "nb_regions":    nb_re,
        "superficie_tot": sup_t,
    }


# ── Recommandations ───────────────────────────────────────────
def get_recommandations(region=None, culture=None, saison=None) -> pd.DataFrame:
    sb    = get_supabase()
    query = sb.table("recommandations").select("*").eq("actif", 1)
    if region:
        query = query.in_("region",  [region,  "Toutes"])
    if culture:
        query = query.in_("culture", [culture, "Toutes"])
    if saison:
        query = query.in_("saison",  [saison,  "Toute saison"])
    res = query.order("priorite").execute()
    return pd.DataFrame(res.data) if res.data else pd.DataFrame()


# ── Climat ────────────────────────────────────────────────────
def get_climat_region(region: str) -> pd.DataFrame:
    sb  = get_supabase()
    res = sb.table("climat").select("*").eq("region", region).order("mois").execute()
    return pd.DataFrame(res.data) if res.data else pd.DataFrame()
