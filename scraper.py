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

SKILL_LIBRARY = [
    "excel",
    "advanced excel",
    "pivot table",
    "vlookup",
    "power query",
    "sap",
    "oracle",
    "erp",
    "sql",
    "python",
    "power bi",
    "ifrs",
    "vas",
    "acca",
    "cpa",
    "audit",
    "tax",
    "bookkeeping",
    "accounting",
    "financial reporting",
    "forecasting",
    "budgeting",
    "english",
    "communication",
    "teamwork",
    "quickbooks",
    "xero"
]


def extract_skills(text):

    text = str(text).lower()

    found = []

    for skill in SKILL_LIBRARY:

        if skill.lower() in text:
            found.append(skill)

    return ", ".join(sorted(set(found)))


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

    try:

        response = requests.get(
            job_url,
            headers=HEADERS,
            timeout=20
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # ==========================
        # BENEFITS
        # ==========================

        welfare_items = soup.select(
            "ul.welfare-list li"
        )

        benefits = [
            x.get_text(strip=True)
            for x in welfare_items
        ]

        if benefits:
            result["benefits"] = " | ".join(benefits)

        # ==========================
        # JOB INFO BOX
        # ==========================

        for li in soup.select("div.detail-box li"):

            strong = li.select_one("strong")

            if not strong:
                continue

            label = strong.get_text(
                " ",
                strip=True
            )

            value_el = li.select_one("p")

            value = (
                value_el.get_text(
                    " ",
                    strip=True
                )
                if value_el
                else None
            )

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

        # ==========================
        # DETAIL BLOCKS
        # ==========================

        for row in soup.select("div.detail-row"):

            title_el = row.select_one(".detail-title")

            if not title_el:
                continue

            title = title_el.get_text(
                " ",
                strip=True
            )

            # MÔ TẢ CÔNG VIỆC

            if "Mô tả" in title:

                result["job_description"] = row.get_text(
                    " ",
                    strip=True
                )

            # YÊU CẦU CÔNG VIỆC

            elif "Yêu Cầu" in title:

                req_text = row.get_text(
                    " ",
                    strip=True
                )

                result["requirements"] = req_text

                result["market_skill"] = extract_skills(
                    req_text
                )

            # THÔNG TIN KHÁC

            elif "Thông tin khác" in title:

                for li in row.select("li"):

                    text = li.get_text(
                        " ",
                        strip=True
                    )

                    if "Bằng cấp" in text:
                        result["degree"] = text

                    elif "Thời gian làm việc" in text:
                        result["working_time"] = text

                    elif "Lương" in text:
                        result["salary_detail"] = text

        return result

    except Exception as e:

        print(
            "Detail Error:",
            job_url,
            e
        )

        return result


# ==================================
# LIST PAGE SCRAPER
# ==================================

for page in range(1, 101):

    if page == 1:
        url = "https://careerviet.vn/viec-lam/accounting-k-vi.html"
    else:
        url = (
            f"https://careerviet.vn/"
            f"viec-lam/accounting-k-trang-{page}-vi.html"
        )

    print(f"\n========== PAGE {page} ==========")
    print(url)

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        if response.status_code != 200:

            print(
                f"Stop - HTTP {response.status_code}"
            )

            break

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        cards = soup.select(
            "div.job-item"
        )

        print(
            "Jobs found:",
            len(cards)
        )

        if len(cards) == 0:

            print(
                "Stop - no jobs found"
            )

            break

        for card in cards:

            title_el = card.select_one(
                "a.job_link"
            )

            company_el = card.select_one(
                "a.company-name"
            )

            salary_el = card.select_one(
                ".salary p"
            )

            location_el = card.select_one(
                ".location li"
            )

            update_times = card.select(
                ".time time"
            )

            if not title_el:
                continue

            job_url = urljoin(
                BASE_URL,
                title_el.get(
                    "href",
                    ""
                )
            )

            if job_url in seen_urls:
                continue

            seen_urls.add(
                job_url
            )

            posted_date = None

            if len(update_times) >= 2:

                posted_date = (
                    update_times[1]
                    .get_text(
                        strip=True
                    )
                )

            elif len(update_times) == 1:

                posted_date = (
                    update_times[0]
                    .get_text(
                        strip=True
                    )
                )

            jobs.append({

                "job_title":
                    title_el.get_text(
                        strip=True
                    ),

                "company":
                    company_el.get_text(
                        strip=True
                    ) if company_el else None,

                "salary":
                    salary_el.get_text(
                        strip=True
                    ) if salary_el else None,

                "location":
                    location_el.get_text(
                        strip=True
                    ) if location_el else None,

                "posted_date":
                    posted_date,

                "job_url":
                    job_url

            })

        time.sleep(
            random.uniform(
                1,
                2
            )
        )

    except Exception as e:

        print(
            "ERROR:",
            e
        )

        break


# ==================================
# DETAIL SCRAPER
# ==================================

print("\nFetching job details...")

for idx, job in enumerate(jobs):

    print(
        f"{idx + 1}/{len(jobs)}",
        job["job_title"]
    )

    detail = get_job_detail(
        job["job_url"]
    )

    job.update(
        detail
    )

    time.sleep(
        random.uniform(
            0.3,
            0.8
        )
    )


# ==================================
# SAVE DATA
# ==================================

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