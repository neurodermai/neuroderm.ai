"""
Inference pipeline for NeuroDerm.AI
"""

import torch
import torch.nn as nn
from PIL import Image
import numpy as np
from typing import Dict, List, Union, Optional
from pathlib import Path
import albumentations as A
from albumentations.pytorch import ToTensorV2

from config import config
from model import SkinConditionClassifier


class SkinAnalyzer:
    """Production inference class for skin analysis"""
    
    def __init__(
        self,
        model_path: Optional[str] = None,
        device: Optional[torch.device] = None
    ):
        """
        Args:
            model_path: Path to trained model checkpoint
            device: Device to run inference on
        """
        self.device = device if device else config.DEVICE
        self.threshold = config.CONFIDENCE_THRESHOLD
        
        # Load model
        self.model = self._load_model(model_path)
        self.model.eval()
        
        # Preprocessing pipeline
        self.transform = self._get_transform()
    
    def _load_model(self, model_path: Optional[str]) -> nn.Module:
        """Load trained model"""
        if model_path is None:
            model_path = config.MODEL_DIR / 'best_model.pth'
        
        print(f"Loading model from {model_path}...")
        
        # Create model
        model = SkinConditionClassifier(
            model_name=config.MODEL_NAME,
            num_classes=config.NUM_CLASSES
        )
        
        # Load checkpoint
        checkpoint = torch.load(model_path, map_location=self.device)
        
        # Load state dict (handle nested model structure)
        if 'model_state_dict' in checkpoint:
            state_dict = checkpoint['model_state_dict']
            # Remove 'model.' prefix if present
            new_state_dict = {}
            for k, v in state_dict.items():
                new_key = k.replace('model.', '') if k.startswith('model.') else k
                new_state_dict[new_key] = v
            model.load_state_dict(new_state_dict)
        else:
            model.load_state_dict(checkpoint)
        
        model.to(self.device)
        
        print("Model loaded successfully!")
        return model
    
    def _get_transform(self):
        """Get preprocessing transform"""
        return A.Compose([
            A.Resize(config.IMAGE_SIZE, config.IMAGE_SIZE),
            A.Normalize(
                mean=config.IMAGENET_MEAN,
                std=config.IMAGENET_STD
            ),
            ToTensorV2()
        ])
    
    def preprocess_image(
        self,
        image: Union[str, Path, Image.Image, np.ndarray]
    ) -> torch.Tensor:
        """
        Preprocess image for inference
        
        Args:
            image: Input image (path, PIL Image, or numpy array)
        
        Returns:
            Preprocessed tensor
        """
        # Load image if path is provided
        if isinstance(image, (str, Path)):
            image = Image.open(image).convert('RGB')
        elif isinstance(image, Image.Image):
            image = image.convert('RGB')
        
        # Convert to numpy array
        image = np.array(image)
        
        # Apply transforms
        transformed = self.transform(image=image)
        image_tensor = transformed['image']
        
        # Add batch dimension
        image_tensor = image_tensor.unsqueeze(0)
        
        return image_tensor
    
    def analyze_image(
        self,
        image: Union[str, Path, Image.Image, np.ndarray],
        return_embeddings: bool = False
    ) -> Dict:
        """
        Analyze skin image and return detailed results
        
        Args:
            image: Input image
            return_embeddings: Whether to return embeddings
        
        Returns:
            Dictionary with analysis results
        """
        # Preprocess
        image_tensor = self.preprocess_image(image).to(self.device)
        
        # Inference
        with torch.no_grad():
            outputs = self.model(image_tensor, return_embeddings=return_embeddings)
            probabilities = torch.sigmoid(outputs['logits']).cpu().numpy()[0]
        
        # Process results
        detected_conditions = []
        
        for idx, prob in enumerate(probabilities):
            if prob >= self.threshold:
                condition = config.CONDITIONS[idx]
                severity, severity_score = self._calculate_severity(prob)
                
                detected_conditions.append({
                    'condition': condition,
                    'confidence': float(prob),
                    'severity': severity,
                    'severity_score': severity_score
                })
        
        # Sort by confidence
        detected_conditions.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Calculate overall skin health score
        overall_score = self._calculate_overall_health_score(probabilities)
        
        # Determine primary concerns (top 3)
        primary_concerns = [
            cond['condition'] for cond in detected_conditions[:3]
        ]
        
        # Build result
        result = {
            'detected_conditions': detected_conditions,
            'overall_health_score': overall_score,
            'primary_concerns': primary_concerns,
            'num_conditions_detected': len(detected_conditions),
            'all_probabilities': {
                config.CONDITIONS[i]: float(probabilities[i])
                for i in range(len(config.CONDITIONS))
            }
        }
        
        if return_embeddings and 'embeddings' in outputs:
            result['embeddings'] = outputs['embeddings'].cpu().numpy()[0].tolist()
        
        return result
    
    def _calculate_severity(self, confidence: float) -> tuple:
        """
        Calculate severity level and score
        
        Args:
            confidence: Confidence score (0-1)
        
        Returns:
            (severity_level, severity_score)
        """
        # Convert confidence to 0-100 scale
        severity_score = int(confidence * 100)
        
        # Determine severity level
        if confidence < 0.3:
            severity = "minimal"
        elif confidence < 0.5:
            severity = "mild"
        elif confidence < 0.7:
            severity = "moderate"
        else:
            severity = "severe"
        
        return severity, severity_score
    
    def _calculate_overall_health_score(
        self,
        probabilities: np.ndarray
    ) -> int:
        """
        Calculate overall skin health score (0-100)
        Higher is better
        
        Args:
            probabilities: Predicted probabilities for all conditions
        
        Returns:
            Health score (0-100)
        """
        # Check if "healthy" is detected with high confidence
        healthy_idx = config.CONDITION_TO_IDX.get('healthy', -1)
        
        if healthy_idx >= 0:
            healthy_score = probabilities[healthy_idx]
        else:
            healthy_score = 0
        
        # Calculate negative impact from other conditions
        negative_conditions = [
            prob for idx, prob in enumerate(probabilities)
            if idx != healthy_idx and prob >= self.threshold
        ]
        
        if negative_conditions:
            avg_negative = np.mean(negative_conditions)
            # Health score inversely proportional to negative conditions
            health_score = max(0, 100 - int(avg_negative * 100))
        else:
            # High score if no issues detected
            health_score = min(100, 80 + int(healthy_score * 20))
        
        return health_score
    
    def batch_analyze(
        self,
        images: List[Union[str, Path, Image.Image]],
        batch_size: int = 8
    ) -> List[Dict]:
        """
        Analyze multiple images in batches
        
        Args:
            images: List of images
            batch_size: Batch size for inference
        
        Returns:
            List of analysis results
        """
        results = []
        
        for i in range(0, len(images), batch_size):
            batch_images = images[i:i + batch_size]
            
            for image in batch_images:
                result = self.analyze_image(image)
                results.append(result)
        
        return results
    
    def compare_analyses(
        self,
        result1: Dict,
        result2: Dict
    ) -> Dict:
        """
        Compare two analysis results to show progress
        
        Args:
            result1: First analysis result
            result2: Second analysis result
        
        Returns:
            Comparison dictionary
        """
        comparison = {
            'health_score_change': result2['overall_health_score'] - result1['overall_health_score'],
            'conditions_resolved': [],
            'conditions_new': [],
            'conditions_improved': [],
            'conditions_worsened': []
        }
        
        # Get condition names from both results
        conditions1 = {c['condition']: c for c in result1['detected_conditions']}
        conditions2 = {c['condition']: c for c in result2['detected_conditions']}
        
        # Find resolved conditions
        for cond in conditions1:
            if cond not in conditions2:
                comparison['conditions_resolved'].append(cond)
        
        # Find new conditions
        for cond in conditions2:
            if cond not in conditions1:
                comparison['conditions_new'].append(cond)
        
        # Find improved/worsened
        for cond in conditions1:
            if cond in conditions2:
                conf_change = conditions2[cond]['confidence'] - conditions1[cond]['confidence']
                if conf_change < -0.1:  # Improved (lower confidence)
                    comparison['conditions_improved'].append({
                        'condition': cond,
                        'improvement': abs(conf_change)
                    })
                elif conf_change > 0.1:  # Worsened
                    comparison['conditions_worsened'].append({
                        'condition': cond,
                        'worsening': conf_change
                    })
        
        return comparison


def export_to_huggingface(
    model_path: str,
    repo_name: str = "neuroderm-dinov2-skin-analyzer",
    token: Optional[str] = None
):
    """
    Export model to HuggingFace Hub - Simplified version
    """
    print("HuggingFace export feature - not implemented in this version")
    return None