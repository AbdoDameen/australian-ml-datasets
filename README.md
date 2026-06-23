# Australian ML Datasets

**80 datasets** across **50+ domains**, all in one place. Each has a `raw/` folder with source data, ready for processing.

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

---

## Tools

### `tools/drawio-skill/` — Diagrams from text

Generate architecture diagrams, flowcharts, ERDs, ML model figures, UML class/sequence diagrams, and network topology — as `.drawio` XML + PNG/SVG/PDF export via the native draw.io desktop CLI.

**Key features:**
- **6 diagram presets** — ERD, UML Class, Sequence, Architecture, ML/DL, Flowchart
- **Shape search** — exact icons for 10k+ AWS/Azure/GCP/Cisco/Kubernetes/UML shapes
- **AI/LLM brand logos** — 321 logos (OpenAI, Claude, Gemini, Llama, LangChain, …)
- **Codebase viz** — extract import graphs from Python/JS/Go/Rust projects, auto-laid out via Graphviz
- **Self-check + review loop** — vision-based auto-fix, up to 5 iterative refinement rounds
- **Browser fallback** — generates diagrams.net URLs when CLI unavailable

**Requires:** draw.io desktop ([install](https://github.com/jgraph/drawio-desktop/releases)). On WSL, the Windows `.exe` is auto-detected at `/mnt/c/Program Files/draw.io/draw.io.exe`.

```
# Generate + export
python3 tools/drawio-skill/scripts/encode_drawio_url.py --edit diagram.drawio

# Search shapes
python3 tools/drawio-skill/scripts/shapesearch.py "aws lambda"

# AI/LLM brand logos
python3 tools/drawio-skill/scripts/aiicons.py "claude"
```
