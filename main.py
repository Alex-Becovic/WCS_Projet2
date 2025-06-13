import streamlit as st

from pages.accueil import accueil
from pages.recherche import recherche
from pages.recommandation import recommandation
from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu("Menu", ["Accueil", 'Recherche', 'Recommandation'], 
        icons=['house', 'film', 'sign-intersection'], menu_icon="cast", default_index=0)
    st.write(selected)
if selected == "Accueil":
    accueil()
elif selected == "Recherche":
    recherche()
elif selected == "Reco":
    recommandation()