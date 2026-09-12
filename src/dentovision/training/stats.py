import os
from collections import Counter
from typing import Dict, List, Any
import yaml
from dentovision.core.logger import logger

class DatasetStats:
    """
    Analyzes and reports statistics for a YOLO format dataset.
    """
    
    def __init__(self, data_yaml_path: str):
        self.data_yaml_path = data_yaml_path
        with open(data_yaml_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.class_names = self.config.get('names', {})
        self.base_path = self.config.get('path', '.')
        
    def generate_report(self) -> Dict[str, Any]:
        report = {}
        for split in ['train', 'val', 'test']:
            split_path = self.config.get(split)
            if not split_path:
                continue
                
            # YOLO usually stores labels in a sibling directory named 'labels'
            images_dir = os.path.join(self.base_path, split_path)
            labels_dir = images_dir.replace('images', 'labels')
            
            if not os.path.exists(labels_dir):
                logger.warning(f"Labels directory not found for {split}: {labels_dir}")
                continue
                
            stats = self._analyze_split(labels_dir)
            report[split] = stats
            
        self._print_report(report)
        return report

    def _analyze_split(self, labels_dir: str) -> Dict[str, Any]:
        class_counts = Counter()
        total_images = 0
        total_instances = 0
        
        for label_file in os.listdir(labels_dir):
            if not label_file.endswith('.txt'):
                continue
                
            total_images += 1
            with open(os.path.join(labels_dir, label_file), 'r') as f:
                for line in f:
                    parts = line.split()
                    if not parts:
                        continue
                    class_id = int(parts[0])
                    class_counts[class_id] += 1
                    total_instances += 1
                    
        return {
            "total_images": total_images,
            "total_instances": total_instances,
            "class_distribution": {self.class_names.get(k, str(k)): v for k, v in class_counts.items()}
        }

    def _print_report(self, report: Dict[str, Any]) -> None:
        logger.info("=== Dataset Statistics Report ===")
        for split, stats in report.items():
            logger.info(f"Split: {split}")
            logger.info(f"  Total Images: {stats['total_images']}")
            logger.info(f"  Total Instances: {stats['total_instances']}")
            logger.info(f"  Class Distribution:")
            for cls_name, count in stats['class_distribution'].items():
                logger.info(f"    - {cls_name}: {count} ({count/stats['total_instances']*100:.2f}%)")
        logger.info("=================================")
