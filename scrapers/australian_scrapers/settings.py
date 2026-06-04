# Scrapy settings for australian_scrapers project
BOT_NAME = "australian_scrapers"

SPIDER_MODULES = ["australian_scrapers.spiders"]
NEWSPIDER_MODULE = "australian_scrapers.spiders"

ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 1.0
RANDOMIZE_DOWNLOAD_DELAY = True

USER_AGENT = "australian-ml-datasets (+https://github.com/AbdoDameen/australian-ml-datasets)"

ITEM_PIPELINES = {}
