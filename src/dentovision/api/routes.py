from fastapi import APIRouter, UploadFile, File, Depends, Request
from dentovision.api.schemas import PredictionResponse, FindingSchema
from dentovision.inference.yolo_detector import YOLODetector
from dentovision.services.prediction_service import PredictionService

router = APIRouter()

def get_detector(request: Request) -> YOLODetector:
    """Retrieves the pre-loaded YOLO detector from app state."""
    return request.app.state.detector

def get_prediction_service(detector: YOLODetector = Depends(get_detector)) -> PredictionService:
    return PredictionService(detector=detector)

@router.post("/predict", response_model=PredictionResponse)
async def predict_image(
    file: UploadFile = File(...),
    service: PredictionService = Depends(get_prediction_service)
):
    """
    Endpoint to predict dental findings (caries, periapical lesions) 
    from an uploaded radiograph image.
    """
    findings = await service.process_image(file)
    
    # Map raw dictionary to Pydantic schemas
    mapped_findings = [FindingSchema(**finding) for finding in findings]
    
    return PredictionResponse(findings=mapped_findings)
