import streamlit as st
import requests
def get_youtube_trailer(title):
    trailer_url = f"https://www.youtube.com/results?search_query={title}+trailer"
    st.markdown("🎥 Bande annonce officielle")

    # Récupérer la première vidéo de la recherche YouTube
    response = requests.get(trailer_url)
    if response.status_code == 200:
    # Extraire l'ID de la première vidéo (simplifié pour cet exemple)
        video_id = response.text.split('watch?v=')[1].split('"')[0]
        video_url = f"https://www.youtube.com/embed/{video_id}"
        # Intégrer l'iframe dans Streamlit
        st.markdown(f"""
            <iframe width="560" height="315" src="{video_url}" 
            frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen></iframe>
        """, unsafe_allow_html=True)
    else:
        st.error("Impossible de récupérer la bande-annonce.")