import argparse
from ultralytics import YOLO
from dentovision.core.logger import logger

def train_model(data_yaml: str, epochs: int, imgsz: int, batch_size: int, weights: str):
    """
    Trains the YOLOv8 model for dental radiograph interpretation.
    """
    logger.info("Starting YOLOv8 training pipeline...")
    try:
        model = YOLO(weights)
        
        results = model.train(
            data=data_yaml,
            epochs=epochs,
            imgsz=imgsz,
            batch=batch_size,
            project="models/runs",
            name="dentovision_train",
            exist_ok=True
        )
        logger.info(f"Training completed. Results saved to {results.save_dir}")
    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DENTOVISION Training Pipeline")
    parser.add_argument("--data", type=str, default="configs/data.yaml", help="Path to data.yaml")
    parser.add_argument("--epochs", type=int, default=100, help="Number of training epochs")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    parser.add_argument("--weights", type=str, default="yolov8n.pt", help="Pretrained weights")
    
    args = parser.parse_args()
    train_model(args.data, args.epochs, args.imgsz, args.batch, args.weights)
