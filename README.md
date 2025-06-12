# DriecTo🚦 Smart Traffic Management System Using Edge Computing  
### *Google Solution Challenge 2025 – Open Innovation*

<p align="center">
  <img src="https://github.com/user-attachments/assets/51a3469b-7e6e-4f44-bc2d-94d94b8b4f04" height="400"/>
</p>

<p align="center">
  <a href="#overview">🌍 Overview</a> •
  <a href="#features">🔧 Features</a> •
  <a href="#tech-stack">🧠 Tech Stack</a> •
  <a href="#demo">📸 Demo</a> •
  <a href="#team">👥 Team</a>
</p>

---

## 🌍 Overview  
**DriecTo** is a revolutionary AI-powered traffic management system designed to **reduce urban traffic congestion by 40%**, **prioritize emergency vehicles**, and **predict traffic patterns** using **Edge Computing** and **Machine Learning**. Built for smart cities, this solution enables scalable, responsive traffic control without relying solely on cloud infrastructure.

### 🎯 Problem Statement
Urban traffic congestion increases travel time, fuel consumption, and pollution. Traditional traffic management relies on centralized processing, causing decision delays. A **real-time, low-latency, intelligent edge computing system** is needed to optimize traffic flow, enhance road safety, and reduce congestion.

---

## 🔧 Features

### 🛑 **Real-Time Signal Control**  
Uses live camera feeds and **YOLOv8 object detection** on edge devices (ESP32-CAM & Raspberry Pi) to control traffic lights based on vehicle density and type-weighted algorithms.

### 🚑 **Emergency Vehicle Prioritization**  
Detects emergency vehicles using **audio + visual recognition** and creates a **Green Corridor** by automatically altering signal states across intersections within seconds.

### 🚗 **Intelligent Vehicle Classification**  
Classifies two-wheelers, cars, buses, and trucks using **YOLOv8** to determine traffic weightage and manage green time efficiently based on vehicle priority.

### 🔮 **AI-Powered Traffic Forecasting**  
Uses **Gemini AI** and **LSTM models** to predict future traffic congestion with **91.4% accuracy** and optimize routing decisions before jams occur.

### 📱 **DriecTo Mobile App**  
- **🗺️ Navigation & Live Map**: Real-time traffic visualization with smart route suggestions over Google Maps
- **🎤 Voice-based Navigation**: Gemini AI-powered voice assistance for hands-free operation
- **📊 Traffic Data Analytics**: Comprehensive traffic insights and congestion heatmaps
- **📍 Real-time Location Updates**: Live updates for nearby locations and traffic conditions
- **🚨 SOS Emergency Call**: One-tap emergency calling system with location sharing
- **🏆 Smart Reward System**: Traffic reporting with credit-based incentives
- **📸 Number Plate Scanner**: AI-powered scanning for traffic violating vehicles
- **💰 Credit System**: Earn credits for successful traffic violation submissions
- **🎁 Voucher Redemption**: Redeem credits for vouchers from integrated store
- **🎨 Vehicle-Specific Themes**: Unique UI themes for different vehicle types (Green, Blue, Yellow)

### ☁️ **Firebase Cloud Integration**  
Syncs traffic data, alerts, and signal state information in real-time for seamless coordination between edge devices and mobile applications.

### 🎛️ ** Dashboard**  
Centralized monitoring, control, and analytics platform for traffic authorities with real-time insights and system management capabilities.

---

## 🧠 Tech Stack

<table>
<tr>
<td>

**🔧 Hardware**
- ESP32-CAM Modules
- Ultrasonic Sensors  
- Raspberry Pi 4
- Traffic Signal Controllers

</td>
<td>

**🤖 AI/ML**
- YOLOv8 (Object Detection)
- Gemini AI (Predictive Analytics)
- LSTM Models (Traffic Forecasting)
- Vertex AI (Image Processing)

</td>
</tr>
<tr>
<td>

**💻 Programming**
- Python (OpenCV, TensorFlow)
- C++ (Arduino IDE)
- Java (Android Studio)
- JavaScript (Web Dashboard)

</td>
<td>

**☁️ Cloud & Integration**
- Firebase (Realtime Database)
- Google Maps SDK
- Google Cloud Platform
- TTS API (Voice Alerts)

</td>
</tr>
</table>

---


### 🔄 How It Works

1. **📹 Detection**: ESP32-CAM captures live traffic footage
2. **🤖 Analysis**: YOLOv8 processes images for vehicle detection and classification
3. **⚖️ Calculation**: System calculates traffic density using type-weighted algorithms
4. **🚦 Control**: Dynamic signal timing adjustment based on real-time traffic
5. **🚨 Emergency**: Automatic detection and green corridor creation for emergency vehicles
6. **☁️ Sync**: Real-time data synchronization via Firebase
7. **📱 Display**: Live updates on mobile app and admin dashboard

---

## 🎯 Alignment with United Nations Sustainable Development Goals (SDGs)

