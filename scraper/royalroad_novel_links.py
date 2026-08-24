import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = (
    "https://www.royalroad.com/fictions/search"
    "?globalFilters=false"
    "&keyword="
    "&author="
    "&minPages=0"
    "&maxPages=20000"
    "&minRating=0"
    "&maxRating=5"
    "&status=ALL"
    "&orderBy=title"
    "&dir=asc"
    "&type=ALL"
    "&includeNotInterested=false"
    "&excludeFollowsFavorites=false"
    "&page={}"
)

DEFAULT_TOTAL_PAGES = 1  # max 7375 as of 24/08/2026
DEFAULT_MAX_PAGES = 7375
DEFAULT_DELAY = 1
DEFAULT_TIMEOUT = 30

ROOT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT_DIR / "results"
DEFAULT_OUTPUT_FILE = RESULTS_DIR / "royalroad_novel_urls.txt"

session = requests.Session()
session.headers.update(
    {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/128.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/avif,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }
)


def scrape_page(page, timeout=DEFAULT_TIMEOUT):

    url = BASE_URL.format(page)

    response = session.get(url, timeout=timeout)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    container = soup.select_one(
        "div.fiction-list.pb-0.h-full.max-w-full"
    )

    if not container:
        container = soup.select_one("div.fiction-list")

    if not container:
        print(
            f"WARNING: Fiction list container not found on page {page}"
        )
        return {}

    novels = {}

    for link in container.select(
        'a[href*="/fiction/"]'
    ):
        href = link.get("href")

        if not href:
            continue

        fiction_url = urljoin(url, href)

        fiction_url = fiction_url.split("?", 1)[0]
        fiction_url = fiction_url.split("#", 1)[0]

        if "/fiction/" not in fiction_url:
            continue

        fiction_url = fiction_url.rstrip("/") + "/"

        title_element = link.select_one("h2")

        if title_element:
            title = title_element.get_text(" ", strip=True)
        else:
            title = link.get_text(" ", strip=True)

        if not title:
            continue

        novels[fiction_url] = title

    return novels


def save_novels(novels, output_file):
    """
    Save fiction URLs to a text file.

    Only URLs are written, one per line.
    """

    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as f:
        for url in sorted(novels):
            f.write(url + "\n")


def scrape_novel_links(
    total_pages=DEFAULT_TOTAL_PAGES,
    output_file=DEFAULT_OUTPUT_FILE,
    delay=DEFAULT_DELAY,
    timeout=DEFAULT_TIMEOUT,
):
    """
    Scrape Royal Road fiction URLs from the search listing pages.

    Parameters
    ----------
    total_pages : int
        Number of Royal Road search pages to scrape.
        Royal Road currently has up to 7375 pages for this search.

    output_file : str or Path
        File where the resulting fiction URLs will be saved.

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

    if total_pages > DEFAULT_MAX_PAGES:
        raise ValueError(
            f"total_pages cannot exceed {DEFAULT_MAX_PAGES}"
        )

    if delay < 0:
        raise ValueError("delay cannot be negative")

    novels = {}

    for page in range(1, total_pages + 1):
        print(
            f"[{page}/{total_pages}] "
            f"Scraping Royal Road page {page}..."
        )

        try:
            page_novels = scrape_page(
                page,
                timeout=timeout,
            )

            before = len(novels)

            novels.update(page_novels)

            new_novels = len(novels) - before

            print(
                f"Found {len(page_novels)} fiction links "
                f"({new_novels} new, "
                f"{len(novels)} total unique)"
            )

        except requests.RequestException as e:
            print(
                f"ERROR scraping page {page}: {e}"
            )

        except Exception as e:
            print(
                f"ERROR processing page {page}: {e}"
            )

        if page < total_pages:
            time.sleep(delay)

    print(
        f"\nTotal unique Royal Road fictions: "
        f"{len(novels)}"
    )

    save_novels(
        novels,
        output_file,
    )

    output_file = Path(output_file)

    print(
        f"Fiction links saved to: {output_file}"
    )

    return {
        "novels": novels,
        "output_file": output_file,
    }


if __name__ == "__main__":
    scrape_novel_links()