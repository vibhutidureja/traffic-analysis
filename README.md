# 🚦 Autonomous Traffic Intelligence System

A production-grade computer vision pipeline engineered to perform real-time multi-class vehicle detection, tracking, and spatial flow analytics. This system integrates deep learning inference with asynchronous telemetry persistence to provide actionable traffic insights.



---

## 🚀 Key Technical Highlights

* **Computer Vision Core:** Powered by **YOLOv8** for high-precision vehicle classification (Cars, Trucks, Buses, Motorcycles) and **ByteTrack** for persistent multi-object tracking.
* **Asynchronous Telemetry Pipeline:** Utilizes **FastAPI** to serve live intersection metrics, featuring a non-blocking thread-safe architecture for high-concurrency data handling.
* **Relational Persistence:** Implements a structured **SQLite** backend to log real-time vehicle flow vectors, cross-line density counts, and classification distribution trends.
* **Performance Engineering:** Engineered with an adaptive frame-ingestion buffer to sustain deterministic throughput on limited-compute edge infrastructure.

---

## 🏗️ System Architecture

1. **Ingestion Layer:** High-speed frame acquisition with adaptive stride processing to maintain optimal FPS.
2. **Inference Engine:** Deep structural feature extraction and identity retention via YOLO-ByteTrack integration.
3. **Analytics Logic:** Spatial boundary intersection algorithm triggers automated volumetric counting.
4. **Data Persistence:** Atomic SQL commits ensure consistent logging of flow state and class distribution.

---

## 🛠️ Tech Stack
* **Frameworks:** `FastAPI`, `YOLOv8 (Ultralytics)`, `Supervision`
* **Storage:** `SQLite` (Relational Persistence Layer)
* **Concurrency:** `Python Threading` & `Queue` (Producer-Consumer Pattern)
* **Compute:** `OpenCV` (Spatial frame manipulation)

---

## 🏁 Quick Setup & Deployment

### 1. Environment Initialization
```bash
pip install -r requirements.txt