<table>
<tr>
<td align="center">
<img src="https://github.com/user-attachments/assets/sdg11.png" width="60"><br>
<b>SDG 11: Sustainable Cities</b><br>
Smarter traffic flow and cleaner air quality
</td>
<td align="center">
<img src="https://github.com/user-attachments/assets/sdg3.png" width="60"><br>
<b>SDG 3: Good Health</b><br>
Faster emergency response saves lives
</td>
<td align="center">
<img src="https://github.com/user-attachments/assets/sdg9.png" width="60"><br>
<b>SDG 9: Infrastructure</b><br>
Next-gen smart road technology
</td>
</tr>
<tr>
<td align="center">
<img src="https://github.com/user-attachments/assets/sdg13.png" width="60"><br>
<b>SDG 13: Climate Action</b><br>
Reduced emissions via optimized traffic
</td>
<td align="center">
<img src="https://github.com/user-attachments/assets/sdg12.png" width="60"><br>
<b>SDG 12: Responsible Consumption</b><br>
Efficient resource utilization
</td>
<td align="center">
<img src="https://github.com/user-attachments/assets/sdg8.png" width="60"><br>
<b>SDG 8: Economic Growth</b><br>
Enhanced productivity and tech jobs
</td>
</tr>
</table>

---

## 📊 Impact Metrics

<table>
<tr>
<th>Metric</th>
<th>Before</th>
<th>After</th>
<th>Improvement</th>
</tr>
<tr>
<td>Average Stop Time</td>
<td>90 seconds</td>
<td>60 seconds</td>
<td>33% reduction</td>
</tr>
<tr>
<td>Emergency Response Time</td>
<td>45 seconds</td>
<td>25 seconds</td>
<td>44% faster</td>
</tr>
<tr>
<td>Traffic Prediction Accuracy</td>
<td>-</td>
<td>91.4%</td>
<td>New capability</td>
</tr>
<tr>
<td>User Satisfaction</td>
<td>-</td>
<td>4.5/5 ⭐</td>
<td>Excellent rating</td>
</tr>
</table>

---

## 📸 Demo & Screenshots

### 🎥 Video Demonstrations
> 📹 **System Demo**: https://youtu.be/QJwAbif5YDM?si=akkazuaz0P0DlBfw

### 📱 Mobile App Screenshots

<p align="center">
<img src= "https://github.com/user-attachments/assets/08ca2f15-90af-415c-8f33-51ccc63a182e" width="150"/>
<img src= "https://github.com/user-attachments/assets/252abb3e-210e-465a-acd2-66a302768aad" width="150"/>
<img src= "https://github.com/user-attachments/assets/3bbaf92d-8473-4824-a073-c44cb985d578" width="150"/>
<img src= "https://github.com/user-attachments/assets/b7ad2e2a-87ac-42b4-8fa3-6b3037ec5855" width="150"/>
<img src= "https://github.com/user-attachments/assets/ab58c05c-4696-496d-8587-1f1a56e48357" width="150"/>
</p>

**App Features Showcase:**
- 🗺️ **Navigation Interface**: Live traffic map with route optimization
- 📸 **Number Plate Scanner**: AI-powered violation detection system  
- 🏆 **Reward Dashboard**: Credit tracking and voucher redemption
- 🎨 **Vehicle Themes**: Customized UI for different vehicle types
- 🚨 **SOS Emergency**: Quick emergency calling with location sharing

---

## 🚀 Getting Started

### 📋 Prerequisites
- Arduino IDE with ESP32 board support
- Android Studio (latest version)
- Firebase account and project setup
- Google Cloud Platform account
- Python 3.8+ for ML components

---


## **Team Members**  
<p align="center">
    <a href="https://github.com/HarishMahto">
        <img src="https://github.com/HarishMahto.png" width="80" height="80" style="border-radius: 50%;" alt="HarishMahto">
    </a>
    <a href="https://github.com/Somie12">
        <img src="https://github.com/Somie12.png" width="80" height="80" style="border-radius: 50%;" alt="Somie12">
    </a>
    <a href="https://github.com/Diksha566">
        <img src="https://github.com/Diksha566.png" width="80" height="80" style="border-radius: 50%;" alt="Diksha566">
    </a>
    <a href="https://github.com/YashaswiniMishra">
        <img src="https://github.com/YashaswiniMishra.png" width="80" height="80" style="border-radius: 50%;" alt="YashaswiniMishra">
    </a>
    
    
</p>


## 📞 Contact & Support

<p align="center">
  <a href="harishmahto2003@gmail.com ">📧 Email</a> •
  <a href="https://www.linkedin.com/posts/diksha-jethwa_googlesolutionchallenge-gdg-hack2skill-activity-7329543678132125696-4ODu?utm_source=share&utm_medium=member_desktop&rcm=ACoAADpUZiEBoEaIJXontSnfGLSnC_V1kkrSsKQ">💼 LinkedIn</a> •
  <a href="https://github.com/yourusername/driecto-smart-traffic">💻 GitHub</a>
</p>

<p align="center">
  <b>🚦 Built with ❤️ by Team Gemini Coders for Google Solution Challenge 2025</b>
</p>

---

<p align="center">
  <i>Making cities smarter, one intersection at a time.</i>
</p>
