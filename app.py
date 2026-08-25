import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu
import os

# --- 1. INITIALISATION DE LA SESSION ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# --- 2. FONCTION DE VÉRIFICATION DES IDENTIFIANTS ---
@st.cache_data
def load_accounts():
    return pd.read_csv("accounts.csv")

def authenticate(username_input, password_input):
    accounts_df = load_accounts()
    user_match = accounts_df[(accounts_df["name"] == username_input) & (accounts_df["password"] == password_input)]
    return not user_match.empty

# Chargement direct du dataset "flights" depuis GitHub (utilisé sur plusieurs pages)
@st.cache_data
def load_flights():
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/flights.csv"
    return pd.read_csv(url)

# Liste les vrais fichiers image du dossier img/ (ignore .DS_Store et autres fichiers cachés)
EXTENSIONS_IMAGE = (".png", ".jpg", ".jpeg", ".gif", ".webp")

def lister_images():
    return [f for f in sorted(os.listdir("img")) if f.lower().endswith(EXTENSIONS_IMAGE)]

# --- 3. GESTION DE L'AFFICHAGE CONDITIONNEL ---
if not st.session_state["logged_in"]:
    st.title("Connexion à l'Application Data")
    st.subheader("Veuillez vous identifier pour accéder au contenu")

    username_input = st.text_input("Nom d'utilisateur")
    password_input = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if authenticate(username_input, password_input):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username_input
            st.success(f"Bienvenue {username_input} !")
            st.rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

else:
    # --- APPLICATION SÉCURISÉE ---
    with st.sidebar:
        st.write(f"Bienvenue, **{st.session_state['username']}** !")
        if st.button("Se déconnecter"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.rerun()
        st.divider()

        selected_page = option_menu(
            menu_title="Menu principal",
            options=["Accueil", "Dashboard Vols", "Galerie Photos"],
            icons=["house", "airplane", "images"],
            default_index=0
        )

    if selected_page == "Accueil":
        st.title("Page d'Accueil Réservée")
        st.write("Ce contenu est uniquement accessible aux utilisateurs authentifiés.")

        st.markdown("---")
        st.subheader("✈️ Ce que racontent les données du trafic aérien")

        df_flights = load_flights()

        # Calculs pour raconter une histoire avec des chiffres réels
        annee_debut = int(df_flights["year"].min())
        annee_fin = int(df_flights["year"].max())
        passagers_debut = df_flights[df_flights["year"] == annee_debut]["passengers"].sum()
        passagers_fin = df_flights[df_flights["year"] == annee_fin]["passengers"].sum()
        croissance = ((passagers_fin - passagers_debut) / passagers_debut) * 100

        moyenne_par_mois = df_flights.groupby("month")["passengers"].mean()
        mois_pic = moyenne_par_mois.idxmax()
        mois_creux = moyenne_par_mois.idxmin()

        col_img, col_texte = st.columns([1, 1.4])

        with col_img:
            st.image(
                os.path.join("img", lister_images()[1]),
                caption="Le transport aérien a transformé notre rapport à la distance.",
                use_container_width=True,
            )

        with col_texte:
            st.markdown(
                f"Entre **{annee_debut}** et **{annee_fin}**, le nombre de passagers "
                f"est passé de **{passagers_debut:,}** à **{passagers_fin:,}** par an, "
                f"soit une croissance de **+{croissance:.0f}%**."
            )
            st.markdown(
                f"Le trafic n'est pas uniforme sur l'année : **{mois_pic}** est le mois "
                f"le plus chargé en moyenne, tandis que **{mois_creux}** reste le plus calme — "
                "un signal typique de saisonnalité que l'on retrouve chaque année dans les données."
            )
            st.markdown(
                "Ces chiffres, vous pouvez les explorer vous-même : ouvrez le **Dashboard Vols** "
                "pour filtrer par année et par mois, et observer où se situent les pics et les creux."
            )

        # KPIs façon "data analyst" : les chiffres clés de l'histoire, en un coup d'œil
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Croissance du trafic", f"+{croissance:.0f}%", f"{annee_debut} → {annee_fin}")
        kpi2.metric("Mois le plus chargé", mois_pic)
        kpi3.metric("Mois le plus calme", mois_creux)

        # Graphique qui appuie visuellement l'histoire racontée ci-dessus
        st.line_chart(df_flights.groupby("year")["passengers"].sum())

    elif selected_page == "Dashboard Vols":
        st.title("Dashboard Analyse des Vols")
        st.subheader("Aperçu des données")

        df_flights = load_flights()

        # je choisi une plage d'années.
        annee_min = int(df_flights["year"].min())
        annee_max = int(df_flights["year"].max())

        plage_annees = st.slider("Choisissez une plage d'années :", annee_min, annee_max, (annee_min, annee_max))

        # Je crée la liste des mois disponibles, avec "Tous les mois" ajouté en premier
        mois_disponibles = ["Tous les mois"] + sorted(df_flights["month"].unique().tolist())

        # Je crée un menu déroulant pour que l'utilisateur choisisse un mois (ou tous les mois)
        mois_choisi = st.selectbox("Choisissez un mois :", mois_disponibles)

        # Je filtre le dataframe pour ne garder que les lignes dans la plage d'années sélectionnée
        df_filtre = df_flights[(df_flights["year"] >= plage_annees[0]) & (df_flights["year"] <= plage_annees[1])]

        # Je filtre en plus par mois, sauf si l'utilisateur a choisi "Tous les mois"
        if mois_choisi != "Tous les mois":
            df_filtre = df_filtre[df_filtre["month"] == mois_choisi]

        # J'affiche le résultat filtré pour vérifier que ça fonctionne
        st.dataframe(df_filtre)

        # Je calcule le total de passagers sur les données filtrées
        total_passagers = df_filtre["passengers"].sum()

        # J'affiche ce total sous forme d'indicateur clé (KPI)
        st.metric(label="Total de passagers sur la période sélectionnée", value=f"{total_passagers:,}")

        # Je regroupe les données filtrées par année pour obtenir le total de passagers par an
        passagers_par_annee = df_filtre.groupby("year")["passengers"].sum()

        # J'affiche un graphique en ligne montrant l'évolution du nombre de passagers
        st.line_chart(passagers_par_annee)

        # Je crée une case à cocher pour afficher ou masquer la heatmap
        afficher_heatmap = st.checkbox("Afficher la heatmap passagers par mois et année")

        if afficher_heatmap:
            # Je transforme le dataframe en tableau croisé : lignes = mois, colonnes = année, valeurs = passagers
            tableau_croise = df_filtre.pivot(index="month", columns="year", values="passengers")

            # Je crée une figure Matplotlib/Seaborn
            fig, ax = plt.subplots(figsize=(10, 5))

            # Je dessine la heatmap avec les valeurs affichées et une palette de couleurs
            sns.heatmap(tableau_croise, annot=True, fmt=".0f", cmap="coolwarm", ax=ax)

            # J'affiche la figure dans Streamlit
            st.pyplot(fig)

    elif selected_page == "Galerie Photos":
        st.title("Album Photos")
        st.write("Voici la galerie multimédia organisée sur 3 colonnes :")

        cols = st.columns(3)
        image_files = lister_images()[:3]
        for idx, img_name in enumerate(image_files):
            with cols[idx % 3]:
                st.image(os.path.join("img", img_name), caption=f"Image {idx+1}", use_container_width=True)
