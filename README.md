# 🌱 AgroSuivi Cameroun

> **Application de collecte et d'analyse de données agricoles — 10 régions du Cameroun**  
> Projet TP 232 – Statistiques · Avril 2025

---

## 📌 Présentation

**AgroSuivi Cameroun** est une application web interactive développée avec **Streamlit** permettant de collecter, gérer, analyser et visualiser les données agricoles provenant des 10 régions du Cameroun.

Elle s'adresse aux étudiants, entrepreneurs agricoles, superviseurs régionaux et tout acteur du secteur agricole souhaitant un outil de suivi moderne et centralisé.

---

## 🎯 Fonctionnalités

| Module | Description |
|--------|-------------|
| 🏠 **Accueil** | Tableau de bord résumé : KPIs, graphiques, dernières fiches collectées |
| 📝 **Saisie des données** | Formulaire complet multi-sections (exploitant, culture, intrants, problèmes) |
| 🗺️ **Carte interactive** | Visualisation géographique des exploitations par région |
| 📊 **Tableau de bord** | Analyses filtrables : rendements, superficies, engrais, boxplots |
| 🔬 **Analyses avancées** | Distributions, corrélations, comparaisons régionales, classements |
| 📈 **Statistiques** | Données climatiques, évolutions temporelles par région |
| 💡 **Recommandations** | Conseils personnalisés basés sur les données et les référentiels nationaux |
| 📥 **Export & Rapports PDF** | Export CSV et génération de rapports PDF professionnels par fiche |
| ℹ️ **À propos** | Informations sur le projet et les technologies utilisées |

---

## 🛠️ Technologies

