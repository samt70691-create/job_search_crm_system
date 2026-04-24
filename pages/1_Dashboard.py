import streamlit as st
import plotly.express as px
from src.services.dashboard_service import get_dashboard_metrics, get_recent_offers, get_offer_status_counts, get_followups_due
from src.services.automation_service import run_daily_maintenance
from src.services.profile_service import load_profile

profile = load_profile()
st.title('Dashboard')
st.caption(f"{profile['candidate_name']} · {profile['headline']}")
if st.button('Lancer maintenance quotidienne'):
    result = run_daily_maintenance()
    st.success(f"Maintenance OK | doublons marqués: {result['duplicates_marked']}")
    st.rerun()

metrics = get_dashboard_metrics()
cols = st.columns(6)
items = [('Offres', metrics['offers_total']), ('Nouvelles', metrics['offers_new']), ('À postuler', metrics['offers_to_apply']), ('Candidatures', metrics['applications_total']), ('Relances', metrics['followups_due']), ('Contacts', metrics['contacts_total'])]
for col, (label, value) in zip(cols, items):
    col.metric(label, value)

left, right = st.columns([1.2, 1])
with left:
    st.subheader('Top offres')
    st.dataframe(get_recent_offers(10), use_container_width=True, hide_index=True)
with right:
    st.subheader('Statuts')
    status_df = get_offer_status_counts()
    if not status_df.empty:
        fig = px.bar(status_df, x='status', y='count')
        st.plotly_chart(fig, use_container_width=True)

st.subheader('Relances dues')
followups = get_followups_due()
if not followups.empty:
    st.dataframe(followups, use_container_width=True, hide_index=True)
else:
    st.caption('Aucune relance due.')
