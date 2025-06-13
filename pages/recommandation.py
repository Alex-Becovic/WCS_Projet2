import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler

def recommandation():
    st.title("Page de Recommandation")

    # Chargement et préparation des données
    df = pd.read_csv("nettoyage_des_donnees.csv")
    df["startYear_original"] = df["startYear"]
    df["film_id"] = df["originalTitle"] + " (" + df["startYear_original"].astype(str) + ")"

    # Normalisation
    scaler = MinMaxScaler()
    df["startYear"] = scaler.fit_transform(df[["startYear"]])

    df_film_annee = df.set_index("originalTitle")

    # Colonnes numériques uniquement
    colonnes_num = df_film_annee.select_dtypes(include='number').columns
    features = df_film_annee[colonnes_num]

    model = NearestNeighbors(n_neighbors=10)
    model.fit(features)

    #  FILTRES supplémentaires
    genres = sorted(set(g for sublist in df['genres'].dropna().str.split(',') for g in sublist))
    acteurs = sorted(set(a for sublist in df['primaryName'].dropna().str.strip('[]').str.replace("'", "").str.split(',') for a in sublist))

    genre_choisi = st.selectbox("Filtrer par genre", ["Tous"] + genres)
    acteur_choisi = st.selectbox("Filtrer par acteur", ["Tous"] + acteurs)
    titre_choisi = st.selectbox("Choisir un film", df["primaryTitle"].unique())

    # Met à jour le film sélectionné si un choix est fait
    film_selectionne = titre_choisi
    st.session_state['reco'] = film_selectionne

    if st.button("Obtenir des recommandations"):
        try:
            distances, indices = model.kneighbors([features.loc[film_selectionne]])
            reco_indices = indices[0][1:]
            reco_df = df_film_annee.iloc[reco_indices].copy()
            reco_df["distance"] = distances[0][1:]
            reco_df["film_id"] = reco_df.index

            # Appliquer les filtres
            if genre_choisi != "Tous":
                reco_df = reco_df[reco_df['genres'].str.contains(genre_choisi, na=False)]
            if acteur_choisi != "Tous":
                reco_df = reco_df[reco_df['primaryName'].str.contains(acteur_choisi, na=False)]

            if not reco_df.empty:
                st.dataframe(reco_df[["film_id", "distance", "genres", "primaryName"]])
            else:
                st.warning("Aucune recommandation trouvée avec les filtres choisis.")
        except KeyError:
            st.error("Film non trouvé.")
