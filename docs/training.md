# Training

Train and evaluate the YOLOv8 detector used by the API. Use de-identified research data only. Do not commit `datasets/` or `models/*.pt`.

## Dataset layout

[`configs/data.yaml`](../configs/data.yaml) expects:

```text
datasets/
  images/
    train/
    val/
  labels/
    train/
    val/
```

`path` in the YAML is `../datasets` relative to `configs/`. Class names:

| ID | Name |
| --- | --- |
| 0 | `caries` |
| 1 | `periapical_lesion` |

Labels are standard YOLO txt files (`class x_center y_center width height`, normalized).

## Prepare data

Helpers live in `dentovision.training`:

- `dataset_prep.DentalDatasetPrep` — DICOM to PNG, optional COCO conversion, train/val/test split
- `converters.COCOToYOLOConverter` — COCO JSON to YOLO labels
- `dataset_utils.preprocess_image` / `normalize_dataset` — resize and histogram equalization
- `stats.DatasetStats` — class counts from a data YAML

Example split output directory used by the prep pipeline: `datasets/final_yolo`.

## Train

From the repository root, with the package installed (`pip install -e .`):

```bash
python -m dentovision.training.train \
  --data configs/data.yaml \
  --epochs 100 \
  --imgsz 640 \
  --batch 16 \
  --weights yolov8n.pt
```

Ultralytics writes runs under `models/runs/dentovision_train`. Copy the checkpoint you want to serve:

```bash
copy models\runs\dentovision_train\weights\best.pt models\best.pt
```

On Linux/macOS use `cp` instead of `copy`. Set `YOLO_MODEL_PATH=models/best.pt` in `.env` (the default).

## Evaluate

```bash
python -m dentovision.training.evaluate \
  --weights models/best.pt \
  --data configs/data.yaml
```

This runs Ultralytics `model.val` and logs mAP50-95.

## Serve trained weights

Restart the API after replacing `models/best.pt`. The process loads the detector once at startup (`lifespan` in `dentovision.api.app`).
