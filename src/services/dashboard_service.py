from src.db.connection import get_connection
import pandas as pd


def get_dashboard_metrics():
    conn = get_connection()
    cur = conn.cursor()
    metrics = {
        'offers_total': cur.execute('SELECT COUNT(*) FROM job_offers WHERE COALESCE(is_duplicate,0)=0').fetchone()[0],
        'offers_new': cur.execute("SELECT COUNT(*) FROM job_offers WHERE status = 'new' AND COALESCE(is_duplicate,0)=0").fetchone()[0],
        'offers_to_apply': cur.execute("SELECT COUNT(*) FROM job_offers WHERE status = 'to_apply' AND COALESCE(is_duplicate,0)=0").fetchone()[0],
        'applications_total': cur.execute('SELECT COUNT(*) FROM applications').fetchone()[0],
        'followups_due': cur.execute("SELECT COUNT(*) FROM applications WHERE application_status = 'followup_due'").fetchone()[0],
        'contacts_total': cur.execute('SELECT COUNT(*) FROM contacts').fetchone()[0],
        'masters_total': cur.execute('SELECT COUNT(*) FROM masters_programs').fetchone()[0],
    }
    conn.close()
    return metrics


def get_recent_offers(limit=10):
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT id, title, company, location, job_type, score, status, date_scraped FROM job_offers WHERE COALESCE(is_duplicate,0)=0 ORDER BY score DESC, id DESC LIMIT {int(limit)}", conn)
    conn.close()
    return df


def get_offer_status_counts():
    conn = get_connection()
    df = pd.read_sql_query("SELECT status, COUNT(*) as count FROM job_offers WHERE COALESCE(is_duplicate,0)=0 GROUP BY status ORDER BY count DESC", conn)
    conn.close()
    return df


def get_followups_due():
    conn = get_connection()
    df = pd.read_sql_query("SELECT a.id, j.title, j.company, a.next_followup_date, a.application_status FROM applications a JOIN job_offers j ON a.job_offer_id = j.id WHERE a.application_status = 'followup_due' ORDER BY a.next_followup_date ASC", conn)
    conn.close()
    return df
