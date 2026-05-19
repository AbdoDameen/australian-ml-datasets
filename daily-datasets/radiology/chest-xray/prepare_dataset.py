#!/usr/bin/env python3
"""
Chest X-Ray (Pneumonia) — Kaggle dataset pipeline.
Creates metadata CSV with file paths and labels, optionally resizes images.
"""
import pandas as pd
import numpy as np
import json
import os
import pickle
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

BASE = Path(__file__).parent
RAW = BASE / "raw"
PROCESSED = BASE / "processed"
FEATURES = BASE / "features"

DATASET_NAME = "chest_xray_pneumonia"
DOMAIN = "radiology"

def scan_images(base_dir):
    """Scan directory structure: split/label/image_path"""
    records = []
    if not base_dir.exists():
        print(f"WARNING: {base_dir} does not exist. Data needs to be downloaded.")
        print("Download from Kaggle: paultimothymooney/chest-xray-pneumonia")
        print(f"Extract to: {RAW}")
        return pd.DataFrame()
    
    # Structure is: raw/chest_xray/{train,val,test}/{NORMAL,PNEUMONIA}/*.jpeg
    data_dir = base_dir
    # Maybe the raw zip extracted with a subdirectory
    candidates = list(base_dir.iterdir())
    if candidates:
        for c in candidates:
            if c.is_dir() and c.name.startswith("chest"):
                data_dir = c
                break
    print(f"Using data directory: {data_dir}")
    
    for split in ["train", "val", "test"]:
        split_dir = data_dir / split
        if not split_dir.exists():
            continue
        for label_dir in sorted(split_dir.iterdir()):
            if not label_dir.is_dir():
                continue
            label = label_dir.name  # NORMAL or PNEUMONIA
            for img_file in sorted(label_dir.iterdir()):
                if img_file.suffix.lower() in ['.jpeg', '.jpg', '.png']:
                    records.append({
                        "image_path": str(img_file.relative_to(BASE)),
                        "label": label,
                        "split": split,
                        "filename": img_file.name,
                    })
    
    return pd.DataFrame(records)


def main():
    # Create dirs
    for d in [PROCESSED, FEATURES]:
        d.mkdir(parents=True, exist_ok=True)

    print("=== Scanning images ===")
    df = scan_images(RAW)
    if len(df) == 0:
        print("No images found. Creating a placeholder pipeline only.")
        print("Download the dataset and re-run this script.")
        # Still save metadata
    else:
        print(f"Found {len(df)} images")
        print(f"Labels: {df['label'].value_counts().to_dict()}")
        print(f"Splits: {df['split'].value_counts().to_dict()}")
        
        # Save cleaned metadata
        clean_path = PROCESSED / f"{DATASET_NAME}_clean.csv"
        df.to_csv(clean_path, index=False)
        print(f"Saved: {clean_path}")
        
        # Create ML-ready files (metadata with encoded labels)
        le = LabelEncoder()
        df['label_encoded'] = le.fit_transform(df['label'])
        
        # Save label encoder
        with open(FEATURES / "label_encoder.pkl", "wb") as f:
            pickle.dump(le, f)
        
        # Train/test split at image level (respect original split)
        train_df = df[df['split'] == 'train']
        val_df = df[df['split'] == 'val']
        test_df = df[df['split'] == 'test']
        
        train_df.to_csv(FEATURES / "X_train.csv", index=False)
        val_df.to_csv(FEATURES / "X_val.csv", index=False)
        test_df.to_csv(FEATURES / "X_test.csv", index=False)
        
        # Save targets
        train_df['label_encoded'].to_csv(FEATURES / "y_train.csv", index=False, header=True)
        val_df['label_encoded'].to_csv(FEATURES / "y_val.csv", index=False, header=True)
        test_df['label_encoded'].to_csv(FEATURES / "y_test.csv", index=False, header=True)
        
        print(f"Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")
    
    # Metadata
    metadata = {
        "name": "Chest X-Ray (Pneumonia)",
        "domain": DOMAIN,
        "source": "https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia",
        "description": "Chest X-ray images for pneumonia classification (NORMAL vs PNEUMONIA)",
        "samples": int(len(df)),
        "classes": ["NORMAL", "PNEUMONIA"],
        "features": int(len(df.columns)) if len(df) > 0 else 0,
        "target_column": "label",
        "ml_task": "Image Classification",
        "has_images": True,
        "train_split": int(len(df[df['split'] == 'train'])) if len(df) > 0 else 0,
        "val_split": int(len(df[df['split'] == 'val'])) if len(df) > 0 else 0,
        "test_split": int(len(df[df['split'] == 'test'])) if len(df) > 0 else 0,
    }
    
    with open(BASE / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadata saved: {len(metadata)} fields")


if __name__ == "__main__":
    main()
