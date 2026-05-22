# Kangaroo Tracking (ALA)

Kangaroo detection dataset — 164 images with PASCAL VOC bounding box annotations. Single class (kangaroo). Good for object detection demos and transfer learning.

**Domain:** Wildlife / Computer Vision  
**ML Task:** Object detection (single class)  
**Source:** https://github.com/experiencor/kangaroo  
**Size:** 164 images, 164 PASCAL VOC XML annotations

## Files

| Folder | Contents |
|--------|----------|
| `raw/images/` | 164 JPEG images (18.8 MB) |
| `raw/annots/` | 164 PASCAL VOC XML annotations |
| `download_data.py` | Script to re-download from GitHub |

## Annotation Format

PASCAL VOC XML with `kangaroo` as the single object class. Each annotation contains:
- Image size (width, height, depth)
- Bounding box (xmin, ymin, xmax, ymax)

## Usage

```bash
cd daily-datasets/wildlife/kangaroo-tracking
python3 download_data.py
```

Data too large for git — run the script to reproduce.
