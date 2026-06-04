import scrapy


class RbaDataSpider(scrapy.Spider):
    """Download RBA (Reserve Bank of Australia) statistical tables.

    The RBA publishes key economic data as CSV files:
    - Cash rate target and history
    - Inflation (CPI) indicators
    - Lenders' interest rates
    - Exchange rates
    - GDP statistics
    - Labour market data

    Run:
        scrapy crawl rba_data -O output/rba_data.csv
    """

    name = "rba_data"
    allowed_domains = ["rba.gov.au"]

    # Key RBA statistical tables (CSV format)
    start_urls = [
        # Cash rate, inflation, economic indicators
        "https://www.rba.gov.au/statistics/tables/csv/fin-indicators.csv",
        # Key economic indicators (GDP, employment, CPI)
        "https://www.rba.gov.au/statistics/tables/csv/g1-data.csv",
        # Interest rates
        "https://www.rba.gov.au/statistics/tables/csv/f1-all-data.csv",
        # Exchange rates
        "https://www.rba.gov.au/statistics/tables/csv/f11-data.csv",
        # Credit aggregates
        "https://www.rba.gov.au/statistics/tables/csv/d1-data.csv",
        # Capital market yields
        "https://www.rba.gov.au/statistics/tables/csv/f2-data.csv",
    ]

    def parse(self, response):
        """Yield each row of a CSV table with series metadata."""
        if response.status == 404:
            self.logger.warning(f"Table not found: {response.url}")
            return

        table_name = response.url.split("/")[-1].replace(".csv", "")
        lines = response.text.strip().split("\n")

        for i, line in enumerate(lines):
            parts = [p.strip().strip('"') for p in line.split(",")]
            yield {
                "table": table_name,
                "row": i,
                "data": ",".join(parts),
                "source_url": response.url,
            }
