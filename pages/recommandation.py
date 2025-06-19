import streamlit as st
import pandas as pd


def recommandation():
    df = st.session_state["df"]
    df_reco = st.session_state["df_reco"]
    st.title("Page de Recommandation")
    if "selected_movie" not in st.session_state:
        st.error("Aucun film sélectionné. Veuillez revenir à la page de recherche.")
    else:
        st.write(f"Le film selectionne est : {st.session_state['selected_movie']}")
        id_film = st.session_state['selected_movie']
        recos = eval(df_reco.loc[id_film].iloc[0])  
        recos_infos = df.loc[recos] 

        # Afficher les films recommandés sous forme de mini fiches
        st.markdown("### Films recommandés")
        for _, row in recos_infos.iterrows():
            st.markdown(f"#### 🎬 {row['originalTitle']} ({row['startYear']})")
            st.image(row["poster_path"], caption=row["originalTitle"], width=150)  # Afficher le poster du film
            st.markdown(f"**Durée** : {row['runtimeMinutes']} minutes")
            st.markdown(f"**Note moyenne** : ⭐ {row['averageRating']}/10")
            st.markdown(f"**Langue originale** : {row['original_language']}")
            st.markdown(f"**Production** : {row['production_companies_name']}")
            st.markdown("---")  # Ajouter une séparation entre les fiches
   