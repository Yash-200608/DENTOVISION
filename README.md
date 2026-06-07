# DENTOVISION 🦷

DENTOVISION is an MCC-funded research prototype for AI-assisted dental radiograph interpretation. It leverages YOLOv8 to detect dental caries and periapical lesions in radiographs and exposes these capabilities via a RESTful FastAPI backend.

## 🚀 Features

- **Object Detection:** Detects `caries` and `periapical_lesion` with bounding boxes.
- **RESTful API:** Fast, documented (Swagger), and robust REST API via FastAPI.
- **DICOM Support:** Native processing of medical DICOM files along with standard formats (PNG, JPEG).
- **Containerized:** Fully Dockerized for seamless deployment.
- **Clean Architecture:** Built on SOLID principles, ready for future AI and AR extensions.

## 📁 Project Structure

```
dentovision/
├── api/             # FastAPI app, routes, schemas
├── configs/         # Model and environment configurations
├── core/            # Config, logger, custom exceptions
├── datasets/        # Data for training (git-ignored)
├── inference/       # Base detector and YOLO implementation
├── models/          # Trained weights (.pt files)
├── repositories/    # File storage and database logic
├── services/        # Business logic layer
├── tests/           # Pytest suite
├── training/        # YOLO model training and evaluation scripts
├── utils/           # Utilities for files and DICOM
```

## 🛠️ Quick Start

### 1. Local Setup

1. **Clone the repository.**
2. **Create a virtual environment:** `python -m venv venv`
3. **Activate it:** `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. **Install requirements:** `pip install -r requirements.txt`
5. **Configure environment:** Copy `.env.example` to `.env` and adjust the variables.
6. **Download YOLO weights:** Place your `best.pt` in the `models/` directory.

### 2. Run the API

```bash
uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```
Navigate to `http://localhost:8000/docs` to view the interactive API documentation.

### 3. Docker Deployment

```bash
docker build -t dentovision-api .
docker run -p 8000:8000 --env-file .env dentovision-api
```

## 🧠 Future Extensibility

The codebase relies on strict abstraction (`BaseDetector`). Integrating AR overlay modules, LLM-based clinical explanations, or voice assistants can be achieved without modifying core API endpoints.
