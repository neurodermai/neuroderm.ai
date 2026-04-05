"""
Training script for NeuroDerm.AI
"""

import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.cuda.amp import autocast, GradScaler
from tqdm import tqdm
import numpy as np
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Optional
import warnings
warnings.filterwarnings('ignore')

from config import config
from model import create_model, count_parameters
from dataset import DatasetPreprocessor, get_dataloaders
from metrics import MetricsCalculator, EarlyStopping


class Trainer:
    """Training pipeline for skin condition classifier"""
    
    def __init__(
        self,
        model: nn.Module,
        dataloaders: Dict,
        optimizer: torch.optim.Optimizer,
        scheduler: Optional[torch.optim.lr_scheduler._LRScheduler] = None,
        device: torch.device = config.DEVICE
    ):
        self.model = model.to(device)
        self.dataloaders = dataloaders
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.device = device
        
        # Mixed precision training
        self.scaler = GradScaler() if config.MIXED_PRECISION else None
        
        # Metrics
        self.metrics_calc = MetricsCalculator()
        
        # Early stopping
        self.early_stopping = EarlyStopping(
            patience=config.EARLY_STOPPING_PATIENCE,
            verbose=True
        )
        
        # Training history
        self.history = {
            'train_loss': [],
            'val_loss': [],
            'train_metrics': [],
            'val_metrics': [],
            'learning_rates': []
        }
        
        # Best model tracking
        self.best_val_loss = float('inf')
        self.best_epoch = 0
    
    def train_epoch(self, epoch: int) -> Dict:
        """Train for one epoch"""
        self.model.train()
        
        running_loss = 0.0
        all_predictions = []
        all_labels = []
        
        pbar = tqdm(
            self.dataloaders['train'],
            desc=f"Epoch {epoch}/{config.NUM_EPOCHS} [Train]"
        )
        
        for batch_idx, batch in enumerate(pbar):
            images = batch['image'].to(self.device)
            labels = batch['labels'].to(self.device)
            
            # Zero gradients
            self.optimizer.zero_grad()
            
            # Forward pass with mixed precision
            if config.MIXED_PRECISION:
                with autocast():
                    outputs = self.model(images, labels)
                    loss = outputs['loss']
                
                # Backward pass
                self.scaler.scale(loss).backward()
                self.scaler.unscale_(self.optimizer)
                torch.nn.utils.clip_grad_norm_(
                    self.model.parameters(),
                    config.MAX_GRAD_NORM
                )
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                outputs = self.model(images, labels)
                loss = outputs['loss']
                
                # Backward pass
                loss.backward()
                torch.nn.utils.clip_grad_norm_(
                    self.model.parameters(),
                    config.MAX_GRAD_NORM
                )
                self.optimizer.step()
            
            # Track metrics
            running_loss += loss.item()
            all_predictions.append(outputs['probabilities'].detach().cpu())
            all_labels.append(labels.detach().cpu())
            
            # Update progress bar
            pbar.set_postfix({'loss': loss.item()})
        
        # Calculate epoch metrics
        avg_loss = running_loss / len(self.dataloaders['train'])
        all_predictions = torch.cat(all_predictions, dim=0)
        all_labels = torch.cat(all_labels, dim=0)
        
        metrics = self.metrics_calc.calculate_metrics(
            all_predictions,
            all_labels
        )
        
        return {
            'loss': avg_loss,
            'metrics': metrics
        }
    
    def validate(self, epoch: int) -> Dict:
        """Validate the model"""
        self.model.eval()
        
        running_loss = 0.0
        all_predictions = []
        all_labels = []
        
        pbar = tqdm(
            self.dataloaders['val'],
            desc=f"Epoch {epoch}/{config.NUM_EPOCHS} [Val]"
        )
        
        with torch.no_grad():
            for batch in pbar:
                images = batch['image'].to(self.device)
                labels = batch['labels'].to(self.device)
                
                outputs = self.model(images, labels)
                loss = outputs['loss']
                
                running_loss += loss.item()
                all_predictions.append(outputs['probabilities'].cpu())
                all_labels.append(labels.cpu())
                
                pbar.set_postfix({'loss': loss.item()})
        
        # Calculate metrics
        avg_loss = running_loss / len(self.dataloaders['val'])
        all_predictions = torch.cat(all_predictions, dim=0)
        all_labels = torch.cat(all_labels, dim=0)
        
        metrics = self.metrics_calc.calculate_metrics(
            all_predictions,
            all_labels
        )
        
        return {
            'loss': avg_loss,
            'metrics': metrics
        }
    
    def train(self):
        """Full training loop"""
        print("=" * 60)
        print("Starting Training")
        print("=" * 60)
        
        for epoch in range(1, config.NUM_EPOCHS + 1):
            # Train
            train_results = self.train_epoch(epoch)
            
            # Validate
            val_results = self.validate(epoch)
            
            # Update learning rate
            if self.scheduler is not None:
                self.scheduler.step()
                current_lr = self.scheduler.get_last_lr()[0]
            else:
                current_lr = config.LEARNING_RATE
            
            # Store history
            self.history['train_loss'].append(train_results['loss'])
            self.history['val_loss'].append(val_results['loss'])
            self.history['train_metrics'].append(train_results['metrics'])
            self.history['val_metrics'].append(val_results['metrics'])
            self.history['learning_rates'].append(current_lr)
            
            # Print epoch summary
            print(f"\nEpoch {epoch} Summary:")
            print(f"Train Loss: {train_results['loss']:.4f} | "
                  f"Val Loss: {val_results['loss']:.4f}")
            print(f"Train F1: {train_results['metrics']['f1_macro']:.4f} | "
                  f"Val F1: {val_results['metrics']['f1_macro']:.4f}")
            print(f"Learning Rate: {current_lr:.6f}")
            
            # Save best model
            if val_results['loss'] < self.best_val_loss:
                self.best_val_loss = val_results['loss']
                self.best_epoch = epoch
                self.save_checkpoint(epoch, is_best=True)
                print(f"✓ New best model saved! (Val Loss: {val_results['loss']:.4f})")
            
            # Regular checkpoint
            if epoch % config.SAVE_FREQUENCY == 0:
                self.save_checkpoint(epoch, is_best=False)
            
            # Early stopping
            self.early_stopping(val_results['loss'])
            if self.early_stopping.early_stop:
                print(f"\nEarly stopping triggered at epoch {epoch}")
                break
            
            print("-" * 60)
        
        # Save training history
        self.save_history()
        
        print("\n" + "=" * 60)
        print("Training Completed!")
        print(f"Best model from epoch {self.best_epoch} "
              f"with Val Loss: {self.best_val_loss:.4f}")
        print("=" * 60)
    
    def save_checkpoint(self, epoch: int, is_best: bool = False):
        """Save model checkpoint"""
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict() if self.scheduler else None,
            'best_val_loss': self.best_val_loss,
            'history': self.history,
            'config': {
                'num_classes': config.NUM_CLASSES,
                'conditions': config.CONDITIONS,
                'image_size': config.IMAGE_SIZE
            }
        }
        
        if is_best:
            path = config.MODEL_DIR / 'best_model.pth'
        else:
            path = config.MODEL_DIR / f'checkpoint_epoch_{epoch}.pth'
        
        torch.save(checkpoint, path)
    
    def save_history(self):
        """Save training history"""
        history_path = config.LOGS_DIR / 'training_history.json'
        
        # Convert to serializable format
        serializable_history = {
            'train_loss': self.history['train_loss'],
            'val_loss': self.history['val_loss'],
            'learning_rates': self.history['learning_rates'],
            'best_epoch': self.best_epoch,
            'best_val_loss': self.best_val_loss
        }
        
        with open(history_path, 'w') as f:
            json.dump(serializable_history, f, indent=2)
        
        print(f"\nTraining history saved to {history_path}")


