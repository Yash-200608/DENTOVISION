import os
import shutil
import random
from typing import List, Tuple
from dentovision.core.logger import logger
from dentovision.utils.dicom_utils import save_dicom_as_png

class DentalDatasetPrep:
    """
    Orchestrates the preparation of dental radiograph datasets.
    """
    
    def __init__(self, raw_data_dir: str, processed_data_dir: str):
        self.raw_data_dir = raw_data_dir
        self.processed_data_dir = processed_data_dir
        
    def convert_dicoms(self) -> None:
        """Converts all DICOM files in raw_data_dir to PNG in processed_data_dir."""
        logger.info("Converting DICOMs to PNG...")
        os.makedirs(self.processed_data_dir, exist_ok=True)
        
        for root, _, files in os.walk(self.raw_data_dir):
            for file in files:
                if file.lower().endswith(".dcm"):
                    dicom_path = os.path.join(root, file)
                    png_name = os.path.splitext(file)[0] + ".png"
                    output_path = os.path.join(self.processed_data_dir, png_name)
                    save_dicom_as_png(dicom_path, output_path)

    def split_data(self, image_dir: str, label_dir: str, 
                   output_base: str, 
                   ratios: Tuple[float, float, float] = (0.7, 0.2, 0.1)) -> None:
        """
        Splits images and labels into train, val, and test sets.
        """
        logger.info(f"Splitting dataset with ratios {ratios}...")
        
        images = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        random.shuffle(images)
        
        n = len(images)
        train_idx = int(n * ratios[0])
        val_idx = train_idx + int(n * ratios[1])
        
        splits = {
            'train': images[:train_idx],
            'val': images[train_idx:val_idx],
            'test': images[val_idx:]
        }
        
        for split_name, split_images in splits.items():
            img_dest = os.path.join(output_base, 'images', split_name)
            lbl_dest = os.path.join(output_base, 'labels', split_name)
            os.makedirs(img_dest, exist_ok=True)
            os.makedirs(lbl_dest, exist_ok=True)
            
            for img_name in split_images:
                # Copy image
                shutil.copy2(os.path.join(image_dir, img_name), os.path.join(img_dest, img_name))
                
                # Copy corresponding label if exists
                label_name = os.path.splitext(img_name)[0] + ".txt"
                label_src = os.path.join(label_dir, label_name)
                if os.path.exists(label_src):
                    shutil.copy2(label_src, os.path.join(lbl_dest, label_name))
                else:
                    # Create empty label file for background images
                    open(os.path.join(lbl_dest, label_name), 'w').close()
                    
        logger.info("Dataset splitting complete.")

    def run_pipeline(self, coco_json: str = None):
        """Runs the full preparation pipeline."""
        # 1. Convert DICOMs (if any)
        self.convert_dicoms()
        
        # 2. Annotation conversion (if COCO provided)
        if coco_json:
            from dentovision.training.converters import COCOToYOLOConverter
            label_dir = os.path.join(self.processed_data_dir, "labels_temp")
            converter = COCOToYOLOConverter(coco_json, label_dir)
            converter.convert()
            
            # 3. Split
            self.split_data(
                image_dir=self.processed_data_dir,
                label_dir=label_dir,
                output_base="datasets/final_yolo"
            )
            
            # 4. Cleanup temp labels
            # shutil.rmtree(label_dir)
            
        logger.info("Pipeline execution finished.")
