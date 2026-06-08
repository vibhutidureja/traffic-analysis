import cv2
import threading
import queue
from ultralytics import YOLO
import supervision as sv
from database import save_telemetry_to_db

class ProductionTrafficEngine:
    def __init__(self, model_weights: str = "yolov8n.pt"):
        self.model = YOLO(model_weights)
        self.target_classes = [2, 3, 5, 7] # car, motorcycle, bus, truck
        self.frame_queue = queue.Queue(maxsize=128)
        self.is_running = False

    def _frame_producer(self, video_path: str):
        cap = cv2.VideoCapture(video_path)
        frame_stride = 0
        while cap.isOpened() and self.is_running:
            success, frame = cap.read()
            if not success:
                break
            frame_stride += 1
            if frame_stride % 2 != 0:
                continue
            if not self.frame_queue.full():
                self.frame_queue.put(frame)
        cap.release()
        self.is_running = False

    def process_stream(self, video_path: str, output_path: str = "production_traffic_output.mp4"):
        video_info = sv.VideoInfo.from_video_path(video_path)
        video_sink = sv.VideoSink(target_path=output_path, video_info=video_info)
        
        start_point = sv.Point(0, video_info.height // 2 + 50)
        end_point = sv.Point(video_info.width, video_info.height // 2 + 50)
        line_zone = sv.LineZone(start=start_point, end=end_point)
        
        box_annotator = sv.BoxAnnotator()
        label_annotator = sv.LabelAnnotator()
        line_annotator = sv.LineZoneAnnotator(thickness=3, text_thickness=2, text_scale=1.2)
        
        self.is_running = True
        producer_thread = threading.Thread(target=self._frame_producer, args=(video_path,))
        producer_thread.daemon = True
        producer_thread.start()
        
        with video_sink as sink:
            while self.is_running or not self.frame_queue.empty():
                try:
                    frame = self.frame_queue.get(timeout=2)
                except queue.Empty:
                    break
                    
                results = self.model.track(frame, persist=True, fuse=True, verbose=False)[0]
                detections = sv.Detections.from_ultralytics(results)
                
                if detections.class_id is not None and detections.tracker_id is not None:
                    mask = [cid in self.target_classes for cid in detections.class_id]
                    detections = detections[mask]
                    
                    line_zone.trigger(detections=detections)
                    
                    # Core Distribution Mapping calculation
                    local_dist = {}
                    for class_id in detections.class_id:
                        name = self.model.model.names[class_id]
                        local_dist[name] = local_dist.get(name, 0) + 1
                    
                    # 🚀 PERSISTENCE LAYER: Stream processing direct SQLite DB mein save ho raha hai!
                    save_telemetry_to_db(
                        in_count=line_zone.in_count,
                        out_count=line_zone.out_count,
                        density=len(detections.tracker_id),
                        distribution=local_dist
                    )
                    
                    labels = [f"ID: {tid} {self.model.model.names[cid]}" for cid, tid in zip(detections.class_id, detections.tracker_id)]
                    frame = box_annotator.annotate(scene=frame, detections=detections)
                    frame = label_annotator.annotate(scene=frame, detections=detections, labels=labels)
                
                frame = line_annotator.annotate(frame=frame, line_zone=line_zone)
                sink.write_frame(frame=frame)
                
        self.is_running = False
        producer_thread.join()