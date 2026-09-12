import pytest
from fastapi import UploadFile
import io
from dentovision.utils.file_utils import validate_uploaded_file
from dentovision.core.exceptions import InvalidImageError, FileSizeExceededError
from dentovision.core.config import settings

@pytest.mark.asyncio
async def test_validate_invalid_extension():
    file_content = b"fake image content"
    file = UploadFile(filename="test.txt", file=io.BytesIO(file_content))
    with pytest.raises(InvalidImageError):
        await validate_uploaded_file(file)

@pytest.mark.asyncio
async def test_validate_large_file(monkeypatch):
    # Mocking size requires generating big file or mocking tell()
    # We will just write big chunk to memory
    file_content = b"a" * (settings.max_upload_size_bytes + 10)
    file = UploadFile(filename="test.jpg", file=io.BytesIO(file_content))
    with pytest.raises(FileSizeExceededError):
        await validate_uploaded_file(file)
