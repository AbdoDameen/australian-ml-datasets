# Australian Data Scrapers

Scrapy spiders for collecting Australian dataset. Most government data is on
data.gov.au with a free CKAN API — use `../scripts/download_data_gov_au.py`
for those. These spiders target sites that don't have bulk APIs.

## Spiders

| Spider | Target | Data | Status |
|--------|--------|------|--------|
| `asx_companies` | ASX | All ASX-listed companies (code, name, GICS sector) — 1,979 rows | ✅ Works |
| `rba_data` | RBA Statistics | Cash rate, inflation, interest rates, exchange rates — 6 CSV tables | ✅ Works |
| `accc_recalls` | ACCC Product Safety | Product recall notices — title, brand, category, hazard | ⚠️ Partial — paginated site might need more URLs |
| `beachwatch` | NSW Beachwatch | Weekly water quality bulletins by beach | ⛔ Broken — RSS feeds redirected to Angular app |
| `tga_artg` | TGA ARTG | Therapeutic goods register | ⛔ Broken — blocks Scrapy UA (403) |
| `myschool` | MySchool (ACARA) | NAPLAN results, ICSEA scores | ⛔ Broken — Cloudflare gated |

## Usage

```bash
cd scrapers
scrapy list

# Working spiders:
scrapy crawl asx_companies -O output/asx_companies.csv
scrapy crawl rba_data -O output/rba_data.csv
scrapy crawl accc_recalls -O output/accc_recalls.csv

# Broken spiders (need Playwright or different approach):
# scrapy crawl tga_artg -O output/tga_artg.csv
# scrapy crawl myschool -O output/myschool.csv
# scrapy crawl beachwatch -O output/beachwatch.csv
```

Output goes to `scrapers/output/<spider_name>.csv`.

## Requirements

```bash
pip install scrapy
```

For broken spiders that need a real browser:
```bash
pip install scrapy-playwright
playwright install chromium
```
Then update the spider's `custom_settings` to enable Playwright.

## Better alternatives to broken spiders

| Broken spider | Use this instead |
|---------------|------------------|
| `tga_artg` | TGA publishes the ARTG as a downloadable spreadsheet on their site |
| `beachwatch` | Data is on data.gov.au — `python ../scripts/download_data_gov_au.py --search beachwatch` |
| `myschool` | ACARA publishes NAPLAN data as Excel files annually |
