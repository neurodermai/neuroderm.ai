"""
Configuration for NeuroDerm.AI Model Training
"""

import torch
from pathlib import Path

class Config:
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    OUTPUT_DIR = BASE_DIR / "outputs"
    MODEL_DIR = OUTPUT_DIR / "models"
    LOGS_DIR = OUTPUT_DIR / "logs"
    
    # Create directories
    DATA_DIR.mkdir(exist_ok=True, parents=True)
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
    MODEL_DIR.mkdir(exist_ok=True, parents=True)
    LOGS_DIR.mkdir(exist_ok=True, parents=True)
    
    # Model Configuration
    MODEL_NAME = "facebook/dinov2-base"
    CUSTOM_MODEL_NAME = "neuroderm-dinov2-skin-analyzer"
    IMAGE_SIZE = 224
    PATCH_SIZE = 14
    
    # Dataset Configuration
    DATASET_NAME = "rachitgoyell/dermoraSkinStressDataset"
    
    # Skin Conditions (Multi-label Classification)
    CONDITIONS = [
        "acne",
        "redness",
        "dryness",
        "oiliness",
        "aging_signs",
        "dark_spots",
        "texture_issues",
        "healthy"
    ]
    
    NUM_CLASSES = len(CONDITIONS)
    
    # Condition to Index Mapping
    CONDITION_TO_IDX = {condition: idx for idx, condition in enumerate(CONDITIONS)}
    IDX_TO_CONDITION = {idx: condition for idx, condition in enumerate(CONDITIONS)}
    
    # Severity Levels
    SEVERITY_LEVELS = {
        "none": 0,
        "mild": 1,
        "moderate": 2,
        "severe": 3
    }
    
    # Training Configuration
    BATCH_SIZE = 16
    NUM_EPOCHS = 30
    LEARNING_RATE = 1e-4
    WEIGHT_DECAY = 0.01
    WARMUP_STEPS = 500
    MAX_GRAD_NORM = 1.0
    
    # Data Split
    TRAIN_SPLIT = 0.7
    VAL_SPLIT = 0.15
    TEST_SPLIT = 0.15
    
    # Training Settings
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    NUM_WORKERS = 4
    PIN_MEMORY = True
    MIXED_PRECISION = True
    
    # Early Stopping
    EARLY_STOPPING_PATIENCE = 5
    
    # Model Saving
    SAVE_BEST_ONLY = True
    SAVE_FREQUENCY = 1  # Save every N epochs
    
    # Logging
    LOG_INTERVAL = 10  # Log every N batches
    USE_WANDB = False  # Set to True if using Weights & Biases
    WANDB_PROJECT = "neuroderm-ai"
    
    # Hugging Face
    HF_TOKEN = None  # Set your token or load from environment
    PUSH_TO_HUB = False  # Set to True to push model to HuggingFace Hub
    
    # Image Augmentation
    AUGMENTATION_CONFIG = {
        "horizontal_flip_prob": 0.5,
        "rotation_limit": 20,
        "brightness_limit": 0.2,
        "contrast_limit": 0.2,
        "hue_shift_limit": 10,
        "saturation_limit": 0.3,
    }
    
    # ImageNet Statistics (for DINOv2)
    IMAGENET_MEAN = [0.485, 0.456, 0.406]
    IMAGENET_STD = [0.229, 0.224, 0.225]
    
    # Inference Configuration
    CONFIDENCE_THRESHOLD = 0.5
    MIN_SEVERITY_SCORE = 0.3
    MAX_SEVERITY_SCORE = 1.0

config = Config()