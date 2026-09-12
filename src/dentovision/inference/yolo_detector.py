from typing import List, Dict, Any
import numpy as np
from ultralytics import YOLO
import os

from inference.base import BaseDetector
from core.config import settings
from core.logger import logger
from core.exceptions import ModelLoadError, PredictionError

class YOLODetector(BaseDetector):
    """YOLOv8 implementation of the BaseDetector."""
    
    def __init__(self, model_path: str = None, conf_threshold: float = None):
        self.model_path = model_path or settings.yolo_model_path
        self.conf_threshold = conf_threshold or settings.confidence_threshold
        self.model = None
        self.load_model()
        
    def load_model(self) -> None:
        try:
            if not os.path.exists(self.model_path):
                logger.warning(f"Model path {self.model_path} does not exist. Using YOLOv8n default weights.")
                self.model = YOLO("yolov8n.pt") 
            else:
                self.model = YOLO(self.model_path)
            logger.info(f"Successfully loaded YOLO model from {self.model_path}")
        except Exception as e:
            logger.error(f"Failed to load YOLO model: {e}")
            raise ModelLoadError(f"Failed to load model: {e}")
            
    def predict(self, image: np.ndarray) -> List[Dict[str, Any]]:
        if self.model is None:
            raise PredictionError("Model is not loaded.")
            
        try:
            results = self.model.predict(
                source=image,
                conf=self.conf_threshold,
                verbose=False
            )
            
            findings = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    conf = float(box.conf[0])
                    class_id = int(box.cls[0])
                    class_name = self.model.names[class_id]
                    
                    findings.append({
                        "class": class_name,
                        "confidence": conf,
                        "bbox": [x1, y1, x2, y2]
                    })
            return findings
        except Exception as e:
            logger.error(f"Error during YOLO prediction: {e}")
            raise PredictionError(f"Prediction failed: {e}")
