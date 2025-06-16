import pandas as pd
import streamlit as st

from pages.accueil import accueil
from pages.recherche import recherche
from pages.recommandation import recommandation
from streamlit_option_menu import option_menu

@st.cache_data
def load_data():
    return pd.read_csv('data/nettoyage_des_donnees_VF2.csv').set_index("index")

st.session_state["df"] = load_data()
with st.sidebar:
    selected = option_menu("Menu", ["Accueil", 'Recherche', 'Recommandation'], 
        icons=['house', 'film', 'sign-intersection'], menu_icon="cast", default_index=0)
    st.write(selected)
if selected == "Accueil":
    accueil()
elif selected == "Recherche":
    recherche()
elif selected == "Recommandation":
    recommandation()