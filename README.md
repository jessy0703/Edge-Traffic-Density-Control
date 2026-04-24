# 🚦 Edge-Based Smart Traffic Density & Signal Controller

## 📌 Project Overview
Urban intersections often suffer from inefficient traffic management due to static signal timings.  
This project presents an **edge AI-based smart traffic control system** that dynamically adjusts signal timing based on real-time vehicle density.

The system uses **YOLOv5 object detection** to analyze traffic video and make decisions locally on an edge device (Jetson Nano), eliminating the need for cloud processing.

---

## 🎯 Objectives
- Detect vehicles in real-time using computer vision  
- Estimate traffic density using Region of Interest (ROI)  
- Dynamically control signal timing  
- Reduce congestion and waiting time  

---

## 🧠 System Pipeline
Video Input → YOLOv5 Detection → ROI Filtering → Vehicle Counting → Density Estimation → Signal Decision → Output (Display / LED)

---

## ⚙️ Technologies Used
- Python  
- OpenCV  
- PyTorch  
- YOLOv5  
- Jetson Nano  
- Jetson.GPIO  

---

## 🚗 Key Features
- Real-time vehicle detection  
- ROI-based vehicle counting  
- Density classification (Low / Medium / High)  
- Adaptive traffic signal logic  
- Multi-video processing (different traffic scenarios)  
- Output video generation  
- Performance metrics (FPS display)  
- Graph-based analysis  

---

## 📊 Dataset Used
The system was tested using:
- Custom traffic video (`traffic.mp4`)  
- Standard dataset sequences (UA-DETRAC image sequences converted to video)  

> Note: Dataset frames were converted into video format using OpenCV for real-time processing.

---

## 📊 Density Logic

| Vehicle Count | Density |
|--------------|--------|
| 0 – 7        | LOW    |
| 8 – 15       | MEDIUM |
| > 15         | HIGH   |

---

## 🚦 Signal Control Logic

| Density| Signal | Time |
|--------|--------|------|
| LOW    | GREEN  | 15s  |
| MEDIUM | YELLOW | 25s  |
| HIGH   | RED    | 40s  |

---

## 🔌 Hardware Implementation
- 🔴 Red LED → Stop  
- 🟡 Yellow LED → Wait  
- 🟢 Green LED → Go  

Controlled via Jetson Nano GPIO pins.

---

## 📁 Project Structure
Edge-Traffic-Density-Control/
│
├── src/ # Main code
├── hardware/ # GPIO control
├── data/ # Input videos
├── outputs/ # Results & logs
├── demo/ # Demo video
├── report/ # Project report
├── presentation/ # PPT
├── README.md

---

## 📈 Results and Analysis
The system was tested on multiple traffic scenarios (low, medium, and high density).  

- Successfully detected vehicles in real-time  
- Correctly classified traffic density  
- Adaptively adjusted signal timing  
- Achieved real-time performance (10–20 FPS approx.)

Graph-based analysis of vehicle counts is included in the `outputs/` folder.

---

## 🎥 Demo
A demonstration video of the working system is available in the `demo/` folder.

---

## 🧠 Advantages
- Real-time processing using edge AI  
- No cloud dependency  
- Low-cost and scalable  
- Reduces congestion and fuel wastage  

---

## 🚀 Future Scope
- Multi-lane traffic control  
- Reinforcement learning-based optimization  
- Integration with real CCTV systems  
- Smart city deployment  

---

## 👨‍💻 Team Members
- Jessica Salonee  
- Gaurav  
- Vansh  

---

## 🧠 Conclusion
This project demonstrates how **edge AI can enable intelligent traffic management systems** by combining computer vision, real-time processing, and control logic.

---
