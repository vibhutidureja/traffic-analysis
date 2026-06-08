# 🚦 Autonomous Traffic Intelligence & Analytics System

An industrial-grade computer vision pipeline designed for real-time vehicle detection, tracking, and traffic flow telemetry. The system utilizes **YOLOv8** and **ByteTrack** for high-precision vehicle monitoring and persists live metrics into a relational **SQLite** database via a **FastAPI** backend.

---

## 🚀 Key Technical Highlights

* **Advanced Object Tracking:** Integrates **YOLOv8** for multi-class vehicle detection (Cars, Trucks, Buses, Motorcycles) paired with **ByteTrack** for robust ID retention across frames.
* **Spatial Flow Telemetry:** Implements a directional frame-boundary intersection algorithm to automate volumetric counting and lane density monitoring.
* **Database Persistence:** Utilizes a **SQLite relational storage layer** to log real-time intersection load, class distribution, and traffic flow trends.
* **High-Throughput API:** Exposes a **FastAPI** interface to serve live telemetry data, designed for seamless integration with downstream dashboards or monitoring tools.
* **Latency-Optimized:** Features a thread-safe frame ingestion buffer with adaptive stride processing to maintain **45+ FPS** performance on standard compute infrastructure.

---

## 📦 Project Architecture

```text
├── app.py                  # FastAPI Backend & Telemetry Endpoint
├── traffic_monitor.py      # Core Computer Vision Engine (YOLO/ByteTrack)
├── database.py             # SQLite Persistence & Schema Management
├── schema.py               # Pydantic validation schemas
├── requirements.txt        # Dependency manifest
└── README.md               # Project documentation
