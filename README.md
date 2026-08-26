# Application Streamlit sécurisée — Analyse des vols

Application Streamlit multi-pages avec authentification par fichier CSV, un dashboard interactif d'analyse du trafic aérien (dataset `flights` de seaborn), et une galerie photo.

## Fonctionnalités

- Connexion obligatoire via `accounts.csv` (identifiants gérés avec Pandas et `st.session_state`)
- Page **Accueil** : storytelling data analyst basé sur les vraies données (KPIs, croissance du trafic, saisonnalité)
- Page **Dashboard Vols** : filtres (plage d'années, mois), KPIs, graphiques interactifs ECharts, heatmap
- Page **Galerie Photos** : galerie d'images sur 3 colonnes

## Comptes de démonstration

| Utilisateur | Mot de passe |
|---|---|
| utilisateur | mdp123654 |
| admin | admin123654 |

## Installation et lancement en local

### 1. Cloner le dépôt

```bash
git clone https://github.com/loicbonicontact-gif/mon-projetstreamlit.git
cd mon-projetstreamlit
```

### 2. Créer l'environnement virtuel

```bash
python3 -m venv venv
```

### 3. Activer l'environnement virtuel

```bash
source venv/bin/activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvre sur [http://localhost:8501](http://localhost:8501).

## Structure du projet

```
.
├── app.py                  # Application principale (connexion + pages)
├── accounts.csv             # Identifiants utilisés pour l'authentification
├── requirements.txt          # Dépendances Python
├── img/                      # Images de la galerie photo
└── .gitignore
```
