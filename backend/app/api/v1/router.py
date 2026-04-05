"""
API v1 router aggregation
"""

from fastapi import APIRouter

from app.api.v1.endpoints import analysis, users, history, recommendations

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    analysis.router,
    prefix="/analysis",
    tags=["Analysis"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

api_router.include_router(
    history.router,
    prefix="/history",
    tags=["History"]
)

api_router.include_router(
    recommendations.router,
    prefix="/recommendations",
    tags=["Recommendations"]
)