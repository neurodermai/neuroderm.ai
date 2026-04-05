# 🧬 NeuroDerm AI

> **Not just what your skin is — but what it's becoming.**

🚀 AI-Powered Skin Analysis • 🧠 DINOv2 Vision AI • 📊 Risk Forecasting • 🧬 Digital Twin System

---

## 🌍 Problem

* Skin diseases are often **detected too late**
* Limited access to **dermatologists**, especially in rural areas
* No system for **continuous skin health monitoring**
* Current solutions are **reactive, not predictive**

---

## 💡 Solution

**NeuroDerm AI** is an intelligent, AI-powered platform that combines:

* 📸 Facial image analysis
* 🧠 Deep learning (DINOv2 Vision Transformer)
* 📊 Lifestyle & behavioral signals

To provide:

* ✅ Instant skin condition detection
* 📈 Future risk prediction
* 🧬 Personalized skincare plans
* 🔁 Continuous monitoring via digital twin

---

## ✨ Key Features

* 🔍 **AI Skin Analysis** — Multi-label detection of 8+ skin conditions
* ⚡ **Real-time Processing** — <3 seconds response time
* 📊 **Risk Forecasting** — Predict future skin issues
* 🧬 **Digital Skin Twin** — Track changes over time
* 🧠 **Lifestyle Insights** — Sleep, stress, diet-based recommendations
* 📱 **Modern Dashboard** — Clean, responsive UI

---

## 🏗️ Architecture

```
User (Image + Lifestyle Input)
        ↓
Frontend (Next.js + Tailwind)
        ↓
Backend (FastAPI)
        ↓
ML Model (DINOv2 Vision Transformer)
        ↓
Database (PostgreSQL + Redis)
        ↓
Results + Recommendations
```

---

## 🧪 Tech Stack

**Frontend**

* Next.js 14
* React 18
* TypeScript
* Tailwind CSS + shadcn/ui

**Backend**

* FastAPI (Python 3.11+)
* JWT Authentication
* REST APIs

**AI / ML**

* DINOv2 (Vision Transformer)
* Multi-label classification

**Database & Infra**

* PostgreSQL
* Redis (Caching)
* Cloudinary / S3 (Image storage)
* Docker & Docker Compose

---

## 📸 Demo


```
assets/
├── landing.png
├── analysis.png
├── dashboard.png
```

```md
![Landing](./assets/landing.png)
![Analysis](./assets/analysis.png)
![Dashboard](./assets/dashboard.png)
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/neurodermai/neuroderm.ai.git
cd neuroderm.ai
```

---

### 2. Backend Setup (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

### 3. Frontend Setup (Next.js)

```bash
cd frontend
npm install
npm run dev
```

---

### 4. Open in Browser

```
http://localhost:3000
```

---

## 🔐 Environment Variables

Create a `.env` file in backend:

```
DATABASE_URL=
SECRET_KEY=
MODEL_NAME=
CLOUDINARY_URL=
```

---

## 🏆 Built for Hackathon

**Team CodeMinds**

* 👨‍💻 Suryamani
* 👨‍💻 Harsh
* 👨‍💻 Piyush
* 👨‍💻 Aryan

---

## 🔮 Future Scope

* 📱 Mobile app (React Native)
* 🧑‍⚕️ Dermatologist integration
* ⌚ Wearable device sync
* 🌍 Rural healthcare deployment
* 🧪 Clinical validation & trials

---

## 📌 Why This Matters

> Early detection saves lives.
> NeuroDerm AI makes advanced skin analysis **accessible, predictive, and scalable**.

---

## ⭐ Support

If you like this project:

* ⭐ Star the repo
* 🍴 Fork it
* 🚀 Share it

---

## 📜 License

MIT License

---
