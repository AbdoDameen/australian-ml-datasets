import scrapy
import json


class BeachwatchSpider(scrapy.Spider):
    """Scrape NSW Beachwatch water quality data.

    NSW Beachwatch publishes weekly water quality bulletins for beaches
    across NSW. Data covers bacterial levels (enterococci), pollution
    forecasts, and swim advisories.

    Note: The old RSS feeds redirected to a new Angular site at
    beachwatch.nsw.gov.au. This spider tries multiple approaches:
    - data.gov.au CKAN API for historical data
    - The live beachwatch site for current conditions

    Run:
        scrapy crawl beachwatch -O output/beachwatch.csv
    """

    name = "beachwatch"
    allowed_domains = [
        "environment.nsw.gov.au",
        "beachwatch.nsw.gov.au",
        "data.gov.au",
        "datasets.seed.nsw.gov.au",
    ]

    def start_requests(self):
        # Try the primary Beachwatch dataset on data.gov.au
        yield scrapy.Request(
            "https://data.gov.au/data/api/3/action/package_show"
            "?id=1a165ed5-3b5d-4486-aa5b-d0a493664f8d",
            callback=self.parse_dataset_metadata,
        )

    def parse_dataset_metadata(self, response):
        """Parse the data.gov.au dataset metadata to find RSS/HTML resources."""
        try:
            data = json.loads(response.text)
            resources = data["result"]["resources"]
        except (KeyError, json.JSONDecodeError):
            self.logger.warning("Could not parse dataset metadata")
            return

        for resource in resources:
            fmt = resource.get("format", "").upper()
            url = resource.get("url", "")
            name = resource.get("name", "")

            if fmt == "RSS" and url:
                yield scrapy.Request(
                    url, callback=self.parse_rss,
                    meta={"region": name, "resource_name": name},
                )

    def parse_rss(self, response):
        """Parse an RSS feed item."""
        # RSS feeds now redirect to beachwatch.nsw.gov.au
        if response.status in (301, 302, 303):
            self.logger.info(f"RSS redirected to {response.url}")
            return

        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.body)
            for item in root.iter("item"):
                yield {
                    "region": response.meta.get("region", ""),
                    "title": (item.findtext("title") or "").strip(),
                    "description": (item.findtext("description") or "").strip(),
                    "published": (item.findtext("pubDate") or "").strip(),
                    "link": (item.findtext("link") or "").strip(),
                    "source": response.url,
                }
        except Exception as e:
            self.logger.warning(f"Could not parse RSS: {e}")
