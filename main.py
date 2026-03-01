from internshala_scraper import scrape_internshala
from linkedin_scraper import scrape_linkedin
import sqlite3

KEYWORDS = [
    "frontend",
    "react",
    "web developer",
    "software engineer"
]

def remove_duplicates():
    conn = sqlite3.connect("jobs.db")
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM jobs
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM jobs
            GROUP BY title, company, link
        )
    """)
    conn.commit()
    conn.close()

def main():
    for kw in KEYWORDS:
        # Internshala (ALWAYS WORKS)
        try:
            scrape_internshala(kw)
        except Exception as e:
            print("❌ Internshala failed:", e)

        # LinkedIn (BEST EFFORT)
        try:
            scrape_linkedin(kw)
        except Exception as e:
            print("⚠️ LinkedIn skipped:", e)

    remove_duplicates()
    print("✅ Scraping completed (Internshala + LinkedIn)")

if __name__ == "__main__":
    main()
