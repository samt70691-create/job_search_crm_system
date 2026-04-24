from pathlib import Path
import pandas as pd
from src.db.connection import get_connection


def export_jobs_to_excel():
    conn = get_connection()
    df = pd.read_sql_query('SELECT * FROM job_offers', conn)
    output = Path(__file__).resolve().parents[2] / 'data' / 'exports' / 'job_offers.xlsx'
    df.to_excel(output, index=False)
    conn.close()
    return output
