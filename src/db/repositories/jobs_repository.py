from src.db.connection import get_connection


def list_jobs(status=None, job_type=None, search=None, include_duplicates=False):
    conn = get_connection()
    query = "SELECT * FROM job_offers WHERE 1=1"
    params = []
    if not include_duplicates:
        query += ' AND COALESCE(is_duplicate, 0) = 0'
    if status and status != 'all':
        query += ' AND status = ?'
        params.append(status)
    if job_type and job_type != 'all':
        query += ' AND job_type = ?'
        params.append(job_type)
    if search:
        query += ' AND (title LIKE ? OR company LIKE ? OR location LIKE ?)'
        like = f'%{search}%'
        params.extend([like, like, like])
    query += ' ORDER BY score DESC, id DESC'
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows


def upsert_job(data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        '''INSERT INTO job_offers
        (source, source_job_id, url, title, company, location, country, job_type, remote_type,
         salary_min, salary_max, currency, description_raw, description_clean, date_posted,
         date_scraped, keywords_detected, score, priority_level, status, ai_summary, ai_fit_reason, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(url) DO UPDATE SET
            title=excluded.title,
            company=excluded.company,
            location=excluded.location,
            job_type=excluded.job_type,
            description_raw=excluded.description_raw,
            description_clean=excluded.description_clean,
            date_posted=excluded.date_posted,
            date_scraped=datetime('now'),
            keywords_detected=excluded.keywords_detected,
            score=excluded.score,
            priority_level=excluded.priority_level,
            ai_summary=excluded.ai_summary,
            ai_fit_reason=excluded.ai_fit_reason,
            notes=excluded.notes,
            updated_at=CURRENT_TIMESTAMP''',
        (
            data.get('source', 'manual'), data.get('source_job_id'), data.get('url'), data.get('title'), data.get('company'),
            data.get('location'), data.get('country', 'France'), data.get('job_type'), data.get('remote_type'),
            data.get('salary_min'), data.get('salary_max'), data.get('currency', 'EUR'), data.get('description_raw'),
            data.get('description_clean'), data.get('date_posted'), data.get('keywords_detected'), data.get('score', 0),
            data.get('priority_level', 'medium'), data.get('status', 'new'), data.get('ai_summary'), data.get('ai_fit_reason'), data.get('notes')
        )
    )
    conn.commit()
    job_id = cur.lastrowid
    if not job_id and data.get('url'):
        row = conn.execute('SELECT id FROM job_offers WHERE url = ?', (data['url'],)).fetchone()
        job_id = row['id'] if row else None
    conn.close()
    return job_id


def create_job(data):
    return upsert_job(data)


def update_job_status(job_id, status):
    conn = get_connection()
    conn.execute("UPDATE job_offers SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (status, job_id))
    conn.commit()
    conn.close()


def update_job(job_id, data):
    conn = get_connection()
    conn.execute(
        '''UPDATE job_offers SET title=?, company=?, location=?, job_type=?, url=?, score=?, priority_level=?, status=?, notes=?, updated_at=CURRENT_TIMESTAMP WHERE id=?''',
        (data.get('title'), data.get('company'), data.get('location'), data.get('job_type'), data.get('url'), data.get('score'), data.get('priority_level'), data.get('status'), data.get('notes'), job_id)
    )
    conn.commit()
    conn.close()


def delete_job(job_id):
    conn = get_connection()
    conn.execute('DELETE FROM job_offers WHERE id = ?', (job_id,))
    conn.commit()
    conn.close()


def get_job(job_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM job_offers WHERE id = ?", (job_id,)).fetchone()
    conn.close()
    return row


def mark_duplicate(job_id, duplicate_of):
    conn = get_connection()
    conn.execute('UPDATE job_offers SET is_duplicate = 1, duplicate_of = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?', (duplicate_of, job_id))
    conn.commit()
    conn.close()
