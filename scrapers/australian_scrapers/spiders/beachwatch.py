import scrapy
from xml.etree import ElementTree


class BeachwatchSpider(scrapy.Spider):
    """Scrape NSW Beachwatch water quality bulletins.

    NSW Beachwatch publishes weekly water quality bulletins via RSS feeds
    covering Sydney, Hunter, Illawarra, Central Coast, and other regions.
    Each bulletin lists beaches with bacterial levels and swim advisories.

    Run:
        scrapy crawl beachwatch -O output/beachwatch.csv
    """

    name = "beachwatch"
    allowed_domains = ["environment.nsw.gov.au"]

    # RSS feeds for each Beachwatch region
    start_urls = [
        "http://www.environment.nsw.gov.au/beachapp/SydneyBulletin.xml",
        "http://www.environment.nsw.gov.au/beachapp/OceanBulletin.xml",
        "http://www.environment.nsw.gov.au/beachapp/BotanyBulletin.xml",
        "http://www.environment.nsw.gov.au/beachapp/PittwaterBulletin.xml",
        "http://www.environment.nsw.gov.au/beachapp/HunterBulletin.xml",
        "http://www.environment.nsw.gov.au/beachapp/CentralcoastBulletin.xml",
        "http://www.environment.nsw.gov.au/beachapp/IllawarraBulletin.xml",
    ]

    def parse(self, response):
        """Parse an RSS bulletin feed into beach-level data points."""
        region = self._region_from_url(response.url)

        try:
            root = ElementTree.fromstring(response.body)
        except ElementTree.ParseError:
            self.logger.warning(f"Could not parse RSS from {response.url}")
            return

        # RSS feeds typically have <rss><channel><item> structure
        for item in root.iter("item"):
            title = item.findtext("title", "")
            description = item.findtext("description", "")
            pub_date = item.findtext("pubDate", "")
            link = item.findtext("link", "")

            yield {
                "region": region,
                "title": title.strip(),
                "description": description.strip(),
                "published": pub_date.strip(),
                "link": link.strip(),
                "source_url": response.url,
            }

    def _region_from_url(self, url: str) -> str:
        mapping = {
            "Sydney": "Sydney",
            "Ocean": "Ocean",
            "Botany": "Botany Bay",
            "Pittwater": "Pittwater",
            "Hunter": "Hunter",
            "Centralcoast": "Central Coast",
            "Illawarra": "Illawarra",
        }
        for key, name in mapping.items():
            if key.lower() in url.lower():
                return name
        return "Unknown"
