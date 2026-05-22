# Protein Sequence (Bioinfo) — Data Preparation Process

## Source

Protein sequence dataset from UCI. Column names originally in Portuguese (ID_Proteína, Sequência, Massa_Molecular, Ponto_Isoelétrico, Hidrofobicidade, Carga_Total, Proporção_Polar, Proporção_Apolar, Comprimento_Sequência, Classe).

60,000 rows (despite filename saying "20000"). Zero duplicates, zero missing values.

## Cleaning

- Renamed Portuguese columns to English
- No duplicates to remove
- No missing values to fill
- Outlier capping (3× IQR) on 4 columns: hydrophobicity (30 values), total_charge (2), polar_ratio (28), apolar_ratio (24)

## Feature Engineering

4 derived features:

1. **charge_density** — total_charge / sequence_length (charge per residue)
2. **hydrophobicity_polar_interaction** — hydrophobicity × polar_ratio
3. **polar_apolar_ratio** — polar_ratio / apolar_ratio (+0.001 to avoid div by zero)
4. **mass_per_residue** — molecular_mass / sequence_length

## ML Preparation

- **Features (11):** 7 original physicochemical + 4 engineered
- **Excluded:** protein_id (unique identifier), sequence (raw amino acid string)
- **Train/test split:** 80/20 stratified — perfectly balanced, each class gets ~20% in both splits
- **Scaling:** StandardScaler

## Target Distribution

| Class | Train | Test |
|-------|------:|-----:|
| Enzyme | 9,563 (19.9%) | 2,391 (19.9%) |
| Outras | 9,773 (20.4%) | 2,443 (20.4%) |
| Receptor | 9,480 (19.8%) | 2,370 (19.8%) |
| Structural | 9,593 (20.0%) | 2,398 (20.0%) |
| Transport | 9,591 (20.0%) | 2,398 (20.0%) |
