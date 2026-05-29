# Australian Rainfall (BOM)

**Domain:** Climatology
**ML Task:** Classification (predict RainToday / RainTomorrow)
**Source:** Australian Bureau of Meteorology (BOM)
**Description:** 145,000+ daily weather observations from 49 weather stations across Australia. The classic "Rain in Australia" dataset.

## Columns

| Column | Description |
|--------|-------------|
| Date | Observation date |
| Location | Weather station name |
| MinTemp / MaxTemp | Daily min/max temperature (°C) |
| Rainfall | Rainfall amount (mm) |
| Evaporation | Class A pan evaporation (mm) |
| Sunshine | Sunshine hours |
| WindGustDir / WindGustSpeed | Strongest wind gust direction and speed |
| WindDir9am / WindDir3pm | Wind direction at 9am / 3pm |
| WindSpeed9am / WindSpeed3pm | Wind speed (km/h) |
| Humidity9am / Humidity3pm | Relative humidity (%) |
| Pressure9am / Pressure3pm | Atmospheric pressure (hPa) |
| Cloud9am / Cloud3pm | Cloud cover (oktas) |
| Temp9am / Temp3pm | Temperature at 9am / 3pm |
| RainToday | 1 if rain >= 1mm today, 0 otherwise (target) |

## Data File

`weatherAUS.csv` (14 MB) — included in this folder.
