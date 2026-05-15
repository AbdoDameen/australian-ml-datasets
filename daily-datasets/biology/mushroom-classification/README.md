# 05 | Mushroom Classification

8,124 mushrooms from the Agaricus and Lepiota families. Binary classification: edible or poisonous.

**Source:** UCI ML Repository — [Mushroom](https://archive.ics.uci.edu/dataset/73/mushroom)

**Task:** Predict if a mushroom is poisonous (p) or edible (e)

## Data

| Attribute | Values | Description |
|-----------|--------|-------------|
| cap_shape | bell, conical, convex, flat, knobbed, sunken | |
| cap_surface | fibrous, grooves, scaly, smooth | |
| cap_color | brown, buff, cinnamon, gray, green, pink, purple, red, white, yellow | |
| bruises | bruises, no | |
| odor | almond, anise, creosote, fishy, foul, musty, none, pungent, spicy | **Strongest predictor** |
| gill_attachment | attached, descending, free, notched | |
| gill_spacing | close, crowded, distant | |
| gill_size | broad, narrow | |
| gill_color | black, brown, buff, chocolate, gray, green, orange, pink, purple, red, white, yellow | |
| stalk_shape | enlarging, tapering | |
| stalk_root | bulbous, club, cup, equal, rhizomorphs, rooted, missing | 2,480 originally missing → mapped to "missing" |
| stalk_surface_above_ring | fibrous, scaly, silky, smooth | |
| stalk_surface_below_ring | fibrous, scaly, silky, smooth | |
| stalk_color_above_ring | brown, buff, cinnamon, gray, orange, pink, red, white, yellow | |
| stalk_color_below_ring | brown, buff, cinnamon, gray, orange, pink, red, white, yellow | |
| veil_type | partial, universal | Constant (partial for all) |
| veil_color | brown, orange, white, yellow | |
| ring_number | none, one, two | |
| ring_type | cobwebby, evanescent, flaring, large, none, pendant, sheathing, zone | |
| spore_print_color | black, brown, buff, chocolate, green, orange, purple, white, yellow | |
| population | abundant, clustered, numerous, scattered, several, solitary | |
| habitat | grasses, leaves, meadows, paths, urban, waste, woods | |

**Class balance:** 4,208 edible (51.8%) / 3,916 poisonous (48.2%)

Notable reference rules from the literature — odor alone catches ~98%:
- P₁: odor ≠ (almond or anise or none)
- P₂: spore-print-color = green
- P₃: odor = none AND stalk-surface-below-ring = scaly AND stalk-color-above-ring ≠ brown

## Files

| File | Description |
|------|-------------|
| `raw/` | Original UCI .data file + metadata |
| `processed/mushroom_clean.csv` | Cleaned data with human-readable labels |
| `processed/mushroom_encoded.csv` | 117 one-hot encoded features |
| `features/` | Train/test splits (80/20, stratified), scaled |
| `prepare_dataset.py` | Reproducible pipeline |
| `metadata.json` | Full transformation log |

## Usage

```bash
cd daily-datasets/biology/mushroom-classification
python3 prepare_dataset.py
```
