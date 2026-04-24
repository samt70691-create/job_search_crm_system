from src.db.connection import get_connection

conn = get_connection()
cur = conn.cursor()
cur.execute("INSERT INTO job_offers (source, title, company, location, job_type, score, status, date_scraped) VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))", ('demo', 'AI Engineer', 'HealthTech Demo', 'Strasbourg', 'CDI', 82, 'new'))
cur.execute("INSERT INTO masters_programs (source, program_name, institution, city, status, score, date_scraped) VALUES (?, ?, ?, ?, ?, ?, datetime('now'))", ('demo', 'Master IA Santé', 'Université Demo', 'Strasbourg', 'new', 78))
conn.commit()
conn.close()
print('Données démo injectées.')
