import streamlit as st
import pandas as pd
import plotly.express as px
from matplotlib import cm
from matplotlib.colors import to_hex

def accueil():
    # Entête de la page:
    logo_path = "images/logo_site.jpg"
    logo_path2 = "images/images_wild.png"
    image1_path = "images/alex.png"  
    image2_path = "images/amin.png"
    image3_path = "images/david.png"
    header_col1, header_col2 = st.columns([3, 3])

    with header_col1:
        st.image(logo_path2, width=100)
        empty_col1, center_col, empty_col2 = st.columns([1, 6, 1])
        with center_col:
            st.image(logo_path, width=300)

    with header_col2:
        _, _, img_col = st.columns([1, 1, 2])
        with img_col:
            st.subheader("Équipe d'experts data")
            st.image(image1_path, width=100, caption="Alex")
            st.image(image2_path, width=100, caption="Amin")
            st.image(image3_path, width=100, caption="David")
                
    st.title("Site de recommandation de films")
    st.header("Présentation:")
    st.image("images/image.png")
    st.write(
        "Bienvenue sur notre site de recommandation de films. "
        "Vous trouverez sur cette page des informations clés sur l'étude de marché "
        "du cinéma en France depuis 1950 à aujourd'hui."
    )

    st.subheader("Résultats études exploratoires")

    # 1er Graphique : Nombre de votes par genre
    df_genre = pd.read_csv("data/genres.csv")
    genres = df_genre.sum()
    genres.drop("Unnamed: 0", inplace=True)
    genres = genres.sort_values(ascending=False)
    genres_df = pd.DataFrame({"Genre": genres.index, "Votes": genres.values})

    top10_genres = genres_df["Genre"].iloc[:10].tolist()
    cmap = cm.get_cmap('plasma', 10)
    top_colors = [to_hex(cmap(i)) for i in range(10)]
    gris = '#d3d3d3'

    color_map = {genre: top_colors[i] if genre in top10_genres else gris 
                 for i, genre in enumerate(genres_df["Genre"])}

    fig = px.bar(
        genres_df,
        x="Genre",
        y="Votes",
        color="Genre",
        title="Nombre de votes par genre (top 10 en couleurs)",
        color_discrete_map=color_map
    )
    fig.update_layout(xaxis=dict(tickangle=45, tickfont=dict(size=10)))
    st.plotly_chart(fig)

    # 2e Graphique : Nombre de films par année
    if "df" in st.session_state:
        df = st.session_state["df"].copy()

        df["startYear"] = pd.to_numeric(df["startYear"], errors="coerce")
        df = df.dropna(subset=["startYear"])
        df["startYear"] = df["startYear"].astype(int)
        df = df[df["startYear"] >= 1950]

        df["Décennie"] = (df["startYear"] // 10) * 10
        df["Décennie"] = df["Décennie"].astype(str) + "s"
        df["Catégorie"] = df["Décennie"].apply(lambda x: "Ancienne décennie" if int(x[:4]) < 1980 else "Moderne")

        df_films_per_year = df.groupby(["startYear", "Décennie", "Catégorie"]).size().reset_index(name="Nombre de films")

        decennies = sorted(df_films_per_year["Décennie"].unique())
        decennies_grises = [d for d in decennies if int(d[:4]) < 1980]
        decennies_colorées = [d for d in decennies if int(d[:4]) >= 1980]

        gris = "#d3d3d3"
        cmap = cm.get_cmap('plasma', len(decennies_colorées))
        couleurs_vives = [to_hex(cmap(i)) for i in range(len(decennies_colorées))]

        color_map = {d: gris for d in decennies_grises}
        color_map.update({d: couleurs_vives[i] for i, d in enumerate(decennies_colorées)})

        fig2 = px.bar(
            df_films_per_year,
            x="startYear",
            y="Nombre de films",
            color="Décennie",
            title="Nombre de films par année",
            color_discrete_map=color_map,
        )

        fig2.update_layout(
            xaxis=dict(tickangle=45),
            height=500,
            title_x=0.5,
            legend_title_text="Décennie",
        )

        fig2.add_annotation(
            xref="paper", yref="paper", x=1.05, y=1,
            text="🟦 Ancienne décennie (1950s–1970s)<br>🌈 Moderne (1980s–2020s)",
            showarrow=False,
            align="left",
            font=dict(size=12, color="black"),
            bordercolor="black",
            borderwidth=1,
            bgcolor="white",
        )

        st.plotly_chart(fig2)

        # 3e Graphique : Nombre de films par langue
        df_films_par_pays = df.groupby("original_language").size().reset_index(name="Nombre de films")
        df_films_par_pays = df_films_par_pays.sort_values(by="Nombre de films", ascending=False)

        top_3 = df_films_par_pays["original_language"].iloc[:3]
        df_films_par_pays = df_films_par_pays[df_films_par_pays["original_language"].isin(['ja', 'fr', 'en'])]

        couleurs = ['#636EFA', '#EF553B', '#00CC96']
        color_map = [couleurs[i] if lang in top_3.values else gris 
                     for i, lang in enumerate(df_films_par_pays["original_language"])]

        fig3 = px.pie(
            df_films_par_pays,
            values='Nombre de films',
            names='original_language',
            title='Pourcentage de films par langue originale',
        )

        fig3.update_traces(marker=dict(colors=color_map))
        st.plotly_chart(fig3)

    else:
        st.error("Le DataFrame principal ('df') n'est pas chargé dans session_state.")
