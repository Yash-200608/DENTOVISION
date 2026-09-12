# API

Base URL for local development: `http://localhost:8000`

Interactive schema: [http://localhost:8000/docs](http://localhost:8000/docs)

There is **no authentication**. Do not expose this API on an untrusted network or upload identifiable patient studies. See [SECURITY.md](../SECURITY.md).

## `GET /health`

Liveness probe. Returns the configured environment label.

```bash
curl -s http://localhost:8000/health
```

```json
{
  "status": "ok",
  "environment": "development"
}
```

## `POST /predict`

Multipart upload of a radiograph. Allowed extensions: `png`, `jpg`, `jpeg`, `dcm` (override with `ALLOWED_EXTENSIONS`). Default size limit: 10 MB (`MAX_UPLOAD_SIZE_MB`).

```bash
curl -s -X POST http://localhost:8000/predict \
  -F "file=@sample.png;type=image/png"
```

DICOM:

```bash
curl -s -X POST http://localhost:8000/predict \
  -F "file=@study.dcm;type=application/dicom"
```

### Success (`200`)

```json
{
  "findings": [
    {
      "class": "caries",
      "confidence": 0.91,
      "bbox": [120.5, 80.0, 210.2, 175.4]
    }
  ]
}
```

| Field | Meaning |
| --- | --- |
| `class` | Detector class name (`caries` or `periapical_lesion` when dental weights are loaded) |
| `confidence` | Score in `[0.0, 1.0]` after `CONFIDENCE_THRESHOLD` |
| `bbox` | `[x1, y1, x2, y2]` in pixel coordinates of the decoded image |

An empty `findings` list means nothing passed the confidence threshold.

### Errors

| Status | When |
| --- | --- |
| `422` | Missing `file` part |
| `400` | Failed validation or decode (`{"error": "..."}`) — bad extension, MIME, size, or corrupt image/DICOM |
| `500` | Unhandled failure (`{"error": "An internal server error occurred."}`) |

Classes come from the loaded YOLO model. With `models/best.pt` trained on [`configs/data.yaml`](../configs/data.yaml) they are `caries` and `periapical_lesion`. The `yolov8n.pt` fallback uses COCO names instead.

Annotated overlay images are **not** returned. `dentovision.inference.visualize.draw_predictions` exists for offline use only.
