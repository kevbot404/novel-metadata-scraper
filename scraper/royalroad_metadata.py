import csv
import random
import re
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


ROOT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT_DIR / "results"

DEFAULT_URLS_FILE = RESULTS_DIR / "royalroad_novel_urls.txt"
DEFAULT_OUTPUT_FILE = RESULTS_DIR / "royalroad_novel_metadata.csv"

DEFAULT_DELAY = 1
DEFAULT_TIMEOUT = 30

BASE_URL = "https://www.royalroad.com/"

HEADERS = {
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

CSV_COLUMNS = [
    "title",
    "url",
    "authors",
    "author_urls",
    "tags",
    "description",
    "overall_score",
    "style_score",
    "story_score",
    "grammar_score",
    "character_score",
    "total_views",
    "average_views",
    "followers",
    "favorites",
    "ratings",
    "pages",
    "word_count",
]


def build_session():
    """
    Build a requests Session with retry/backoff and a warm-up request.

    The first several requests from a fresh session sometimes get
    blocked (connection aborted, 404, etc.). Hitting the homepage first lets the
    session pick up cookies.
    """
    session = requests.Session()
    session.headers.update(HEADERS)

    retry = Retry(
        total=5,
        backoff_factor=2,  # 2s, 4s, 8s, 16s, 32s
        status_forcelist=[403, 404, 429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    # Warm up: grab cookies from the homepage before scraping anything
    try:
        session.get(BASE_URL, timeout=DEFAULT_TIMEOUT)
        time.sleep(1.5)
    except requests.RequestException:
        pass

    return session


session = build_session()


def clean_text(text):
    """Normalize whitespace into a single line."""
    return " ".join(text.split())


def get_description(soup):
    """Extract the novel description as a single line."""
    desc_element = soup.select_one(".description .hidden-content")

    if not desc_element:
        return ""

    text = desc_element.get_text(" ", strip=True)

    return clean_text(text)


def get_score(soup, label):
    """Extract a numeric star score by label and next sibling <li>."""
    for li in soup.select(".fiction-stats li"):
        text = li.get_text(" ", strip=True)
        text = re.sub(r"\s+", " ", text)

        if text.lower() == label.lower():
            next_li = li.find_next_sibling("li")

            if not next_li:
                return ""

            span = next_li.select_one("span.star[data-content]")

            if not span:
                return ""

            content = span.get("data-content", "")
            match = re.match(r"([\d.]+)\s*/\s*\d+", content)

            if match:
                score = match.group(1)
                if "." not in score:
                    score = score + ".0"
                return score

    return ""


def get_stat(soup, label):
    """Extract a general statistic value from the next sibling <li>."""
    for li in soup.select(".fiction-stats li"):
        text = li.get_text(" ", strip=True)
        text = re.sub(r"\s+", " ", text)

        pattern = rf"^{re.escape(label)}\s*:?$"
        match = re.match(pattern, text, re.IGNORECASE)

        if match:
            next_li = li.find_next_sibling("li")

            if next_li:
                return next_li.get_text(" ", strip=True)

    return ""


def get_word_count(soup):
    """Extract word count from the Pages statistic tooltip."""
    pages_li = None
    for li in soup.select(".fiction-stats li"):
        text = li.get_text(" ", strip=True)
        text = re.sub(r"\s+", " ", text)
        if text.lower().startswith("pages"):
            pages_li = li
            break

    if not pages_li:
        return ""

    i_element = pages_li.select_one("i[data-content]")

    if not i_element:
        return ""

    data_content = i_element.get("data-content", "")
    match = re.search(
        r"calculated from ([\d,]+) words",
        data_content,
        re.IGNORECASE,
    )

    if match:
        return match.group(1).replace(",", "")

    return ""


def scrape_novel(url, timeout=DEFAULT_TIMEOUT):
    response = session.get(url, timeout=timeout)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title_element = soup.select_one(".fic-title h1")

    if title_element:
        title = clean_text(title_element.get_text())
    else:
        title = ""

    authors = []
    author_urls = []

    for a in soup.select(".fic-title h4 a"):
        href = a.get("href", "")
        name = clean_text(a.get_text())

        if name:
            authors.append(name)

            if href:
                author_urls.append(urljoin(url, href))

    tags = []

    for a in soup.select("a.fiction-tag"):
        name = clean_text(a.get_text())

        if name:
            tags.append(name)

    description = get_description(soup)

    overall_score = get_score(soup, "Overall Score")
    style_score = get_score(soup, "Style Score")
    story_score = get_score(soup, "Story Score")
    grammar_score = get_score(soup, "Grammar Score")
    character_score = get_score(soup, "Character Score")

    total_views = get_stat(soup, "Total Views").replace(",", "")
    average_views = get_stat(soup, "Average Views").replace(",", "")
    followers = get_stat(soup, "Followers").replace(",", "")
    favorites = get_stat(soup, "Favorites").replace(",", "")
    ratings = get_stat(soup, "Ratings").replace(",", "")
    pages = get_stat(soup, "Pages").replace(",", "")
    word_count = get_word_count(soup)

    return {
        "title": title,
        "url": url,
        "authors": " | ".join(authors),
        "author_urls": " | ".join(author_urls),
        "tags": " | ".join(tags),
        "description": description,
        "overall_score": overall_score,
        "style_score": style_score,
        "story_score": story_score,
        "grammar_score": grammar_score,
        "character_score": character_score,
        "total_views": total_views,
        "average_views": average_views,
        "followers": followers,
        "favorites": favorites,
        "ratings": ratings,
        "pages": pages,
        "word_count": word_count,
    }


def load_checked_urls(output_file):
    """
    Read URLs already successfully saved to the CSV.

    This makes the scraper resumable.
    """
    checked = set()
    output_file = Path(output_file)

    if not output_file.exists():
        return checked

    with output_file.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as f:
        reader = csv.DictReader(f)

        for row in reader:
            url = row.get("url")

            if url:
                checked.add(url)

    return checked


def scrape_urls(
    urls_file=DEFAULT_URLS_FILE,
    output_file=DEFAULT_OUTPUT_FILE,
    delay=DEFAULT_DELAY,
    timeout=DEFAULT_TIMEOUT,
):
    """
    Scrape metadata from all URLs in a URL file.

    The scraper is resumable: URLs already present in the
    output CSV are skipped.
    """
    urls_file = Path(urls_file)
    output_file = Path(output_file)

    if not urls_file.exists():
        raise FileNotFoundError(
            f"URL file not found: {urls_file}"
        )

    if delay < 0:
        raise ValueError(
            "delay cannot be negative"
        )

    if timeout <= 0:
        raise ValueError(
            "timeout must be greater than 0"
        )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with urls_file.open(
        "r",
        encoding="utf-8",
    ) as f:
        urls = [
            line.strip()
            for line in f
            if line.strip()
        ]

    urls = list(dict.fromkeys(urls))

    checked_urls = load_checked_urls(
        output_file
    )

    remaining = [
        url
        for url in urls
        if url not in checked_urls
    ]

    print(
        f"Total URLs:     {len(urls)}"
    )

    print(
        f"Already checked: {len(checked_urls)}"
    )

    print(
        f"Remaining:      {len(remaining)}"
    )

    if not remaining:
        print("\nNothing left to scrape.")
        print(
            f"Metadata saved to: {output_file}"
        )
        return

    print()

    file_exists = output_file.exists()

    with output_file.open(
        "a",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=CSV_COLUMNS
        )

        if (
            not file_exists
            or output_file.stat().st_size == 0
        ):
            writer.writeheader()
            f.flush()

        for index, url in enumerate(
            remaining,
            start=1
        ):
            print(
                f"[{index}/{len(remaining)}] {url}"
            )

            try:
                metadata = scrape_novel(
                    url,
                    timeout=timeout
                )

                writer.writerow(metadata)

                f.flush()

                print(
                    f"Saved: {metadata['title']}"
                )

            except requests.RequestException as e:
                print(
                    f"REQUEST ERROR: {e}"
                )

            except Exception as e:
                print(
                    f"ERROR: {e}"
                )

            # Don't wait after the final URL.
            if index < len(remaining):
                time.sleep(delay + random.uniform(0, 0.5))

    print()
    print("Finished.")
    print(
        f"Metadata saved to: {output_file}"
    )


if __name__ == "__main__":
    scrape_urls()