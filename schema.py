from pydantic import BaseModel
from typing import List, Dict

class VehicleDetectionPayload(BaseModel):
    track_id: int
    class_name: str
    confidence: float
    box_coordinates: List[float]

class TrafficTelemetryMetrics(BaseModel):
    total_vehicles_in: int
    total_vehicles_out: int
    current_density_count: int
    active_tracking_ids: List[int]
    class_distribution: Dict[str, int]