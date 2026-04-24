import streamlit as st
from src.db.init_db import init_db
from src.services.dashboard_service import get_dashboard_metrics
from src.services.bootstrap_service import ensure_bootstrap

st.set_page_config(page_title='Job Search CRM', page_icon='📌', layout='wide')
init_db()
ensure_bootstrap()
metrics = get_dashboard_metrics()

st.title('Job Search CRM')
st.caption('Pilotage des offres, candidatures, contacts et masters')

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric('Offres', metrics['offers_total'])
c2.metric('Nouvelles', metrics['offers_new'])
c3.metric('À postuler', metrics['offers_to_apply'])
c4.metric('Candidatures', metrics['applications_total'])
c5.metric('Relances', metrics['followups_due'])
c6.metric('Contacts', metrics['contacts_total'])

st.info('Système prêt. Utilise le menu de gauche.')
