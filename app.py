import streamlit as st
from src.db.init_db import init_db

st.set_page_config(
    page_title="Job Search CRM",
    page_icon="📌",
    layout="wide",
    initial_sidebar_state="expanded",
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

st.info("Système prêt. Utilise les boutons ci-dessous.")

st.subheader("Navigation")
c1, c2, c3, c4, c5 = st.columns(5)

if c1.button("Offres"):
    st.switch_page("pages/1_Offres.py")

if c2.button("Candidatures"):
    st.switch_page("pages/2_Candidatures.py")

if c3.button("Contacts"):
    st.switch_page("pages/3_Contacts.py")

if c4.button("Masters"):
    st.switch_page("pages/4_Masters.py")

if c5.button("Paramètres"):
    st.switch_page("pages/6_Parametres.py")
