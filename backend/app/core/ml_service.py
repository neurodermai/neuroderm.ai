"""
ML Service for skin analysis inference
"""

import random
from pathlib import Path
from typing import Dict, Union, Optional
import logging

logger = logging.getLogger(__name__)

# Try to import ML dependencies - they may not be installed in dev
try:
    import torch
    import numpy as np
    from PIL import Image as PILImage
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    logger.warning("ML dependencies (torch/numpy) not available. Using mock predictions.")

# Try to import the inference module
SkinAnalyzer = None
if ML_AVAILABLE:
    try:
        import sys
        ML_TRAINING_PATH = Path(__file__).parent.parent.parent.parent / "ml-training" / "src"
        sys.path.insert(0, str(ML_TRAINING_PATH))
        from inference import SkinAnalyzer
    except ImportError:
        logger.warning("SkinAnalyzer not available. Using mock predictions.")

from app.config import settings


class MLService:
    """Service for ML inference operations"""
    
    def __init__(self):
        """Initialize ML service with trained model"""
        self.analyzer = None
        
        if not ML_AVAILABLE:
            logger.warning("ML dependencies not installed. Running in mock mode.")
            return
        
        try:
            logger.info("Initializing ML Service...")
            
            model_path = Path(settings.MODEL_PATH)
            
            if not model_path.exists():
                logger.warning(f"Model not found at {model_path}, using mock predictions")
            elif SkinAnalyzer is not None:
                self.analyzer = SkinAnalyzer(
                    model_path=str(model_path),
                    device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
                )
                logger.info(f"Model loaded successfully from {model_path}")
            
        except Exception as e:
            logger.error(f"Failed to initialize ML Service: {e}")
            self.analyzer = None
    
    async def analyze_image(
        self,
        image,
        return_embeddings: bool = False
    ) -> Dict:
        """
        Analyze skin image
        
        Args:
            image: Input image
            return_embeddings: Whether to return embeddings
        
        Returns:
            Analysis results dictionary
        """
        try:
            if self.analyzer is None:
                # Return mock results for testing
                return self._get_mock_results()
            
            # Run analysis
            result = self.analyzer.analyze_image(
                image,
                return_embeddings=return_embeddings
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error during image analysis: {e}")
            raise
    
    def _get_mock_results(self) -> Dict:
        """Generate mock results for testing when model is not available"""
        mock_conditions = random.sample(settings.CONDITIONS, k=random.randint(1, 3))
        
        detected_conditions = []
        for condition in mock_conditions:
            confidence = round(random.uniform(0.5, 0.95), 3)
            severity_score = int(confidence * 100)
            
            if confidence < 0.6:
                severity = "mild"
            elif confidence < 0.75:
                severity = "moderate"
            else:
                severity = "severe"
            
            detected_conditions.append({
                "condition": condition,
                "confidence": confidence,
                "severity": severity,
                "severity_score": severity_score
            })
        
        return {
            "detected_conditions": detected_conditions,
            "overall_health_score": random.randint(60, 90),
            "primary_concerns": [c["condition"] for c in detected_conditions[:3]],
            "num_conditions_detected": len(detected_conditions),
            "all_probabilities": {
                cond: round(random.uniform(0.1, 0.9), 3)
                for cond in settings.CONDITIONS
            }
        }
    
    async def compare_analyses(
        self,
        result1: Dict,
        result2: Dict
    ) -> Dict:
        """
        Compare two analysis results
        
        Args:
            result1: First analysis result
            result2: Second analysis result
        
        Returns:
            Comparison dictionary
        """
        if self.analyzer is None:
            # Mock comparison
            return {
                "health_score_change": round(random.uniform(-10, 20), 1),
                "conditions_resolved": [],
                "conditions_new": [],
                "conditions_improved": [],
                "conditions_worsened": []
            }
        
        return self.analyzer.compare_analyses(result1, result2)


# Singleton instance
_ml_service_instance: Optional[MLService] = None


def get_ml_service() -> MLService:
    """Get or create ML service instance"""
    global _ml_service_instance
    
    if _ml_service_instance is None:
        _ml_service_instance = MLService()
    
    return _ml_service_instance