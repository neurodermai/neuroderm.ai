"""
SQLAlchemy ORM models for NeuroDerm.AI
"""

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Text,
    ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    skin_type = Column(String(50), nullable=True)
    age = Column(Integer, nullable=True)
    concerns = Column(JSON, nullable=True)  # List of skin concerns
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    analyses = relationship("SkinAnalysis", back_populates="user", cascade="all, delete-orphan")
    comparisons = relationship("AnalysisComparison", back_populates="user", cascade="all, delete-orphan")


class SkinAnalysis(Base):
    """Skin analysis result model"""
    __tablename__ = "skin_analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    image_url = Column(String(512), nullable=False)
    image_filename = Column(String(255), nullable=False)
    detected_conditions = Column(JSON, nullable=False)  # List of detected conditions
    all_probabilities = Column(JSON, nullable=True)  # All condition probabilities
    overall_score = Column(Float, nullable=False)
    primary_concerns = Column(JSON, nullable=True)  # List of primary concerns
    recommendations = Column(JSON, nullable=True)  # Recommendations dict
    user_notes = Column(Text, nullable=True)
    analysis_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="analyses")


class AnalysisComparison(Base):
    """Comparison between two analyses"""
    __tablename__ = "analysis_comparisons"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    analysis_1_id = Column(Integer, ForeignKey("skin_analyses.id"), nullable=False)
    analysis_2_id = Column(Integer, ForeignKey("skin_analyses.id"), nullable=False)
    health_score_change = Column(Float, nullable=True)
    comparison_data = Column(JSON, nullable=True)
    compared_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="comparisons")
    analysis_1 = relationship("SkinAnalysis", foreign_keys=[analysis_1_id])
    analysis_2 = relationship("SkinAnalysis", foreign_keys=[analysis_2_id])


class ConditionInfo(Base):
    """Condition information for the knowledge base"""
    __tablename__ = "condition_info"

    id = Column(Integer, primary_key=True, index=True)
    condition_name = Column(String(100), unique=True, index=True, nullable=False)
    display_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    causes = Column(JSON, nullable=False)  # List of causes
    symptoms = Column(JSON, nullable=False)  # List of symptoms
    immediate_actions = Column(JSON, nullable=False)  # List of actions
    skincare_tips = Column(JSON, nullable=False)  # List of tips
    lifestyle_tips = Column(JSON, nullable=False)  # List of tips
    product_categories = Column(JSON, nullable=False)  # List of categories
    when_to_see_doctor = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
