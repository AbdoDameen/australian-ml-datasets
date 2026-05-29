# Species Distribution (GBIF)

**Domain:** Ecology
**ML Task:** Classification
**Source:** Global Biodiversity Information Facility (GBIF)
**Description:** 23 million species occurrence records from Australia. Focuses on bird species (Aves) with rich spatial and temporal metadata.

## Key Columns

| Column | Description |
|--------|-------------|
| gbifID | Unique occurrence identifier |
| kingdom / phylum / class / order / family / genus / species | Full taxonomic classification |
| decimalLatitude / decimalLongitude | GPS coordinates of observation |
| year / month / day | Date of observation |
| countryCode / stateProvince | Geographic location |
| elevation | Elevation (metres) |
| basisOfRecord | How the record was made (human observation, machine, etc.) |
| occurrenceStatus | PRESENT or ABSENT |
| individualCount | Number of individuals observed |
| eventDate | Full date string |

## Data

The full 23-million-record dataset (~13 GB) is available from [GBIF.org](https://www.gbif.org). A sampled subset is available on request.
