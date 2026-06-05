import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time
import random

BASE_URL = "https://careerviet.vn"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )
}

jobs = []
seen_urls = set()

# Thử tối đa 100 trang
for page in range(1, 101):

    if page == 1:
        url = "https://careerviet.vn/viec-lam/accounting-k-vi.html"
    else:
        url = f"https://careerviet.vn/viec-lam/accounting-k-trang-{page}-vi.html"

    print(f"\n========== PAGE {page} ==========")
    print(url)

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        if response.status_code != 200:
            print(f"Stop - HTTP {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        cards = soup.select("div.job-item")

        print("Jobs found:", len(cards))

        # Không còn job => hết trang
        if len(cards) == 0:
            print("Stop - no jobs found")
            break

        for card in cards:

            title_el = card.select_one("a.job_link")
            company_el = card.select_one("a.company-name")

            salary_el = card.select_one(".salary p")
            location_el = card.select_one(".location li")

            update_times = card.select(".time time")

            if not title_el:
                continue

            job_url = urljoin(
                BASE_URL,
                title_el.get("href", "")
            )

            # chống trùng
            if job_url in seen_urls:
                continue

            seen_urls.add(job_url)

            posted_date = None

            if len(update_times) >= 2:
                posted_date = update_times[1].get_text(strip=True)
            elif len(update_times) == 1:
                posted_date = update_times[0].get_text(strip=True)

            jobs.append({
                "Job_Title": title_el.get_text(strip=True),
                "Company": company_el.get_text(strip=True) if company_el else None,
                "Salary": salary_el.get_text(strip=True) if salary_el else None,
                "Location": location_el.get_text(strip=True) if location_el else None,
                "Posted_Date": posted_date,
                "Job_Url": job_url
            })

        time.sleep(random.uniform(1.0, 2.0))

    except Exception as e:
        print("ERROR:", e)
        break

# ======================
# SAVE DATA
# ======================

df = pd.DataFrame(jobs)

print("\n======================")
print("TOTAL JOBS:", len(df))
print("======================")

print(df.head())

df.to_parquet(
    "jobs.parquet",
    index=False
)

df.to_csv(
    "jobs.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved:")
print("- jobs.parquet")
print("- jobs.csv")