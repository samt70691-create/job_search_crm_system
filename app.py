import streamlit as st
from src.db.init_db import init_db

st.set_page_config(
    page_title="Job Search CRM",
    page_icon="📌",
    layout="wide",
)

init_db()

st.title("Job Search CRM")
st.caption("Pilotage des offres, candidatures, contacts et masters")

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Offres", 3)
col2.metric("Nouvelles", 1)
col3.metric("À postuler", 2)
col4.metric("Candidatures", 0)
col5.metric("Relances", 0)
col6.metric("Contacts", 1)

st.info("Système prêt. Utilise le menu ci-dessous.")

page = st.selectbox(
    "Choisis une section",
    [
        "Accueil",
        "Offres",
        "Candidatures",
        "Contacts",
        "Masters",
        "Paramètres",
    ],
)

if page == "Accueil":
    st.success("Application en ligne et fonctionnelle.")
    st.write("Tu peux maintenant utiliser le menu déroulant pour naviguer.")

elif page == "Offres":
    st.subheader("Offres")
    st.write("Section Offres prête. Nous pouvons ensuite brancher l'affichage détaillé.")

elif page == "Candidatures":
    st.subheader("Candidatures")
    st.write("Section Candidatures prête.")

elif page == "Contacts":
    st.subheader("Contacts")
    st.write("Section Contacts prête.")

elif page == "Masters":
    st.subheader("Masters")
    st.write("Section Masters prête.")

elif page == "Paramètres":
    st.subheader("Paramètres")
    st.text_input("Nom")
    st.text_input("Email")
    st.text_input("Localisation")
    st.text_area("Postes cibles")
    st.text_area("Mots-clés prioritaires")
    st.text_area("Villes prioritaires")
    st.button("Sauvegarder")
