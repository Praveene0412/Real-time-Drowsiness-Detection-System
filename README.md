# 🚗 Real-Time Drowsiness Detection System

This is an AI-based real-time drowsiness detection system that monitors driver alertness using Eye Aspect Ratio (EAR) and facial landmark detection. The system detects eye closure through a webcam and alerts the driver using alarms, Email, and SMS notifications along with live location tracking to improve road safety.

---

## ✨ Features

- 👁️ Real-Time Eye Monitoring using Webcam
- 🧠 Drowsiness Detection using Eye Aspect Ratio (EAR)
- 📍 Live Location Tracking using IP-based Geolocation
- 🔔 Alarm Alert System for Driver Warning
- 📧 Email Notification System using SMTP
- 📱 SMS Alerts using Twilio API
- 📸 Automatic Screenshot Capture during Detection
- 🌐 Flask Web Dashboard for Monitoring
- 🗄️ SQLite Database for Alert History & Contacts
- 👥 Emergency Contact Management

---

## 🛠️ Technologies Used

### 👨‍💻 Programming Language
- Python

### 🌐 Frontend
- HTML
- CSS
- JavaScript

### ⚙️ Backend
- Flask

### 🤖 Computer Vision & AI
- OpenCV
- Dlib
- NumPy
- Imutils

### 🗄️ Database
- SQLite

### 📡 Notification Services
- SMTP (Gmail)
- Twilio API

### 📍 Location Services
- Requests API
- Geopy

---

## 📂 Project Structure

```text
Drowsiness-Detection-System/
│
├── app.py
├── realtime_detection.py
├── config.py
├── init_database.py
├── requirements_new.txt
├── README.md
│
├── templates/
├── static/
├── Screenshots/
│
├── drowsiness_data.db
├── shape_predictor_68_face_landmarks.dat
└── sound1.mp3
```

---

## ▶️ How to Run

### 1️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### 2️⃣ Activate Environment

```bash
venv\Scripts\activate
```

### 3️⃣ Install Requirements

```bash
pip install -r requirements_new.txt
```

### 4️⃣ Initialize Database

```bash
python init_database.py
```

### 5️⃣ Run Flask Application

```bash
python app.py
```

Open in browser:

```text
http://127.0.0.1:5000
```

### 6️⃣ Start Real-Time Detection

```bash
python realtime_detection.py
```

---

## 📈 Future Enhancements

- 🤖 CNN-based Deep Learning Detection
- 📱 Mobile Application Integration
- ☁️ Cloud Deployment Support
- 🚘 Multi-Driver Monitoring
- 🌙 Improved Low-Light Detection
- 📊 Advanced Analytics Dashboard

---

## 🎯 Conclusion

This project successfully demonstrates a real-time AI-powered drowsiness detection system using computer vision and facial landmark analysis. The system helps improve driver safety by detecting fatigue early and sending instant alerts and emergency notifications.

---

## 👨‍💻 Developed By

**Praveene**  

Sri Krishna Institute of Technology
