# novel-metadata-collector

A CLI tool for scraping metadata from Light, Wuxia and Web Novel hosting sites. Supports batch scraping with resumable execution and structured CSV output.

## Features

- Scrapes novel metadata from supported novel hosting sites
- Resumable metadata scraping (skips URLs already saved to CSV)
- Saves structured metadata to CSV
- Configurable request delay and timeouts
- Batch novel link collection from listing pages

## Installation

```bash
pip install -r requirements.txt
```

## Project Structure

```
novel-metadata-collector/
├── main.py                           # CLI entry point
├── requirements.txt                  # Dependencies
├── wuxiaworld_urls_example.txt       # WuxiaWorld URLs file example
├── royalroad_urls_example.txt        # RoyalRoad URLs file example
├── scraper/
│   ├── wuxiaworld_novel_links.py     # WuxiaWorld listing page scraper
│   └── wuxiaworld_metadata.py        # WuxiaWorld novel page scraper
│   ├── royalroad_novel_links.py      # RoyalRoad listing page scraper
│   └── royalroad_metadata.py         # RoyalRoad novel page scraper
└── results/                          # Default output folder
```

## Dependencies

- `requests` — HTTP client with session reuse and configurable timeouts
- `beautifulsoup4` — HTML parsing for novel metadata extraction

## Usage

Run the interactive CLI menu:

```bash
python main.py
```

### Menu Options

**1) Scrape WuxiaWorld Novels**

Opens a submenu with three modes:

1. **Scrape novel links** — crawl WuxiaWorld's novel listing pages and collect novel URLs into a text file.
   - Prompts for: total pages, output file path, delay between requests, request timeout

2. **Scrape single novel** — fetch and display metadata for one novel in the terminal.
   - Prompts for: novel URL, request timeout

3. **Scrape novels from URL file** — batch scrape metadata from a list of URLs with resumable execution.
   - Prompts for: URLs file path, output CSV path, delay between requests, request timeout

**2) Scrape RoyalRoad Novels**

1. **Scrape novel links** — crawl RoyalRoad's novel listing pages and collect novel URLs into a text file.
   - Prompts for: total pages, output file path, delay between requests, request timeout

2. **Scrape single novel** — fetch and display metadata for one novel in the terminal.
   - Prompts for: novel URL, request timeout

3. **Scrape novels from URL file** — batch scrape metadata from a list of URLs with resumable execution.
   - Prompts for: URLs file path, output CSV path, delay between requests, request timeout

Already-scraped URLs (present in the output CSV) are automatically skipped, so interrupted runs can be resumed without re-scraping completed novels. (Not applicable to listing page link collecting)

## Supported Websites

| Website                                 | Status    |
| --------------------------------------- | --------- |
| [WuxiaWorld](https://wuxiaworld.site/)  | Supported |
| [RoyalRoad](https://www.royalroad.com/) | Supported |

## Output Fields

The CSV includes the following fields:

WuxiaWorld:

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

RoyalRoad:

Multi-value fields (e.g. `authors`, `genres`, `release_year`) are joined with `|`.
