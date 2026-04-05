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

from app.core.ml_service import MLService
from app.services.storage_service import StorageService
from app.core.recommendation_engine import RecommendationEngine
from app.utils.validators import validate_image_file

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/analyze")
async def analyze_skin(
    file: UploadFile = File(...),
    user_notes: Optional[str] = Form(None)
):
    try:
        # Read image
        file_content = await file.read()
        image = Image.open(io.BytesIO(file_content))

        # Use MLService (mock mode will auto work)
        ml_service = MLService()
        ml_results = await ml_service.analyze_image(image)

        return {
            "message": "analysis successful",
            "results": ml_results
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

'''
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
'''