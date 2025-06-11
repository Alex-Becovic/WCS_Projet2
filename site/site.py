import streamlit as st
from PIL import Image
from pathlib import Path
import streamlit as st
import numpy as np
import pandas as pd

# Sidebar avec le menu
from streamlit_option_menu import option_menu
from pages import accueil
from pages import recherche

with st.sidebar:
    selected = option_menu("Menu", ["Accueil", 'Recherche', 'Recommandation'], 
        icons=['house', 'film', 'sign-intersection'], menu_icon="cast", default_index=1)
    st.write(selected)
if selected == "Accueil":
    accueil()
elif selected == "Recherche":
    recherche()

      
    
    


 