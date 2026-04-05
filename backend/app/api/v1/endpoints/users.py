"""
User management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.database import get_db
from app.db.models import User
from app.db.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    Token
)
from app.dependencies import get_current_user, require_auth
from app.utils.security import (
    verify_password,
    get_password_hash,
    create_access_token
)
from app.utils.validators import validate_skin_type
from app.config import settings

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    
    - **email**: Valid email address
    - **password**: Minimum 8 characters
    - **full_name**: Optional full name
    - **skin_type**: Optional skin type (oily, dry, combination, normal)
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate skin type
    if user_data.skin_type:
        validate_skin_type(user_data.skin_type)
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        skin_type=user_data.skin_type,
        age=user_data.age,
        concerns=user_data.concerns
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login and receive access token
    
    - **email**: User email
    - **password**: User password
    """
    # Find user
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(require_auth)
):
    """
    Get current user information
    
    Requires authentication
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """
    Update current user information
    
    Requires authentication
    """
    # Validate skin type if provided
    if user_update.skin_type:
        validate_skin_type(user_update.skin_type)
    
    # Update fields
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    if user_update.skin_type is not None:
        current_user.skin_type = user_update.skin_type
    if user_update.age is not None:
        current_user.age = user_update.age
    if user_update.concerns is not None:
        current_user.concerns = user_update.concerns
    
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.delete("/me")
async def delete_current_user(
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """
    Delete current user account
    
    Requires authentication
    WARNING: This will delete all user data including analysis history
    """
    db.delete(current_user)
    db.commit()
    
    return {"message": "User account deleted successfully"}