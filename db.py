import sqlite3

conn = sqlite3.connect("jobs.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    company TEXT,
    link TEXT,
    start_date TEXT,
    source TEXT,
    job_type TEXT,
    skills TEXT
)
""")

def insert_job(title, company, link, start_date, source, job_type, skills):
    cursor.execute("""
        INSERT INTO jobs
        (title, company, link, start_date, source, job_type, skills)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, company, link, start_date, source, job_type, skills))
    conn.commit()
