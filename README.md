# DENTOVISION

DENTOVISION is a research prototype for AI-assisted dental radiograph interpretation. It uses YOLOv8 to detect `caries` and `periapical_lesion` in PNG, JPEG, and DICOM radiographs and serves results through a FastAPI REST API.

**This software is proprietary.** See [LICENSE](LICENSE). No patent license is granted. Do not publish, redistribute, or use this codebase without written permission.

**Not a medical device. Not for clinical use.** Predictions are experimental and must not be used for diagnosis or treatment decisions.

## Features

- Object detection for `caries` and `periapical_lesion` with bounding boxes
- REST API with OpenAPI docs at `/docs`
- Native DICOM (`.dcm`) plus PNG/JPEG uploads
- Docker image with a non-root runtime user
- Detector abstraction (`BaseDetector`) so other models can be swapped in later

## Requirements

- Python 3.11+
- pip
- Optional: Docker
- Trained weights at `models/best.pt` (the API falls back to `yolov8n.pt` if that file is missing)

On Windows, `python-magic` needs libmagic. Install `python-magic-bin` in the same virtualenv, or use Docker (the image already includes `libmagic1`).

## Quick start

```bash
git clone https://github.com/Yash-200608/DENTOVISION.git
cd DENTOVISION
python -m venv venv
```

Activate the environment (`source venv/bin/activate` on Linux/macOS, `venv\Scripts\activate` on Windows), then:

```bash
pip install -r requirements.txt
pip install -e .
copy .env.example .env   # Windows: copy   |  Linux/macOS: cp .env.example .env
```

Place trained weights at `models/best.pt`, then start the API:

```bash
uvicorn dentovision.api.app:app --reload --host 0.0.0.0 --port 8000
```

- Swagger UI: http://localhost:8000/docs
- Health: http://localhost:8000/health

### Docker

```bash
docker build -t dentovision-api .
docker run -p 8000:8000 --env-file .env dentovision-api
```

### Tests

```bash
pytest
```

## Project structure

```
dentovision/
├── src/dentovision/   # Installable Python package
│   ├── api/           # FastAPI app, routes, schemas
│   ├── core/          # Settings, logger, exceptions
│   ├── inference/     # BaseDetector and YOLOv8 implementation
│   ├── repositories/  # Local file storage (not used by /predict today)
│   ├── services/      # Prediction business logic
│   ├── training/      # Train, evaluate, and dataset prep
│   └── utils/         # Upload validation and DICOM conversion
├── configs/           # YOLO data.yaml
├── models/            # Trained weights (git-ignored except .gitkeep)
├── datasets/          # Training data (git-ignored except .gitkeep)
├── tests/             # Pytest suite
├── docs/              # Setup, API, training, and deployment guides
└── .github/           # CI, issue templates, pull request template
```

## Documentation

| Doc | Contents |
| --- | --- |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Layers, request flow, and endpoints |
| [docs/getting-started.md](docs/getting-started.md) | Local setup (Windows and Linux) |
| [docs/api.md](docs/api.md) | `/health`, `/predict`, curl examples |
| [docs/training.md](docs/training.md) | Dataset layout and train/eval commands |
| [docs/deployment.md](docs/deployment.md) | Docker and runtime configuration |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to propose changes |
| [SECURITY.md](SECURITY.md) | Vulnerability reporting and data handling |
| [CHANGELOG.md](CHANGELOG.md) | Release history |

## Extensibility

New detectors should implement `dentovision.inference.base.BaseDetector`. Training and evaluation run as modules:

```bash
python -m dentovision.training.train --data configs/data.yaml --epochs 100 --imgsz 640 --batch 16 --weights yolov8n.pt
python -m dentovision.training.evaluate --weights models/best.pt --data configs/data.yaml
```
