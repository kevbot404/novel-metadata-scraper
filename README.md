# novel-metadata-collector

A multi-source metadata scraper for Light, Wuxia and Web Novels.

## Features

- Scrapes novel metadata from supported novel hosting sites
- Resumable scraping (skips URLs already saved to CSV)
- Saves structured metadata to CSV
- Configurable request delay and timeouts

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the full WuxiaWorld pipeline (get novel links & scrape metadata):

```bash
python scraper/wuxiaworld-full.py
```

Or run individual stages:

```bash
python scraper/wuxiaworld-novel-links.py # (change TOTAL_PAGES to 526 to scrape every novel link in site)
python scraper/wuxiaworld-metadata.py
```

Output is saved to the `results/` directory.

## Supported Websites

| Website                                 | Status    | Output                                  |
| --------------------------------------- | --------- | --------------------------------------- |
| [WuxiaWorld](https://wuxiaworld.site/)  | Supported | `results/wuxiaworld_novel_metadata.csv` |
| [RoyalRoad](https://www.royalroad.com/) | Planned   | -                                       |

## Output Fields

The CSV includes the following fields:

- `title`
- `url`
- `rating`
- `rating_count`
- `rank`
- `monthly_views`
- `authors`
- `genres`
- `type`
- `release_year`
- `status`
- `comments`
- `bookmarks`
- `first_chapter_url`
- `last_chapter_url`
- `last_chapter`
- `summary`
