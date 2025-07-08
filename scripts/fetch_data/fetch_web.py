# fetch_data/fetch_web.py
# Download raw HTML of blog posts (URLs defined in this file) into data/raw/

import os
import requests
from urllib.parse import urlparse

# List of blog URLs to fetch
URLS = [
    "https://www.unchartedbackpacker.com/hunza-valley-pakistan-last-paradise/"  # replace with your target URL(s)
    # "https://yourblog.com/another-post",
]

OUTPUT_DIR = "data/raw"


def fetch_blog(url: str, output_dir: str = OUTPUT_DIR) -> str:
    """
    Fetches the HTML content of a given blog URL and saves it to output_dir.
    Returns the path of the saved file.
    """
    os.makedirs(output_dir, exist_ok=True)

    response = requests.get(url)
    response.raise_for_status()

    parsed = urlparse(url)
    safe_name = (parsed.netloc + parsed.path).replace('/', '_').strip('_') + '.html'
    filepath = os.path.join(output_dir, safe_name)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(response.text)

    print(f"Fetched and saved: {url}\n  -> {filepath}")
    return filepath


def main():
    for url in URLS:
        try:
            fetch_blog(url)
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")


if __name__ == '__main__':
    main()
