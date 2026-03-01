from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

from db import insert_job


def scrape_linkedin(keyword):
    """
    Stable LinkedIn scraper (NO login, NO profile reuse)
    Headless Chrome – prevents DevToolsActivePort crash
    """

    print(f"🔍 LinkedIn scraping: {keyword}")

    # ---------- STABLE CHROME OPTIONS ----------
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    # ---------- LINKEDIN JOB SEARCH URL ----------
    url = (
        "https://www.linkedin.com/jobs/search/"
        f"?keywords={keyword.replace(' ', '%20')}"
        "&location=India"
        "&f_TPR=r604800"   # last 7 days
    )

    driver.get(url)
    time.sleep(5)

    # ---------- SCROLL (LOAD MORE JOBS) ----------
    for _ in range(3):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        time.sleep(2)

    # ---------- JOB CARDS ----------
    cards = driver.find_elements(By.CLASS_NAME, "base-card")
    print(f"📄 LinkedIn cards found: {len(cards)}")

    for card in cards:
        try:
            title = card.find_element(
                By.CLASS_NAME, "base-search-card__title"
            ).text.strip()

            company = card.find_element(
                By.CLASS_NAME, "base-search-card__subtitle"
            ).text.strip()

            link = card.find_element(
                By.TAG_NAME, "a"
            ).get_attribute("href")

            title_l = title.lower()

            # ---------- JOB TYPE ----------
            if "intern" in title_l:
                job_type = "Internship"
            elif "part time" in title_l or "part-time" in title_l:
                job_type = "Part Time"
            else:
                job_type = "Full Time"

            # ---------- SKILLS ----------
            skill_keywords = [
                "frontend", "react", "javascript", "html", "css",
                "web", "ui", "angular", "vue",
                "python", "java"
            ]

            skills = ", ".join(
                [s for s in skill_keywords if s in title_l]
            )

            # ---------- SAVE ----------
            insert_job(
                title=title,
                company=company,
                link=link,
                start_date="N/A",
                source="LinkedIn",
                job_type=job_type,
                skills=skills
            )

        except Exception:
            continue

    driver.quit()
    print(f"✅ LinkedIn done: {keyword}")
