from src.db.connection import get_connection


def list_contacts(search=None):
    conn = get_connection()
    query = "SELECT * FROM contacts WHERE 1=1"
    params = []
    if search:
        query += ' AND (full_name LIKE ? OR company LIKE ? OR email LIKE ?)'
        like = f'%{search}%'
        params.extend([like, like, like])
    query += ' ORDER BY id DESC'
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows


def create_contact(data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        '''INSERT INTO contacts
        (job_offer_id, company, full_name, role, email, linkedin_url, phone, contact_type, source, confidence_score, notes, date_found)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))''',
        (
            data.get('job_offer_id'), data.get('company'), data.get('full_name'), data.get('role'), data.get('email'),
            data.get('linkedin_url'), data.get('phone'), data.get('contact_type'), data.get('source', 'manual'),
            data.get('confidence_score', 0.5), data.get('notes')
        )
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id
