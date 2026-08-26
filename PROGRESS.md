# Progression du projet

## Fait
- Guide 5 (Fonctionnalités avancées & sécurisation) : terminé
  - `streamlit-option-menu` et `streamlit-echarts` installés dans le venv
  - `accounts.csv` créé à la racine (colonnes: name, password, email, failed_login_attempts, logged_in, role)
  - Identifiants actuels : utilisateur/mdp123654, admin/admin123654
- `app.py` : fichier principal unique (connexion + dashboard vols + galerie). `app_dataviz.py` et `app_taxis.py` supprimés du dépôt (contenu repris dans app.py). `app_securisee.py` reste en local, jamais suivi par Git.
  - Page de connexion obligatoire, sidebar avec bienvenue + déconnexion
  - Menu : Accueil / Dashboard Vols / Galerie Photos
  - Page Accueil : storytelling "data analyst" basé sur les vraies données flights (KPIs de croissance, mois pic/creux, graphique ECharts), avec photo du dossier img/
  - Page Dashboard Vols (redesign façon vrai dashboard) : filtres (plage d'années + multiselect mois) déplacés dans la sidebar sous le menu, 4 KPIs en haut (total, moyenne mensuelle, croissance période, mois le plus chargé), graphique d'évolution ECharts en pleine largeur, puis saisonnalité (bar chart ECharts) et heatmap Seaborn côte à côte, données détaillées repliées dans un expander
  - Page Galerie Photos : 3 images du dossier img/, sur 3 colonnes
  - Testé en local : tout fonctionne

## Point 1 des Livrables (dépôt GitHub) : fait
- `app.py` ✅ / `.gitignore` avec venv/ ✅ / `requirements.txt` (pip freeze) ✅ / `accounts.csv` inclus (voir décision ci-dessous) ✅ / `README.md` avec présentation + procédure d'installation pas à pas ✅
- Tout commité et poussé sur GitHub (dernier commit : 4f0c1ba)

## Bugs rencontrés et résolus
- `use_column_width` déprécié → remplacé par `use_container_width`
- Affichage incohérent dans le Chrome de l'utilisateur (page mélangeant deux écrans différents, ex. titre "Connexion..." resté affiché après connexion) → confirmé comme un bug propre au Chrome de l'utilisateur (testé et fonctionnel sur Safari) ; résolu de son côté, pas un bug de l'application
- `PIL.UnidentifiedImageError` sur la galerie → le dossier `img/` contenait un fichier caché `.DS_Store` (macOS) que le code tentait d'afficher comme image → corrigé avec un filtre sur les extensions image (fonction `lister_images()`)

## Décisions prises
- Le dashboard taxis (`app_taxis.py`) n'est PAS intégré dans `app.py`, à la demande de l'utilisateur (uniquement flights)
- Les images viennent d'un dossier local `img/` (captures d'écran perso) plutôt que d'URLs internet
- `accounts.csv` est finalement INCLUS dans le dépôt GitHub public (mots de passe en clair visibles) : le point 1 des Livrables l'exige explicitement. Décision confirmée avec l'utilisateur malgré le risque de sécurité déjà signalé.

## Reste à faire (Activité 3 / Livrables)
- Personnalisation des couleurs de l'app (palette proposée par l'utilisateur : noir #000000, bleu-gris foncé #36494E, bleu-gris moyen #597081, bleu-gris clair #7EA0B7, bleu pastel #A9CEF4) — pas encore commencé
- Point 2 des Livrables : page GitHub Pages issue de l'Activité 1 — pas encore abordé
- Point 3 des Livrables : déploiement sur Streamlit Cloud (lien URL public) — pas encore commencé, PDF du Guide 6 pas encore fourni
- Point 4 des Livrables : support de présentation (PPTX/PDF/lien) — pas encore commencé
