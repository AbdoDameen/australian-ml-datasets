# Quick Reference — 20 Dataset Catalog

## How daily upload works

When you say "today's dataset" or pick a number 1-20, I will:
1. Download the dataset from the source listed
2. Run the full pipeline (clean → feature engineer → ML-ready)
3. Save to the corresponding folder
4. Create documentation
5. Commit and push to GitHub

---

## QUICK PICK

Just say: **"Dataset [1-20]"** or **"Upload dataset [name]"**

| # | Dataset | Domain | Folder |
|---|---------|--------|--------|
| 1 | Heart Disease | Medicine | `medicine/heart-disease/` |
| 2 | Gene Expression Cancer | Genomics | `genomics/gene-expression-cancer/` |
| 3 | Earth Surface Temperature | Climate | `climate/earth-surface-temperature/` |
| 4 | Wine Quality | Chemistry | `chemistry/wine-quality/` |
| 5 | Mushroom Classification | Biology | `biology/mushroom-classification/` |
| 6 | Epileptic Seizure | Neuroscience | `neuroscience/epileptic-seizure/` |
| 7 | Dengue Prediction | Infectious Diseases | `infectious-diseases/dengue-prediction/` |
| 8 | Breast Cancer Wisconsin | Cancer | `cancer/breast-cancer-wisconsin/` |
| 9 | E. coli Protein Localization | Microbiology | `microbiology/ecoli-protein-localization/` |
| 10 | Handwritten Digits | Computer Vision | `computer-vision/handwritten-digits/` |
| 11 | Adult Census Income | Sociology | `sociology/adult-census-income/` |
| 12 | Drug Reviews | Pharmacology | `pharmacology/drug-reviews/` |
| 13 | Human Activity Recognition | Biophysics | `biophysics/human-activity-recognition/` |
| 14 | Forest Cover Type | Ecology | `ecology/forest-cover-type/` |
| 15 | Protein Tertiary Structure | Biochemistry | `biochemistry/protein-tertiary-structure/` |
| 16 | Cyberbullying Detection | Psychology | `psychology/cyberbullying-detection/` |
| 17 | Diabetic Retinopathy | Ophthalmology | `ophthalmology/diabetic-retinopathy/` |
| 18 | Australian Visitor Arrivals | Tourism | `tourism/australian-visitor-arrivals/` |
| 19 | Beachwatch Water Quality | Oceanography | `oceanography/beachwatch-water-quality/` |
| 20 | DNA Gene Sequences | Genomics | `genomics/dna-gene-sequences/` |

---

## Folders Created

All 20 folders are ready at:
```
/home/abdodameen/australian-ml-datasets/datasets/_catalog/  ← full catalog
/home/abdodameen/australian-ml-datasets/datasets/[domain]/[dataset]/ ← individual datasets
```

Each folder has: `raw/`, `processed/`, `features/` subdirectories ready to be populated.
