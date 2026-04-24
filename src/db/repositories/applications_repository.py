from src.db.connection import get_connection


def list_applications(status=None):
    conn = get_connection()
    query = '''
    SELECT a.*, j.title, j.company, j.location
    FROM applications a
    JOIN job_offers j ON a.job_offer_id = j.id
    WHERE 1=1
    '''
    params = []
    if status and status != 'all':
        query += ' AND a.application_status = ?'
        params.append(status)
    query += ' ORDER BY a.id DESC'
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows


def create_application(job_offer_id, application_channel, application_status='sent', custom_message=None, notes=None, next_followup_date=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        '''INSERT INTO applications
        (job_offer_id, application_date, application_channel, application_status, custom_message, notes, next_followup_date)
        VALUES (?, datetime('now'), ?, ?, ?, ?, ?)''',
        (job_offer_id, application_channel, application_status, custom_message, notes, next_followup_date)
    )
    conn.execute("UPDATE job_offers SET status = 'applied', updated_at = CURRENT_TIMESTAMP WHERE id = ?", (job_offer_id,))
    conn.commit()
    app_id = cur.lastrowid
    conn.close()
    return app_id


def update_application_status(app_id, status):
    conn = get_connection()
    conn.execute("UPDATE applications SET application_status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (status, app_id))
    conn.commit()
    conn.close()


def set_followup(app_id, next_followup_date):
    conn = get_connection()
    conn.execute("UPDATE applications SET next_followup_date = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (next_followup_date, app_id))
    conn.commit()
    conn.close()


def delete_application(app_id):
    conn = get_connection()
    conn.execute('DELETE FROM applications WHERE id = ?', (app_id,))
    conn.commit()
    conn.close()
