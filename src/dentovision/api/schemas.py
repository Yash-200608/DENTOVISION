from pydantic import BaseModel, Field
from typing import List, Tuple

class FindingSchema(BaseModel):
    class_name: str = Field(..., alias="class", description="The predicted class name (e.g., caries)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0 and 1")
    bbox: Tuple[float, float, float, float] = Field(..., description="Bounding box [x1, y1, x2, y2]")
    
    class Config:
        populate_by_name = True

class PredictionResponse(BaseModel):
    findings: List[FindingSchema] = Field(..., description="List of detected findings in the image")
