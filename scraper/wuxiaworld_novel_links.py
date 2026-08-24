import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://wuxiaworld.site/novels-list/page/{}/?m_orderby=alphabet"

DEFAULT_TOTAL_PAGES = 1 # max 526
DEFAULT_DELAY = 1
DEFAULT_TIMEOUT = 30

ROOT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT_DIR / "results"
DEFAULT_OUTPUT_FILE = RESULTS_DIR / "wuxiaworld_novel_urls.txt"

session = requests.Session()
session.headers["User-Agent"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/128.0 Safari/537.36"
)


def scrape_page(page, timeout=DEFAULT_TIMEOUT):
    url = BASE_URL.format(page)

    response = session.get(url, timeout=timeout)
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


def save_novels(novels, output_file):
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as f:
        f.write("\n".join(novels))


def scrape_novel_links(
    total_pages=DEFAULT_TOTAL_PAGES,
    output_file=DEFAULT_OUTPUT_FILE,
    delay=DEFAULT_DELAY,
    timeout=DEFAULT_TIMEOUT,
):
    """
    Scrape novel URLs from WuxiaWorld's novel listing pages.

    Parameters
    ----------
    total_pages : int
        Number of listing pages to scrape.

    output_file : str or Path
        Where to save the resulting novel URLs.

    delay : float
        Delay between requests in seconds.

    timeout : int
        Request timeout in seconds.

    Returns
    -------
    dict
        Dictionary containing the scraped novels and output path.
    """

    if total_pages < 1:
        raise ValueError("total_pages must be at least 1")

    if total_pages > 526:
        raise ValueError("total_pages cannot exceed 526")

    if delay < 0:
        raise ValueError("delay cannot be negative")

    novels = {}

    for page in range(1, total_pages + 1):
        print(
            f"[{page}/{total_pages}] "
            f"Scraping page {page}..."
        )

        try:
            page_novels = scrape_page(
                page,
                timeout=timeout,
            )

            novels.update(page_novels)

            print(
                f"Found {len(page_novels)} novels"
            )

        except requests.RequestException as e:
            print(
                f"ERROR scraping page {page}: {e}"
            )

        if page < total_pages:
            time.sleep(delay)

    print(
        f"\nTotal unique novels: {len(novels)}"
    )

    save_novels(
        novels,
        output_file,
    )

    output_file = Path(output_file)

    print(
        f"Novel links saved to: {output_file}"
    )

    return {
        "novels": novels,
        "output_file": output_file,
    }


if __name__ == "__main__":
    scrape_novel_links()