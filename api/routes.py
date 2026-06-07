from fastapi import APIRouter, UploadFile, File, Depends
from api.schemas import PredictionResponse, FindingSchema
from inference.yolo_detector import YOLODetector
from services.prediction_service import PredictionService

router = APIRouter()

# Global detector instance loaded once at startup for performance
# In a true production app, this would be managed via application lifespan events.
detector_instance = None

def get_detector():
    global detector_instance
    if detector_instance is None:
        detector_instance = YOLODetector()
    return detector_instance

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
