import cv2
import os
import time
import sys
import torch
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

from hardware.gpio_control import TrafficSignalController
from src.accuracy_metrics import AccuracyMetrics

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# Load YOLOv5 using torch.hub (simpler, no import issues)
print("Loading YOLOv5 model...")
model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True, force_reload=False)
model.to(device)
model.eval()

print("✅ Model loaded successfully")

# Initialize GPIO
gpio_controller = TrafficSignalController()

# Initialize metrics tracker
metrics = AccuracyMetrics()

# Folder containing videos
video_folder = "data"
output_folder = "outputs"
os.makedirs(output_folder, exist_ok=True)

# Get all video files
video_files = [f for f in os.listdir(video_folder) if f.endswith((".mp4", ".avi"))]

if not video_files:
    print("❌ No video files found in data/ folder")
    sys.exit(1)

results_log = []

try:
    for video_name in video_files:
        print(f"\n{'='*60}")
        print(f"Processing: {video_name}")
        print(f"LED blinking + Processing...") 
        print(f"{'='*60}")
        
        metrics.start_video(video_name)
        
        cap = cv2.VideoCapture(os.path.join(video_folder, video_name))
        
        if not cap.isOpened():
            print(f"❌ Failed to open {video_name}")
            continue
        
        # Video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = None
        prev_time = 0
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            h, w, _ = frame.shape
            
            # Initialize output video writer
            if out is None:
                out = cv2.VideoWriter(
                    os.path.join(output_folder, f"output_{video_name}"),
                    fourcc, 10, (w, h)
                )
            
            # Frame processing time
            frame_start = time.time()
            
            # FPS calculation
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
            prev_time = curr_time
            
            # ROI (full frame for better detection - detects all vehicles)
            roi = (0, 0, w, h)
            cv2.rectangle(frame, (roi[0], roi[1]), (roi[2], roi[3]), (255, 0, 0), 2)
            
            # YOLOv5 Detection
            results = model(frame)
            detections = results.xyxy[0].cpu().numpy()
            
            vehicle_count = 0
            confidences = []
            
            for detection in detections:
                x1, y1, x2, y2, conf, cls = detection
                cls = int(cls)
                
                # Vehicle classes: 2=car, 3=motorcycle, 5=bus, 7=truck
                if cls in [2, 3, 5, 7]:
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    
                    # Count only vehicles in ROI
                    if roi[0] < cx < roi[2] and roi[1] < cy < roi[3]:
                        vehicle_count += 1
                        confidences.append(float(conf))
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Log frame metrics
            frame_time = time.time() - frame_start
            metrics.log_frame(vehicle_count, frame_time, confidences)
            
            # Traffic density logic
            if vehicle_count > 15:
                density = "HIGH"
                signal = "RED"
            elif vehicle_count > 7:
                density = "MEDIUM"
                signal = "YELLOW"
            else:
                density = "LOW"
                signal = "GREEN"
            
            # Control LED (blinks while video is processed)
            gpio_controller.set_signal(signal)
            
            # Log results
            results_log.append([video_name, vehicle_count, density])
            
            # Display info on frame
            cv2.putText(frame, f"{video_name}", (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
            cv2.putText(frame, f"Vehicles: {vehicle_count}", (20, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            cv2.putText(frame, f"Density: {density}", (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)
            cv2.putText(frame, f"Signal: {signal}", (20, 140),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
            cv2.putText(frame, f"FPS: {int(fps)}", (20, 180),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            
            # Save output video
            out.write(frame)
            
            if frame_count % 30 == 0:
                print(f"  Frame {frame_count}: Vehicles={vehicle_count}, Density={density}")
        
        cap.release()
        if out:
            out.release()
        
        # Log final metrics for this video
        metrics.end_video()
        
        print(f"✅ Finished {video_name}")
    
    metrics.log_summary()

except KeyboardInterrupt:
    print("\n[USER] Stopped by user")
except Exception as e:
    print(f"[ERROR] {str(e)}")
finally:
    gpio_controller.cleanup()

# Save results to file
with open("outputs/results.txt", "w") as f:
    for row in results_log:
        f.write(f"{row[0]}, {row[1]}, {row[2]}\n")

print("\n" + "="*60)
print("✅ Processing complete!")
print("="*60)