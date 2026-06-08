from fastapi import FastAPI, HTTPException
from traffic_monitor import ProductionTrafficEngine
from database import init_db, fetch_latest_telemetry
import threading

app = FastAPI(title="Autonomous Traffic Intelligence System Engine")
engine = ProductionTrafficEngine()

@app.on_event("startup")
async def startup_event():
    # 1. Startup par real SQLite database tables initialize karo
    init_db()
    
    # 2. Background worker model engine execute karo
    def start_background_processing():
        engine.process_stream(video_path="input_traffic.mp4")
        
    threading.Thread(target=start_background_processing, daemon=True).start()

@app.get("/telemetry/traffic")
async def get_live_traffic_telemetry():
    """Endpoint querying continuous structural vehicle intelligence directly from SQL database."""
    db_payload = fetch_latest_telemetry()
    if not db_payload:
        raise HTTPException(status_code=404, detail="No telemetry frames logged in relational database yet.")
    return db_payload