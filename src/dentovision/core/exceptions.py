class DentovisionException(Exception):
    """Base exception for all DENTOVISION custom exceptions."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class InvalidImageError(DentovisionException):
    """Raised when the uploaded image is invalid, corrupted, or unsupported."""
    pass

class FileSizeExceededError(DentovisionException):
    """Raised when the uploaded file exceeds the maximum allowed size."""
    pass

class ModelLoadError(DentovisionException):
    """Raised when the ML model fails to load."""
    pass

class PredictionError(DentovisionException):
    """Raised when an error occurs during model inference."""
    pass
