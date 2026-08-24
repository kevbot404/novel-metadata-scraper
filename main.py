from pathlib import Path

from scraper.wuxiaworld_novel_links import (
    scrape_novel_links,
)

from scraper.wuxiaworld_metadata import (
    scrape_novel as scrape_wuxiaworld,
    scrape_urls as scrape_wuxiaworld_urls,
    CSV_COLUMNS as WUXIAWORLD_CSV_COLUMNS,
)

from scraper.royalroad_novel_links import (
    scrape_novel_links as scrape_royalroad_links,
)

from scraper.royalroad_metadata import (
    scrape_novel as scrape_royalroad,
    scrape_urls as scrape_royalroad_urls,
    CSV_COLUMNS as ROYALROAD_CSV_COLUMNS,
)

from helpers import (
    get_float,
    get_int,
    get_input_path,
    get_output_path,
    print_result,
    print_royalroad_result,
)

ROOT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = ROOT_DIR / "results"


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
            RESULTS_DIR / "wuxiaworld_novel_urls.txt",
            RESULTS_DIR,
            ROOT_DIR,
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
            print_result(result, WUXIAWORLD_CSV_COLUMNS)

        except Exception as e:
            print(f"\nScraping failed: {e}")

    elif choice == "3":

        print("\nMetadata Scraper Configuration")
        print("-" * 35)

        urls_file = get_input_path(
            "URLs file",
            ROOT_DIR / "wuxiaworld_urls_example.txt",
            ROOT_DIR,
        )

        output_file = get_output_path(
            "Output CSV file",
            RESULTS_DIR / "wuxiaworld_novel_metadata.csv",
            RESULTS_DIR,
            ROOT_DIR,
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
            RESULTS_DIR,
            ROOT_DIR,
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
            print_royalroad_result(result, ROYALROAD_CSV_COLUMNS)
        
        except Exception as e:
            print(f"\nScraping failed: {e}")
        
    elif choice == "3":
        
        print("\nMetadata Scraper Configuration")
        print("-" * 35)
        
        urls_file = get_input_path(
            "URLs file",
            ROOT_DIR / "royalroad_urls_example.txt",
            ROOT_DIR,
        )
        
        output_file = get_output_path(
            "Output CSV file",
            RESULTS_DIR / "royalroad_novel_metadata.csv",
            RESULTS_DIR,
            ROOT_DIR,
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
