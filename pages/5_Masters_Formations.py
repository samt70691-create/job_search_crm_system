import streamlit as st
import pandas as pd
from src.db.repositories.masters_repository import list_masters, create_master

st.title('Masters & Formations')
with st.expander('Ajouter un master / formation'):
    with st.form('master_form'):
        c1, c2 = st.columns(2)
        program_name = c1.text_input('Nom du programme *')
        institution = c2.text_input('Institution')
        city = st.text_input('Ville')
        domain = st.text_input('Domaine')
        deadline = st.text_input('Date limite')
        url = st.text_input('URL')
        score = st.slider('Score', 0, 100, 50)
        description = st.text_area('Description')
        if st.form_submit_button('Ajouter') and program_name:
            create_master({'program_name': program_name, 'institution': institution, 'city': city, 'domain': domain, 'deadline': deadline, 'url': url, 'score': score, 'description': description})
            st.success('Programme ajouté')
            st.rerun()
status_filter = st.selectbox('Statut master', ['all', 'new', 'to_review', 'preparing', 'submitted', 'rejected', 'admitted'])
search = st.text_input('Recherche master')
rows = list_masters(status_filter, search)
df = pd.DataFrame([dict(r) for r in rows])
if not df.empty:
    st.dataframe(df[['id','program_name','institution','city','domain','deadline','score','status']], use_container_width=True, hide_index=True)
else:
    st.info('Aucun programme.')
