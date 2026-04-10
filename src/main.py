import torch
import cv2
import os
import time

from hardware.gpio_control import set_signal, cleanup

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)

# Folder containing ALL videos
video_folder = "data"

# Output folder
output_folder = "outputs"
os.makedirs(output_folder, exist_ok=True)

# Get all video files
video_files = [f for f in os.listdir(video_folder) if f.endswith((".mp4", ".avi"))]

# Store results for report
results_log = []

try:
    for video_name in video_files:

        print(f"\nProcessing: {video_name}")

        cap = cv2.VideoCapture(os.path.join(video_folder, video_name))

        # Video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = None

        prev_time = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            h, w, _ = frame.shape

            # Initialize output video writer
            if out is None:
                out = cv2.VideoWriter(
                    os.path.join(output_folder, f"output_{video_name}"),
                    fourcc, 10, (w, h)
                )

            # FPS calculation
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
            prev_time = curr_time

            # ROI
            roi = (0, int(h * 0.5), w, h)
            cv2.rectangle(frame, (roi[0], roi[1]), (roi[2], roi[3]), (255, 0, 0), 2)

            # Detection
            results = model(frame)
            detections = results.xyxy[0]

            vehicle_count = 0

            for *box, conf, cls in detections:
                cls = int(cls.item())

                if cls in [2, 3, 5, 7]:
                    x1, y1, x2, y2 = [int(x.item()) for x in box]

                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    if roi[0] < cx < roi[2] and roi[1] < cy < roi[3]:
                        vehicle_count += 1
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Density logic
            if vehicle_count > 15:
                density = "HIGH"
            elif vehicle_count > 7:
                density = "MEDIUM"
            else:
                density = "LOW"

            # Signal logic
            if density == "HIGH":
                signal = "GREEN"
                green_time = 40
            elif density == "MEDIUM":
                signal = "YELLOW"
                green_time = 25
            else:
                signal = "RED"
                green_time = 15

            set_signal(signal)

            # Save data
            results_log.append([video_name, vehicle_count, density])

            # Display text
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

            cv2.imshow("Traffic System", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        if out:
            out.release()

    cv2.destroyAllWindows()

finally:
    cleanup()

# Save results to file
with open("outputs/results.txt", "w") as f:
    for row in results_log:
        f.write(f"{row[0]}, {row[1]}, {row[2]}\n")