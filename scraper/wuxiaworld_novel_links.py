import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://wuxiaworld.site/novels-list/page/{}/?m_orderby=alphabet"
TOTAL_PAGES = 1  # max=526, last checked 08/24/2026; last novel uploaded to site 03/07/2025
DELAY = 1

ROOT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT_DIR / "results"
OUTPUT_FILE = RESULTS_DIR / "wuxiaworld_novel_urls.txt"

session = requests.Session()
session.headers["User-Agent"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/128.0 Safari/537.36"
)


def scrape_page(page):
    url = BASE_URL.format(page)

    response = session.get(url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    container = soup.select_one(".c-page__content")

    if not container:
        print(".c-page__content not found")
        return {}

    novels = {}

    for link in container.select(".page-listing-item .post-title h3 a[href]"):
        url = urljoin(url, link["href"]).split("#")[0]

        if "/novel/" not in url:
            continue

        url = url.rstrip("/") + "/"
        title = link.get_text(" ", strip=True)

        novels[url] = title

    return novels


def save_novels(novels):
    RESULTS_DIR.mkdir(exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        f.write("\n".join(novels))


def main():
    novels = {}

    for page in range(1, TOTAL_PAGES + 1):
        print(f"[{page}/{TOTAL_PAGES}] Scraping page {page}...")

        try:
            page_novels = scrape_page(page)
            novels.update(page_novels)

            print(f"Found {len(page_novels)} novels")

        except requests.RequestException as e:
            print(f"ERROR: {e}")

        time.sleep(DELAY)

    print(f"\nTotal unique novels: {len(novels)}")

    save_novels(novels)

    print(f"Novel links saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()