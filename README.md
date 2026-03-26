<<<<<<< HEAD
# NeuroDerm.AI - AI-Powered Skin Health Analysis Platform

An intelligent skin analysis platform using fine-tuned DINOv2 vision transformer for detecting skin conditions and providing personalized skincare recommendations.

## 🌟 Features

- **AI-Powered Analysis**: Multi-label classification for 8+ skin conditions
- **Real-time Processing**: Instant analysis with <3s response time
- **Personalized Recommendations**: Customized skincare routines and product suggestions
- **Progress Tracking**: Monitor skin health improvements over time
- **Comparison Mode**: Before/after visualization
- **Professional UI**: Modern, responsive interface built with Next.js and Tailwind CSS

## 🏗️ Architecture

### ML Model
- **Base**: facebook/dinov2-base (Vision Transformer)
- **Task**: Multi-label skin condition classification
- **Conditions Detected**:
  - Acne (with severity grading)
  - Redness/Inflammation
  - Dryness
  - Oiliness
  - Aging signs
  - Dark spots/Hyperpigmentation
  - Texture issues
  - Healthy skin baseline

### Backend (FastAPI)
- Python 3.11+
- PostgreSQL database
- Redis caching
- S3/Cloudinary image storage
- JWT authentication

### Frontend (Next.js 14)
- React 18
- TypeScript
- Tailwind CSS + shadcn/ui
- Real-time updates

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 20+
- PostgreSQL 15+
- Redis 7+

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/neuroderm-ai.git
cd neuroderm-ai
=======
# Neuroderma.ai
AI-powered skin analysis, prediction &amp; digital twin simulation system (FastAPI + React + ML)
>>>>>>> 4d7f53ff773e68d63aa3c58ef993e49f3e93d172
