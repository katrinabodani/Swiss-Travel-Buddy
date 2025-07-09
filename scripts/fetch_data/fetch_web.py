# scripts/fetch_web.py

import requests
from readability import Document
import os
from urllib.parse import urlparse

# Directory for cleaned text output
OUTPUT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        os.pardir,  # scripts/
        os.pardir,  # project root
        'data',
        'cleaned'
    )
)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Standard browser headers to avoid bot blocking
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0 Safari/537.36"
    )
}


def slugify_url(url: str) -> str:
    """
    Create a unique, filesystem-safe slug from a URL by combining netloc and path.
    """
    parsed = urlparse(url)
    # domain without port
    domain = parsed.netloc.replace(':', '_')
    # clean path: remove leading/trailing slashes, replace inner slashes
    path = parsed.path.strip('/').replace('/', '_')
    slug = f"{domain}_{path}" if path else domain
    # remove any characters not alphanumeric or underscore
    safe = ''.join(c for c in slug if c.isalnum() or c == '_')
    return safe.lower()


def fetch_and_clean(url: str):
    """
    Fetches a URL, extracts main article text via Readability, 
    strips HTML, and writes plain text to a uniquely-named file.
    """
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()

    # Extract main content
    doc = Document(resp.text)
    summary_html = doc.summary()
    from bs4 import BeautifulSoup
    text = BeautifulSoup(summary_html, "html.parser").get_text(separator="\n")

    # Normalize whitespace
    clean_text = ' '.join(text.split())

    # Generate unique slug and write
    slug = slugify_url(url)
    out_path = os.path.join(OUTPUT_DIR, f"{slug}.txt")
    with open(out_path, 'w', encoding='utf-8') as wf:
        wf.write(clean_text)

    print(f"Fetched and cleaned: {url} -> {out_path}")


if __name__ == '__main__':
    urls = [
        # list your URLs here
        "https://happytowander.com/switzerland-travel-guide/",
        "https://www.lostinswitzerland.com/",
        "https://vacationsnippets.in/switzerland/",
        "https://lostinswitzerland.com/swiss-timetables/",
        "https://lostinswitzerland.com/bern-travel-guide/",
        "https://lostinswitzerland.com/zurich-travel-guide/",
        "https://lostinswitzerland.com/lucerne-travel-guide/",
        "https://lostinswitzerland.com/zermatt-travel-guide/",
        "https://lostinswitzerland.com/interlaken-travel-guide/",
        "https://lostinswitzerland.com/mobile-internet/",
        "https://lostinswitzerland.com/best-road-trips/",
        "https://lostinswitzerland.com/how-to-plan-your-perfect-road-trip/",
        "https://lostinswitzerland.com/weather-and-climate/",
        "https://lostinswitzerland.com/traffic-rules/",
        "https://lostinswitzerland.com/swiss-motorway-vignette/",
        "https://lostinswitzerland.com/apps/",
        "https://lostinswitzerland.com/renting-a-car-in-switzerland/",
        "https://lostinswitzerland.com/health-and-safety/",
        "https://lostinswitzerland.com/credit-card/",
        "https://lostinswitzerland.com/swiss-travel-money/",
        "https://lostinswitzerland.com/swiss-coupon-pass/",
        "https://lostinswitzerland.com/swiss-languages/",
        "https://lostinswitzerland.com/visa-and-entry-requirements/",
        "https://lostinswitzerland.com/things-to-know-about-switzerland/",
        "https://lostinswitzerland.com/postauto-rides/",
        "https://lostinswitzerland.com/sbb-day-passes/",
        "https://lostinswitzerland.com/spectacular-mountain-railways/"
        "https://lostinswitzerland.com/public-transport-101/",
        "https://lostinswitzerland.com/budget-accommodation/",
        "https://lostinswitzerland.com/sweet-treats/",
        "https://lostinswitzerland.com/supermarkets/",
        "https://lostinswitzerland.com/stgallen-city-guide/",
        "https://lostinswitzerland.com/scenic-train-rides-in-switzerland/",
        "https://lostinswitzerland.com/train-ticket-sbb-machine/",
        "https://lostinswitzerland.com/solothurn-city-guide/",
        "https://lostinswitzerland.com/chocolate-factories-in-switzerland/",
        "https://lostinswitzerland.com/save-money/",
        "https://lostinswitzerland.com/swiss-mountain-lakes/",
        "https://lostinswitzerland.com/hiking/",
        "https://lostinswitzerland.com/cheese-factories-in-switzerland/",
        "https://lostinswitzerland.com/jungfraujoch/",
        "https://lostinswitzerland.com/swiss-travel-pass-yes-or-no/",
        "https://lostinswitzerland.com/swiss-travel-pass-alternatives/",
        "https://lostinswitzerland.com/activate-and-use-swiss-travel-pass/"# ... etc ...
    ]
    for u in urls:
        try:
            fetch_and_clean(u)
        except Exception as e:
            print(f"Error fetching {u}: {e}")

