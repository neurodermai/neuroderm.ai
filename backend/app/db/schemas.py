"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    skin_type: Optional[str] = None
    age: Optional[int] = None
    concerns: Optional[List[str]] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    skin_type: Optional[str] = None
    age: Optional[int] = None
    concerns: Optional[List[str]] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Skin Analysis Schemas
class ConditionDetection(BaseModel):
    condition: str
    confidence: float = Field(..., ge=0, le=1)
    severity: str
    severity_score: int = Field(..., ge=0, le=100)


class AnalysisResult(BaseModel):
    detected_conditions: List[ConditionDetection]
    overall_health_score: int = Field(..., ge=0, le=100)
    primary_concerns: List[str]
    num_conditions_detected: int
    all_probabilities: Dict[str, float]


class RecommendationItem(BaseModel):
    title: str
    description: str
    priority: str = "medium"  # low, medium, high


class Recommendations(BaseModel):
    immediate_actions: List[RecommendationItem]
    skincare_routine: Dict[str, List[str]]  # morning, evening
    lifestyle_tips: List[RecommendationItem]
    product_categories: List[str]
    when_to_see_doctor: Optional[str] = None


class AnalysisResponse(BaseModel):
    analysis_id: int
    timestamp: datetime
    image_url: str
    results: AnalysisResult
    recommendations: Recommendations
    user_id: Optional[int] = None


class AnalysisCreate(BaseModel):
    user_id: Optional[int] = None
    user_notes: Optional[str] = None


class AnalysisHistory(BaseModel):
    id: int
    analysis_date: datetime
    overall_score: float
    primary_concerns: List[str]
    image_url: str
    
    class Config:
        from_attributes = True


# Comparison Schemas
class ComparisonResult(BaseModel):
    health_score_change: float
    conditions_resolved: List[str]
    conditions_new: List[str]
    conditions_improved: List[Dict[str, Any]]
    conditions_worsened: List[Dict[str, Any]]
    improvement_percentage: float
    time_between_analyses: int  # days


class ComparisonResponse(BaseModel):
    comparison_id: int
    analysis_1: AnalysisHistory
    analysis_2: AnalysisHistory
    comparison: ComparisonResult
    compared_at: datetime


# Condition Info Schemas
class ConditionInfoResponse(BaseModel):
    condition_name: str
    display_name: str
    description: str
    causes: List[str]
    symptoms: List[str]
    immediate_actions: List[str]
    skincare_tips: List[str]
    lifestyle_tips: List[str]
    product_categories: List[str]
    when_to_see_doctor: Optional[str]
    
    class Config:
        from_attributes = True


# Error Response
class ErrorResponse(BaseModel):
    detail: str
    message: Optional[str] = None
    error_code: Optional[str] = None