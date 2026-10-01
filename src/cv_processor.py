"""
Computer Vision Module using YOLOv8 for Road Hazard and Vehicle Detection
"""

import cv2
import os
from ultralytics import YOLO

class RoadVisionAnalyzer:
    def __init__(self, model_name="yolov8n.pt"):
        print(f"[INFO] Loading YOLOv8 model ({model_name})...")
        # Automatically downloads pretrained YOLOv8 nano model on first run
        self.model = YOLO(model_name)

    def analyze_frame(self, image_path):
        """
        Detects vehicles, counts objects, and estimates road conditions from an image frame.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image path not found: {image_path}")
            
        results = self.model(image_path)
        boxes = results[0].boxes
        
        vehicle_count = 0
        detections = []
        
        for box in boxes:
            cls_id = int(box.cls[0])
            cls_name = self.model.names[cls_id]
            conf = float(box.conf[0])
            
            # Count common road vehicles (car, motorcycle, bus, truck)
            if cls_name in ['car', 'motorcycle', 'bus', 'truck']:
                vehicle_count += 1
                
            detections.append({
                "class": cls_name,
                "confidence": round(conf, 2)
            })
            
        return {
            "vehicle_count": vehicle_count,
            "total_detections": len(detections),
            "detections": detections
        }

if __name__ == "__main__":
    analyzer = RoadVisionAnalyzer()
    print("[SUCCESS] YOLOv8 vision analyzer initialized successfully!")