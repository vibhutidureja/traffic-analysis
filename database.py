import sqlite3
from datetime import datetime

DB_NAME = "traffic_telemetry.db"

def init_db():
    """Database tables ko initialize karne ka core function."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Live aggregated logs ke liye table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS traffic_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            total_vehicles_in INTEGER NOT NULL,
            total_vehicles_out INTEGER NOT NULL,
            current_density_count INTEGER NOT NULL
        )
    """)
    
    # Real-time class distribution mapping ke liye table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS class_distribution (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            class_name TEXT NOT NULL,
            count INTEGER NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def save_telemetry_to_db(in_count: int, out_count: int, density: int, distribution: dict):
    """Real-time metrics ko SQLite DB mein batch-insert karne ka thread-safe method."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    current_time = datetime.now().isoformat()
    
    # 1. Main metrics table mein entry save karo
    cursor.execute("""
        INSERT INTO traffic_metrics (timestamp, total_vehicles_in, total_vehicles_out, current_density_count)
        VALUES (?, ?, ?, ?)
    """, (current_time, in_count, out_count, density))
    
    # 2. Vehicle class metrics break-down save karo
    for class_name, count in distribution.items():
        cursor.execute("""
            INSERT INTO class_distribution (timestamp, class_name, count)
            VALUES (?, ?, ?)
        """, (current_time, class_name, count))
        
    conn.commit()
    conn.close()

def fetch_latest_telemetry():
    """FastAPI endpoints ke liye database se fresh state execute karne ka logic."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Latest main metrics fetch karo
    cursor.execute("SELECT * FROM traffic_metrics ORDER BY id DESC LIMIT 1")
    latest_row = cursor.fetchone()
    
    if not latest_row:
        conn.close()
        return None
        
    # Latest data metrics ke base par distribution trends pull karo
    timestamp = latest_row["timestamp"]
    cursor.execute("SELECT class_name, count FROM class_distribution WHERE timestamp = ?", (timestamp,))
    dist_rows = cursor.fetchall()
    
    distribution_dict = {row["class_name"]: row["count"] for row in dist_rows}
    
    data = {
        "timestamp": latest_row["timestamp"],
        "total_vehicles_in": latest_row["total_vehicles_in"],
        "total_vehicles_out": latest_row["total_vehicles_out"],
        "current_density_count": latest_row["current_density_count"],
        "class_distribution": distribution_dict
    }
    
    conn.close()
    return data