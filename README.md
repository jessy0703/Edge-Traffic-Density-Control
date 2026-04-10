# 🚦 Edge-Based Smart Traffic Density & Signal Controller

## 📌 Project Overview
Urban traffic congestion is a major problem due to static signal timings that do not adapt to real-time traffic conditions.  
This project presents an **edge AI-based intelligent traffic control system** that dynamically adjusts traffic signal timing based on real-time vehicle density.

The system uses **YOLOv5 object detection** deployed on an edge device (Jetson Nano) to analyze traffic video and make decisions without relying on cloud infrastructure.

---

## 🎯 Objectives
- Detect vehicles in real-time using computer vision  
- Estimate traffic density using Region of Interest (ROI)  
- Dynamically adjust signal timing based on traffic conditions  
- Reduce congestion, waiting time, and fuel consumption  

---

## 🧠 System Pipeline
Video Input → YOLOv5 Detection → ROI Filtering → Vehicle Counting → Density Estimation → Signal Decision → LED Output


---

## ⚙️ Technologies Used

- **Python**  
- **OpenCV** (video processing)  
- **PyTorch** (model inference)  
- **YOLOv5** (object detection)  
- **Jetson Nano** (edge computing platform)  
- **Jetson.GPIO** (hardware interfacing)  

---

## 🚗 Key Features

- ✅ Real-time vehicle detection using YOLOv5  
- ✅ ROI-based filtering for accurate queue estimation  
- ✅ Density classification (Low / Medium / High)  
- ✅ Adaptive traffic signal control logic  
- ✅ Edge deployment (no cloud dependency)  
- ✅ Hardware simulation using LED traffic signals  

---

## 📊 Density Estimation Logic

| Vehicle Count | Density Level |
|--------------|-------------|
| 0 – 7        | LOW         |
| 8 – 15       | MEDIUM      |
| > 15         | HIGH        |

---

## 🚦 Signal Control Logic

| Density | Signal | Time Duration |
|--------|--------|--------------|
| LOW    | RED    | 15 seconds   |
| MEDIUM | YELLOW | 25 seconds   |
| HIGH   | GREEN  | 40 seconds   |

---

## 🔌 Hardware Implementation

The system simulates a traffic signal using LEDs connected to the Jetson Nano:

- 🔴 Red LED → Stop  
- 🟡 Yellow LED → Wait  
- 🟢 Green LED → Go  

Each LED is controlled via GPIO pins based on the decision logic.

---

## 📁 Project Structure
Edge-Traffic-Density-Control/
│
├── src/ # Main detection & control code
├── hardware/ # GPIO control module
├── data/ # Input traffic videos
├── demo/ # Demo video of working system
├── report/ # Project report (IEEE format)
├── presentation/ # PPT slides
├── README.md

---

## 🎥 Demo

A demonstration of the system is available in the `demo/` folder, showcasing:
- Real-time vehicle detection  
- Density estimation  
- Signal decision updates  
- Hardware (LED) response  

---

## 📄 Report

The complete project report (written in IEEE format) is available in the `report/` folder.

---

## 🧠 System Advantages

- 🚀 Real-time processing using edge AI  
- 💰 Low-cost implementation  
- 🔌 No dependency on internet/cloud  
- 📉 Reduces traffic congestion and idle time  
- 🌱 Helps reduce fuel consumption and emissions  

---

## 🚀 Future Scope

- Multi-lane traffic management  
- Reinforcement learning-based signal optimization  
- Integration with real-time CCTV systems  
- Smart city deployment  
- Vehicle priority (ambulance/fire truck detection)  

---

## 👨‍💻 Team Members

- Jessica Salonee  
- Gaurav  
- Vansh  

---

## 🧠 Conclusion

This project demonstrates how **edge AI can be effectively used to design intelligent traffic systems**.  
By combining computer vision, real-time processing, and control logic, the system provides a scalable solution for modern urban traffic management.

---