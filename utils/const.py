CULTURES = [
 "Maïs", "Manioc", "Cacao", "Café", "Plantain", "Igname",
 "Sorgho", "Mil", "Arachide", "Palmier à huile", "Riz",
 "Haricot", "Tomate", "Piment", "Gombo", "Macabo",
 "Patate douce", "Coton", "Canne à sucre", "Autre"
]
REGIONS = [
 "Adamaoua", "Centre", "Est", "Extrême-Nord",
 "Littoral", "Nord", "Nord-Ouest", "Ouest",
 "Sud", "Sud-Ouest"
]
SAISONS = [
 "Grande saison des pluies",
 "Grande saison sèche",
 "Petite saison des pluies",
 "Petite saison sèche",
 "Toute saison",
]
TYPES_SOL = [
 "Ferrallitique (rouge)", "Hydromorphe (bas-fond)",
 "Volcanique (noir)", "Sableux", "Argileux",
 "Limoneux", "Limono-argileux", "Latéritique"
]
ENGRAIS = [
 "Aucun", "NPK (15-15-15)", "NPK (20-10-10)",
 "Urée (46%)", "Fumier organique", "Compost maison",
 "Engrais foliaire", "Phosphate naturel", "Kiesérite",
 "Mixte organique/chimique"
]
PROBLEMES = [
 "Sécheresse / manque d'eau", "Inondations",
 "Ravageurs (insectes)", "Maladies fongiques",
 "Maladies virales", "Adventices (mauvaises herbes)",
 "Manque d'engrais / intrants", "Sol appauvri",
 "Accès au marché difficile", "Prix de vente bas",
 "Main-d'œuvre insuffisante", "Manque de semences améliorées",
 "Crédits agricoles insuffisants", "Aucun problème majeur", "Autre"
]
RENDEMENTS_REF = {
 "Maïs": 1500, "Manioc": 8000, "Cacao": 400, "Café": 300,
 "Plantain": 5000, "Igname": 4000, "Sorgho": 900, "Mil": 700,
 "Arachide": 800, "Palmier à huile": 3500, "Riz": 2000,
 "Haricot": 600, "Tomate": 10000, "Piment": 3000,
 "Gombo": 4000, "Macabo": 5500, "Patate douce": 6000,
 "Coton": 700, "Canne à sucre": 50000, "Autre": 1000
}

# Coordonnées centrales des régions
COORDS_REGIONS = {
 "Adamaoua": {"lat": 7.33, "lon": 12.59, "couleur": "#e67e22"},
 "Centre": {"lat": 3.85, "lon": 11.50, "couleur": "#2e7d32"},
 "Est": {"lat": 4.50, "lon": 13.70, "couleur": "#8e44ad"},
 "Extrême-Nord":{"lat": 10.60, "lon": 14.30, "couleur": "#c0392b"},
 "Littoral": {"lat": 4.06, "lon": 9.70, "couleur": "#2980b9"},
 "Nord": {"lat": 8.60, "lon": 13.60, "couleur": "#d35400"},
 "Nord-Ouest": {"lat": 6.00, "lon": 10.20, "couleur": "#27ae60"},
 "Ouest": {"lat": 5.48, "lon": 10.42, "couleur": "#f39c12"},
 "Sud": {"lat": 3.20, "lon": 11.80, "couleur": "#16a085"},
 "Sud-Ouest": {"lat": 4.50, "lon": 9.30, "couleur": "#2c3e50"},
}
# Zones agro-écologiques
ZONES_AGROECO = {
 "Guinéenne forestière": ["Sud", "Est", "Sud-Ouest"],
 "Bimodale subéquatoriale": ["Centre", "Littoral"],
 "Hautes terres": ["Ouest", "Nord-Ouest"],
 "Soudano-sahélienne": ["Adamaoua", "Nord"],
 "Sahélienne": ["Extrême-Nord"],
}
# Cultures dominantes par région
CULTURES_PAR_REGION = {
 "Centre": ["Maïs", "Manioc", "Plantain", "Cacao", "Tomate"],
 "Littoral": ["Plantain", "Palmier à huile", "Maïs", "Cacao"],
 "Ouest": ["Maïs", "Café", "Plantain", "Pomme de terre"],
 "Adamaoua": ["Maïs", "Sorgho", "Manioc", "Haricot", "Igname"],
 "Nord": ["Sorgho", "Mil", "Arachide", "Coton", "Riz"],
 "Extrême-Nord":["Mil", "Sorgho", "Arachide", "Coton", "Poivron"],
 "Est": ["Manioc", "Plantain", "Maïs", "Igname", "Cacao"],
 "Nord-Ouest": ["Café", "Maïs", "Pomme de terre", "Haricot"],
 "Sud-Ouest": ["Plantain", "Palmier à huile", "Cacao", "Maïs"],
 "Sud": ["Manioc", "Plantain", "Cacao", "Maïs"],
}
COULEURS_REGIONS = {r: d["couleur"] for r, d in COORDS_REGIONS.items()}
MOIS_NOMS = ["Jan","Fév","Mar","Avr","Mai","Jun","Jul","Aoû","Sep","Oct","Nov","Déc"]
