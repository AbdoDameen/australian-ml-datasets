# Forest Cover Type

Cartographic data predicting forest cover types from US Forest Service (Roosevelt National Forest). 581K cells across 54 raw features — elevation, aspect, slope, hydrology distances, hillshade, wilderness areas, and soil types.

**Domain:** Ecology  
**ML Task:** Multi-class classification (7 cover types)  
**Source:** UCI ML Repository — https://archive.ics.uci.edu/dataset/31/covertype  
**Size:** 581,012 rows × 68 features (after engineering)

## Columns

**Quantitative (10):** elevation, aspect, slope, horizontal_distance_to_hydrology, vertical_distance_to_hydrology, horizontal_distance_to_roadways, hillshade_9am, hillshade_noon, hillshade_3pm, horizontal_distance_to_fire_points

**Binary (44):** wilderness_area_1–4, soil_type_1–40

**Derived (12):** elevation_slope, horiz_vert_hydrology_ratio, avg_hillshade, hillshade_range, total_hydrology_distance, near_water, near_road, near_fire, northness, eastness, wilderness_count, soil_count

**Target:** cover_type (1=Spruce/Fir, 2=Lodgepole Pine, 3=Ponderosa Pine, 4=Cottonwood/Willow, 5=Aspen, 6=Douglas-fir, 7=Krummholz)

## Files

| Folder | Contents |
|--------|----------|
| `raw/` | Original UCI .data + .info files |
| `processed/` | `forest_cover_type_clean.csv` (122MB) |
| `features/` | X_train_scaled, X_test_scaled, y_train, y_test, scaler.pkl, label_encoder.pkl |

## Usage

```bash
cd daily-datasets/ecology/forest-cover-type
python3 prepare_dataset.py    # full pipeline (clean → engineer → ML prep)
```

Feature files are too large for git — run the script to regenerate.
