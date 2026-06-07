import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

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

SKILL_LIBRARY = [
    "excel","advanced excel","pivot table","vlookup","power query",
    "sap","oracle","erp","sql","python","power bi","ifrs","vas",
    "acca","cpa","audit","tax","bookkeeping","accounting",
    "financial reporting","forecasting","budgeting","english",
    "communication","teamwork","quickbooks","xero"
]


def extract_skills(text):
    text = str(text).lower()
    found = [s for s in SKILL_LIBRARY if s in text]
    return ", ".join(sorted(set(found)))


def get_soup(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            return None
        return BeautifulSoup(r.text, "html.parser")
    except:
        return None


def get_job_detail(job_url):

    result = {
        "benefits": None,
        "job_description": None,
        "requirements": None,
        "market_skill": None,
        "industry": None,
        "employment_type": None,
        "experience": None,
        "job_level": None,
        "deadline": None,
        "updated_date": None,
        "degree": None,
        "working_time": None,
        "salary_detail": None
    }

    soup = get_soup(job_url)
    if not soup:
        return result

    try:
        # benefits
        benefits = [x.get_text(strip=True) for x in soup.select("ul.welfare-list li")]
        if benefits:
            result["benefits"] = " | ".join(benefits)

        # info box
        for li in soup.select("div.detail-box li"):
            strong = li.select_one("strong")
            p = li.select_one("p")
            if not strong:
                continue

            label = strong.get_text(strip=True)
            value = p.get_text(strip=True) if p else None

            if "Ngành nghề" in label:
                result["industry"] = value
            elif "Hình thức" in label:
                result["employment_type"] = value
            elif "Kinh nghiệm" in label:
                result["experience"] = value
            elif "Cấp bậc" in label:
                result["job_level"] = value
            elif "Hết hạn nộp" in label:
                result["deadline"] = value
            elif "Ngày cập nhật" in label:
                result["updated_date"] = value

        # detail blocks
        for row in soup.select("div.detail-row"):
            title = row.select_one(".detail-title")
            if not title:
                continue

            title_text = title.get_text(strip=True)

            if "Mô tả" in title_text:
                result["job_description"] = row.get_text(" ", strip=True)

            elif "Yêu Cầu" in title_text:
                req = row.get_text(" ", strip=True)
                result["requirements"] = req
                result["market_skill"] = extract_skills(req)

            elif "Thông tin khác" in title_text:
                for li in row.select("li"):
                    text = li.get_text(strip=True)
                    if "Bằng cấp" in text:
                        result["degree"] = text
                    elif "Thời gian làm việc" in text:
                        result["working_time"] = text
                    elif "Lương" in text:
                        result["salary_detail"] = text

        return result

    except:
        return result


# =========================
# LIST SCRAPER
# =========================

for page in range(1, 101):

    url = (
        "https://careerviet.vn/viec-lam/accounting-k-vi.html"
        if page == 1
        else f"https://careerviet.vn/viec-lam/accounting-k-trang-{page}-vi.html"
    )

    print(f"PAGE {page}")

    soup = get_soup(url)
    if not soup:
        break

    cards = soup.select("div.job-item")

    if not cards:
        break

    for card in cards:
        title = card.select_one("a.job_link")
        company = card.select_one("a.company-name")
        salary = card.select_one(".salary p")
        location = card.select_one(".location li")
        times = card.select(".time time")

        if not title:
            continue

        job_url = urljoin(BASE_URL, title.get("href", ""))

        if job_url in seen_urls:
            continue

        seen_urls.add(job_url)

        posted = None
        if len(times) >= 1:
            posted = times[-1].get_text(strip=True)

        jobs.append({
            "job_title": title.get_text(strip=True),
            "company": company.get_text(strip=True) if company else None,
            "salary": salary.get_text(strip=True) if salary else None,
            "location": location.get_text(strip=True) if location else None,
            "posted_date": posted,
            "job_url": job_url
        })

# =========================
# DETAIL (FAST THREADPOOL)
# =========================

print("Fetching details...")

def worker(job):
    job.update(get_job_detail(job["job_url"]))
    return job

with ThreadPoolExecutor(max_workers=10) as ex:
    futures = [ex.submit(worker, j) for j in jobs]

    for i, f in enumerate(as_completed(futures)):
        f.result()
        print(f"{i+1}/{len(jobs)} done")


# =========================
# SAVE
# =========================

df = pd.DataFrame(jobs)

df.to_parquet("jobs.parquet", index=False)
df.to_csv("jobs.csv", index=False, encoding="utf-8-sig")

print("DONE:", len(df))