from abc import ABC, abstractmethod
from typing import List, Dict, Any
import numpy as np

class BaseDetector(ABC):
    """Abstract base class for all object detectors."""
    
    @abstractmethod
    def load_model(self) -> None:
        """Load the model into memory."""
        pass
        
    @abstractmethod
    def predict(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        Run inference on an image.
        
        Args:
            image: NumPy array of the image (BGR format for OpenCV compatibility).
            
        Returns:
            List of dictionaries representing findings:
            [{"class": "caries", "confidence": 0.95, "bbox": [x1, y1, x2, y2]}]
        """
        pass
