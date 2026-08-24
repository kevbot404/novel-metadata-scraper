import csv
import re
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


ROOT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT_DIR / "results"

DEFAULT_URLS_FILE = RESULTS_DIR / "wuxiaworld_novel_urls.txt"
DEFAULT_OUTPUT_FILE = RESULTS_DIR / "wuxiaworld_novel_metadata.csv"

DEFAULT_DELAY = 1
DEFAULT_TIMEOUT = 30

BASE_URL = "https://wuxiaworld.site/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0 Safari/537.36"
    )
}

CSV_COLUMNS = [
    "title",
    "url",
    "rating",
    "rating_count",
    "rank",
    "monthly_views",
    "authors",
    "genres",
    "type",
    "release_year",
    "status",
    "comments",
    "bookmarks",
    "first_chapter_url",
    "last_chapter_url",
    "last_chapter",
    "summary",
]

session = requests.Session()
session.headers.update(HEADERS)


def clean_text(text):
    """Normalize whitespace into a single line."""
    return " ".join(text.split())


def get_value(container, label):
    """
    Find a metadata item such as:

    <h5>Author(s)</h5>
    <div class="summary-content">...</div>
    """
    for item in container.select(".post-content_item"):
        heading = item.select_one(".summary-heading h5")

        if not heading:
            continue

        if clean_text(heading.get_text()) == label:
            content = item.select_one(".summary-content")

            if content:
                return clean_text(
                    content.get_text(" ", strip=True)
                )

    return ""


def get_links(container, label):
    """
    Get all links from a metadata item.
    Used for authors, genres, release year, etc.
    """
    for item in container.select(".post-content_item"):
        heading = item.select_one(".summary-heading h5")

        if not heading:
            continue

        if clean_text(heading.get_text()) == label:
            content = item.select_one(".summary-content")

            if content:
                return [
                    clean_text(link.get_text())
                    for link in content.select("a")
                ]

    return []


def get_rating(soup):
    """Extract the numeric average rating."""
    element = soup.select_one("#averagerate")

    if not element:
        return ""

    return clean_text(element.get_text())


def get_rating_count(soup):
    """Extract the number of ratings."""
    element = soup.select_one("#countrate")

    if not element:
        return ""

    return clean_text(element.get_text())


def get_summary(soup):
    """Extract the novel summary without the WuxiaWorld notice."""
    summary = soup.select_one(
        ".description-summary .summary__content"
    )

    if not summary:
        return ""

    for element in summary.find_all(["b", "strong"]):
        text = clean_text(
            element.get_text(" ", strip=True)
        )

        if (
            text.lower().startswith("you’re reading")
            or text.lower().startswith("you're reading")
        ):
            element.decompose()

    text = summary.get_text(" ", strip=True)

    text = re.sub(
        r"^(?:You’re|You're)\s+Reading.*?"
        r"WuxiaWorld\.Site(?:\s+|$)",
        "",
        text,
        count=1,
        flags=re.IGNORECASE,
    )

    return clean_text(text)


def get_chapter_info(soup, page_url):
    """Extract first/last chapter URLs and last chapter number."""
    first_url = ""
    last_url = ""
    last_chapter = ""

    first_link = soup.select_one("#btn-read-last")
    last_link = soup.select_one("#btn-read-first")

    if first_link and first_link.get("href"):
        first_url = urljoin(
            page_url,
            first_link["href"]
        )

    if last_link and last_link.get("href"):
        last_url = urljoin(
            page_url,
            last_link["href"]
        )

        match = re.search(
            r"/chapter-(\d+)(?:-[^/]*)?/?$",
            last_url,
            re.IGNORECASE,
        )

        if match:
            last_chapter = match.group(1)

    return first_url, last_url, last_chapter


def scrape_novel(url, timeout=DEFAULT_TIMEOUT):
    response = session.get(
        url,
        timeout=timeout
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    title_element = soup.select_one(
        ".post-title h1"
    )

    if title_element:
        title = clean_text(
            title_element.get_text()
        )
    else:
        title = ""

    summary_container = soup.select_one(
        ".summary_content_wrap"
    )

    if not summary_container:
        raise ValueError(
            "Novel metadata container not found"
        )

    rating = get_rating(soup)
    rating_count = get_rating_count(soup)

    rank_text = get_value(
        summary_container,
        "Rank"
    )

    rank = rank_text
    monthly_views = ""

    if rank_text:
        match = re.match(
            r"^(.*?),\s*it has\s+(.+?)\s+monthly views$",
            rank_text,
            re.IGNORECASE,
        )

        if match:
            rank = clean_text(
                match.group(1)
            )

            monthly_views = clean_text(
                match.group(2)
            )

    authors = " | ".join(
        get_links(
            summary_container,
            "Author(s)"
        )
    )

    genres = " | ".join(
        get_links(
            summary_container,
            "Genre(s)"
        )
    )

    novel_type = get_value(
        summary_container,
        "Type"
    )

    release_year = " | ".join(
        get_links(
            summary_container,
            "Release"
        )
    )

    status = get_value(
        summary_container,
        "Status"
    )

    comments = ""

    comments_element = soup.select_one(
        ".count-comment .action_detail span"
    )

    if comments_element:
        comments = clean_text(
            comments_element.get_text()
        )

        match = re.search(
            r"(\d[\d,]*)",
            comments
        )

        if match:
            comments = match.group(1).replace(
                ",",
                ""
            )

    bookmarks = ""

    bookmarks_element = soup.select_one(
        ".add-bookmark .action_detail span"
    )

    if bookmarks_element:
        bookmarks = clean_text(
            bookmarks_element.get_text()
        )

        match = re.search(
            r"(\d[\d,]*)",
            bookmarks
        )

        if match:
            bookmarks = match.group(1).replace(
                ",",
                ""
            )

    first_chapter_url, last_chapter_url, last_chapter = (
        get_chapter_info(
            soup,
            url
        )
    )

    summary = get_summary(soup)

    return {
        "title": title,
        "url": url,
        "rating": rating,
        "rating_count": rating_count,
        "rank": rank,
        "monthly_views": monthly_views,
        "authors": authors,
        "genres": genres,
        "type": novel_type,
        "release_year": release_year,
        "status": status,
        "comments": comments,
        "bookmarks": bookmarks,
        "first_chapter_url": first_chapter_url,
        "last_chapter_url": last_chapter_url,
        "last_chapter": last_chapter,
        "summary": summary,
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

    # Remove duplicate URLs while preserving order.
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

                # Save immediately so the scraper
                # can safely resume if interrupted.
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
                time.sleep(delay)

    print()
    print("Finished.")
    print(
        f"Metadata saved to: {output_file}"
    )


if __name__ == "__main__":
    scrape_urls()