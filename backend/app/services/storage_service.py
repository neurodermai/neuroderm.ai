"""
Storage service for handling image uploads
Supports local storage, AWS S3, and Cloudinary
"""

import os
import uuid
from pathlib import Path
from typing import Optional, BinaryIO
import logging
from datetime import datetime

from fastapi import UploadFile
from PIL import Image
import io

from app.config import settings

logger = logging.getLogger(__name__)


class StorageService:
    """Handle file storage operations"""
    
    def __init__(self):
        self.use_s3 = settings.USE_S3
        self.use_cloudinary = settings.USE_CLOUDINARY
        
        # Initialize appropriate storage backend
        if self.use_s3:
            self._init_s3()
        elif self.use_cloudinary:
            self._init_cloudinary()
        else:
            self._init_local()
    
    def _init_s3(self):
        """Initialize AWS S3 client"""
        try:
            import boto3
            
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            self.bucket_name = settings.AWS_S3_BUCKET
            logger.info("S3 storage initialized")
        except Exception as e:
            logger.error(f"Failed to initialize S3: {e}")
            raise
    
    def _init_cloudinary(self):
        """Initialize Cloudinary"""
        try:
            import cloudinary
            import cloudinary.uploader
            
            cloudinary.config(
                cloud_name=settings.CLOUDINARY_CLOUD_NAME,
                api_key=settings.CLOUDINARY_API_KEY,
                api_secret=settings.CLOUDINARY_API_SECRET
            )
            self.cloudinary = cloudinary
            logger.info("Cloudinary storage initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Cloudinary: {e}")
            raise
    
    def _init_local(self):
        """Initialize local storage"""
        self.upload_dir = settings.UPLOAD_DIR
        self.upload_dir.mkdir(exist_ok=True, parents=True)
        logger.info(f"Local storage initialized at {self.upload_dir}")
    
    async def save_image(
        self,
        file: UploadFile,
        user_id: Optional[int] = None
    ) -> tuple[str, str]:
        """
        Save uploaded image
        
        Args:
            file: Uploaded file
            user_id: Optional user ID
        
        Returns:
            Tuple of (file_url, filename)
        """
        # Validate file
        self._validate_image(file)
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # Read file content
        content = await file.read()
        
        # Process image (resize if needed, convert format)
        processed_image = self._process_image(content)
        
        # Save based on storage backend
        if self.use_s3:
            file_url = await self._save_to_s3(processed_image, unique_filename)
        elif self.use_cloudinary:
            file_url = await self._save_to_cloudinary(processed_image, unique_filename)
        else:
            file_url = await self._save_to_local(processed_image, unique_filename)
        
        logger.info(f"Image saved: {unique_filename}")
        return file_url, unique_filename
    
    def _validate_image(self, file: UploadFile):
        """Validate uploaded image"""
        # Check file extension
        if not file.filename:
            raise ValueError("No filename provided")
        
        file_extension = file.filename.split('.')[-1].lower()
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            raise ValueError(
                f"File type .{file_extension} not allowed. "
                f"Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        # Check content type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise ValueError("File must be an image")
    
    def _process_image(self, content: bytes) -> bytes:
        """
        Process image (resize, optimize)
        
        Args:
            content: Image bytes
        
        Returns:
            Processed image bytes
        """
        try:
            # Open image
            image = Image.open(io.BytesIO(content))
            
            # Convert to RGB if needed
            if image.mode not in ('RGB', 'L'):
                image = image.convert('RGB')
            
            # Resize if too large (max 2048x2048)
            max_size = 2048
            if max(image.size) > max_size:
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Save to bytes
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=90, optimize=True)
            output.seek(0)
            
            return output.read()
            
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            # Return original if processing fails
            return content
    
    async def _save_to_s3(self, content: bytes, filename: str) -> str:
        """Save to AWS S3"""
        try:
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=f"uploads/{filename}",
                Body=content,
                ContentType='image/jpeg',
                ACL='public-read'
            )
            
            # Generate URL
            url = f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/uploads/{filename}"
            return url
            
        except Exception as e:
            logger.error(f"Error uploading to S3: {e}")
            raise
    
    async def _save_to_cloudinary(self, content: bytes, filename: str) -> str:
        """Save to Cloudinary"""
        try:
            result = self.cloudinary.uploader.upload(
                content,
                public_id=filename.split('.')[0],
                folder="neuroderm",
                resource_type="image"
            )
            return result['secure_url']
            
        except Exception as e:
            logger.error(f"Error uploading to Cloudinary: {e}")
            raise
    
    async def _save_to_local(self, content: bytes, filename: str) -> str:
        """Save to local filesystem"""
        try:
            # Create date-based subdirectory
            date_path = datetime.now().strftime("%Y/%m/%d")
            save_dir = self.upload_dir / date_path
            save_dir.mkdir(exist_ok=True, parents=True)
            
            # Save file
            file_path = save_dir / filename
            with open(file_path, 'wb') as f:
                f.write(content)
            
            # Return relative URL
            url = f"/uploads/{date_path}/{filename}"
            return url
            
        except Exception as e:
            logger.error(f"Error saving to local storage: {e}")
            raise
    
    async def delete_image(self, file_url: str):
        """
        Delete image from storage
        
        Args:
            file_url: URL or path of the file to delete
        """
        try:
            if self.use_s3:
                # Extract key from URL
                key = file_url.split('.amazonaws.com/')[-1]
                self.s3_client.delete_object(
                    Bucket=self.bucket_name,
                    Key=key
                )
            elif self.use_cloudinary:
                # Extract public_id from URL
                public_id = file_url.split('/')[-1].split('.')[0]
                self.cloudinary.uploader.destroy(f"neuroderm/{public_id}")
            else:
                # Delete from local storage
                file_path = Path(file_url.lstrip('/'))
                if file_path.exists():
                    file_path.unlink()
            
            logger.info(f"Image deleted: {file_url}")
            
        except Exception as e:
            logger.error(f"Error deleting image: {e}")


# Singleton instance
_storage_service: Optional[StorageService] = None


def get_storage_service() -> StorageService:
    """Get or create storage service instance"""
    global _storage_service
    
    if _storage_service is None:
        _storage_service = StorageService()
    
    return _storage_service