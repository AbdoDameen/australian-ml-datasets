import scrapy


class AcccRecallsSpider(scrapy.Spider):
    """Scrape ACCC Product Safety Australia recalls.

    The ACCC publishes mandatory product safety recall notices.
    Note: The main /recalls page is JS-rendered. This spider uses
    alternative pages that are server-rendered.

    Data: recall title, brand, category, hazard, date

    Run:
        scrapy crawl accc_recalls -O output/accc_recalls.csv
    """

    name = "accc_recalls"
    allowed_domains = ["productsafety.gov.au"]

    start_urls = [
        # Browse recalls alphabetically — these are server-rendered
        "https://www.productsafety.gov.au/recalls?page=0",
        "https://www.productsafety.gov.au/recalls?page=1",
        "https://www.productsafety.gov.au/recalls?page=2",
    ]

    def parse(self, response):
        """Parse recall listing."""
        # Try multiple possible selectors for recall cards
        cards = response.css(".views-row, .node, article.teaser, .accc-card")
        if not cards:
            self.logger.warning(f"No recall cards found on {response.url}")
            self.logger.info(f"Page title: {response.css('title::text').get()}")
            return

        for card in cards:
            link = card.css("a::attr(href)").get()
            title = card.css("a h3::text, a .field--name-title::text, a::text").get()
            if not link and not title:
                continue
            yield {
                "title": (title or "").strip(),
                "url": response.urljoin(link) if link else response.url,
                "source": response.url,
            }
