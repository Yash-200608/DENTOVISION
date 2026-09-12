# Deployment

The supported runtime is a single FastAPI process behind Uvicorn, optionally in Docker. There is no TLS terminator, reverse-proxy config, or orchestrator in this repository.

**Do not** put this service on the public internet. There is no authentication, and CORS allows all origins. See [SECURITY.md](../SECURITY.md).

## Environment

Copy [`.env.example`](../.env.example) to `.env` and set at least:

| Variable | Role |
| --- | --- |
| `YOLO_MODEL_PATH` | Checkpoint path inside the container or host (`models/best.pt`) |
| `API_HOST` | Bind address (Docker default `0.0.0.0`) |
| `API_PORT` | Listen port (`8000`) |
| `ENVIRONMENT` | Label returned by `/health` (`development`, `staging`, `production`) |
| `MAX_UPLOAD_SIZE_MB` | Upload cap |
| `CONFIDENCE_THRESHOLD` | Detector cutoff |

The container user is `appuser` (non-root). The process working directory is `/app`. Place weights where `YOLO_MODEL_PATH` points, or rely on `/app/yolov8n.pt` as the generic fallback.

## Docker

Build from the repository root:

```bash
docker build -t dentovision-api .
```

The image installs `requirements.txt`, installs the `dentovision` package, and copies `configs/` plus `yolov8n.pt`. It does **not** copy `models/best.pt` (those files are gitignored). Mount weights at runtime:

```bash
docker run --rm -p 8000:8000 --env-file .env \
  -v ${PWD}/models/best.pt:/app/models/best.pt:ro \
  dentovision-api
```

Windows PowerShell equivalent volume:

```powershell
docker run --rm -p 8000:8000 --env-file .env `
  -v ${PWD}/models/best.pt:/app/models/best.pt:ro `
  dentovision-api
```

Health check from the host:

```bash
curl -s http://localhost:8000/health
```

## Process command

Equivalent without Docker, after `pip install -e .`:

```bash
uvicorn dentovision.api.app:app --host 0.0.0.0 --port 8000
```

Do not use `--reload` in a deployed process.

## Logs

The app writes rotating logs to `logs/app.log` (10 MB, 5 backups). Mount or persist `logs/` if you need them outside the container. Treat logs as sensitive if real filenames were uploaded.

## Checklist before any shared environment

- [ ] Repository and image stay private
- [ ] `.env` is not baked into the image
- [ ] Clinical weights are mounted, not committed
- [ ] Network access is limited to trusted clients
- [ ] No identifiable DICOM/PHI is stored under `datasets/`
