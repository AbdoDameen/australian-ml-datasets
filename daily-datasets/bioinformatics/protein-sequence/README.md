# Protein Sequence (Bioinfo)

Protein classification from sequence-derived physicochemical features. 60K proteins across 5 structural/functional classes.

**Domain:** Bioinformatics  
**ML Task:** Multi-class classification (5 balanced classes)  
**Source:** UCI — protein sequence dataset (enriched protein dataset)  
**Size:** 60,000 rows × 11 features (7 original + 4 engineered)

## Target

**protein_class** — 5 balanced classes (~20% each):
- Enzyme, Receptor, Structural, Transport, Outras (Other)

## Features

- **molecular_mass** — protein molecular weight
- **isoelectric_point** — pI (pH at which protein carries no net charge)
- **hydrophobicity** — average hydrophobicity score
- **total_charge** — net charge at neutral pH
- **polar_ratio** — proportion of polar amino acids
- **apolar_ratio** — proportion of apolar amino acids
- **sequence_length** — number of amino acid residues
- **charge_density** — charge per residue (engineered)
- **hydrophobicity_polar_interaction** — hydrophobicity × polar ratio (engineered)
- **polar_apolar_ratio** — polar/apolar proportion (engineered)
- **mass_per_residue** — mass per residue count (engineered)

## Files

| Folder | Contents |
|--------|----------|
| `raw/` | `proteinas_20000_enriquecido.csv` |
| `processed/` | `protein_sequence_bioinfo_clean.csv` |
| `features/` | X_train_scaled, X_test_scaled, y_train, y_test, scaler.pkl, label_encoder.pkl |

## Usage

```bash
cd daily-datasets/bioinformatics/protein-sequence
python3 prepare_dataset.py
```
