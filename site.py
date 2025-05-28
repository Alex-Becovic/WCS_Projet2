import streamlit as st
from PIL import Image
from pathlib import Path
import streamlit as st

# icone
logo_path = "logo_site.jpg" 
logo_path2 = "images_wild.png"
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.image(logo_path, width=150)  # Logo à gauche
with col2:
    st.image(logo_path2, width=150)  # Image centrée


st.title("Site de recommandation de films")

st.header("Présentation:")  

image_path = "image.png" 

st.image(image_path)

st.write("Voici une étude de marché sur la consommation de cinéma en France, afin de mieux comprendre les attentes et les préférences du public local. Cette étape préliminaire vous permettra de définir une orientation adaptée pour la suite de l’analyse de votre base de données.")

st.subheader("Résultats études exploratoires")

# Affiche une ligne de texte simple (sans mise en forme particulière)
st.text("My classic text")

# Affiche du texte avec mise en forme Markdown
st.markdown(''':rainbow: :rainbow[My markdown]''')  # Ici, un effet arc-en-ciel est appliqué

# Affiche un dataframe (st.write accepte plusieurs arguments et plusieurs types de données)
# st.write    
# st.sidebar.image("logo_site.png", use_container_width=True)