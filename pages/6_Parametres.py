import streamlit as st
from pathlib import Path
from src.db.init_db import init_db
from src.services.export_service import export_jobs_to_excel
from src.services.automation_service import run_daily_maintenance
from src.services.profile_service import load_profile, save_profile
from src.services.report_service import build_summary_report

st.title('Paramètres & Profil')
profile = load_profile()
with st.form('profile_form'):
    candidate_name = st.text_input('Nom', value=profile['candidate_name'])
    headline = st.text_input('Titre', value=profile['headline'])
    email = st.text_input('Email', value=profile['email'])
    phone = st.text_input('Téléphone', value=profile['phone'])
    location = st.text_input('Localisation', value=profile['location'])
    mobility = st.text_input('Mobilité', value=profile['mobility'])
    target_roles = st.text_area('Postes cibles', value=profile['target_roles'])
    priority_locations = st.text_area('Lieux prioritaires', value=profile['priority_locations'])
    priority_keywords = st.text_area('Mots-clés prioritaires', value=profile['priority_keywords'])
    cv_summary = st.text_area('Résumé CV', value=profile['cv_summary'])
    if st.form_submit_button('Sauvegarder le profil'):
        save_profile({'candidate_name': candidate_name, 'headline': headline, 'email': email, 'phone': phone, 'location': location, 'mobility': mobility, 'target_roles': target_roles, 'priority_locations': priority_locations, 'priority_keywords': priority_keywords, 'cv_summary': cv_summary, 'languages': profile['languages']})
        st.success('Profil sauvegardé')
        st.rerun()

c1, c2, c3, c4 = st.columns(4)
if c1.button('Initialiser / réparer la base'):
    init_db()
    st.success('Base initialisée')
if c2.button('Lancer maintenance quotidienne'):
    result = run_daily_maintenance()
    st.success(f"Maintenance terminée | doublons marqués: {result['duplicates_marked']}")
if c3.button('Exporter les offres en Excel'):
    export_path = export_jobs_to_excel()
    st.success(f'Export généré : {export_path.name}')
if c4.button('Générer rapport synthétique'):
    report_path = build_summary_report()
    st.success(f'Rapport généré : {report_path.name}')

export_file = Path(__file__).resolve().parents[1] / 'data' / 'exports' / 'job_offers.xlsx'
if export_file.exists():
    with open(export_file, 'rb') as f:
        st.download_button('Télécharger le dernier export Excel', f, file_name='job_offers.xlsx')
report_file = Path(__file__).resolve().parents[1] / 'data' / 'exports' / 'system_report.txt'
if report_file.exists():
    with open(report_file, 'rb') as f:
        st.download_button('Télécharger le rapport système', f, file_name='system_report.txt')
