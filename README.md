# The Polite Scraper

## Target Classification
- **Site:** https://books.toscrape.com
- **Why:** Books to Scrape is an official practice sandbox built explicitly for learning web scraping.
- **Scope:** First 3 catalogue pages only (60 books total).
- **Data collected:** Title, price, availability, rating, description, product URL.
- **robots.txt result:** No robots.txt file found at https://books.toscrape.com/robots.txt — returned 404 Not Found (checked Aug 24, 2026).

I will not reuse this code on another site without checking its rules and terms first.

## How to Run
```powershell
pip install -r requirements.txt
python src/main.py
```

## Lane
Python 3.14 — requests, BeautifulSoup4, Pydantic

## Record Schema
- title: string
- product_url: string (https://)
- price_text: string (raw, e.g. "£51.77")
- price_gbp: number (normalized, e.g. 51.77)
- availability_text: string
- rating_text: string or null
- description: string or null
- source_page: string (https://)
- fetched_at: ISO 8601 timestamp

## Politeness Rules
- Identifying User-Agent: `FlyRankInternshipA9/1.0 (+https://github.com/mohamedaahmed6541/polite-scraper)`
- 10-second timeout on every request
- 0.5 second delay between real (non-cached) requests
- Status code checked before parsing; only 200 is treated as success
- All pages cached locally after first fetch — development reads from cache, not the live site

## Run Report Example
```json
{"start_time": "2026-08-24T22:04:01.602392+00:00", "duration_seconds": 31.89, "pages_fetched": 60, "valid_records": 60, "invalid_records": 0, "failed_pages": 0}
```

## Why No Browser Was Needed
The book data (title, price, availability, description) is present directly in the server-rendered HTML — there's no client-side JavaScript rendering required to see it, so a headless browser like Playwright would only add cost and complexity with no benefit here.

## Ethics Note
This scraper only targets Books to Scrape, a site built specifically for scraping practice. In general: use an official API when one exists, never bypass logins, paywalls, or explicit blocks, and only collect the data actually needed for the task.

## Known Limitation
The CSS selectors assume the current page structure of Books to Scrape. If the site's HTML layout changes, the extraction logic in `extract_book_safe()` would need to be updated.