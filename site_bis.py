
import streamlit as st
from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu("Menu", ["Accueil", 'Recherche', 'Recommandation'], 
        icons=['house', 'film', 'sign-intersection'], menu_icon="cast", default_index=1)
    st.write(selected)
if selected == "Accueil":
    st.title("Bienvenue sur le site de votre Taxi favori Alex")
elif selected == "Recherche":
    st.title("Tapez le nom d'un film qui vous plait")