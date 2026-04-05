"""
Analysis history endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime, timedelta

from app.db.database import get_db
from app.db.models import User, SkinAnalysis, AnalysisComparison
from app.db.schemas import AnalysisHistory, ComparisonResponse, ComparisonResult
from app.dependencies import require_auth, get_ml_service_dep
from app.core.ml_service import MLService

router = APIRouter()


@router.get("/", response_model=List[AnalysisHistory])
async def get_user_history(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """
    Get user's analysis history
    
    - **limit**: Number of results to return (max 100)
    - **offset**: Number of results to skip
    
    Requires authentication
    """
    analyses = db.query(SkinAnalysis).filter(
        SkinAnalysis.user_id == current_user.id
    ).order_by(
        desc(SkinAnalysis.analysis_date)
    ).limit(limit).offset(offset).all()
    
    return analyses


@router.get("/stats")
async def get_user_stats(
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """
    Get user's analysis statistics
    
    Requires authentication
    """
    analyses = db.query(SkinAnalysis).filter(
        SkinAnalysis.user_id == current_user.id
    ).order_by(SkinAnalysis.analysis_date).all()
    
    if not analyses:
        return {
            "total_analyses": 0,
            "average_health_score": 0,
            "trend": "no_data",
            "most_common_conditions": [],
            "improvement_rate": 0
        }
    
    # Calculate statistics
    total = len(analyses)
    avg_score = sum(a.overall_score for a in analyses) / total
    
    # Calculate trend (last 3 vs first 3)
    if total >= 6:
        first_three_avg = sum(a.overall_score for a in analyses[:3]) / 3
        last_three_avg = sum(a.overall_score for a in analyses[-3:]) / 3
        
        if last_three_avg > first_three_avg + 5:
            trend = "improving"
        elif last_three_avg < first_three_avg - 5:
            trend = "declining"
        else:
            trend = "stable"
    else:
        trend = "insufficient_data"
    
    # Most common conditions
    condition_counts = {}
    for analysis in analyses:
        for condition in analysis.primary_concerns:
            condition_counts[condition] = condition_counts.get(condition, 0) + 1
    
    most_common = sorted(
        condition_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]
    
    # Improvement rate
    if total >= 2:
        first_score = analyses[0].overall_score
        last_score = analyses[-1].overall_score
        improvement_rate = ((last_score - first_score) / first_score) * 100
    else:
        improvement_rate = 0
    
    return {
        "total_analyses": total,
        "average_health_score": round(avg_score, 1),
        "trend": trend,
        "most_common_conditions": [
            {"condition": cond, "count": count}
            for cond, count in most_common
        ],
        "improvement_rate": round(improvement_rate, 1),
        "first_analysis_date": analyses[0].analysis_date,
        "last_analysis_date": analyses[-1].analysis_date
    }


@router.get("/timeline")
async def get_health_timeline(
    days: int = Query(default=30, ge=7, le=365),
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """
    Get health score timeline for charting
    
    - **days**: Number of days to include (7-365)
    
    Requires authentication
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    analyses = db.query(SkinAnalysis).filter(
        SkinAnalysis.user_id == current_user.id,
        SkinAnalysis.analysis_date >= cutoff_date
    ).order_by(SkinAnalysis.analysis_date).all()
    
    timeline = [
        {
            "date": analysis.analysis_date.isoformat(),
            "health_score": analysis.overall_score,
            "conditions_count": len(analysis.detected_conditions)
        }
        for analysis in analyses
    ]
    
    return {
        "period_days": days,
        "data_points": len(timeline),
        "timeline": timeline
    }


@router.post("/compare/{analysis_id_1}/{analysis_id_2}", response_model=ComparisonResponse)
async def compare_analyses(
    analysis_id_1: int,
    analysis_id_2: int,
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db),
    ml_service: MLService = Depends(get_ml_service_dep)
):
    """
    Compare two analysis results to track progress
    
    - **analysis_id_1**: First analysis ID (typically older)
    - **analysis_id_2**: Second analysis ID (typically newer)
    
    Requires authentication
    """
    # Get both analyses
    analysis_1 = db.query(SkinAnalysis).filter(
        SkinAnalysis.id == analysis_id_1,
        SkinAnalysis.user_id == current_user.id
    ).first()
    
    analysis_2 = db.query(SkinAnalysis).filter(
        SkinAnalysis.id == analysis_id_2,
        SkinAnalysis.user_id == current_user.id
    ).first()
    
    if not analysis_1 or not analysis_2:
        raise HTTPException(status_code=404, detail="One or both analyses not found")
    
    # Ensure analysis_1 is older
    if analysis_1.analysis_date > analysis_2.analysis_date:
        analysis_1, analysis_2 = analysis_2, analysis_1
    
    # Calculate time difference
    time_diff = (analysis_2.analysis_date - analysis_1.analysis_date).days
    
    # Build result dictionaries for comparison
    result_1 = {
        "detected_conditions": analysis_1.detected_conditions,
        "overall_health_score": analysis_1.overall_score,
        "primary_concerns": analysis_1.primary_concerns
    }
    
    result_2 = {
        "detected_conditions": analysis_2.detected_conditions,
        "overall_health_score": analysis_2.overall_score,
        "primary_concerns": analysis_2.primary_concerns
    }
    
    # Use ML service to compare
    comparison_data = await ml_service.compare_analyses(result_1, result_2)
    
    # Calculate improvement percentage
    if analysis_1.overall_score > 0:
        improvement_pct = (
            (analysis_2.overall_score - analysis_1.overall_score) / 
            analysis_1.overall_score
        ) * 100
    else:
        improvement_pct = 0
    
    # Create comparison result
    comparison_result = ComparisonResult(
        health_score_change=analysis_2.overall_score - analysis_1.overall_score,
        conditions_resolved=comparison_data.get('conditions_resolved', []),
        conditions_new=comparison_data.get('conditions_new', []),
        conditions_improved=comparison_data.get('conditions_improved', []),
        conditions_worsened=comparison_data.get('conditions_worsened', []),
        improvement_percentage=round(improvement_pct, 1),
        time_between_analyses=time_diff
    )
    
    # Save comparison
    comparison = AnalysisComparison(
        user_id=current_user.id,
        analysis_1_id=analysis_1.id,
        analysis_2_id=analysis_2.id,
        health_score_change=comparison_result.health_score_change,
        comparison_data=comparison_data
    )
    
    db.add(comparison)
    db.commit()
    db.refresh(comparison)
    
    # Build response
    response = ComparisonResponse(
        comparison_id=comparison.id,
        analysis_1=AnalysisHistory(
            id=analysis_1.id,
            analysis_date=analysis_1.analysis_date,
            overall_score=analysis_1.overall_score,
            primary_concerns=analysis_1.primary_concerns,
            image_url=analysis_1.image_url
        ),
        analysis_2=AnalysisHistory(
            id=analysis_2.id,
            analysis_date=analysis_2.analysis_date,
            overall_score=analysis_2.overall_score,
            primary_concerns=analysis_2.primary_concerns,
            image_url=analysis_2.image_url
        ),
        comparison=comparison_result,
        compared_at=comparison.compared_at
    )
    
    return response