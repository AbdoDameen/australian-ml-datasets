# Dataset #60: Chest X-Ray (Pneumonia)

**Domain:** Radiology  
**ML Task:** Image Classification  
**Source:** [Kaggle - Chest X-Ray Pneumonia](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)  
**Samples:** 5,856 chest X-ray images (1,583 NORMAL / 4,273 PNEUMONIA)  
**Splits:** 5,216 train / 16 val / 624 test

## Contents

| Folder | Description |
|--------|-------------|
| `raw/` | Original JPEG images sorted by split/label |
| `processed/` | Metadata CSV with file paths and encoded labels |
| `features/` | Train/val/test split CSVs + label encoder |
| `prepare_dataset.py` | Pipeline script |

## Usage

```python
import pandas as pd
df = pd.read_csv("processed/chest_xray_pneumonia_clean.csv")
print(f"{len(df)} images: {df['label'].value_counts().to_dict()}")
```

## Notes

- Images are 224×224 JPEGs. Use with CNN or vision transformer models.
- The dataset is heavily class-imbalanced (73% pneumonia). Account for this in training.
- `prepare_dataset.py` scans the directory structure and creates train/val/test metadata CSVs.
