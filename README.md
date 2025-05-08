# Website Crawler Tool

A configurable web crawler that extracts page content and link structure while respecting crawling etiquette.

## Features

- **Respectful Crawling**: Configurable delay between requests
- **Content Filtering**: Skips static files and duplicate content
- **Structured Output**: Generates CSV with URLs, text content, and links
- **Duplicate Detection**: MD5 hash-based content deduplication
- **Domain Focus**: Separates internal/external links

## Requirements

`requirements.txt`:
```text
requests
beautifulsoup4
pandas
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python web_crawler.py --url https://example.com [--delay 1.0] [--max-pages 100] [--output results.csv]
```

**Arguments**:
- `--url`: Starting URL (required)
- `--delay`: Seconds between requests (default: 1.0)
- `--max-pages`: Maximum pages to crawl (optional)
- `--output`: Output CSV path (default: output.csv)

**Example**:
```bash
python web_crawler.py --url https://news.example.com --delay 2.0 --max-pages 50 --output news_site.csv
```

## Output CSV Structure
| Column           | Description                                  |
|-------------------|----------------------------------------------|
| URL              | Page URL                                    |
| Page Text        | Cleaned text content                        |
| Internal Links   | Semicolon-separated list of same-domain links |
| External Links   | Semicolon-separated list of external links   |

## Important Notes

1. **Legal Compliance**:
   - Check robots.txt before crawling
   - Obtain website owner permission
   - Respect `User-Agent` policies

2. **Performance**:
   - Increase delay for fragile websites
   - Use `--max-pages` for large sites

3. **Limitations**:
   - No JavaScript rendering
   - Basic duplicate detection (MD5 hash)
   - Single-domain focus

## Disclaimer
Use this tool responsibly and ethically. The developers are not responsible for misuse or unauthorized crawling activities.
