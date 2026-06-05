import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time
import random

BASE_URL = "https://careerviet.vn"
START_URL = "https://careerviet.vn/viec-lam/accounting-k-vi.html"

headers = {
    "User-Agent": "Mozilla/5.0"
}

jobs = []
seen = set()

def get_html(url):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return r.text
    except:
        return None
    return None


url = START_URL
page = 0

while url:
    page += 1
    print(f"Scraping page {page}: {url}")

    html = get_html(url)
    if not html:
        break

    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("div.job-item")

    if len(cards) == 0:
        break

    for card in cards:
        title_el = card.select_one("a.job_link")
        company_el = card.select_one("a.company-name")
        salary_el = card.select_one("div.salary p")
        location_el = card.select_one("div.location li")
        times = card.select("div.time time")

        if not title_el:
            continue

        job_url = urljoin(BASE_URL, title_el["href"])

        if job_url in seen:
            continue
        seen.add(job_url)

        jobs.append({
            "job_title": title_el.text.strip(),
            "company": company_el.text.strip() if company_el else None,
            "salary": salary_el.text.strip() if salary_el else None,
            "location": location_el.text.strip() if location_el else None,
            "posted_date": times[1].text.strip() if len(times) >= 2 else None,
            "job_url": job_url
        })

    # pagination (next button)
    next_btn = soup.select_one("a.next")

    if next_btn and next_btn.get("href"):
        url = urljoin(BASE_URL, next_btn["href"])
    else:
        break

    time.sleep(random.uniform(1.2, 2.5))

df = pd.DataFrame(jobs)
df.to_parquet("jobs.parquet", index=False)

print("TOTAL JOBS:", len(df))