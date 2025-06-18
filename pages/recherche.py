import streamlit as st
import pandas as pd
from outils.yt_link import get_youtube_trailer

def recherche():
    df = st.session_state["df"]

    # Choix d'un film de référence
    pick_movies = st.selectbox(
        "Tapez le nom d'un film qui vous plaît",
        df.index,
        index=None
    )

    if pick_movies is not None:
        selected_movie = df.loc[[pick_movies]]
        image_url = selected_movie["poster_path"].iloc[0]
        st.image(image_url, caption=pick_movies, width=300)

        clicked = st.button("Accéder à la reco")
        if clicked:
            st.session_state["selected_movie"] = selected_movie.index[0]
            st.session_state.page = 'Recommandation'
            st.rerun()

        title = selected_movie["originalTitle"].iloc[0]
        year = selected_movie["startYear"].iloc[0]
        overview = selected_movie["overview"].iloc[0]
        runtime = selected_movie["runtimeMinutes"].iloc[0]
        rating = selected_movie["averageRating"].iloc[0]
        production = selected_movie["production_companies_name"].iloc[0]
        original = selected_movie["original_language"].iloc[0]

        st.markdown(f"## 🎬 {title} ({year})")
        st.markdown(f"**Durée** : {runtime} minutes")
        st.markdown(f"**Note moyenne** : ⭐ {rating}/10")
        st.markdown(f"**Langue originale** : {original}")
        st.markdown(f"**Production** : {production}")
        st.markdown("### Synopsis")
        st.write(overview)

        # get_youtube_trailer(title)  # décommenter si la fonction est prête

    # Titre de la section
    st.title("🎥 Filtres pour explorer les films")

    # Widgets de filtres
    st.header("Filtres")
    selected_years = st.multiselect(
        "Années de sortie",
        options=sorted(df["startYear"].dropna().unique()),
        default=[]
    )

    selected_original_languages = st.multiselect(
        "Langue originale",
        options=sorted(df["original_language"].dropna().unique()),
        default=[]
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
        ((df["averageRating"] >= min_rating) & (df["averageRating"] <= max_rating))
    ]

    if sort_by_popularity:
        filtered_df = filtered_df.sort_values(by="numVotes", ascending=False)

    # Affichage des résultats
    st.markdown("## 🎞️ Résultats des films filtrés")

    if filtered_df.empty:
        st.info("Aucun film ne correspond aux filtres sélectionnés.")
    else:
        for idx, row in filtered_df.iloc[:10].iterrows():
            with st.container():
                cols = st.columns([1, 3])  # image | infos
                with cols[0]:
                    st.image(row["poster_path"], width=150)
                with cols[1]:
                    st.markdown(f"### {row['originalTitle']} ({row['startYear']})")
                    st.markdown(f"**Durée** : {row['runtimeMinutes']} min")
                    st.markdown(f"**Note** : ⭐ {row['averageRating']}/10")
                    st.markdown(f"**Langue** : {row['original_language']}")
                    clicked = st.button("Accéder à la reco",key=idx)
                       
                    if clicked:
                        st.session_state["selected_movie"] = row.name
                        st.session_state.page = 'Recommandation'
                        st.rerun()
                    st.markdown("---")

