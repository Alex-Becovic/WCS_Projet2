import pandas as pd
import streamlit as st

from pages.accueil import accueil
from pages.recherche import recherche
from pages.recommandation import recommandation
from streamlit_option_menu import option_menu

@st.cache_data
def load_data():
    return pd.read_csv('data/nettoyage_des_donnees_VF2.csv').set_index("index")

@st.cache_data
def load_reco():
    return pd.read_csv('data/dico_reco_2.csv').set_index("index")
st.session_state["df"] = load_data()
st.session_state["df_reco"] = load_reco()
if "page" not in st.session_state:
    st.session_state["page"] = "Accueil"
st.markdown("<style>[data-testid=stSidebarNav]{display:None;}</style>", unsafe_allow_html=True)
with st.sidebar:
    selected = option_menu("Menu", ["Accueil", 'Recherche', 'Recommandation'], 
        icons=['house', 'film', 'sign-intersection'], menu_icon="cast", default_index=["Accueil", "Recherche", "Recommandation"].index(st.session_state["page"]))
    st.write(selected)
if st.session_state["page"] != selected:
    st.session_state.page = selected
if selected == "Accueil":
    accueil()
elif selected == "Recherche":
    recherche()
elif selected == "Recommandation":
    recommandation()