import streamlit as st
import pandas as pd
import plotly.express as px
import difflib
# Fonction pour la page d'accueil

##################################page d'accueil##########################################
def accueil():
    # Entête de la page:
    logo_path = "logo_site.jpg"
    logo_path2 = "images_wild.png"
    image1_path = "alex.png"  
    image2_path = "amin.png"
    image3_path = "david.png"
    header_col1, header_col2 = st.columns([3, 3])  # 75% / 25% : pour placer images à droite

    with header_col1:
        # Logo à gauche (images_wild.png)
        st.image(logo_path2, width=100)

        # Crée des colonnes pour centrer le logo principal
        empty_col1, center_col, empty_col2 = st.columns([1, 6, 1])  # Ajustable

        with center_col:
            st.image(logo_path, width=300)
        
    # Images de l'équipe à droite    
    with header_col2:
        # Crée des colonnes invisibles pour pousser img_col vers la droite
        _, _, img_col = st.columns([1, 1, 2])

        # Affiche le titre + les images dans img_col
        with img_col:
            st.subheader("Équipe d'experts data")
            st.image(image1_path, width=100, caption="Alex")
            st.image(image2_path, width=100, caption="Amin")
            st.image(image3_path, width=100, caption="David")
            
    st.title("Site de recommandation de films")

    st.header("Présentation:")  

    image_path = "image.png" 

    st.image(image_path)

    st.write("Bienvenu sur notre site de recommandation de films. Vous trouverez sur cette page des informations clés sur l'étude de marché du cinéma en France depuis 1950 à aujourd'hui.")

    st.subheader("Résultats études exploratoires")
    
    

# 1e Graphique: Nombre de votes par genre

    df_genre = pd.read_csv("genres.csv")
    genres = df_genre.sum()
    genres.drop("Unnamed: 0", inplace=True)
    # je sort les genres dans l'ordre croissant de leur occurrence
    genres = genres.sort_values(ascending=False)
    # Conversion en DataFrame pour l'utilisation de `color`
    genres_df = pd.DataFrame({"Genre": genres.index, "Votes": genres.values})
    # Création du graphique à barres avec Plotly Express
    fig = px.bar(genres_df, x="Genre", y="Votes", color="Genre", title="Nombre de votes par genre", labels={"x": "Genre", "y": "Nombre de votes"})
    # pour incliner l'axe des x:
    fig.update_layout(xaxis=dict(tickangle=45, tickfont=dict(size=10), showline=True, showticklabels=True))
    st.plotly_chart(fig)

    # 2e Graphique: Nombre de films par année

    df = pd.read_csv('nettoyage_des_donnees.csv')
    df_films_per_year = df.groupby("startYear").size().reset_index(name="Nombre de films")
    fig2 = px.bar(df_films_per_year, x='startYear', y='Nombre de films', title='Nombre de films par année')
    fig2.update_layout(xaxis=dict(tickangle=45),height=500, title_x=0.5)
    st.plotly_chart(fig2)

    # 3e Graphique: Nombre de films par pays
    # On compte le nombre de films par pays (original_language)
    # On utilise groupby pour regrouper par 'original_language' et size() pour compter les occurrences
    # On réinitialise l'index pour obtenir un DataFrame propre
    df_films_par_pays = df.groupby("original_language").size().reset_index(name="Nombre de films")
    fig3 = px.pie(df_films_par_pays, values='Nombre de films', names='original_language', title='Pourcentage de films par langue originale',
                color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig3)
    
##################################""page de recherche""##########################################

# Fonction pour la page de recherche    
    
def recherche():
    df= pd.read_csv("nettoyage_des_donnees.csv")
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

    
################################### Fonction pour la page de recommandation###########################################
def recommandation():
    pass
 
    # Vous pouvez ajouter des éléments interactifs ou des informations supplémentaires ici
    