- **[Streamlit](https://streamlit.io/)** — Interface web Python interactive
- **[Supabase](https://supabase.com/)** — Base de données PostgreSQL hébergée (REST API)
- **[Plotly](https://plotly.com/)** — Graphiques et visualisations interactives
- **[ReportLab](https://www.reportlab.com/)** — Génération de rapports PDF
- **[Pandas](https://pandas.pydata.org/) / [NumPy](https://numpy.org/)** — Traitement et analyse des données
- **[Scikit-learn](https://scikit-learn.org/)** / **[Statsmodels](https://www.statsmodels.org/)** — Analyses statistiques avancées

---

## 📁 Structure du projet

```
agrosuivi-cameroun/
│
├── app.py                    # Point d'entrée principal — routing & CSS global
│
├── modules/                  # Pages de l'application
│   ├── accueil.py            # Page d'accueil avec KPIs et graphiques
│   ├── saisie.py             # Formulaire de collecte agricole
│   ├── carte.py              # Carte interactive des régions
│   ├── dashboard.py          # Tableau de bord analytique avec filtres
│   ├── analyses.py           # Analyses statistiques avancées
│   ├── statistiques.py       # Statistiques et données climatiques
│   ├── recommandations.py    # Recommandations personnalisées
│   ├── export_page.py        # Export CSV et rapports PDF
│   ├── rapport_pdf.py        # Génération PDF avec ReportLab
│   ├── apropos.py            # Page À propos
│   └── login.py              # Page de connexion (optionnel)
│
├── utils/                    # Utilitaires partagés
│   ├── db.py                 # Connexion Supabase & requêtes
│   ├── auth.py               # Gestion de l'authentification
│   └── const.py              # Constantes : cultures, régions, référentiels
│
└── requirements.txt          # Dépendances Python
```

---

## ⚙️ Installation et lancement

### 1. Cloner le projet

```bash
git clone https://github.com/kamdememmanuel10-ops/agrosuivi-cameroun.git
cd agrosuivi-cameroun
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer les secrets Supabase

Créer le fichier `.streamlit/secrets.toml` :

```toml
SUPABASE_URL = "https://xxxxxxxxxxxxxxxx.supabase.co"
SUPABASE_KEY = "votre_clé_anon_supabase"
OPENWEATHER_KEY = "votre_clé_openweathermap"
```

### 4. Lancer l'application

```bash
streamlit run app.py
```

L'application sera accessible à l'adresse : `http://localhost:8501`

---

## 🗄️ Base de données Supabase

L'application utilise **Supabase** (PostgreSQL) avec les tables suivantes :

### Table `fiches`
Contient les données de collecte agricole. Colonnes principales :

| Colonne | Type | Description |
|--------|------|-------------|
| `code_fiche` | text | Identifiant unique (ex: AGR-2025-0001) |
| `nom_exploitant` | text | Nom de l'agriculteur |
| `region` | text | Région du Cameroun |
| `culture` | text | Culture pratiquée |
| `superficie_ha` | float | Superficie en hectares |
| `rendement_kg_ha` | float | Rendement en kg/ha |
| `production_totale_kg` | float | Production calculée |
| `revenu_estime` | float | Revenu estimé en FCFA |
| `type_engrais` | text | Type d'engrais utilisé |
| `irrigation` | text | Oui / Non |
| `problemes` | text | Problèmes rencontrés |
| `valide` | int | 1 = validé, 0 = brouillon |

### Table `utilisateurs`
Gestion des comptes agents, superviseurs et administrateurs.

### Table `recommandations`
Recommandations agricoles filtrables par région, culture et saison.

### Table `climat`
Données climatiques mensuelles par région (température, pluviométrie).

---

## 📊 Données de référence

L'application intègre des **référentiels nationaux camerounais** pour 20 cultures :

| Culture | Rendement de référence |
|---------|----------------------|
| Maïs | 1 500 kg/ha |
| Manioc | 8 000 kg/ha |
| Cacao | 400 kg/ha |
| Café | 300 kg/ha |
| Plantain | 5 000 kg/ha |
| Tomate | 10 000 kg/ha |
| Canne à sucre | 50 000 kg/ha |
| … | … |

Ces données permettent de détecter automatiquement les **cultures sous-performantes** (< -20% de la référence) et **sur-performantes** (> +20%).

---

## 🗺️ Régions couvertes

L'application couvre les **10 régions administratives** du Cameroun :

- Adamaoua · Centre · Est · Extrême-Nord
- Littoral · Nord · Nord-Ouest · Ouest
- Sud · Sud-Ouest

Chaque région est associée à ses **coordonnées GPS**, ses **cultures dominantes** et sa **zone agro-écologique**.

---

## 📄 Rapport PDF

La fonctionnalité d'export génère un **rapport PDF professionnel** pour chaque fiche agriculteur, comprenant :

- En-tête AgroSuivi avec code fiche et date
- Identification complète de l'exploitant
- Informations sur la culture (variété, superficie, type de sol)
- Bloc KPI : rendement, superficie, production totale, revenu estimé
- Tableau des intrants et pratiques agricoles
- Section problèmes, solutions et observations
- Zone de signatures (agent, exploitant, superviseur)

L'export en lot (ZIP) est disponible pour les rôles Admin et Superviseur.

---

## 🚀 Déploiement sur Streamlit Cloud

1. Pousser le projet sur GitHub
2. Connecter le dépôt sur [share.streamlit.io](https://share.streamlit.io)
3. Ajouter les secrets (`SUPABASE_URL`, `SUPABASE_KEY`, `OPENWEATHER_KEY`) dans les paramètres de l'application
4. Déployer 🎉

---

## 📦 Dépendances (`requirements.txt`)

```
streamlit==1.45.0
pandas==2.2.2
plotly==5.22.0
numpy==1.26.4
psycopg2-binary==2.9.9
scikit-learn==1.4.2
openpyxl==3.1.5
statsmodels==0.14.2
reportlab==4.2.0
```

---

## 👨‍💻 Auteur

**KAMDEM Emmanuel**  
📧 kamdememmanuel10@gmail.com  
🐙 [github.com/kamdememmanuel10-ops](https://github.com/kamdememmanuel10-ops/)

---

## 📜 Licence

Projet académique — **TP 232 · Statistiques · Avril 2025**  
Usage libre dans un cadre éducatif et de recherche.

---

<div align="center">
  🌱 <strong>AgroSuivi Cameroun</strong> · Fait avec ❤️ pour les agriculteurs camerounais
</div>