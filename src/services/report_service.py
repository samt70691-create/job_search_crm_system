from src.db.connection import get_connection
import pandas as pd
from pathlib import Path


def build_summary_report():
    conn = get_connection()
    offers = pd.read_sql_query("SELECT id, title, company, location, score, status FROM job_offers WHERE COALESCE(is_duplicate,0)=0 ORDER BY score DESC", conn)
    applications = pd.read_sql_query("SELECT id, job_offer_id, application_status, next_followup_date FROM applications ORDER BY id DESC", conn)
    contacts = pd.read_sql_query("SELECT id, full_name, company, email, contact_type FROM contacts ORDER BY id DESC", conn)
    masters = pd.read_sql_query("SELECT id, program_name, institution, city, score, status FROM masters_programs ORDER BY score DESC", conn)
    conn.close()
    out = Path(__file__).resolve().parents[2] / 'data' / 'exports' / 'system_report.txt'
    lines = []
    lines.append('JOB SEARCH CRM - RAPPORT SYNTHETIQUE')
    lines.append('')
    lines.append(f'Offres actives: {len(offers)}')
    lines.append(f'Candidatures: {len(applications)}')
    lines.append(f'Contacts: {len(contacts)}')
    lines.append(f'Masters: {len(masters)}')
    lines.append('')
    lines.append('TOP OFFRES')
    for _, r in offers.head(10).iterrows():
        lines.append(f"- #{int(r['id'])} | {r['title']} | {r['company']} | {r['location']} | score={r['score']} | {r['status']}")
    lines.append('')
    lines.append('RELANCES')
    due = applications[applications['application_status'] == 'followup_due'] if not applications.empty else applications
    if due.empty:
        lines.append('- Aucune relance due')
    else:
        for _, r in due.iterrows():
            lines.append(f"- candidature #{int(r['id'])} | relance: {r['next_followup_date']}")
    out.write_text('\n'.join(lines), encoding='utf-8')
    return out
