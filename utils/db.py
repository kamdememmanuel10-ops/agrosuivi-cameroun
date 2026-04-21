
import pandas as pd
import hashlib
import streamlit as st
from supabase import create_client

# — Connexion Supabase (API REST, port 443) —
@st.cache_resource
def get_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def _hash_pwd(pwd: str) -> str:
    return hashlib.sha256(pwd.encode()).hexdigest()

# — Initialisation DB —
def init_db():
    """Vérifie la connexion et crée l'admin si absent."""
    try:
        sb = get_supabase()
        res = sb.table("utilisateurs").select("id").execute()
        if len(res.data) == 0:
            pwd = _hash_pwd("admin2025")
            sb.table("utilisateurs").insert({
                "nom": "Administrateur",
                "email": "admin@agrosuivi.cm",
                "mot_de_passe": pwd,
                "role": "admin",
                "actif": 1
            }).execute()
    except Exception as e:
        st.error(f"Erreur de connexion Supabase : {e}")
        st.info("Vérifiez vos secrets SUPABASE_URL et SUPABASE_KEY dans .streamlit/secrets.toml")
        st.stop()

def get_fiches_user(user_id):
    sb = get_supabase()
    return sb.table("fiches").select("*").eq("user_id", user_id).execute().data

# — Authentification —
def verify_user(email: str, pwd: str):
    """Retourne le dict utilisateur si les credentials sont valides, sinon None."""
    sb = get_supabase()
    hashed = _hash_pwd(pwd)
    res = sb.table("utilisateurs")\
            .select("*")\
            .eq("email", email)\
            .eq("mot_de_passe", hashed)\
            .eq("actif", 1)\
            .execute()
    return res.data[0] if res.data else None

# — Stats rapides —
def get_stats_rapides():
    sb = get_supabase()
    fiches = sb.table("fiches").select("id, culture, region").eq("valide", 1).execute()
    rows = fiches.data
    nb_f = len(rows)
    nb_cu = len(set(r["culture"] for r in rows if r.get("culture")))
    nb_re = len(set(r["region"] for r in rows if r.get("region")))
    return {"nb_fiches": nb_f, "nb_cultures": nb_cu, "nb_regions": nb_re}

# — Fiches —
def get_all_fiches():
    sb = get_supabase()
    res = sb.table("fiches").select("*").eq("valide", 1).order("date_collecte", desc=True).execute()
    if not res.data:
        return pd.DataFrame(columns=["id", "culture", "region", "saison", "valide", "rendement_kg_ha", "nom_exploitant", "superficie_ha", "revenu_estime", "problemes", "production_total_kg", "irrigation", "type_engrais", "prix_vente_fcfa_kg", "lat", "lon"])
    return pd.DataFrame(res.data)


def get_fiche_by_id(fiche_id: int):
    sb = get_supabase()
    res = sb.table("fiches").select("*").eq("id", fiche_id).execute()
    return res.data[0] if res.data else None

def insert_fiche(data: dict):
    sb = get_supabase()
    sb.table("fiches").insert(data).execute()

# — Recommandations —
def get_recommandations(region=None, culture=None, saison=None):
    sb = get_supabase()
    query = sb.table("recommandations").select("*").eq("actif", 1)
    if region:
        query = query.in_("region", [region, "Toutes"])
    if culture:
        query = query.in_("culture", [culture, "Toutes"])
    if saison:
        query = query.in_("saison", [saison, "Toute saison"])
    res = query.order("priorite").execute()
    return pd.DataFrame(res.data) if res.data else pd.DataFrame()

# — Climat —
def get_climat_region(region: str):
    sb = get_supabase()
    res = sb.table("climat").select("*").eq("region", region).order("mois").execute()
    return pd.DataFrame(res.data) if res.data else pd.DataFrame()