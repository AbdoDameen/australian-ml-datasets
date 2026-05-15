# Australian ML Datasets

**60 datasets** across **45 domains**, all in one place. Each has a `raw/` folder with source data, ready for processing.

📁 **`daily-datasets/`** — browse them all here.

Full catalog: `daily-datasets/_catalog/20_datasets_catalog.md`

---

## Quick start

```bash
# Pick any dataset
cd daily-datasets/medicine/heart-disease/

# Process it (once I write the pipeline)
python3 prepare_dataset.py
```

---

## What's inside

Each dataset folder follows the same layout:

```
[domain]/[dataset-name]/
├── raw/           # Source data (downloaded)
├── processed/     # Cleaned data (after pipeline)
├── features/      # ML-ready features (after pipeline)
└── prepare_dataset.py  # Pipeline script (when processed)
```

We currently have **raw data downloaded for 20 datasets**, with the remaining 40 ready to download on request.
