import torch
import cv2 

from hardware.gpio_control import set_signal, cleanup

model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)

cap = cv2.VideoCapture("data/traffic.mp4")

# Vehicle classes (COCO dataset IDs)
vehicle_classes = [2, 3, 5, 7]  
# 2=car, 3=motorcycle, 5=bus, 7=truck

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    roi = (0, int(h*0.5), w, h)  # bottom half of frame

    cv2.rectangle(frame, (roi[0], roi[1]), (roi[2], roi[3]), (255,0,0), 2)

    results = model(frame)
    detections = results.xyxy[0]

    vehicle_count = 0

    for *box, conf, cls in detections:

        cls = int(cls.item())  # ✅ FIX 1

        if cls in vehicle_classes:

            x1, y1, x2, y2 = [int(x.item()) for x in box]  # ✅ FIX 2

            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            # Check if inside ROI
            if roi[0] < cx < roi[2] and roi[1] < cy < roi[3]:
                vehicle_count += 1
                cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
    
    # Density classification
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


    # Display count
    cv2.putText(frame, f"Vehicles: {vehicle_count}",
                (20,50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0,0,255), 2)
    cv2.putText(frame, f"Density: {density}",
            (20, 100), cv2.FONT_HERSHEY_SIMPLEX,
            0.8, (255,255,0), 2)

    cv2.putText(frame, f"Signal: {signal}",
            (20, 140), cv2.FONT_HERSHEY_SIMPLEX,
            0.8, (0,255,255), 2)

    cv2.putText(frame, f"Time: {green_time}s",
            (20, 180), cv2.FONT_HERSHEY_SIMPLEX,
            0.8, (255,0,255), 2)

    cv2.imshow("Traffic Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
cleanup()