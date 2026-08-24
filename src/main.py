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


if __name__ == "__main__":
    fetch(BASE_URL, "catalogue-page-1.html")