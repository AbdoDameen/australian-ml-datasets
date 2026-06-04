import scrapy
from urllib.parse import urljoin


class MySchoolSpider(scrapy.Spider):
    """Scrape MySchool (ACARA) for Australian school data.

    MySchool publishes NAPLAN results, ICSEA scores, enrollment numbers,
    and demographic data for every school in Australia.

    NOTE: MySchool uses Cloudflare anti-bot protection. This spider may
    not work without Scrapy-Playwright or similar JS rendering middleware.
    Test locally before relying on output.

    Run:
        scrapy crawl myschool -O output/myschool.csv
    """

    name = "myschool"
    allowed_domains = ["myschool.edu.au"]

    def start_requests(self):
        yield scrapy.Request(
            "https://www.myschool.edu.au/",
            callback=self.parse_search_page,
            meta={"handle_httpstatus_list": [301, 302, 403]},
        )

    def parse_search_page(self, response):
        """Navigate to the school search/lookup page."""
        if response.status in (301, 302, 403):
            self.logger.warning(
                f"MySchool blocking access ({response.status}). "
                f"May need Playwright middleware or a real browser."
            )
            return

        # Extract search form action URL or state selector links
        search_url = response.css(
            "form.search-form, a[href*='school']"
        ).attrib.get("action")
        if search_url:
            yield scrapy.Request(
                urljoin(response.url, search_url), callback=self.parse_search_results
            )

    def parse_search_results(self, response):
        """Parse school listing and follow pagination."""
        for school_link in response.css("a.school-link, a[href*='/school/']"):
            url = school_link.attrib.get("href")
            if url:
                yield scrapy.Request(
                    urljoin(response.url, url), callback=self.parse_school_page
                )

        # Follow pagination
        next_page = response.css("a[rel='next'], .pagination a.next").attrib.get("href")
        if next_page:
            yield scrapy.Request(
                urljoin(response.url, next_page), callback=self.parse_search_results
            )

    def parse_school_page(self, response):
        """Extract data from an individual school profile page."""
        yield {
            "school_name": self._extract(response, "h1.page-title, .school-name"),
            "suburb": self._extract(response, ".suburb, .field--name-field-suburb"),
            "state": self._extract(response, ".state, .field--name-field-state"),
            "sector": self._extract(response, ".sector, .field--name-field-sector"),
            "school_type": self._extract(response, ".school-type, .field--name-field-type"),
            "icsea_score": self._extract(response, ".icsea-score, .field--name-field-icsea"),
            "enrollment": self._extract(response, ".enrollment, .field--name-field-enrollment"),
            "naplan_reading": self._extract(response, ".naplan-reading"),
            "naplan_writing": self._extract(response, ".naplan-writing"),
            "naplan_numeracy": self._extract(response, ".naplan-numeracy"),
            "naplan_grammar": self._extract(response, ".naplan-grammar"),
            "naplan_spelling": self._extract(response, ".naplan-spelling"),
            "url": response.url,
        }

    def _extract(self, response_or_sel, css):
        el = response_or_sel.css(css)
        return el.xpath("normalize-space()").get("").strip()
