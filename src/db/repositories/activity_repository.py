from src.db.connection import get_connection


def log_activity(entity_type, entity_id, action_type, details=None):
    conn = get_connection()
    conn.execute(
        'INSERT INTO activity_log (entity_type, entity_id, action_type, details) VALUES (?, ?, ?, ?)',
        (entity_type, entity_id, action_type, details),
    )
    conn.commit()
    conn.close()
