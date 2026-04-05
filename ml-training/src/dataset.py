"""
Dataset preparation and loading for NeuroDerm.AI
"""

import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import albumentations as A
from albumentations.pytorch import ToTensorV2
import numpy as np
from datasets import load_dataset
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json
from config import config

class SkinConditionDataset(Dataset):
    """Custom Dataset for Skin Condition Classification"""
    
    def __init__(
        self,
        data: List[Dict],
        transform=None,
        augment: bool = False
    ):
        """
        Args:
            data: List of dictionaries with 'image' and 'labels' keys
            transform: Albumentations transform pipeline
            augment: Whether to apply data augmentation
        """
        self.data = data
        self.transform = transform
        self.augment = augment
        
        if self.augment and self.transform is None:
            self.transform = self._get_augmentation_pipeline()
        elif not self.augment and self.transform is None:
            self.transform = self._get_basic_pipeline()
    
    def _get_augmentation_pipeline(self):
        """Get augmentation pipeline for training"""
        return A.Compose([
            A.Resize(config.IMAGE_SIZE, config.IMAGE_SIZE),
            A.HorizontalFlip(p=config.AUGMENTATION_CONFIG['horizontal_flip_prob']),
            A.Rotate(
                limit=config.AUGMENTATION_CONFIG['rotation_limit'],
                p=0.5
            ),
            A.ColorJitter(
                brightness=config.AUGMENTATION_CONFIG['brightness_limit'],
                contrast=config.AUGMENTATION_CONFIG['contrast_limit'],
                saturation=config.AUGMENTATION_CONFIG['saturation_limit'],
                hue=config.AUGMENTATION_CONFIG['hue_shift_limit'],
                p=0.5
            ),
            A.Normalize(
                mean=config.IMAGENET_MEAN,
                std=config.IMAGENET_STD
            ),
            ToTensorV2()
        ])
    
    def _get_basic_pipeline(self):
        """Get basic pipeline for validation/test"""
        return A.Compose([
            A.Resize(config.IMAGE_SIZE, config.IMAGE_SIZE),
            A.Normalize(
                mean=config.IMAGENET_MEAN,
                std=config.IMAGENET_STD
            ),
            ToTensorV2()
        ])
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        item = self.data[idx]
        
        # Load image
        if isinstance(item['image'], str):
            image = Image.open(item['image']).convert('RGB')
        else:
            image = item['image'].convert('RGB')
        
        # Convert to numpy array
        image = np.array(image)
        
        # Apply transforms
        if self.transform:
            transformed = self.transform(image=image)
            image = transformed['image']
        
        # Get labels (multi-label binary vector)
        labels = torch.zeros(config.NUM_CLASSES, dtype=torch.float32)
        for condition in item['labels']:
            if condition in config.CONDITION_TO_IDX:
                labels[config.CONDITION_TO_IDX[condition]] = 1.0
        
        return {
            'image': image,
            'labels': labels,
            'image_id': item.get('id', idx)
        }


