import streamlit as st
import pandas as pd
from src.db.repositories.applications_repository import list_applications, update_application_status, set_followup, delete_application

st.title('Candidatures')
status_filter = st.selectbox('Filtrer par statut', ['all', 'draft', 'sent', 'followup_due', 'interview', 'rejected', 'accepted'])
rows = list_applications(status_filter)
df = pd.DataFrame([dict(r) for r in rows])

if not df.empty:
    st.dataframe(df[['id','title','company','location','application_date','application_channel','application_status','next_followup_date']], use_container_width=True, hide_index=True)
    selected_id = st.selectbox('Choisir une candidature', df['id'].tolist())
    c1, c2, c3 = st.columns(3)
    new_status = c1.selectbox('Nouveau statut', ['draft', 'sent', 'followup_due', 'interview', 'rejected', 'accepted'])
    next_followup = c2.text_input('Date relance (YYYY-MM-DD)')
    if c3.button('Mettre à jour le statut'):
        update_application_status(selected_id, new_status)
        st.success('Statut candidature mis à jour')
        st.rerun()
    c4, c5 = st.columns(2)
    if c4.button('Enregistrer la relance') and next_followup:
        set_followup(selected_id, next_followup)
        st.success('Relance enregistrée')
        st.rerun()
    if c5.button('Supprimer la candidature'):
        delete_application(selected_id)
        st.warning('Candidature supprimée')
        st.rerun()
else:
    st.info('Aucune candidature enregistrée.')
