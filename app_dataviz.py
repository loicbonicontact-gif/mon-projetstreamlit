import streamlit as st
import pandas as pd
# J'importe matplotlib pour créer des figures
import matplotlib.pyplot as plt
# J'importe seaborn pour dessiner la heatmap
import seaborn as sns


st.subheader("Aperçu des données")

# Chargement direct du dataset "flights" depuis GitHub
@st.cache_data
def load_data():
 url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/flights.csv"
 return pd.read_csv(url)
df_flights = load_data()

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

# J'importe matplotlib pour créer des figures
import matplotlib.pyplot as plt
# J'importe seaborn pour dessiner la heatmap
import seaborn as sns