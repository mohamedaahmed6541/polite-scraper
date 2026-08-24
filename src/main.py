import os
import requests

USER_AGENT = "FlyRankInternshipA9/1.0 (https://github.com/mohamedaahmed6541/polite-scraper)"
TIMEOUT = 10
CACHE_DIR = "cache"
BASE_URL = "https://books.toscrape.com/catalogue/page-1.html"


def fetch(url, cache_filename):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, cache_filename)

    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            html = f.read()
        print(f"CACHE HIT {url} ({len(html)} bytes)")
        return html

    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, timeout=TIMEOUT)

    if response.status_code != 200:
        raise RuntimeError(f"Failed fetch: {url} returned {response.status_code}")

    html = response.text
    with open(cache_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"FETCH {url} ({len(html)} bytes)")
    return html


from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

CATALOGUE_BASE = "https://books.toscrape.com/catalogue/page-{}.html"


def discover_book_urls():
    all_urls = []
    page_num = 1
    catalogue_pages = 0
    MAX_PAGES = 3

    while page_num <= MAX_PAGES:
        page_url = CATALOGUE_BASE.format(page_num)
        try:
            html = fetch(page_url, f"catalogue-page-{page_num}.html")
        except RuntimeError:
            break

        catalogue_pages += 1
        soup = BeautifulSoup(html, "html.parser")

        book_links = soup.select("h3 a")
        for link in book_links:
            href = link.get("href")
            absolute = urljoin(page_url, href)
            all_urls.append(absolute)

        next_link = soup.select_one("li.next a")
        if next_link and page_num < MAX_PAGES:
            time.sleep(0.5)
            page_num += 1
        else:
            break

    unique_urls = list(dict.fromkeys(all_urls))

    print(f"catalogue_pages={catalogue_pages}")
    print(f"discovered={len(all_urls)}")
    print(f"unique_urls={len(unique_urls)}")

    return unique_urls


if __name__ == "__main__":
    urls = discover_book_urls()