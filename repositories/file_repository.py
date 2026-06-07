import os
from fastapi import UploadFile
from core.logger import logger
import shutil

class FileRepository:
    """
    Handles saving uploaded files or metadata to storage.
    Placeholder for future database/S3 integration.
    """
    
    def __init__(self, upload_dir: str = "datasets/uploads"):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)
        
    def save_file(self, file: UploadFile, filename: str) -> str:
        """Saves the file to local disk and returns the path."""
        try:
            file_path = os.path.join(self.upload_dir, filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file.file.seek(0) # reset for subsequent reads
            logger.info(f"Saved file to {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Failed to save file: {e}")
            raise
