# Australian Data Scrapers

Scrapy spiders for collecting Australian datasets that don't have public APIs.

## Spiders

| Spider | Target | Data | Status |
|--------|--------|------|--------|
| `beachwatch` | NSW Beachwatch | Weekly water quality bulletins by beach (bacterial levels, swim advisories) | RSS-based, works |
| `tga_artg` | TGA ARTG | Australian Register of Therapeutic Goods — medicines, devices, biologicals | Needs TGA site access |
| `myschool` | MySchool (ACARA) | NAPLAN results, ICSEA scores, enrollment by school | Cloudflare gated — needs Playwright |

## Usage

```bash
cd scrapers
scrapy list                    # List all spiders
scrapy crawl beachwatch        # Run Beachwatch spider
scrapy crawl tga_artg          # Run TGA spider
scrapy crawl myschool          # Run MySchool spider (may need Playwright)
```

Output goes to `scrapers/output/<spider_name>.csv`.

## Requirements

```bash
pip install scrapy
# For MySchool (if hitting Cloudflare):
pip install scrapy-playwright
playwright install
```

## Adding a Spider

```bash
scrapy genspider <name> <domain>
```
