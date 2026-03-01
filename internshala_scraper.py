import socket
socket.setdefaulttimeout(20)
import requests
from bs4 import BeautifulSoup
from db import insert_job


def scrape_internshala(keyword):
    print(f"🔍 Internshala scraping: {keyword}")

    url = f"https://internshala.com/internships/keywords-{keyword}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    res = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(res.text, "html.parser")

    # Each internship is inside this anchor
    cards = soup.select("a.view_detail_button")

    print(f"📄 Internshala cards found: {len(cards)}")

    for card in cards:
        try:
            link = "https://internshala.com" + card.get("href")

            container = card.find_parent("div", class_="internship_meta")
            if not container:
                continue

            title = container.select_one("h3").get_text(strip=True)
            company = container.select_one("h4").get_text(strip=True)

            insert_job(
                title=title,
                company=company,
                link=link,
                start_date="N/A",
                source="Internshala",
                job_type="Internship",
                skills=keyword
            )

        except Exception as e:
            continue
