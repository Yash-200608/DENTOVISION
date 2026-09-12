# Getting started

Local setup for the DENTOVISION API. This is a research prototype, **not for clinical use**.

## Prerequisites

- Python 3.11 or newer
- pip
- Git
- Optional: Docker (see [deployment.md](deployment.md))

On **Linux**, install libmagic for MIME checks, for example:

```bash
sudo apt-get update
sudo apt-get install -y libmagic1
```

On **Windows**, either:

- `pip install python-magic-bin` after the requirements, or
- run the API in Docker, which already includes `libmagic1`.

## Install

From the repository root:

```bash
python -m venv venv
```

Activate the virtual environment:

- Linux/macOS: `source venv/bin/activate`
- Windows (PowerShell): `venv\Scripts\Activate.ps1`
- Windows (cmd): `venv\Scripts\activate.bat`

Then install dependencies and the package in editable mode:

```bash
pip install -r requirements.txt
pip install -e .
```

Copy the environment template:

```bash
# Linux/macOS
cp .env.example .env

# Windows
copy .env.example .env
```

Edit `.env` if you need non-default host, port, model path, or upload limits. The setting that points at weights is `YOLO_MODEL_PATH` (not `MODEL_PATH`).

## Weights

Place a trained checkpoint at `models/best.pt` (the default `YOLO_MODEL_PATH`).

If that file is missing, `YOLODetector` loads `yolov8n.pt` from the working directory. That fallback is a generic COCO model and will **not** detect dental classes reliably.

## Run the API

```bash
uvicorn dentovision.api.app:app --reload --host 0.0.0.0 --port 8000
```

| URL | Purpose |
| --- | --- |
| http://localhost:8000/docs | Interactive OpenAPI UI |
| http://localhost:8000/health | Liveness / environment |
| http://localhost:8000/predict | Multipart prediction (see [api.md](api.md)) |

Bind host and port also come from `API_HOST` and `API_PORT` if you launch through Docker.

## Tests

```bash
pytest
```

`pytest.ini` adds `src` to `pythonpath`. An editable install (`pip install -e .`) is still recommended so `import dentovision` matches production.

## Training

Optional. See [training.md](training.md).

```bash
python -m dentovision.training.train --data configs/data.yaml --epochs 100 --imgsz 640 --batch 16 --weights yolov8n.pt
```

## Common issues

- **`ImportError: failed to find libmagic`**: install `libmagic1` (Linux) or `python-magic-bin` (Windows).
- **Model warning then COCO classes**: `models/best.pt` is missing; the generic `yolov8n.pt` fallback is in use.
- **Port already in use**: change `API_PORT` or the `--port` flag.
