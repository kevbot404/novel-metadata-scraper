from pathlib import Path

from scraper.wuxiaworld_novel_links import (
    scrape_novel_links,
)

from scraper.wuxiaworld_metadata import (
    scrape_novel as scrape_wuxiaworld,
    scrape_urls as scrape_wuxiaworld_urls,
)

from scraper.royalroad_novel_links import (
    scrape_novel_links as scrape_royalroad_links,
)

from scraper.royalroad_metadata import (
    scrape_novel as scrape_royalroad,
    scrape_urls as scrape_royalroad_urls,
    CSV_COLUMNS as ROYALROAD_CSV_COLUMNS,
)

ROOT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = ROOT_DIR / "results"


def get_float(prompt, default):
    value = input(f"{prompt} [{default}]: ").strip()

    if not value:
        return default

    try:
        return float(value)
    except ValueError:
        print(f"Invalid number. Using default: {default}")
        return default


def get_int(prompt, default):
    value = input(f"{prompt} [{default}]: ").strip()

    if not value:
        return default

    try:
        return int(value)
    except ValueError:
        print(f"Invalid number. Using default: {default}")
        return default


def get_output_path(prompt, default):
    value = input(f"{prompt} [{default}]: ").strip()

    if not value:
        return Path(default)

    path = Path(value)

    if path.is_absolute():
        return path

    if len(path.parts) == 1:
        return RESULTS_DIR / path

    return ROOT_DIR / path


def get_input_path(prompt, default):
    value = input(f"{prompt} [{default}]: ").strip()

    if not value:
        return Path(default)

    path = Path(value)

    if path.is_absolute():
        return path

    return ROOT_DIR / path


