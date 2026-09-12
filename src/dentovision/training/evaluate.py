import argparse
from ultralytics import YOLO
from dentovision.core.logger import logger

def evaluate_model(weights_path: str, data_yaml: str):
    """
    Evaluates the trained YOLOv8 model on the validation dataset.
    """
    logger.info(f"Evaluating model {weights_path} on dataset {data_yaml}...")
    try:
        model = YOLO(weights_path)
        metrics = model.val(data=data_yaml)
        
        logger.info(f"Evaluation Metrics: mAP50-95: {metrics.box.map}")
    except Exception as e:
        logger.error(f"Evaluation failed: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DENTOVISION Evaluation Pipeline")
    parser.add_argument("--weights", type=str, required=True, help="Path to trained weights (e.g. best.pt)")
    parser.add_argument("--data", type=str, default="configs/data.yaml", help="Path to data.yaml")
    
    args = parser.parse_args()
    evaluate_model(args.weights, args.data)
