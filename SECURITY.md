# Security

## Not for clinical use

DENTOVISION is a research prototype. It is **not** a medical device, is **not** validated for diagnosis, and must **not** process production patient data in an uncontrolled environment.

## Reporting a vulnerability

Do **not** open a public issue for security problems.

Report privately through [GitHub Security Advisories](https://github.com/Yash-200608/DENTOVISION/security/advisories/new) on this repository. Include:

- Affected component and version / commit
- Impact (data exposure, unauthenticated access, model/file abuse)
- Reproduction notes **without** patient files or PHI

You should receive an acknowledgement when a maintainer is available. Do not share exploit details outside that advisory.

## Current security posture

This prototype is intentionally incomplete for production:

| Area | Current state |
| --- | --- |
| Authentication | None. `/health` and `/predict` are open. |
| CORS | `allow_origins=["*"]` with credentials enabled. |
| PHI / DICOM | Uploads may contain identifying metadata. `/predict` keeps bytes in memory; `FileRepository` can write to `datasets/uploads` if used. |
| Persistence | No encryption, retention policy, or audit trail. |
| Secrets | `.env` is gitignored. `.env.example` has no credentials. |

Upload checks that **are** present: maximum size (`MAX_UPLOAD_SIZE_MB`), extension allowlist, and MIME sniffing via `python-magic`. Filenames saved through `FileRepository` are basenamed and checked against path traversal.

The Docker image runs as non-root `appuser`.

## Handling radiographs and DICOM

- Prefer de-identified research datasets.
- Do not commit files under `datasets/` or trained clinical weights (`models/*.pt` is gitignored).
- Do not paste DICOM headers, patient names, or images into GitHub, chat, or logs.
- Treat `logs/app.log` as potentially sensitive if real filenames were uploaded.

## Scope

Hardening authentication, locking CORS, and adding clinical-grade data controls are out of scope for the current documentation work. Until those exist, run the API only on trusted networks with non-production data.
