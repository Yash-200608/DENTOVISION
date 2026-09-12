import os
import magic
from fastapi import UploadFile
from dentovision.core.config import settings
from dentovision.core.exceptions import InvalidImageError, FileSizeExceededError
from dentovision.core.logger import logger

async def validate_uploaded_file(file: UploadFile) -> None:
    """
    Validates file size and MIME type.
    Raises custom exceptions if validation fails.
    """
    # 1. Validate File Size using FastAPI's built-in size attribute
    if file.size is not None and file.size > settings.max_upload_size_bytes:
        logger.warning(f"File size exceeded: {file.size} bytes")
        raise FileSizeExceededError(f"File size exceeds maximum allowed size of {settings.max_upload_size_mb} MB")
        
    # 2. Validate Extension
    filename = file.filename or ""
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    if ext not in settings.allowed_extensions:
        logger.warning(f"Invalid file extension: {ext}")
        raise InvalidImageError(f"File extension '{ext}' is not allowed. Allowed: {', '.join(settings.allowed_extensions)}")
        
    # 3. Validate MIME Type (using magic)
    header = await file.read(2048)
    await file.seek(0) # Proper async seek for UploadFile
    
    mime = magic.from_buffer(header, mime=True)
    allowed_mimes = ["image/jpeg", "image/png", "application/dicom", "image/dicom"]
    
    if mime not in allowed_mimes and ext != "dcm":
         # DICOM files might sometimes be identified as application/octet-stream
         if not (ext == "dcm" and mime == "application/octet-stream"):
             logger.warning(f"Invalid MIME type: {mime}")
             raise InvalidImageError(f"MIME type '{mime}' is not supported.")
