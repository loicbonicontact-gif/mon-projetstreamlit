import streamlit as st
import pandas as pd

# --- Chargement des données ---
URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/taxis.csv"

@st.cache_data
def load_data():
    return pd.read_csv(URL)

df = load_data()

# --- Titre personnalisé ---
st.title("Dashboard Analyse Taxis - Loïc")

# --- Menu déroulant pour choisir un quartier de prise en charge ---
boroughs = df["pickup_borough"].dropna().unique()
selected_borough = st.selectbox("Choisissez un quartier de prise en charge (pickup_borough) :", sorted(boroughs))

# --- Filtrage du dataframe ---
df_filtered = df[df["pickup_borough"] == selected_borough]

# --- Affichage des 5 premières lignes ---
st.subheader(f"Aperçu des courses - {selected_borough}")
st.dataframe(df_filtered.head(5))

# --- Métrique : nombre total de courses ---
st.metric(label=f"Nombre total de courses ({selected_borough})", value=len(df_filtered))