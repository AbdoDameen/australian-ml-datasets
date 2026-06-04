import scrapy


class AsxCompaniesSpider(scrapy.Spider):
    """Download the ASX listed companies directory.

    The ASX publishes a CSV of all listed companies with their ASX code,
    company name, and GICS industry sector.

    Run:
        scrapy crawl asx_companies -O output/asx_companies.csv
    """

    name = "asx_companies"
    allowed_domains = ["asx.com.au"]

    start_urls = [
        "https://www.asx.com.au/asx/research/ASXListedCompanies.csv",
    ]

    def parse(self, response):
        """Parse ASX listed companies CSV."""
        lines = response.text.strip().split("\n")
        for i, line in enumerate(lines):
            if i < 3:  # skip meta line, blank, header
                continue
            parts = [p.strip().strip('"') for p in line.split(",")]
            if len(parts) < 2:
                continue
            yield {
                "company": parts[0],
                "asx_code": parts[1],
                "gics_sector": parts[2] if len(parts) > 2 else "",
            }