def print_result(result):
    fields = [
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

    print("\n" + "=" * 80)
    print("SCRAPING RESULT")
    print("=" * 80)

    for field in fields:
        print(f"{field}: {result.get(field, 'N/A')}")

    print("=" * 80)


def print_royalroad_result(result):
    print("\n" + "=" * 80)
    print("SCRAPING RESULT")
    print("=" * 80)

    for field in ROYALROAD_CSV_COLUMNS:
        print(f"{field}: {result.get(field, 'N/A')}")

    print("=" * 80)


def wuxiaworld_menu():
    print("\nWuxiaWorld Scraper")
    print("-" * 30)

    print("\n1) Scrape novel links")
    print("2) Scrape single novel")
    print("3) Scrape novels from URL file")

    choice = input("\nEnter your choice: ").strip()

    if choice == "1":

        total_pages = get_int("Total pages (max 526)", 1)

        output_file = get_output_path(
            "Output file",
            RESULTS_DIR / "wuxiaworld_novel_urls.txt"
        )

        delay = get_float("Delay between requests in seconds", 1)

        timeout = get_int("Request timeout in seconds", 30)

        print("\nConfiguration")
        print("-" * 30)
        print(f"Total pages: {total_pages}")
        print(f"Output file: {output_file}")
        print(f"Delay:       {delay}s")
        print(f"Timeout:     {timeout}s")

        confirm = input("\nStart scraping? [Y/n]: ").strip().lower()

        if confirm not in ("", "y", "yes"):
            print("Cancelled.")
            return

        print(
            "\nStarting WuxiaWorld novel link scraper..."
        )

        try:
            scrape_novel_links(
                total_pages=total_pages,
                output_file=output_file,
                delay=delay,
                timeout=timeout,
            )

            print("\nScraping completed.")

        except Exception as e:
            print(f"\nScraping failed: {e}")

    elif choice == "2":

        url = input("\nEnter WuxiaWorld novel link: ").strip()

        if not url:
            print("No URL provided.")
            return

        timeout = get_int("Request timeout in seconds", 30)

        print(
            "\nStarting WuxiaWorld scraper..."
        )

        try:
            result = scrape_wuxiaworld(url, timeout=timeout)

            print("\nScraping completed.")
            print_result(result)

        except Exception as e:
            print(f"\nScraping failed: {e}")

    elif choice == "3":

        print("\nMetadata Scraper Configuration")
        print("-" * 35)

        urls_file = get_input_path(
            "URLs file",
            ROOT_DIR / "wuxiaworld_urls_example.txt"
        )

        output_file = get_output_path(
            "Output CSV file",
            RESULTS_DIR / "wuxiaworld_novel_metadata.csv"
        )

        delay = get_float("Delay between requests in seconds", 1)

        timeout = get_int("Request timeout in seconds", 30)

        print("\nConfiguration")
        print("-" * 30)
        print(f"URLs file:   {urls_file}")
        print(f"Output file: {output_file}")
        print(f"Delay:       {delay}s")
        print(f"Timeout:     {timeout}s")

        confirm = input("\nStart scraping? [Y/n]: ").strip().lower()

        if confirm not in ("", "y", "yes"):
            print("Cancelled.")
            return

        print("\nStarting WuxiaWorld metadata scraper...")

        try:
            scrape_wuxiaworld_urls(
                urls_file=urls_file,
                output_file=output_file,
                delay=delay,
                timeout=timeout,
            )

            print("\nScraping completed.")

        except Exception as e:
            print(f"\nScraping failed: {e}")

def royalroad_menu():
    print("\nRoyal Road Scraper")
    print("-" * 30)

    print("\n1) Scrape novel links")
    print("2) Scrape single novel")
    print("3) Scrape novels from URL file")

    choice = input("\nEnter your choice: ").strip()

    if choice == "1":

        total_pages = get_int("Total pages (max 7375)", 1,)

        output_file = get_output_path(
            "Output file",
            RESULTS_DIR / "royalroad_novel_urls.txt",
        )

        delay = get_float("Delay between requests in seconds", 1,)

        timeout = get_int("Request timeout in seconds", 30,)

        print("\nConfiguration")
        print("-" * 30)
        print(f"Total pages: {total_pages}")
        print(f"Output file: {output_file}")
        print(f"Delay:       {delay}s")
        print(f"Timeout:     {timeout}s")

        confirm = input("\nStart scraping? [Y/n]: ").strip().lower()

        if confirm not in ("", "y", "yes"):
            print("Cancelled.")
            return

        print("\nStarting Royal Road listing URL scraper...")

        try:
            scrape_royalroad_links(
                total_pages=total_pages,
                output_file=output_file,
                delay=delay,
                timeout=timeout,
            )

            print("\nScraping completed.")

        except Exception as e:
            print(f"\nScraping failed: {e}")

    elif choice == "2":
        url = input("\nEnter RoyalRoad novel link: ").strip()
        
        if not url:
            print("No URL provided.")
            return
        
        timeout = get_int("Request timeout in seconds", 30)
        
        print("\nStarting RoyalRoad scraper...")
        
        try:
            result = scrape_royalroad(url, timeout=timeout)
        
            print("\nScraping completed.")
            print_royalroad_result(result)
        
        except Exception as e:
            print(f"\nScraping failed: {e}")
        
    elif choice == "3":
        
        print("\nMetadata Scraper Configuration")
        print("-" * 35)
        
        urls_file = get_input_path(
            "URLs file",
            ROOT_DIR / "royalroad_urls_example.txt"
        )
        
        output_file = get_output_path(
            "Output CSV file",
            RESULTS_DIR / "royalroad_novel_metadata.csv"
        )
        
        delay = get_float("Delay between requests in seconds", 1)
        
        timeout = get_int("Request timeout in seconds", 30)
        
        print("\nConfiguration")
        print("-" * 30)
        print(f"URLs file:   {urls_file}")
        print(f"Output file: {output_file}")
        print(f"Delay:       {delay}s")
        print(f"Timeout:     {timeout}s")
        
        confirm = input("\nStart scraping? [Y/n]: ").strip().lower()
        
        if confirm not in ("", "y", "yes"):
            print("Cancelled.")
            return
        
        print("\nStarting RoyalRoad metadata scraper...")
        
        try:
            scrape_royalroad_urls(
                urls_file=urls_file,
                output_file=output_file,
                delay=delay,
                timeout=timeout,
            )
        
            print("\nScraping completed.")
        
        except Exception as e:
            print(f"\nScraping failed: {e}")

def main():
    print("=" * 50)
    print("Choose what you want to do")
    print("=" * 50)

    print("1) Scrape WuxiaWorld Novels")
    print("2) Scrape RoyalRoad Novels")

    choice = input("\nEnter your choice: ").strip()

    if choice == "1":
        wuxiaworld_menu()

    elif choice == "2":
        royalroad_menu()
    else:
        print("Invalid choice. Please choose 1 or 2.")


if __name__ == "__main__":
    main()
