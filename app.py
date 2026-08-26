import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_echarts import st_echarts
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
        selected_page = option_menu(
            menu_title="Menu principal",
            options=["Accueil", "Dashboard Vols", "Galerie Photos"],
            icons=["house", "airplane", "images"],
            default_index=0
        )

        # Filtres du Dashboard Vols, affichés uniquement sur cette page
        plage_annees = None
        mois_choisis = None
        if selected_page == "Dashboard Vols":
            st.divider()
            st.markdown("**Filtres**")
            _df_flights_filtres = load_flights()
            _annee_min = int(_df_flights_filtres["year"].min())
            _annee_max = int(_df_flights_filtres["year"].max())
            _tous_les_mois = _df_flights_filtres["month"].unique().tolist()

            plage_annees = st.slider(
                "Plage d'années :", _annee_min, _annee_max, (_annee_min, _annee_max)
            )
            mois_choisis = st.multiselect(
                "Mois : (vide = tous les mois)", _tous_les_mois, default=[]
            )

        # Bloc compte, affiché en bas du menu (après la navigation et les filtres)
        st.divider()
        st.write(f"Bienvenue, **{st.session_state['username']}** !")
        if st.button("Se déconnecter"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.rerun()

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
        st.caption("Trafic aérien mensuel — dataset seaborn 'flights' — filtres dans le menu latéral")

        df_flights = load_flights()
        tous_les_mois = df_flights["month"].unique().tolist()

        # Je filtre le dataframe selon la plage d'années et les mois choisis dans la sidebar
        # (aucun mois sélectionné = pas de filtre, on garde tous les mois)
        mois_filtre = mois_choisis if mois_choisis else tous_les_mois
        df_filtre = df_flights[
            (df_flights["year"] >= plage_annees[0])
            & (df_flights["year"] <= plage_annees[1])
            & (df_flights["month"].isin(mois_filtre))
        ]

        if df_filtre.empty:
            st.warning("Aucune donnée pour cette combinaison de filtres.")
            st.stop()

        # --- LIGNE DE KPIs ---
        total_passagers = df_filtre["passengers"].sum()
        moyenne_mensuelle = df_filtre["passengers"].mean()

        passagers_debut = df_filtre[df_filtre["year"] == plage_annees[0]]["passengers"].sum()
        passagers_fin = df_filtre[df_filtre["year"] == plage_annees[1]]["passengers"].sum()
        croissance_periode = (
            ((passagers_fin - passagers_debut) / passagers_debut) * 100
            if passagers_debut > 0 and plage_annees[0] != plage_annees[1]
            else 0
        )

        mois_pic_filtre = df_filtre.groupby("month")["passengers"].mean().idxmax()

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Total passagers", f"{total_passagers:,}")
        kpi2.metric("Moyenne mensuelle", f"{moyenne_mensuelle:,.0f}")
        kpi3.metric("Croissance sur la période", f"{croissance_periode:+.0f}%")
        kpi4.metric("Mois le plus chargé", mois_pic_filtre)

        st.markdown("---")

        # --- GRAPHIQUE PRINCIPAL : évolution du trafic, en pleine largeur ---
        st.markdown("**Évolution du trafic par année**")
        passagers_par_annee = df_filtre.groupby("year")["passengers"].sum()
        options_evolution = {
            "tooltip": {"trigger": "axis"},
            "xAxis": {
                "type": "category",
                "data": [str(annee) for annee in passagers_par_annee.index.tolist()],
            },
            "yAxis": {"type": "value"},
            "series": [
                {
                    "data": passagers_par_annee.values.tolist(),
                    "type": "line",
                    "smooth": True,
                    "areaStyle": {},
                    "name": "Passagers",
                }
            ],
            "grid": {"left": "6%", "right": "3%", "bottom": "10%", "containLabel": True},
        }
        st_echarts(options=options_evolution, height="380px")

        st.markdown("---")

        # --- GRAPHIQUES SECONDAIRES, CÔTE À CÔTE ---
        col_saisonnalite, col_heatmap = st.columns(2)

        with col_saisonnalite:
            st.markdown("**Saisonnalité (moyenne par mois)**")
            moyenne_par_mois = df_filtre.groupby("month")["passengers"].mean().reindex(tous_les_mois).dropna()
            options_saisonnalite = {
                "tooltip": {"trigger": "axis"},
                "xAxis": {
                    "type": "category",
                    "data": moyenne_par_mois.index.tolist(),
                    "axisLabel": {"rotate": 45},
                },
                "yAxis": {"type": "value"},
                "series": [
                    {
                        "data": [round(v) for v in moyenne_par_mois.values.tolist()],
                        "type": "bar",
                        "name": "Moyenne passagers",
                        "itemStyle": {"color": "#5470c6"},
                    }
                ],
                "grid": {"left": "12%", "right": "5%", "bottom": "22%", "containLabel": True},
            }
            st_echarts(options=options_saisonnalite, height="350px")

        with col_heatmap:
            st.markdown("**Heatmap passagers (mois × année)**")
            # Tableau croisé : lignes = mois (janvier en haut, ECharts empile son axe Y de bas en haut donc on inverse la liste)
            tableau_croise = df_filtre.pivot(index="month", columns="year", values="passengers").reindex(tous_les_mois)
            annees_heatmap = [str(a) for a in tableau_croise.columns.tolist()]
            mois_heatmap = list(reversed(tableau_croise.index.tolist()))
            tableau_croise = tableau_croise.reindex(mois_heatmap)

            donnees_heatmap = []
            for i, mois in enumerate(mois_heatmap):
                for j, annee in enumerate(annees_heatmap):
                    valeur = tableau_croise.iloc[i, j]
                    if pd.notna(valeur):
                        donnees_heatmap.append([j, i, round(valeur)])

            options_heatmap = {
                "tooltip": {"position": "top"},
                "grid": {"height": "75%", "top": "5%", "left": "18%", "right": "5%"},
                "xAxis": {"type": "category", "data": annees_heatmap, "splitArea": {"show": True}},
                "yAxis": {"type": "category", "data": mois_heatmap, "splitArea": {"show": True}},
                "visualMap": {
                    "min": 0,
                    "max": int(df_filtre["passengers"].max()),
                    "calculable": True,
                    "orient": "horizontal",
                    "left": "center",
                    "bottom": "0%",
                    "inRange": {"color": ["#DCEEFF", "#5470c6", "#0B3D91"]},
                },
                "series": [
                    {
                        "name": "Passagers",
                        "type": "heatmap",
                        "data": donnees_heatmap,
                        "label": {"show": True, "fontSize": 9},
                    }
                ],
            }
            st_echarts(options=options_heatmap, height="380px")

        # Le détail des données brutes reste disponible, mais replié par défaut
        with st.expander("Voir les données détaillées"):
            st.dataframe(df_filtre, use_container_width=True)

    elif selected_page == "Galerie Photos":
        st.title("Album Photos")
        st.write("Voici la galerie multimédia organisée sur 3 colonnes :")

        # Les photos ont des ratios différents : on force une hauteur uniforme
        # pour que la galerie reste alignée, quelle que soit l'image.
        st.markdown(
            """
            <style>
            [data-testid="stImage"] img {
                height: 220px;
                width: 100%;
                object-fit: cover;
                border-radius: 12px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        cols = st.columns(3)
        image_files = lister_images()[:3]
        for idx, img_name in enumerate(image_files):
            with cols[idx % 3]:
                st.image(os.path.join("img", img_name), caption=f"Image {idx+1}", use_container_width=True)
