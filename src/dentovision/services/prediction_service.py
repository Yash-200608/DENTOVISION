from fastapi import UploadFile
import numpy as np
import cv2
from typing import List, Dict, Any

from inference.base import BaseDetector
from utils.file_utils import validate_uploaded_file
from utils.dicom_utils import dicom_to_numpy
from core.logger import logger
from core.exceptions import InvalidImageError

class PredictionService:
    def __init__(self, detector: BaseDetector):
        self.detector = detector
        
    async def process_image(self, file: UploadFile) -> List[Dict[str, Any]]:
        """
        Business logic for processing the uploaded image and returning predictions.
        """
        # 1. Validate file
        await validate_uploaded_file(file)
        
        # 2. Read bytes
        file_bytes = await file.read()
        
        # 3. Convert to NumPy array
        filename = file.filename or ""
        if filename.lower().endswith(".dcm"):
            image = dicom_to_numpy(file_bytes)
        else:
            np_arr = np.frombuffer(file_bytes, np.uint8)
            image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if image is None:
                raise InvalidImageError("Could not decode the image file.")
                
        # 4. Predict
        logger.info(f"Running inference on image: {filename}")
        findings = self.detector.predict(image)
        
        return findings
