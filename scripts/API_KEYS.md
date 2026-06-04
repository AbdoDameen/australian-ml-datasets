# Australian Data Sources — API Key Requirements

Some Australian government and private data sources require API keys, registration,
or special access. This list documents what I found and what you'd need to apply for.

## ✅ No Key Required — Open Access (scraper or direct download works)

| Source | What you get | How to access |
|--------|-------------|---------------|
| **[data.gov.au](https://data.gov.au/)** | 30K+ datasets across all domains | CKAN API, no key |
| **[ABS.Stat](https://stat.data.abs.gov.au/)** | Census, economy, population, labor | SDMX/JSON API, no key |
| **[BOM Climate Data Online](http://www.bom.gov.au/climate/data/)** | Weather station data, rainfall, temp | FTP + HTTP, blocks scrapers though |
| **[Geoscience Australia](https://pid.geoscience.gov.au/)** | Earthquakes, geology, satellite | OGC API, no key |
| **[Atlas of Living Australia](https://api.ala.org.au/)** | Species occurrences, biodiversity | REST API, no key |
| **[TERN](https://www.tern.org.au/)** | Soil moisture, ecosystem monitoring | Data portal, free registration |
| **[SEED NSW](https://www.seed.nsw.gov.au/)** | NSW environmental data | Web portal + API |
| **[NSW Beachwatch](https://beachwatch.nsw.gov.au/)** | Beach water quality | data.gov.au (via CKAN) |

## 🔑 API Key Required — Free Registration

| Source | Key needed for | Apply at |
|--------|---------------|----------|
| **ABS API** | Higher rate limits, structured access | https://api.data.abs.gov.au/ |
| **BOM Weather Data Services** | Geospatial/sector-specific data | http://www.bom.gov.au/regulations/ |
| **Transport for NSW Open Data** | Real-time transport, incidents, timetables | https://opendata.transport.nsw.gov.au/ |
| **NSW Spatial Services** | Cadastre, topography, imagery | https://www.nsw.gov.au/spatial-services |
| **VicRoads Open Data** | Victorian transport data | https://vicroadsopendata.vicroads.gov.au/ |

## 🔒 API Key Required — Application Process

| Source | What you get | Apply at | Notes |
|--------|-------------|----------|-------|
| **Domain API** | Property listings, prices, suburb data | https://developer.domain.com.au/ | Free tier available |
| **REA Group API** | Property listings, market trends | https://developer.realestate.com.au/ | Free tier for research |
| **Google Maps / Places API** | Geocoding, places, route optimization | https://console.cloud.google.com/ | Free tier ($200/mo credit) |
| **OpenStreetMap Overpass API** | Map data, routes, land use | Free tier with rate limits | No key for basic use |

## ❌ No API Available — Scraping Only

These sites don't offer APIs. Scrapy (or Playwright) is the only way:

| Target | Data | Difficulty |
|--------|------|------------|
| **MySchool (ACARA)** | NAPLAN, ICSEA, enrollment by school | Hard — Cloudflare gated |
| **TGA ARTG** | Therapeutic goods register | Medium — accessible but paginated |
| **Domain / REA Group** | Property details | Hard — JS rendered, anti-bot |
| **Seek / Indeed** | Job listings, salaries | Hard — anti-bot |
| **Wine Companion / Halliday** | Wine ratings, wineries | Medium — check access |

## Recommended First Steps

1. No key needed: `python scripts/download_data_gov_au.py --search beachwatch`
2. Register for: **Transport for NSW** (transport patterns), **Domain API** (housing)
3. Scrape: **TGA ARTG** (already have the spider), then **MySchool** if you need NAPLAN data
