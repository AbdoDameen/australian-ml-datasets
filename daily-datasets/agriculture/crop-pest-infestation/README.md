# Crop Pest Infestation

**Domain:** Agriculture
**ML Task:** Image Classification (22 classes)
**Source:** DAFF (Department of Agriculture, Fisheries and Forestry)
**Images:** 25,220 labeled JPEGs — crop pests, diseases, and healthy foliage

Four crops covered: Cashew, Cassava, Maize, and Tomato.

## Classes

| Crop | Classes |
|------|---------|
| 🌰 Cashew | anthracnose, gumosis, healthy, leaf miner, red rust |
| 🌱 Cassava | bacterial blight, brown spot, green mite, healthy, mosaic |
| 🌽 Maize | fall armyworm, grasshoper, healthy, leaf beetle, leaf blight, leaf spot, streak virus |
| 🍅 Tomato | healthy, leaf blight, leaf curl, septoria leaf spot, verticulium wilt |

## Data

Raw images are on [GitHub Releases](https://github.com/AbdoDameen/australian-ml-datasets/releases/tag/raw-data-v1) (`crop_pest_raw.zip`, 1.3 GB).

## Pipeline

```bash
# Full pipeline — download, validate, generate splits
python prepare_dataset.py

# Skip download if images are already present
python prepare_dataset.py --skip-dl
```

This generates stratified splits in `data/`:
- `train.csv` — 17,654 (70%)
- `val.csv` — 3,783 (15%)
- `test.csv` — 3,783 (15%)
- `class_labels.json` — class ID mapping
- `dataset_stats.json` — full distribution

For EDA and visualization, open the preprocessing notebook:
```bash
jupyter notebook 01_crop_pest_preprocessing.ipynb
```

## Splits

Stratified by class (preserves proportions across all 22 classes).
Imbalanced — ranges from 208 (Maize healthy) to 2,743 (Tomato septoria leaf spot) images per class.
