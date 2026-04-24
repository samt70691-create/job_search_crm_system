from pathlib import Path
from src.db.connection import get_connection


def init_db():
    schema_path = Path(__file__).resolve().parent / 'schema.sql'
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = f.read()
    conn = get_connection()
    conn.executescript(schema)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
