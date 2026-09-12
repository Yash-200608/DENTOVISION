# Contributing

DENTOVISION is a private, proprietary research project. Contribute only if you have permission from the copyright holder. Do not fork or publish this repository.

**Never attach, commit, or paste patient radiographs, DICOM files, or other PHI** in issues, pull requests, logs, or sample fixtures.

## Development setup

Follow [docs/getting-started.md](docs/getting-started.md). In short:

```bash
python -m venv venv
# activate the venv
pip install -r requirements.txt
pip install -e .
copy .env.example .env
pytest
```

On Windows, install `python-magic-bin` if MIME validation fails.

## Branch and pull request workflow

1. Branch from `main` with a short name (`fix/upload-validation`, `docs/api-examples`).
2. Keep the change focused. Do not mix refactors with feature work.
3. Run `pytest` locally and fix failures before opening a pull request.
4. Fill in [`.github/pull_request_template.md`](.github/pull_request_template.md).
5. Request review from a maintainer.

## Coding guidelines

- Python 3.11+; match the existing package layout under `src/dentovision/`.
- Import the public package (`from dentovision.core.config import settings`), not relative sibling trees at the repo root.
- New detectors implement `dentovision.inference.base.BaseDetector`.
- Do not commit `.env`, `models/*.pt` (except the existing fallback `yolov8n.pt` if maintainers already track it), or anything under `datasets/`.
- Do not commit secrets, API keys, or credentials.

## Tests

- Place tests in `tests/` as `test_*.py`.
- Use `pytest` and `pytest-asyncio` for async validators.
- Prefer small synthetic fixtures (blank images, invalid extensions). Do not add real clinical images.

## Issues

Use the GitHub issue templates. Strip identifying metadata from any description of a failure. If a bug only reproduces on real patient data, describe the symptoms without sharing the file.
