import sqlite3

conn = sqlite3.connect("jobs.db")
cur = conn.cursor()

cur.execute("""
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

conn.commit()
conn.close()

print("✅ jobs table created successfully")