def main():
    """Main training function"""
    
    # Set random seed for reproducibility
    torch.manual_seed(42)
    np.random.seed(42)
    
    print("NeuroDerm.AI - Model Training")
    print("=" * 60)
    
    # Prepare dataset
    print("\n1. Preparing Dataset...")
    preprocessor = DatasetPreprocessor()
    splits = preprocessor.download_and_prepare()
    dataloaders = get_dataloaders(splits)
    
    # Create model
    print("\n2. Creating Model...")
    model = create_model(freeze_backbone=False)
    
    params = count_parameters(model)
    print(f"Total parameters: {params['total']:,}")
    print(f"Trainable parameters: {params['trainable']:,}")
    
    # Create optimizer
    print("\n3. Setting up Optimizer...")
    optimizer = AdamW(
        model.parameters(),
        lr=config.LEARNING_RATE,
        weight_decay=config.WEIGHT_DECAY
    )
    
    # Create scheduler
    scheduler = CosineAnnealingLR(
        optimizer,
        T_max=config.NUM_EPOCHS,
        eta_min=1e-6
    )
    
    # Create trainer
    print("\n4. Initializing Trainer...")
    trainer = Trainer(
        model=model,
        dataloaders=dataloaders,
        optimizer=optimizer,
        scheduler=scheduler
    )
    
    # Train
    print("\n5. Starting Training...")
    trainer.train()
    
    print("\nTraining complete! Model saved to:", config.MODEL_DIR)


if __name__ == "__main__":
    main()