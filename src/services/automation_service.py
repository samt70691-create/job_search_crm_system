from datetime import datetime, timedelta
from src.services.dedup_service import detect_and_mark_duplicates
from src.db.connection import get_connection


def mark_followups_due():
    conn = get_connection()
    today = datetime.utcnow().strftime('%Y-%m-%d')
    conn.execute(
        "UPDATE applications SET application_status = 'followup_due', updated_at = CURRENT_TIMESTAMP WHERE next_followup_date IS NOT NULL AND date(next_followup_date) <= date(?) AND application_status IN ('sent','draft')",
        (today,)
    )
    conn.commit()
    conn.close()


def run_daily_maintenance():
    duplicates = detect_and_mark_duplicates()
    mark_followups_due()
    return {'duplicates_marked': duplicates, 'status': 'ok'}


def default_followup_date(days=7):
    return (datetime.utcnow() + timedelta(days=days)).strftime('%Y-%m-%d')
