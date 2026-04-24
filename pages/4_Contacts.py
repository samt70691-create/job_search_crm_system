import streamlit as st
import pandas as pd
from src.db.repositories.contacts_repository import list_contacts, create_contact

st.title('Contacts')
with st.expander('Ajouter un contact'):
    with st.form('contact_form'):
        c1, c2 = st.columns(2)
        full_name = c1.text_input('Nom complet *')
        company = c2.text_input('Entreprise')
        role = st.text_input('Rôle')
        email = st.text_input('Email')
        linkedin_url = st.text_input('LinkedIn URL')
        contact_type = st.selectbox('Type de contact', ['RH', 'recruteur', 'manager', 'école', 'autre'])
        confidence_score = st.slider('Niveau de confiance', 0.0, 1.0, 0.7, 0.1)
        notes = st.text_area('Notes')
        if st.form_submit_button('Créer le contact') and full_name:
            create_contact({'full_name': full_name, 'company': company, 'role': role, 'email': email, 'linkedin_url': linkedin_url, 'contact_type': contact_type, 'confidence_score': confidence_score, 'notes': notes})
            st.success('Contact ajouté')
            st.rerun()
search = st.text_input('Recherche contact')
rows = list_contacts(search)
df = pd.DataFrame([dict(r) for r in rows])
if not df.empty:
    st.dataframe(df[['id','full_name','company','role','email','contact_type','confidence_score','date_found']], use_container_width=True, hide_index=True)
else:
    st.info('Aucun contact.')
