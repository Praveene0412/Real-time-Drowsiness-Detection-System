📌 Project Overview

Driver drowsiness is one of the major causes of road accidents worldwide. This project aims to detect driver fatigue in real time using a webcam and trigger alerts when drowsiness is identified.

The system continuously monitors the driver's eye movements using the Eye Aspect Ratio (EAR) method with Dlib facial landmarks. When the EAR value falls below a threshold for consecutive frames, the system:

Detects drowsiness
Plays an alarm sound
Captures screenshots
Sends Email notifications
Sends SMS alerts
Stores alert history in database
Displays monitoring information in a Flask dashboard
🚀 Features

✅ Real-time driver drowsiness detection
✅ Eye Aspect Ratio (EAR) based detection
✅ Facial landmark detection using Dlib
✅ Alarm alert system
✅ Screenshot capture during detection
✅ Email notifications using SMTP
✅ SMS notifications using Twilio
✅ Live location tracking using IP-based geolocation
✅ Flask web dashboard
✅ SQLite database integration
✅ Emergency contact management
✅ Alert history monitoring

🛠️ Technologies Used
Frontend
HTML
CSS
JavaScript
Backend
Python
Flask
Computer Vision & AI
OpenCV
Dlib
NumPy
Imutils
Database
SQLite
Notification Services
SMTP (Gmail)
Twilio API
Additional Libraries
Geopy
Requests
Playsound
🧠 Detection Methodology

The system uses Dlib’s 68 Facial Landmark Detector to identify eye coordinates from the webcam feed.

Eye Landmark Points
Right Eye → Points 36–41
Left Eye → Points 42–47

The Eye Aspect Ratio (EAR) is calculated using vertical and horizontal eye distances.

EAR Formula:

EAR=(∣∣p2−p6∣∣+∣∣p3−p5∣∣)/(2∣∣p1−p4∣∣)
Detection Logic
If EAR > Threshold → Eyes Open
If EAR < Threshold → Eyes Closed

When the EAR value remains below 0.25 for 30 consecutive frames, the system identifies drowsiness.

📂 Project Structure
Drowsiness-Detection-System/
│
├── app.py
├── realtime_detection.py
├── config.py
├── init_database.py
├── requirements_new.txt
├── README.md
├── drowsiness_data.db
│
├── templates/
│   ├── index.html
│   ├── setup.html
│   ├── dashboard.html
│   └── about.html
│
├── static/
│
├── Screenshots/
│
├── shape_predictor_68_face_landmarks.dat
└── sound1.mp3
⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/yourusername/drowsiness-detection-system.git
2️⃣ Open Project Folder
cd drowsiness-detection-system
3️⃣ Create Virtual Environment
Windows
python -m venv venv

Activate environment:

venv\Scripts\activate
4️⃣ Install Dependencies
pip install -r requirements_new.txt
5️⃣ Configure Email & SMS

Update config.py with:

Gmail App Password
Twilio SID
Twilio Auth Token
Twilio Phone Number
6️⃣ Initialize Database
python init_database.py
7️⃣ Run Flask Application
python app.py

Open browser:

http://127.0.0.1:5000
📸 Running Real-Time Detection

Run:

python realtime_detection.py

Controls:

Key	Action
q	Quit detection
r	Refresh location
t	Test notifications
📧 Email Notification Setup

To enable Email alerts:

Enable 2-Step Verification in Gmail
Generate Gmail App Password
Add App Password in config.py

Example:

EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your_email@gmail.com',
    'sender_password': 'your_app_password'
}
📱 SMS Notification Setup

Create a Twilio account and update:

SMS_CONFIG = {
    'account_sid': 'your_sid',
    'auth_token': 'your_token',
    'twilio_phone_number': '+1234567890'
}
🗄️ Database Tables
user_settings

Stores:

User email
Phone number
emergency_contacts

Stores:

Contact details
Relationship
drowsiness

Stores:

Timestamp
EAR value
Location
Notification status
🌐 Web Dashboard

The Flask dashboard provides:

Real-time monitoring
Alert history
Emergency contact management
User configuration
Detection controls
📈 Future Enhancements
Deep Learning based detection
CNN integration
Mobile application support
Cloud deployment
GPS hardware integration
Multi-driver detection
Higher accuracy under low lighting
⚠️ Limitations
Requires webcam access
Performance depends on lighting conditions
Cloud deployment cannot access local webcam
Current system works on local machine
🎯 Conclusion

This project successfully demonstrates a real-time AI-based drowsiness detection system using facial landmark detection and Eye Aspect Ratio analysis. The system helps improve driver safety by detecting fatigue early and providing immediate alerts and emergency notifications.

👨‍💻 Developed By

Praveen E

Sri Krishna Institute of Technology

📜 License

This project is developed for educational and research purposes.
