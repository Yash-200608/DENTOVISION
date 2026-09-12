import os
import cv2
import numpy as np
from typing import List, Tuple
from dentovision.core.logger import logger

def preprocess_image(image_path: str, target_size: Tuple[int, int] = (640, 640)) -> np.ndarray:
    """
    Standardizes a dental radiograph for model input.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image at {image_path}")
        
    # 1. Resize
    img_resized = cv2.resize(img, target_size)
    
    # 2. Histogram Equalization (common for radiographs)
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    equalized = cv2.equalizeHist(gray)
    img_processed = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)
    
    return img_processed

def normalize_dataset(image_dir: str, output_dir: str) -> None:
    """
    Applies preprocessing to all images in a directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                processed = preprocess_image(os.path.join(image_dir, filename))
                cv2.imwrite(os.path.join(output_dir, filename), processed)
            except Exception as e:
                logger.error(f"Failed to preprocess {filename}: {e}")
