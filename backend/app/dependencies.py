"""
Dependency injection for FastAPI
"""

from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.utils.security import verify_token
from app.core.ml_service import get_ml_service, MLService
from app.services.storage_service import get_storage_service, StorageService
from app.services.cache_service import get_cache_service, CacheService
from app.core.recommendation_engine import get_recommendation_engine, RecommendationEngine

# Security
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get current authenticated user
    
    Args:
        credentials: Bearer token credentials
        db: Database session
    
    Returns:
        User object or None
    """
    if not credentials:
        return None
    
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    return user


async def require_auth(
    user: Optional[User] = Depends(get_current_user)
) -> User:
    """
    Require authentication
    
    Args:
        user: Current user (optional)
    
    Returns:
        User object
    
    Raises:
        HTTPException: If not authenticated
    """
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


# Service dependencies
def get_ml_service_dep() -> MLService:
    """Get ML service dependency"""
    return get_ml_service()


def get_storage_service_dep() -> StorageService:
    """Get storage service dependency"""
    return get_storage_service()


def get_cache_service_dep() -> CacheService:
    """Get cache service dependency"""
    return get_cache_service()


def get_recommendation_engine_dep() -> RecommendationEngine:
    """Get recommendation engine dependency"""
    return get_recommendation_engine()