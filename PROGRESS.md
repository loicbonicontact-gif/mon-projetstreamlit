# Progression du projet

## Fait
- Guide 5 (Fonctionnalités avancées & sécurisation) : terminé
  - `streamlit-option-menu` installé dans le venv
  - `accounts.csv` créé à la racine (colonnes: name, password, email, failed_login_attempts, logged_in, role)
  - Identifiants actuels : utilisateur/mdp123654, admin/admin123654
- `app.py` : fichier principal qui regroupe connexion + dashboard vols + galerie (remplace les anciens app_securisee.py / app_dataviz.py / app_taxis.py, qui restent en place mais ne sont plus utilisés)
  - Page de connexion obligatoire, sidebar avec bienvenue + déconnexion
  - Menu : Accueil / Dashboard Vols / Galerie Photos
  - Page Accueil : storytelling "data analyst" basé sur les vraies données flights (KPIs de croissance, mois pic/creux, graphique), avec photo du dossier img/
  - Page Dashboard Vols : filtres années/mois, KPI, line chart, heatmap (contenu de l'ancien app_dataviz.py)
  - Page Galerie Photos : 3 images du dossier img/, sur 3 colonnes
  - Testé en local sur localhost:8501 : tout fonctionne

## Bugs rencontrés et résolus
- `use_column_width` déprécié → remplacé par `use_container_width`
- Affichage incohérent dans le Chrome de l'utilisateur (page mélangeant deux écrans différents) → probablement lié à la traduction automatique Chrome ou une extension ; contourné en travaillant en navigation privée / testant avec un navigateur indépendant
- `PIL.UnidentifiedImageError` sur la galerie → le dossier `img/` contenait un fichier caché `.DS_Store` (macOS) que le code tentait d'afficher comme image → corrigé avec un filtre sur les extensions image (fonction `lister_images()`)

## Décisions prises
- Le dashboard taxis (`app_taxis.py`) n'est PAS intégré dans `app.py`, à la demande de l'utilisateur (uniquement flights)
- Les images viennent d'un dossier local `img/` (captures d'écran perso) plutôt que d'URLs internet

## Reste à faire (Activité 3)
- Personnalisation des couleurs de l'app (palette proposée par l'utilisateur : noir #000000, bleu-gris foncé #36494E, bleu-gris moyen #597081, bleu-gris clair #7EA0B7, bleu pastel #A9CEF4) — pas encore commencé
- Guide 6 (Déploiement sur Streamlit Cloud) : pas encore commencé, PDF du guide pas encore fourni
  - Génération de `requirements.txt` (pip freeze)
  - Commit/push sur GitHub
  - Déploiement public sur Streamlit Cloud
- Point de vigilance à rappeler avant de pousser sur GitHub : `accounts.csv` contient des mots de passe en clair et le dépôt semble public → décision à prendre (gitignore le fichier, ou le pousser tel quel comme le veut l'exercice)
