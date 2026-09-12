import cv2
import numpy as np
from typing import List, Dict, Any

def draw_predictions(image: np.ndarray, findings: List[Dict[str, Any]]) -> np.ndarray:
    """
    Draw bounding boxes and labels on an image.
    
    Args:
        image: Original image as a NumPy array (BGR).
        findings: List of predictions.
        
    Returns:
        Image with drawn bounding boxes.
    """
    img_drawn = image.copy()
    
    # Class colors mapping (BGR format)
    colors = {
        "caries": (0, 0, 255),             # Red
        "periapical_lesion": (0, 255, 255) # Yellow
    }
    
    for finding in findings:
        cls_name = finding.get("class", "unknown")
        conf = finding.get("confidence", 0.0)
        bbox = finding.get("bbox", [0, 0, 0, 0])
        
        x1, y1, x2, y2 = map(int, bbox)
        color = colors.get(cls_name, (0, 255, 0)) # Default green
        
        # Draw box
        cv2.rectangle(img_drawn, (x1, y1), (x2, y2), color, 2)
        
        # Draw label
        label = f"{cls_name} {conf:.2f}"
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img_drawn, (x1, y1 - 20), (x1 + w, y1), color, -1)
        cv2.putText(img_drawn, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        
    return img_drawn
