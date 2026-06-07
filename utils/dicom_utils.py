import pydicom
import numpy as np
import cv2
from io import BytesIO
from core.exceptions import InvalidImageError
from core.logger import logger

def dicom_to_numpy(file_bytes: bytes) -> np.ndarray:
    """
    Converts DICOM bytes to a NumPy array (BGR image).
    """
    try:
        dicom_file = pydicom.dcmread(BytesIO(file_bytes))
        pixel_array = dicom_file.pixel_array
        
        # Normalize to 0-255
        if pixel_array.max() > pixel_array.min():
            pixel_array = (pixel_array - pixel_array.min()) / (pixel_array.max() - pixel_array.min()) * 255.0
            
        pixel_array = pixel_array.astype(np.uint8)
        
        # Convert grayscale to BGR for OpenCV consistency
        if len(pixel_array.shape) == 2:
            img_bgr = cv2.cvtColor(pixel_array, cv2.COLOR_GRAY2BGR)
        else:
            img_bgr = cv2.cvtColor(pixel_array, cv2.COLOR_RGB2BGR)
            
        return img_bgr
    except Exception as e:
        logger.error(f"Failed to parse DICOM: {e}")
        raise InvalidImageError("Invalid or corrupted DICOM file.")

def save_dicom_as_png(dicom_path: str, output_path: str) -> None:
    """
    Reads a DICOM file from disk and saves it as a PNG.
    """
    try:
        with open(dicom_path, "rb") as f:
            file_bytes = f.read()
        image = dicom_to_numpy(file_bytes)
        cv2.imwrite(output_path, image)
        logger.info(f"Converted {dicom_path} to {output_path}")
    except Exception as e:
        logger.error(f"Failed to convert DICOM {dicom_path} to PNG: {e}")
        raise
