"""
Metrics calculation and early stopping for NeuroDerm.AI
"""

import torch
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    roc_auc_score,
    hamming_loss,
    classification_report
)
from typing import Dict
from config import config


class MetricsCalculator:
    """Calculate various metrics for multi-label classification"""
    
    def __init__(self, threshold: float = config.CONFIDENCE_THRESHOLD):
        self.threshold = threshold
    
    def calculate_metrics(
        self,
        predictions: torch.Tensor,
        labels: torch.Tensor
    ) -> Dict[str, float]:
        """
        Calculate comprehensive metrics
        
        Args:
            predictions: Predicted probabilities (N, num_classes)
            labels: Ground truth labels (N, num_classes)
        
        Returns:
            Dictionary of metrics
        """
        # Convert to numpy
        pred_probs = predictions.numpy()
        true_labels = labels.numpy()
        
        # Apply threshold to get binary predictions
        pred_binary = (pred_probs >= self.threshold).astype(int)
        
        # Calculate metrics
        metrics = {}
        
        # Hamming Loss (lower is better)
        metrics['hamming_loss'] = hamming_loss(true_labels, pred_binary)
        
        # Subset Accuracy (exact match)
        metrics['subset_accuracy'] = accuracy_score(
            true_labels,
            pred_binary
        )
        
        # Per-sample accuracy
        sample_acc = []
        for i in range(len(true_labels)):
            if true_labels[i].sum() > 0:  # Only if there are positive labels
                acc = (true_labels[i] == pred_binary[i]).mean()
                sample_acc.append(acc)
        metrics['sample_accuracy'] = np.mean(sample_acc) if sample_acc else 0.0
        
        # Precision, Recall, F1 (macro and micro)
        precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
            true_labels,
            pred_binary,
            average='macro',
            zero_division=0
        )
        
        precision_micro, recall_micro, f1_micro, _ = precision_recall_fscore_support(
            true_labels,
            pred_binary,
            average='micro',
            zero_division=0
        )
        
        metrics['precision_macro'] = precision_macro
        metrics['recall_macro'] = recall_macro
        metrics['f1_macro'] = f1_macro
        
        metrics['precision_micro'] = precision_micro
        metrics['recall_micro'] = recall_micro
        metrics['f1_micro'] = f1_micro
        
        # Per-class metrics
        precision_per_class, recall_per_class, f1_per_class, support = \
            precision_recall_fscore_support(
                true_labels,
                pred_binary,
                average=None,
                zero_division=0
            )
        
        for idx, condition in enumerate(config.CONDITIONS):
            metrics[f'{condition}_precision'] = precision_per_class[idx]
            metrics[f'{condition}_recall'] = recall_per_class[idx]
            metrics[f'{condition}_f1'] = f1_per_class[idx]
        
        # ROC AUC (if possible)
        try:
            metrics['roc_auc_macro'] = roc_auc_score(
                true_labels,
                pred_probs,
                average='macro'
            )
            metrics['roc_auc_micro'] = roc_auc_score(
                true_labels,
                pred_probs,
                average='micro'
            )
        except ValueError:
            # Not enough classes present
            metrics['roc_auc_macro'] = 0.0
            metrics['roc_auc_micro'] = 0.0
        
        return metrics
    
    def get_classification_report(
        self,
        predictions: torch.Tensor,
        labels: torch.Tensor
    ) -> str:
        """Get detailed classification report"""
        pred_probs = predictions.numpy()
        true_labels = labels.numpy()
        pred_binary = (pred_probs >= self.threshold).astype(int)
        
        report = classification_report(
            true_labels,
            pred_binary,
            target_names=config.CONDITIONS,
            zero_division=0
        )
        
        return report


class EarlyStopping:
    """Early stopping to prevent overfitting"""
    
    def __init__(
        self,
        patience: int = 5,
        min_delta: float = 0.0,
        verbose: bool = True
    ):
        """
        Args:
            patience: Number of epochs to wait before stopping
            min_delta: Minimum change to qualify as improvement
            verbose: Whether to print messages
        """
        self.patience = patience
        self.min_delta = min_delta
        self.verbose = verbose
        
        self.counter = 0
        self.best_loss = None
        self.early_stop = False
    
    def __call__(self, val_loss: float):
        """Check if should stop"""
        if self.best_loss is None:
            self.best_loss = val_loss
        elif val_loss > self.best_loss - self.min_delta:
            self.counter += 1
            if self.verbose:
                print(f"EarlyStopping counter: {self.counter}/{self.patience}")
            
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_loss = val_loss
            self.counter = 0


if __name__ == "__main__":
    # Test metrics calculation
    calc = MetricsCalculator()
    
    # Create dummy data
    dummy_preds = torch.rand(100, config.NUM_CLASSES)
    dummy_labels = torch.randint(0, 2, (100, config.NUM_CLASSES)).float()
    
    metrics = calc.calculate_metrics(dummy_preds, dummy_labels)
    
    print("Sample Metrics:")
    for key, value in metrics.items():
        if not key.startswith(tuple(config.CONDITIONS)):
            print(f"{key}: {value:.4f}")
    
    print("\nClassification Report:")
    report = calc.get_classification_report(dummy_preds, dummy_labels)
    print(report)