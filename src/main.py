import cv2
import os
import time
import sys
import torch
import numpy as np
from pathlib import Path
import threading

from hardware.gpio_control import TrafficSignalController
from src.accuracy_metrics import AccuracyMetrics

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

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

class MotionDetector:
    """Lightweight motion detection"""
    def __init__(self):
        self.prev_frame_gray = None
    
    def is_moving(self, frame, x1, y1, x2, y2):
        """Check if vehicle is moving"""
        try:
            curr_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            if self.prev_frame_gray is None:
                self.prev_frame_gray = curr_frame_gray.copy()
                return True
            
            # Get frame difference
            frame_diff = cv2.absdiff(self.prev_frame_gray, curr_frame_gray)
            
            # Check motion in vehicle ROI
            roi_diff = frame_diff[max(0, y1):min(frame_diff.shape[0], y2), 
                                   max(0, x1):min(frame_diff.shape[1], x2)]
            
            if roi_diff.size == 0:
                return True
            
            # Count pixels with motion (threshold: 20)
            motion_pixels = np.sum(roi_diff > 20)
            motion_ratio = motion_pixels / roi_diff.size
            
            # Update prev frame every 3 frames
            if int(time.time() * 30) % 3 == 0:
                self.prev_frame_gray = curr_frame_gray.copy()
            
            # Return True if motion > 1%
            return motion_ratio > 0.01
            
        except Exception as e:
            return True

# Initialize motion detector
motion_detector = MotionDetector()

try:
    for video_name in video_files:
        print(f"\n{'='*60}")
        print(f"Processing: {video_name}")
        print(f"{'='*60}")
        
        metrics.start_video(video_name)
        motion_detector.prev_frame_gray = None
        
        cap = cv2.VideoCapture(os.path.join(video_folder, video_name))
        
        if not cap.isOpened():
            print(f"❌ Failed to open {video_name}")
            continue
        
        # Video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = None
        prev_time = 0
        frame_count = 0
        current_signal = "GREEN"
        frames_buffer = []  # Buffer to collect frames
        LED_UPDATE_INTERVAL = 15  # Update LED every 15 frames
        
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
            
            # ROI (100% full frame)
            roi = (0, 0, w, h)
            cv2.rectangle(frame, (roi[0], roi[1]), (roi[2], roi[3]), (255, 0, 0), 2)
            
            # YOLOv5 Detection
            results = model(frame)
            detections = results.xyxy[0].cpu().numpy()
            
            vehicle_count = 0
            moving_count = 0
            stationary_count = 0
            confidences = []
            
            for detection in detections:
                x1, y1, x2, y2, conf, cls = detection
                cls = int(cls)
                
                # Vehicle classes: 2=car, 3=motorcycle, 5=bus, 7=truck
                if cls in [2, 3, 5, 7]:
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    
                    # Count only vehicles in full frame ROI
                    if roi[0] < cx < roi[2] and roi[1] < cy < roi[3]:
                        vehicle_count += 1
                        confidences.append(float(conf))
                        
                        # Check if moving
                        if motion_detector.is_moving(frame, x1, y1, x2, y2):
                            moving_count += 1
                            # Green box = Moving
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        else:
                            stationary_count += 1
                            # Red box = Stationary
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            
            # Log frame metrics (only moving vehicles)
            frame_time = time.time() - frame_start
            metrics.log_frame(moving_count, frame_time, confidences)
            
            # Traffic density logic (based on moving vehicles)
            if moving_count > 15:
                density = "HIGH"
                new_signal = "RED"
            elif moving_count > 7:
                density = "MEDIUM"
                new_signal = "YELLOW"
            else:
                density = "LOW"
                new_signal = "GREEN"
            
            # Store frame data in buffer
            frames_buffer.append({
                'moving': moving_count,
                'stationary': stationary_count,
                'total': vehicle_count,
                'density': density,
                'signal': new_signal
            })
            
            # Update LED every 15 frames (average over buffer)
            if len(frames_buffer) >= LED_UPDATE_INTERVAL:
                # Calculate average moving vehicles over 15 frames
                avg_moving = sum(f['moving'] for f in frames_buffer) / len(frames_buffer)
                
                # Determine signal based on average (ORIGINAL THRESHOLDS)
                if avg_moving > 15:
                    final_signal = "RED"
                elif avg_moving > 7:
                    final_signal = "YELLOW"
                else:
                    final_signal = "GREEN"
                
                # Only change if signal differs
                if final_signal != current_signal:
                    current_signal = final_signal
                    gpio_controller.set_signal(current_signal)
                    print(f"  [LED] {current_signal} (Avg Moving: {avg_moving:.1f}) - Frame {frame_count}")
                
                # Clear buffer
                frames_buffer = []
            
            # Log results
            results_log.append([video_name, moving_count, density])
            
            # Display info on frame with COLOR indicator for LED status
            led_color_map = {
                "RED": (0, 0, 255),
                "YELLOW": (0, 255, 255),
                "GREEN": (0, 255, 0)
            }
            led_color = led_color_map.get(current_signal, (0, 255, 0))
            
            # Draw LED indicator box
            cv2.rectangle(frame, (w-100, 20), (w-20, 80), led_color, -1)
            cv2.rectangle(frame, (w-100, 20), (w-20, 80), (255, 255, 255), 2)
            cv2.putText(frame, current_signal, (w-95, 55),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            
            # Display info on frame
            cv2.putText(frame, f"{video_name}", (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"Moving: {moving_count} | Stationary: {stationary_count}", (20, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(frame, f"Total Detected: {vehicle_count}", (20, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
            cv2.putText(frame, f"Density: {density}", (20, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(frame, f"FPS: {int(fps)}", (20, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Save output video
            out.write(frame)
            
            if frame_count % 15 == 0:
                print(f"  Frame {frame_count}: Moving={moving_count}, Stationary={stationary_count}, Signal={current_signal}")
        
        cap.release()
        if out:
            out.release()
        
        metrics.end_video()
        
        print(f"✅ Finished {video_name}")
    
    metrics.log_summary()

except KeyboardInterrupt:
    print("\n[USER] Stopped by user")
except Exception as e:
    print(f"[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    gpio_controller.cleanup()

# Save results to file
with open("outputs/results.txt", "w") as f:
    for row in results_log:
        f.write(f"{row[0]}, {row[1]}, {row[2]}\n")

print("\n" + "="*60)
print("✅ Processing complete!")
print("="*60)