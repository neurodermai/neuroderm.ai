"""
Validation utilities
"""

from typing import Optional
from fastapi import UploadFile, HTTPException
from app.config import settings


def validate_image_file(file: UploadFile) -> None:
    """
    Validate uploaded image file
    
    Args:
        file: Uploaded file
    
    Raises:
        HTTPException: If validation fails
    """
    # Check filename
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check extension
    file_extension = file.filename.split('.')[-1].lower()
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type .{file_extension} not allowed. "
                   f"Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Check content type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="File must be an image"
        )


def validate_skin_type(skin_type: Optional[str]) -> None:
    """
    Validate skin type
    
    Args:
        skin_type: Skin type string
    
    Raises:
        HTTPException: If validation fails
    """
    if skin_type is None:
        return
    
    valid_types = ["oily", "dry", "combination", "normal", "sensitive"]
    
    if skin_type.lower() not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid skin type. Must be one of: {', '.join(valid_types)}"
        )