class DatasetPreprocessor:
    """Preprocess and prepare datasets for training"""
    
    def __init__(self):
        self.dataset_name = config.DATASET_NAME
    
    def download_and_prepare(self) -> Dict[str, List]:
        """
        Download and prepare the dataset
        Returns train, val, test splits
        """
        print(f"Loading dataset: {self.dataset_name}")
        
        try:
            # Try to load from HuggingFace
            dataset = load_dataset(self.dataset_name)
            processed_data = self._process_hf_dataset(dataset)
        except Exception as e:
            print(f"Could not load from HuggingFace: {e}")
            print("Creating synthetic dataset for demonstration...")
            processed_data = self._create_synthetic_dataset()
        
        # Split data
        splits = self._split_data(processed_data)
        
        # Save statistics
        self._save_statistics(splits)
        
        return splits
    
    def _process_hf_dataset(self, dataset) -> List[Dict]:
        """Process HuggingFace dataset"""
        processed = []
        
        # Assuming dataset has 'train' split
        if 'train' in dataset:
            data = dataset['train']
        else:
            data = dataset
        
        for idx, item in enumerate(data):
            processed.append({
                'id': idx,
                'image': item['image'],
                'labels': item.get('labels', []),
            })
        
        return processed
    
    def _create_synthetic_dataset(self, num_samples: int = 1000) -> List[Dict]:
        """
        Create a synthetic dataset for demonstration
        In production, replace this with real data loading
        """
        import random
        
        print(f"Creating {num_samples} synthetic samples...")
        
        synthetic_data = []
        
        for i in range(num_samples):
            # Random labels (1-3 conditions per image)
            num_conditions = random.randint(1, 3)
            labels = random.sample(config.CONDITIONS, num_conditions)
            
            # Create a random colored image (placeholder)
            image = Image.new(
                'RGB',
                (config.IMAGE_SIZE, config.IMAGE_SIZE),
                color=tuple(random.randint(0, 255) for _ in range(3))
            )
            
            synthetic_data.append({
                'id': i,
                'image': image,
                'labels': labels
            })
        
        return synthetic_data
    
    def _split_data(self, data: List[Dict]) -> Dict[str, List]:
        """Split data into train, val, test"""
        import random
        random.shuffle(data)
        
        total = len(data)
        train_end = int(total * config.TRAIN_SPLIT)
        val_end = train_end + int(total * config.VAL_SPLIT)
        
        splits = {
            'train': data[:train_end],
            'val': data[train_end:val_end],
            'test': data[val_end:]
        }
        
        print(f"\nDataset splits:")
        print(f"Train: {len(splits['train'])} samples")
        print(f"Val: {len(splits['val'])} samples")
        print(f"Test: {len(splits['test'])} samples")
        
        return splits
    
    def _save_statistics(self, splits: Dict[str, List]):
        """Calculate and save dataset statistics"""
        stats = {
            'total_samples': sum(len(split) for split in splits.values()),
            'splits': {
                name: len(split) for name, split in splits.items()
            },
            'condition_distribution': {}
        }
        
        # Calculate condition distribution
        for condition in config.CONDITIONS:
            count = 0
            for split in splits.values():
                for item in split:
                    if condition in item['labels']:
                        count += 1
            stats['condition_distribution'][condition] = count
        
        # Save to JSON
        stats_path = config.OUTPUT_DIR / 'dataset_statistics.json'
        with open(stats_path, 'w') as f:
            json.dump(stats, f, indent=2)
        
        print(f"\nDataset statistics saved to {stats_path}")
        print(f"Condition distribution: {stats['condition_distribution']}")


def get_dataloaders(splits: Dict[str, List]) -> Dict[str, DataLoader]:
    """Create DataLoaders for train, val, test"""
    
    datasets = {
        'train': SkinConditionDataset(splits['train'], augment=True),
        'val': SkinConditionDataset(splits['val'], augment=False),
        'test': SkinConditionDataset(splits['test'], augment=False)
    }
    
    dataloaders = {
        'train': DataLoader(
            datasets['train'],
            batch_size=config.BATCH_SIZE,
            shuffle=True,
            num_workers=config.NUM_WORKERS,
            pin_memory=config.PIN_MEMORY
        ),
        'val': DataLoader(
            datasets['val'],
            batch_size=config.BATCH_SIZE,
            shuffle=False,
            num_workers=config.NUM_WORKERS,
            pin_memory=config.PIN_MEMORY
        ),
        'test': DataLoader(
            datasets['test'],
            batch_size=config.BATCH_SIZE,
            shuffle=False,
            num_workers=config.NUM_WORKERS,
            pin_memory=config.PIN_MEMORY
        )
    }
    
    return dataloaders


if __name__ == "__main__":
    # Test dataset preparation
    preprocessor = DatasetPreprocessor()
    splits = preprocessor.download_and_prepare()
    dataloaders = get_dataloaders(splits)
    
    # Test loading a batch
    batch = next(iter(dataloaders['train']))
    print(f"\nBatch test:")
    print(f"Images shape: {batch['image'].shape}")
    print(f"Labels shape: {batch['labels'].shape}")
    print(f"Sample labels: {batch['labels'][0]}")