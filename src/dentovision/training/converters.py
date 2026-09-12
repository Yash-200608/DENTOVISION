import json
import os
from typing import Dict, List, Any
from dentovision.core.logger import logger

class COCOToYOLOConverter:
    """
    Converts COCO format annotations to YOLOv8 format.
    """
    
    def __init__(self, coco_json_path: str, output_dir: str):
        self.coco_json_path = coco_json_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def convert(self) -> None:
        logger.info(f"Converting {self.coco_json_path} to YOLO format...")
        
        with open(self.coco_json_path, 'r') as f:
            data = json.load(f)
            
        categories = {cat['id']: i for i, cat in enumerate(data['categories'])}
        images = {img['id']: img for img in data['images']}
        
        annotations_by_image: Dict[int, List[Dict[str, Any]]] = {}
        for ann in data['annotations']:
            img_id = ann['image_id']
            if img_id not in annotations_by_image:
                annotations_by_image[img_id] = []
            annotations_by_image[img_id].append(ann)
            
        for img_id, anns in annotations_by_image.items():
            img_info = images.get(img_id)
            if not img_info:
                continue
                
            file_name = img_info['file_name']
            width = img_info['width']
            height = img_info['height']
            
            # Create YOLO label file
            label_file_name = os.path.splitext(file_name)[0] + ".txt"
            label_path = os.path.join(self.output_dir, label_file_name)
            
            with open(label_path, 'w') as f_out:
                for ann in anns:
                    cat_id = ann['category_id']
                    yolo_cat = categories[cat_id]
                    
                    # COCO bbox: [x, y, width, height]
                    # YOLO bbox: [x_center, y_center, width, height] (normalized)
                    x, y, w, h = ann['bbox']
                    
                    x_center = (x + w / 2) / width
                    y_center = (y + h / 2) / height
                    w_norm = w / width
                    h_norm = h / height
                    
                    f_out.write(f"{yolo_cat} {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}\n")
                    
        logger.info(f"Conversion complete. Labels saved to {self.output_dir}")
