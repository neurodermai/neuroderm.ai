"""
Configuration management for NeuroDerm.AI Backend
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "NeuroDerm.AI"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "sqlite:///./neuroderm.db"
    DATABASE_ECHO: bool = False
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600
    
    # ML Model
    MODEL_PATH: str = "../ml-training/outputs/models/best_model.pth"
    MODEL_NAME: str = "facebook/dinov2-base"
    CONFIDENCE_THRESHOLD: float = 0.5
    HUGGINGFACE_TOKEN: Optional[str] = None
    
    # Storage
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    USE_S3: bool = False
    
    CLOUDINARY_CLOUD_NAME: Optional[str] = None
    CLOUDINARY_API_KEY: Optional[str] = None
    CLOUDINARY_API_SECRET: Optional[str] = None
    USE_CLOUDINARY: bool = False
    
    # Local storage fallback
    UPLOAD_DIR: Path = Path("uploads")
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001"
    ]
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "heic"]
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # seconds
    
    # Skin Conditions
    CONDITIONS: List[str] = [
        "acne",
        "redness",
        "dryness",
        "oiliness",
        "aging_signs",
        "dark_spots",
        "texture_issues",
        "healthy"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

# Create upload directory if using local storage
if not settings.USE_S3 and not settings.USE_CLOUDINARY:
    settings.UPLOAD_DIR.mkdir(exist_ok=True, parents=True)