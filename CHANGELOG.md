# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Moved Python packages into `src/dentovision/` and install via `pyproject.toml`.
- API entrypoint is now `uvicorn dentovision.api.app:app`.
- Training and evaluation run as `python -m dentovision.training.train` and `python -m dentovision.training.evaluate`.
- `.env.example` now uses `YOLO_MODEL_PATH` to match `Settings.yolo_model_path`.

### Added

- Proprietary `LICENSE`, architecture, contributing, and security docs.
- Guides under `docs/` (getting started, API, training, deployment).
- GitHub Actions CI, issue templates, and pull request template.
- `pytest-asyncio` dependency; `models/.gitkeep` and `datasets/.gitkeep`.

## [1.0.0] - 2026-06-07

### Added

- FastAPI application with `GET /health` and `POST /predict`.
- YOLOv8 inference for `caries` and `periapical_lesion`.
- DICOM and raster upload validation.
- Training, evaluation, and dataset-prep scripts.
- Dockerfile with a non-root runtime user.
- Pytest coverage for health, invalid uploads, and detector fallback.
