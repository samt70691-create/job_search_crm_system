import streamlit as st
import pandas as pd
from src.db.repositories.jobs_repository import list_jobs, create_job, update_job_status, update_job, delete_job, get_job
from src.db.repositories.applications_repository import create_application
from src.db.repositories.activity_repository import log_activity
from src.services.scoring_service import compute_offer_score
from src.services.automation_service import default_followup_date

st.title('Offres')

tab1, tab2, tab3 = st.tabs(['Liste', 'Créer', 'Éditer / supprimer'])

with tab1:
    f1, f2, f3, f4 = st.columns([1,1,2,1])
    status_filter = f1.selectbox('Statut', ['all', 'new', 'to_review', 'to_apply', 'applied', 'ignored', 'closed'])
    job_type_filter = f2.selectbox('Type', ['all', 'CDI', 'alternance', 'stage', 'autre'])
    search = f3.text_input('Recherche')
    include_duplicates = f4.checkbox('Inclure doublons')
    rows = list_jobs(status=status_filter, job_type=job_type_filter, search=search, include_duplicates=include_duplicates)
    df = pd.DataFrame([dict(r) for r in rows])
    if not df.empty:
        st.dataframe(df[['id','title','company','location','job_type','score','priority_level','status','is_duplicate','date_scraped']], use_container_width=True, hide_index=True)
        st.subheader('Actions rapides')
        selected_id = st.selectbox('Choisir une offre', df['id'].tolist(), key='selected_offer_action')
        c1, c2, c3 = st.columns(3)
        if c1.button('Passer en à postuler'):
            update_job_status(selected_id, 'to_apply')
            log_activity('job_offer', selected_id, 'status_update', 'to_apply')
            st.rerun()
        if c2.button('Marquer ignorée'):
            update_job_status(selected_id, 'ignored')
            log_activity('job_offer', selected_id, 'status_update', 'ignored')
            st.rerun()
        if c3.button('Marquer postulée'):
            create_application(selected_id, 'manual', application_status='sent', next_followup_date=default_followup_date(7))
            log_activity('job_offer', selected_id, 'application_created', 'manual')
            st.rerun()
    else:
        st.info('Aucune offre trouvée.')

with tab2:
    with st.form('add_job_form'):
        c1, c2 = st.columns(2)
        title = c1.text_input('Titre *')
        company = c2.text_input('Entreprise')
        c3, c4 = st.columns(2)
        location = c3.text_input('Lieu')
        job_type = c4.selectbox('Type', ['CDI', 'alternance', 'stage', 'autre'])
        url = st.text_input('URL *')
        description = st.text_area('Description')
        has_contact = st.checkbox('Contact trouvé')
        attractive_salary = st.checkbox('Salaire attractif')
        recent = st.checkbox('Annonce récente', value=True)
        notes = st.text_area('Notes')
        submitted = st.form_submit_button('Créer / Upsert l’offre')
        if submitted and title and url:
            score = compute_offer_score(job_type, has_contact=has_contact, recent=recent, attractive_salary=attractive_salary, title=title, description=description, location=location)
            new_id = create_job({'title': title, 'company': company, 'location': location, 'job_type': job_type, 'url': url, 'description_raw': description, 'description_clean': description, 'score': score, 'status': 'new', 'notes': notes, 'priority_level': 'high' if score >= 70 else 'medium'})
            log_activity('job_offer', new_id or 0, 'upsert', url)
            st.success('Offre enregistrée')
            st.rerun()

with tab3:
    rows = list_jobs(include_duplicates=True)
    df = pd.DataFrame([dict(r) for r in rows])
    if not df.empty:
        selected_id = st.selectbox('Choisir une offre à éditer', df['id'].tolist(), key='selected_offer_edit')
        job = get_job(selected_id)
        with st.form('edit_job_form'):
            title = st.text_input('Titre', value=job['title'] or '')
            company = st.text_input('Entreprise', value=job['company'] or '')
            location = st.text_input('Lieu', value=job['location'] or '')
            job_type = st.selectbox('Type', ['CDI', 'alternance', 'stage', 'autre'], index=['CDI','alternance','stage','autre'].index(job['job_type']) if job['job_type'] in ['CDI','alternance','stage','autre'] else 0)
            url = st.text_input('URL', value=job['url'] or '')
            score = st.number_input('Score', min_value=0.0, max_value=100.0, value=float(job['score'] or 0))
            priority = st.selectbox('Priorité', ['low', 'medium', 'high'], index=['low','medium','high'].index(job['priority_level']) if job['priority_level'] in ['low','medium','high'] else 1)
            status = st.selectbox('Statut', ['new', 'to_review', 'to_apply', 'applied', 'ignored', 'closed'], index=['new','to_review','to_apply','applied','ignored','closed'].index(job['status']) if job['status'] in ['new','to_review','to_apply','applied','ignored','closed'] else 0)
            notes = st.text_area('Notes', value=job['notes'] or '')
            save = st.form_submit_button('Sauvegarder')
            if save:
                update_job(selected_id, {'title': title, 'company': company, 'location': location, 'job_type': job_type, 'url': url, 'score': score, 'priority_level': priority, 'status': status, 'notes': notes})
                st.success('Offre mise à jour')
                st.rerun()
        if st.button('Supprimer cette offre'):
            delete_job(selected_id)
            st.warning('Offre supprimée')
            st.rerun()
