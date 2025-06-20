import streamlit as st
import os
from google import genai
from google.genai import types
import pandas as pd

GOOGLE_API_KEY="AIzaSyAITEeCyfnW3Rf5RokHRcHA-2ORzfJw_d4"
client = genai.Client(api_key=GOOGLE_API_KEY)


from dotenv import load_dotenv
load_dotenv()


def recommandation():
    df = st.session_state["df"]
    df_reco = st.session_state["df_reco"]
    st.title("Page de Recommandation")
    if "selected_movie" not in st.session_state:
        st.error("Aucun film sélectionné. Veuillez revenir à la page de recherche.")
    else:
        st.write(f"Le film selectionne est : {st.session_state['selected_movie']}")
        id_film = st.session_state['selected_movie']
        # recos = eval(df_reco.loc[id_film].iloc[0])  
        recos = reco_films(id_film, df)
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
   
   
def reco_films(film, df):
    sys_instruct=f"""
    Tu es un expert en films. Je vais te donner le nom d un film 

    et ton objectif est de me donner 20 recos de films que j'ai importé et formatées de la maniere

    nomfilm_annee qui est le plus similaire au films que je t'ai envoyé. Par exemple même genre de films, même réal, même acteurs,

    donc les films les plus similaires

    Dans ton output tu me fourniras SEULEMENT la liste des 20 meileures recos et rien d autre

    Si tu ne connais pas 20 films de l'acteur ou du réal, ne me met seulement ceux que tu connais.

    Ne renvoie QUE les recos en texte brut et AUCUN FORMATAGE DE TEXT car je vais le parser en liste. 

    Au passage ce sont les titres originales en anglais.


    exemple:

    spiderman_2002

    spiderman 2_2004

    """
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction=sys_instruct),
    contents=[f"Maintenant donne moi la reco pour le film  : {film}"]
    )

    liste_match = []
    liste_recos = response.text.split("\n")
    for reco in liste_recos:
        try:
            liste_match.append(df.loc[reco].name)
        except:
            pass
    return liste_match
