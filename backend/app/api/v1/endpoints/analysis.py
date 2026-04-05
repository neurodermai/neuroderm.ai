"""
Skin analysis endpoints
"""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
from typing import Optional
from PIL import Image
import io
import logging

from app.db.database import get_db
from app.db.models import User, SkinAnalysis
from app.db.schemas import AnalysisResponse, AnalysisResult, Recommendations
from app.dependencies import (
    get_current_user,
    get_ml_service_dep,
    get_storage_service_dep,
    get_recommendation_engine_dep
)
from app.core.ml_service import MLService
from app.services.storage_service import StorageService
from app.core.recommendation_engine import RecommendationEngine
from app.utils.validators import validate_image_file

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_skin(
    file: UploadFile = File(..., description="Skin image to analyze"),
    user_notes: Optional[str] = Form(None, description="Optional user notes"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user),
    ml_service: MLService = Depends(get_ml_service_dep),
    storage_service: StorageService = Depends(get_storage_service_dep),
    recommendation_engine: RecommendationEngine = Depends(get_recommendation_engine_dep)
):
    """
    Analyze a skin image and return detailed results with recommendations
    
    - **file**: Image file (JPEG, PNG, HEIC)
    - **user_notes**: Optional notes about the image
    
    Returns comprehensive skin analysis with:
    - Detected conditions and severity
    - Overall health score
    - Personalized recommendations
    """
    try:
        # Validate file
        validate_image_file(file)
        
        logger.info(f"Processing analysis for user: {current_user.id if current_user else 'anonymous'}")
        
        # Save image to storage
        image_url, filename = await storage_service.save_image(
            file,
            user_id=current_user.id if current_user else None
        )
        
        # Convert uploaded file to PIL Image for analysis
        # Need to seek back since storage_service already read the file
        await file.seek(0)
        file_content = await file.read()
        image = Image.open(io.BytesIO(file_content))
        
        # Run ML analysis
        ml_results = await ml_service.analyze_image(image)
        
        # Generate recommendations
        recommendations = recommendation_engine.generate_recommendations(ml_results)
        
        # Save to database
        analysis = SkinAnalysis(
            user_id=current_user.id if current_user else None,
            image_url=image_url,
            image_filename=filename,
            detected_conditions=ml_results['detected_conditions'],
            all_probabilities=ml_results['all_probabilities'],
            overall_score=ml_results['overall_health_score'],
            primary_concerns=ml_results['primary_concerns'],
            recommendations=recommendations,
            user_notes=user_notes
        )
        
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        logger.info(f"Analysis completed: ID={analysis.id}, Score={analysis.overall_score}")
        
        # Build response
        response = AnalysisResponse(
            analysis_id=analysis.id,
            timestamp=analysis.analysis_date,
            image_url=image_url,
            results=AnalysisResult(**ml_results),
            recommendations=Recommendations(**recommendations),
            user_id=current_user.id if current_user else None
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error during analysis: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/result/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis_result(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Get a specific analysis result by ID
    
    - **analysis_id**: ID of the analysis to retrieve
    """
    analysis = db.query(SkinAnalysis).filter(
        SkinAnalysis.id == analysis_id
    ).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    # Check if user has access (only if authenticated)
    if current_user and analysis.user_id and analysis.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Build response
    response = AnalysisResponse(
        analysis_id=analysis.id,
        timestamp=analysis.analysis_date,
        image_url=analysis.image_url,
        results=AnalysisResult(
            detected_conditions=analysis.detected_conditions,
            overall_health_score=analysis.overall_score,
            primary_concerns=analysis.primary_concerns,
            num_conditions_detected=len(analysis.detected_conditions),
            all_probabilities=analysis.all_probabilities
        ),
        recommendations=Recommendations(**analysis.recommendations),
        user_id=analysis.user_id
    )
    
    return response


@router.delete("/result/{analysis_id}")
async def delete_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    storage_service: StorageService = Depends(get_storage_service_dep)
):
    """
    Delete an analysis result
    
    - **analysis_id**: ID of the analysis to delete
    """
    analysis = db.query(SkinAnalysis).filter(
        SkinAnalysis.id == analysis_id,
        SkinAnalysis.user_id == current_user.id
    ).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    # Delete image from storage
    try:
        await storage_service.delete_image(analysis.image_url)
    except Exception as e:
        logger.warning(f"Failed to delete image: {e}")
    
    # Delete from database
    db.delete(analysis)
    db.commit()
    
    return {"message": "Analysis deleted successfully"}