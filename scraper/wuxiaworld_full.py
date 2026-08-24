import subprocess
import sys
from pathlib import Path


SCRAPER_DIR = Path(__file__).resolve().parent

LINKS_SCRIPT = SCRAPER_DIR / "wuxiaworld_novel_links.py"
METADATA_SCRIPT = SCRAPER_DIR / "wuxiaworld_metadata.py"


def run_script(script):
    print()
    print("=" * 60)
    print(f"Running: {script.name}")
    print("=" * 60)
    print()

    result = subprocess.run(
        [sys.executable, str(script)]
    )

    if result.returncode != 0:
        print()
        print(f"ERROR: {script.name} failed.")
        sys.exit(result.returncode)


def main():
    run_script(LINKS_SCRIPT)
    run_script(METADATA_SCRIPT)

    print()
    print("=" * 60)
    print("All scrapers finished successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()