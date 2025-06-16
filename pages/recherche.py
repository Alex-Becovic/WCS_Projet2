import streamlit as st
import pandas as pd
from outils.yt_link import get_youtube_trailer
def recherche():
    df = st.session_state["df"]
    pick_movies = st.selectbox("Tapez le nom d'un film qui vous plait",
                df.index,index=None)
    if pick_movies is not None:
        selected_movie = df.loc[[pick_movies]] # créé un filtre qui affiche la ligne du film selctionné
        image_url = selected_movie["poster_path"].iloc[0]  # Récupérer l'URL de l'image
        st.image(image_url, caption=pick_movies, width=300)  # Afficher l'image
        clicked = st.button("Accéder à la reco")
        if clicked:
            st.session_state["selected_movie"] = selected_movie.index[0]
            st.rerun()
        title = selected_movie["originalTitle"].iloc[0]
        year = selected_movie["startYear"].iloc[0]
        overview = selected_movie["overview"].iloc[0]
        runtime = selected_movie["runtimeMinutes"].iloc[0]
        rating = selected_movie["averageRating"].iloc[0]
        production = selected_movie["production_companies_name"].iloc[0]
        original = selected_movie["original_language"].iloc[0]
        image_url = selected_movie["poster_path"].iloc[0]
        st.markdown(f"## 🎬 {title} ({year})")
        st.markdown(f"**Durée** : {runtime} minutes")
        st.markdown(f"**Note moyenne** : ⭐ {rating}/10")
        st.markdown(f"**Langue originale** : {original}")
        st.markdown(f"**Production** : {production}")
        st.markdown("### Synopsis")
        st.write(overview)

        # Chargement de l'iframe pour la bande annonce
        #title_encoded = selected_movie["encodedTitle"].iloc[0]
        #get_youtube_trailer(title_encoded)

    # Colonnes à afficher dans le tableau
    columns_to_display = ["originalTitle", "startYear", "runtimeMinutes", "averageRating", "original_language"]

    # Titre de la section
    st.title("🎥 Tableau intéractif des films")

    # Widgets pour les filtres
    st.header("Filtres")
    selected_years = st.multiselect(
        "Années de sortie",
        options=df["startYear"].dropna().unique(),
        default=[],  # Par défaut, vide
        help="Sélectionnez une ou plusieurs années de sortie"
    )

    selected_original_languages = st.multiselect(
        "Langue originale",
        options=df["original_language"].dropna().unique(),
        default=[],  # Par défaut, vide
        help="Sélectionnez une ou plusieurs langues originales"
    )

    min_rating, max_rating = st.slider(
        "Sélectionnez une fourchette de notes",
        min_value=0.0, max_value=10.0, value=(8.0, 9.0), step=0.1
    )

    sort_by_popularity = st.checkbox("Afficher les films les plus populaires")

    # Appliquer les filtres
    filtered_df = df[
        ((df["startYear"].isin(selected_years)) if selected_years else True) &
        ((df["original_language"].isin(selected_original_languages)) if selected_original_languages else True) &
        (((df["averageRating"] >= min_rating) & (df["averageRating"] <= max_rating)) if min_rating or max_rating else True)
    ]

    # Trier par popularité si le bouton est activé
    if sort_by_popularity:
        filtered_df = filtered_df.sort_values(by="numVotes", ascending=False)

    # Afficher le tableau filtré
    st.dataframe(filtered_df[columns_to_display])