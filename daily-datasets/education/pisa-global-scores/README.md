# PISA Global Scores

**Domain:** Education
**ML Task:** Classification / Regression
**Source:** OECD Programme for International Student Assessment (PISA)
**Description:** PISA 2022 assessment data — 600,000+ students from 80+ countries. Tests in mathematics, reading, and scientific literacy.

## Files

| File | Description | Size |
|------|-------------|------|
| `CY08MSP_CRT_COG.FORMAT.SAS` | Cognitive data format definitions | 110 KB |
| `CY08MSP_FLT_COG.FORMAT.SAS` | Filtered cognitive format | 221 KB |
| `CY08MSP_FLT_QQQ.FORMAT.SAS` | Student questionnaire format | 345 KB |
| `CY08MSP_FLT_TIM.FORMAT.SAS` | Timing data format | 106 KB |

## Data

The full PISA 2022 SAS data files are available from the [OECD PISA website](https://www.oecd.org/pisa/). The .FORMAT.SAS files in this folder define the column schemas for:

- **STU_COG**: Student cognitive scores (plausible values for math, reading, science)
- **STU_QQQ**: Student background questionnaire (demographics, socioeconomic status, attitudes)
- **FLT**: Filtered/derived variables
- **CRT**: Rotated cognitive data
- **TCH_QQQ**: Teacher questionnaire

## Target Variables

For regression: PV1MATH, PV1READ, PV1SCIE (plausible values for math, reading, science proficiency)
For classification: binary math proficiency (above/below OECD average ~450 score)
