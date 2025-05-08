#!/usr/bin/env python3
import argparse
import time
import hashlib
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup
import pandas as pd

def crawl_website(start_url, max_pages=None, delay=1.0):
    domain = urlparse(start_url).netloc
    visited = set()
    to_visit = [start_url]
    seen_hashes = set()

    data = []

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; CSVCrawler/1.0)"
    }

    static_exts = ('.jpg', '.jpeg', '.png', '.gif', '.bmp',
                   '.svg', '.webp', '.tiff', '.ico', '.zip', '.pdf')

    while to_visit:
        url = to_visit.pop(0)
        if url in visited:
            continue

        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            print(f"[!] Failed to fetch {url}: {e}")
            continue

        visited.add(url)
        print(f"[+] Visited ({len(visited)}): {url}")

        soup = BeautifulSoup(resp.text, 'html.parser')

        # Remove scripts, styles, etc.
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form", "iframe", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=' ')
        text = ' '.join(text.split())
        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()

        if len(text) < 50 or text_hash in seen_hashes:
            # skip very short or duplicate pages
            continue
        seen_hashes.add(text_hash)

        internal_links = set()
        external_links = set()

        for a in soup.find_all('a', href=True):
            href = a['href'].strip()
            # ignore fragments
            if href.startswith('#'):
                continue

            abs_url = urljoin(url, href)
            parsed = urlparse(abs_url)

            # skip static files
            if any(parsed.path.lower().endswith(ext) for ext in static_exts):
                continue

            if parsed.netloc == domain:
                internal_links.add(abs_url)
                if abs_url not in visited and abs_url not in to_visit:
                    to_visit.append(abs_url)
            else:
                external_links.add(abs_url)

        data.append({
            "URL": url,
            "Page Text": text,
            "Internal Links": ";".join(sorted(internal_links)),
            "External Links": ";".join(sorted(external_links))
        })

        if max_pages and len(visited) >= max_pages:
            print("[*] Reached max_pages limit.")
            break

        time.sleep(delay)

    df = pd.DataFrame(data)
    return df

def main():
    parser = argparse.ArgumentParser(description="Crawl a website and output a CSV of page data.")
    parser.add_argument("--url", required=True, help="URL to start crawling from.")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests in seconds.")
    parser.add_argument("--max-pages", type=int, help="Maximum number of pages to crawl.")
    parser.add_argument("--output", default="output.csv", help="Path to save the CSV file.")
    args = parser.parse_args()

    df = crawl_website(
        start_url=args.url,
        max_pages=args.max_pages,
        delay=args.delay
    )

    df.to_csv(args.output, index=False)
    print(f"[✔] Crawl finished. Data saved to {args.output}")

if __name__ == "__main__":
    main()
