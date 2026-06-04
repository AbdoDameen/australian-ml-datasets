import scrapy
from urllib.parse import urljoin


class TgaArtgSpider(scrapy.Spider):
    """Scrape the TGA Australian Register of Therapeutic Goods (ARTG).

    The ARTG lists every therapeutic good legally supplied in Australia:
    prescription medicines, OTC drugs, medical devices, biologicals, etc.

    Data includes: product name, ARTG ID, sponsor, active ingredients,
    product category, and dates.

    Run:
        scrapy crawl tga_artg -O output/tga_artg.csv
    """

    name = "tga_artg"
    allowed_domains = ["tga.gov.au"]

    start_urls = [
        "https://www.tga.gov.au/resources/artg?search=&f%5B0%5D=type%3Aartg",
    ]

    def parse(self, response):
        """Parse ARTG listing page and follow pagination."""
        # Extract each ARTG entry card
        for entry in response.css(".article-card, .teaser, .views-row, tr.artg-row"):
            yield self._parse_entry(entry, response)

        # Follow pagination
        next_page = response.css(
            "a[rel='next'], a.pagination__next, .pager__item--next a"
        ).attrib.get("href")
        if next_page:
            yield scrapy.Request(urljoin(response.url, next_page), callback=self.parse)

    def _parse_entry(self, entry, response):
        """Extract fields from a single ARTG entry."""
        return {
            "product_name": self._extract(entry, "h2 a, .title a, .field--name-title"),
            "artg_id": self._extract(entry, ".artg-id, .field--name-field-artg-id"),
            "sponsor": self._extract(entry, ".sponsor, .field--name-field-sponsor"),
            "category": self._extract(entry, ".category, .field--name-field-product-category"),
            "status": self._extract(entry, ".status, .field--name-field-status"),
            "url": self._extract(entry, "h2 a", "href") or self._extract(entry, ".title a", "href"),
            "scraped_url": response.url,
        }

    def _extract(self, selector, css, attr=None):
        el = selector.css(css)
        if attr:
            return el.attrib.get(attr, "").strip()
        return el.xpath("normalize-space()").get("").strip()
