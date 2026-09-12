import numpy as np
from dentovision.inference.yolo_detector import YOLODetector

def test_detector_initialization():
    detector = YOLODetector(model_path="dummy_path.pt", conf_threshold=0.5)
    assert detector.conf_threshold == 0.5
    # Should fallback to yolov8n.pt if not found
    assert detector.model is not None

def test_detector_predict():
    detector = YOLODetector()
    # Create a dummy image
    dummy_image = np.zeros((640, 640, 3), dtype=np.uint8)
    
    findings = detector.predict(dummy_image)
    assert isinstance(findings, list)
