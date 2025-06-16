import streamlit as st
import pandas as pd


def recommandation():
    st.title("Page de Recommandation")
    if "selected_movie" not in st.session_state:
        st.error("Aucun film sélectionné. Veuillez revenir à la page de recherche.")
    else:
        st.write(f"Le film selectionne est : {st.session_state['selected_movie']}")

   