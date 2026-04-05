"""
Model architecture for NeuroDerm.AI
Fine-tuned DINOv2 for skin condition classification
"""

import torch
import torch.nn as nn
from transformers import Dinov2Model, Dinov2Config
from typing import Dict, Optional
from config import config


class SkinConditionClassifier(nn.Module):
    """
    DINOv2-based multi-label skin condition classifier
    """
    
    def __init__(
        self,
        model_name: str = config.MODEL_NAME,
        num_classes: int = config.NUM_CLASSES,
        dropout_rate: float = 0.1,
        freeze_backbone: bool = False
    ):
        """
        Args:
            model_name: HuggingFace model name
            num_classes: Number of skin conditions to classify
            dropout_rate: Dropout rate for regularization
            freeze_backbone: Whether to freeze DINOv2 backbone
        """
        super(SkinConditionClassifier, self).__init__()
        
        self.num_classes = num_classes
        
        # Load pretrained DINOv2
        print(f"Loading {model_name}...")
        self.dinov2 = Dinov2Model.from_pretrained(model_name)
        
        # Get embedding dimension
        self.embedding_dim = self.dinov2.config.hidden_size
        
        # Freeze backbone if specified
        if freeze_backbone:
            print("Freezing DINOv2 backbone...")
            for param in self.dinov2.parameters():
                param.requires_grad = False
        
        # Classification head
        self.classifier = nn.Sequential(
            nn.LayerNorm(self.embedding_dim),
            nn.Dropout(dropout_rate),
            nn.Linear(self.embedding_dim, 512),
            nn.GELU(),
            nn.Dropout(dropout_rate),
            nn.Linear(512, 256),
            nn.GELU(),
            nn.Dropout(dropout_rate),
            nn.Linear(256, num_classes)
        )
        
        # Initialize classification head weights
        self._initialize_weights()
    
    def _initialize_weights(self):
        """Initialize the classification head weights"""
        for module in self.classifier.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
    
    def forward(
        self,
        pixel_values: torch.Tensor,
        return_embeddings: bool = False
    ) -> Dict[str, torch.Tensor]:
        """
        Forward pass
        
        Args:
            pixel_values: Input images (B, C, H, W)
            return_embeddings: Whether to return embeddings
        
        Returns:
            Dictionary with logits and optionally embeddings
        """
        # Get DINOv2 embeddings
        outputs = self.dinov2(pixel_values)
        
        # Use [CLS] token embedding
        embeddings = outputs.last_hidden_state[:, 0, :]
        
        # Classification
        logits = self.classifier(embeddings)
        
        result = {'logits': logits}
        
        if return_embeddings:
            result['embeddings'] = embeddings
        
        return result
    
    def get_embeddings(self, pixel_values: torch.Tensor) -> torch.Tensor:
        """Extract embeddings without classification"""
        with torch.no_grad():
            outputs = self.dinov2(pixel_values)
            embeddings = outputs.last_hidden_state[:, 0, :]
        return embeddings


class ModelWithLoss(nn.Module):
    """
    Wrapper that combines model and loss function
    """
    
    def __init__(
        self,
        model: SkinConditionClassifier,
        pos_weight: Optional[torch.Tensor] = None
    ):
        """
        Args:
            model: The base classifier model
            pos_weight: Positive class weights for imbalanced data
        """
        super(ModelWithLoss, self).__init__()
        self.model = model
        
        # Binary Cross Entropy with Logits for multi-label
        self.criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    
    def forward(
        self,
        pixel_values: torch.Tensor,
        labels: Optional[torch.Tensor] = None
    ) -> Dict[str, torch.Tensor]:
        """
        Forward pass with loss calculation
        """
        outputs = self.model(pixel_values)
        
        result = {
            'logits': outputs['logits'],
            'probabilities': torch.sigmoid(outputs['logits'])
        }
        
        if labels is not None:
            loss = self.criterion(outputs['logits'], labels)
            result['loss'] = loss
        
        return result


def create_model(
    freeze_backbone: bool = False,
    pos_weight: Optional[torch.Tensor] = None
) -> ModelWithLoss:
    """
    Factory function to create the complete model
    
    Args:
        freeze_backbone: Whether to freeze DINOv2
        pos_weight: Positive class weights
    
    Returns:
        ModelWithLoss instance
    """
    base_model = SkinConditionClassifier(
        model_name=config.MODEL_NAME,
        num_classes=config.NUM_CLASSES,
        freeze_backbone=freeze_backbone
    )
    
    model = ModelWithLoss(base_model, pos_weight=pos_weight)
    
    return model


def count_parameters(model: nn.Module) -> Dict[str, int]:
    """Count model parameters"""
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    return {
        'total': total_params,
        'trainable': trainable_params,
        'frozen': total_params - trainable_params
    }


if __name__ == "__main__":
    # Test model creation
    print("Creating model...")
    model = create_model(freeze_backbone=False)
    
    # Count parameters
    params = count_parameters(model)
    print(f"\nModel parameters:")
    print(f"Total: {params['total']:,}")
    print(f"Trainable: {params['trainable']:,}")
    print(f"Frozen: {params['frozen']:,}")
    
    # Test forward pass
    dummy_input = torch.randn(2, 3, config.IMAGE_SIZE, config.IMAGE_SIZE)
    dummy_labels = torch.randint(0, 2, (2, config.NUM_CLASSES)).float()
    
    model.eval()
    with torch.no_grad():
        outputs = model(dummy_input, dummy_labels)
    
    print(f"\nTest forward pass:")
    print(f"Logits shape: {outputs['logits'].shape}")
    print(f"Probabilities shape: {outputs['probabilities'].shape}")
    print(f"Loss: {outputs['loss'].item():.4f}")