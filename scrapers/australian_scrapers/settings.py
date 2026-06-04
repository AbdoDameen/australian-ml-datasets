# Scrapy settings for australian_scrapers project
BOT_NAME = "australian_scrapers"

SPIDER_MODULES = ["australian_scrapers.spiders"]
NEWSPIDER_MODULE = "australian_scrapers.spiders"

ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 2.0
RANDOMIZE_DOWNLOAD_DELAY = True

USER_AGENT = "australian-ml-datasets (+https://github.com/AbdoDameen/australian-ml-datasets)"

ITEM_PIPELINES = {
    "australian_scrapers.pipelines.CsvPipeline": 300,
}

FEED_FORMAT = "csv"
FEED_URI = "output/%(name)s_%(time)s.csv"
FEED_EXPORT_ENCODING = "utf-8"
