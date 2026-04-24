from src.db.connection import get_connection


def list_masters(status=None, search=None):
    conn = get_connection()
    query = 'SELECT * FROM masters_programs WHERE 1=1'
    params = []
    if status and status != 'all':
        query += ' AND status = ?'
        params.append(status)
    if search:
        query += ' AND (program_name LIKE ? OR institution LIKE ? OR city LIKE ?)'
        like = f'%{search}%'
        params.extend([like, like, like])
    query += ' ORDER BY score DESC, id DESC'
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows


def create_master(data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        '''INSERT INTO masters_programs
        (source, url, program_name, institution, city, country, program_type, domain, deadline, start_date, description, status, score, notes, date_scraped)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))''',
        (
            data.get('source', 'manual'), data.get('url'), data.get('program_name'), data.get('institution'), data.get('city'),
            data.get('country', 'France'), data.get('program_type'), data.get('domain'), data.get('deadline'), data.get('start_date'),
            data.get('description'), data.get('status', 'new'), data.get('score', 0), data.get('notes')
        )
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id
