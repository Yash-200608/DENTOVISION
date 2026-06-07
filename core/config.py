import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables and .env file.
    """
    api_title: str = "DENTOVISION API"
    api_version: str = "1.0.0"
    api_description: str = "AI-assisted dental radiograph interpretation platform."
    
    environment: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    yolo_model_path: str = "models/best.pt"
    confidence_threshold: float = 0.5
    
    log_level: str = "INFO"
    log_dir: str = "logs"
    
    max_upload_size_mb: int = 10
    allowed_extensions: List[str] = ["png", "jpg", "jpeg", "dcm"]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024

settings = Settings()

# Ensure critical directories exist
os.makedirs(settings.log_dir, exist_ok=True)
os.makedirs("models", exist_ok=True)
os.makedirs("datasets", exist_ok=True)
