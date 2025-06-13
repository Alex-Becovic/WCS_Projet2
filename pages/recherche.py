import streamlit as st
import pandas as pd

def recherche():
    df= pd.read_csv("data/nettoyage_des_donnees.csv")
    films = df["primaryTitle"].dropna().unique().tolist()  # Liste unique des titres
    films.sort() 
    st.title("Tapez le nom d'un film qui vous plait:")
    options = st.selectbox(
    "Quel est votre film préféré?",
    films,
    accept_new_options=False,
    placeholder="Commencez à taper le titre..."
    )
    
    # Cherche l'entrée correspondant au film sélectionné
    film_info = df[df["primaryTitle"] == options].iloc[0]
    
    # Récupère le chemin de l'image
    image_path = film_info.get("backdrop_path", None)

    if pd.notna(image_path):
        # Si ce sont des chemins relatifs d'API (ex: "/abc.jpg"), compléter avec l'URL de base
        if image_path.startswith("/"):
            image_url = f"https://image.tmdb.org/t/p/w500{image_path}"
        else:
            image_url = image_path  # Chemin complet déjà

        st.image(image_url, caption=options, use_container_width=True)

    else:
        st.warning("Aucune image disponible pour ce film.")
    overview = film_info.get("overview", "Aucune description disponible.")
    st.write("Description:")
    st.write(overview)


    clicked = st.button('Accéder à la recommandation')
    if clicked:
        st.session_state['reco'] = film_info["primaryTitle"]
        st.rerun()
    