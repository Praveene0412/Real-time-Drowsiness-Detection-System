import cv2
import imutils
import datetime
import dlib
import os
import numpy as np
from playsound import playsound
import sqlite3
import requests
import json
import threading
import time
from geopy.geocoders import Nominatim
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class RealtimeDrowsinessDetector:
    def __init__(self):
        # Initialize database
        self.conn = sqlite3.connect('drowsiness_data.db', check_same_thread=False)
        self.c = self.conn.cursor()
        self.create_tables()
        
        # Detection parameters
        self.EAR_THRESHOLD = 0.25
        self.COUNTER = 0
        self.ALARM_ON = False
        
        # Initialize face detector
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        
        # Geolocation
        self.geolocator = Nominatim(user_agent="drowsiness_detector")
        self.current_location = None
        
        # User contacts (will be loaded from database)
        self.emergency_contacts = []
        self.user_email = ""
        
        # Load user settings
        self.load_user_settings()
        
    def create_tables(self):
        # Create drowsiness detection table
        self.c.execute('''CREATE TABLE IF NOT EXISTS drowsiness (
                     id INTEGER PRIMARY KEY,
                     timestamp DATETIME,
                     eye_aspect_ratio REAL,
                     location TEXT,
                     notified BOOLEAN DEFAULT 0
                     )''')
        
        # Create user contacts table
        self.c.execute('''CREATE TABLE IF NOT EXISTS emergency_contacts (
                     id INTEGER PRIMARY KEY,
                     name TEXT NOT NULL,
                     email TEXT,
                     phone TEXT,
                     relationship TEXT
                     )''')
        
        # Create user settings table
        self.c.execute('''CREATE TABLE IF NOT EXISTS user_settings (
                     id INTEGER PRIMARY KEY,
                     user_email TEXT,
                     user_phone TEXT,
                     notification_enabled BOOLEAN DEFAULT 1
                     )''')
        
        self.conn.commit()
    
    def load_user_settings(self):
        # Load emergency contacts
        self.c.execute("SELECT * FROM emergency_contacts")
        contacts = self.c.fetchall()
        self.emergency_contacts = [{'name': c[1], 'email': c[2], 'phone': c[3], 'relationship': c[4]} for c in contacts]
        
        # Load user settings
        self.c.execute("SELECT * FROM user_settings LIMIT 1")
        user_setting = self.c.fetchone()
        if user_setting:
            self.user_email = user_setting[1] or ""
    
    def get_current_location(self):
        """Get current location using IP-based geolocation"""
        try:
            # Using ipinfo.io for IP-based geolocation
            response = requests.get('https://ipinfo.io/json')
            data = response.json()
            
            location_str = f"{data.get('city', 'Unknown')}, {data.get('region', 'Unknown')}, {data.get('country', 'Unknown')}"
            coords = data.get('loc', '').split(',')
            
            if len(coords) == 2:
                lat, lon = coords
                self.current_location = {
                    'address': location_str,
                    'latitude': float(lat),
                    'longitude': float(lon),
                    'full_data': data
                }
            else:
                self.current_location = {'address': location_str, 'full_data': data}
                
            return self.current_location
        except Exception as e:
            print(f"Error getting location: {e}")
            return {'address': 'Location unavailable', 'full_data': {}}
    
    def eye_aspect_ratio(self, eye):
        """Calculate eye aspect ratio"""
        A = np.linalg.norm(eye[1] - eye[5])
        B = np.linalg.norm(eye[2] - eye[4])
        C = np.linalg.norm(eye[0] - eye[3])
        ear = (A + B) / (2.0 * C)
        return ear
    
    def send_emergency_notification(self, ear_value, timestamp):
        """Send emergency notifications to all contacts"""
        if not self.current_location:
            self.current_location = self.get_current_location()
        
        location_str = self.current_location.get('address', 'Unknown location')
        
        # Prepare message
        message = f"""
🚨 EMERGENCY ALERT - DROWSINESS DETECTED 🚨

Time: {timestamp}
Location: {location_str}
Eye Aspect Ratio: {ear_value:.3f}

The driver has been detected as drowsy and may be at risk of an accident. 
Please contact them immediately to ensure their safety.

System: Real-time Drowsiness Detection System
        """
        
        # Send notifications in separate threads
        for contact in self.emergency_contacts:
            if contact['email']:
                threading.Thread(target=self.send_email_alert, 
                               args=(contact['email'], contact['name'], message)).start()
            
            if contact['phone']:
                threading.Thread(target=self.send_sms_alert, 
                               args=(contact['phone'], message)).start()
        
        # Also send to user if email is configured
        if self.user_email:
            threading.Thread(target=self.send_email_alert, 
                           args=(self.user_email, "Driver", message)).start()
    
    def send_email_alert(self, to_email, recipient_name, message):
        """Send email notification"""
        try:
            from config import EMAIL_CONFIG
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            print(f"\n📧 Attempting email to: {to_email}")

            msg = MIMEMultipart()
            msg['From'] = EMAIL_CONFIG['sender_email']
            msg['To'] = to_email
            msg['Subject'] = "🚨 EMERGENCY: Drowsiness Detection Alert"

            msg.attach(MIMEText(message, 'plain'))

            server = smtplib.SMTP(
                EMAIL_CONFIG['smtp_server'],
                EMAIL_CONFIG['smtp_port']
            )

            server.starttls()

            print("🔐 Logging into Gmail...")

            server.login(
                EMAIL_CONFIG['sender_email'],
                EMAIL_CONFIG['sender_password']
            )

            print("📤 Sending message...")

            server.send_message(msg)

            server.quit()

            print(f"✅ Email successfully sent to {to_email}")

            return True

        except smtplib.SMTPAuthenticationError:
            print("❌ Gmail authentication failed")
            print("➡ Use Gmail App Password")
            return False

        except Exception as e:
            import traceback
            print(f"❌ Email sending failed: {e}")
            return False
    
    def send_sms_alert(self, phone_number, message):
        """Send SMS notification using Twilio"""
        try:
            # Import config
            from config import SMS_CONFIG
            
            from twilio.rest import Client
            
            # Initialize Twilio client
            client = Client(SMS_CONFIG['account_sid'], SMS_CONFIG['auth_token'])
            
            # Send SMS
            message_obj = client.messages.create(
                body=message,
                from_=SMS_CONFIG['twilio_phone_number'],
                to=phone_number
            )
            
            print(f"✅ SMS alert sent to {phone_number} (SID: {message_obj.sid})")
        except Exception as e:
            print(f"❌ Failed to send SMS to {phone_number}: {e}")
    
    def sound_alarm(self):
        """Play alarm sound"""
        try:
            playsound("sound1.mp3")
        except Exception as e:
            print(f"Error playing alarm: {e}")
    
    def capture_screenshot(self, frame, ear):
        """Capture screenshot with detection info"""
        output_folder = "Screenshots"
        os.makedirs(output_folder, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(output_folder, f"drowsiness_{timestamp}.png")
        
        # Add detection info to frame
        ear_text = f"EAR: {ear:.2f}"
        cv2.putText(frame, ear_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        if self.current_location:
            loc_text = f"Location: {self.current_location.get('address', 'Unknown')[:30]}..."
            cv2.putText(frame, loc_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imwrite(filename, frame)
        return filename
    
    def process_frame(self, frame):
        """Process a single frame for drowsiness detection"""
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = self.detector(gray, 0)
        
        drowsiness_detected = False
        
        for rect in rects:
            shape = self.predictor(gray, rect)
            shape_np = np.array([(shape.part(i).x, shape.part(i).y) for i in range(68)], dtype=int)
            
            left_eye = shape_np[42:48]
            right_eye = shape_np[36:42]
            
            left_ear = self.eye_aspect_ratio(left_eye)
            right_ear = self.eye_aspect_ratio(right_eye)
            ear = (left_ear + right_ear) / 2.0
            
            left_eye_hull = cv2.convexHull(left_eye)
            right_eye_hull = cv2.convexHull(right_eye)
            cv2.drawContours(frame, [left_eye_hull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [right_eye_hull], -1, (0, 255, 0), 1)
            
            if ear < self.EAR_THRESHOLD:
                self.COUNTER += 1
                if self.COUNTER >= 30:  # Drowsiness detected for 30 consecutive frames
                    if not self.ALARM_ON:
                        self.ALARM_ON = True
                        self.sound_alarm()
                        
                        # Get location and send notifications
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        screenshot_path = self.capture_screenshot(frame, ear)
                        
                        # Send emergency notifications
                        self.send_emergency_notification(ear, timestamp)
                        
                        # Log to database
                        location_str = self.current_location.get('address', 'Unknown') if self.current_location else 'Unknown'
                        self.c.execute("INSERT INTO drowsiness (timestamp, eye_aspect_ratio, location, notified) VALUES (?, ?, ?, ?)", 
                                     (timestamp, ear, location_str, 1))
                        self.conn.commit()
                    
                    cv2.putText(frame, "DROWSINESS DETECTED!", (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    drowsiness_detected = True
            else:
                self.COUNTER = 0
                self.ALARM_ON = False
            
            cv2.putText(frame, f"EAR: {ear:.2f}", (300, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        return frame, drowsiness_detected
    
    def start_detection(self):
        """Start real-time drowsiness detection"""
        # Get initial location
        self.current_location = self.get_current_location()
        print(f"Starting detection at location: {self.current_location.get('address', 'Unknown')}")
        
        # Initialize video capture
        vs = cv2.VideoCapture(0)
        
        # Check if camera opened successfully
        if not vs.isOpened():
            print("Error: Could not open camera.")
            return
        
        print("Detection started. Press 'q' to quit, 'r' to refresh location.")
        
        try:
            while True:
                ret, frame = vs.read()
                if not ret:
                    print("Error: Could not read frame from camera.")
                    break
                
                processed_frame, drowsiness_detected = self.process_frame(frame)
                
                # Display location info
                if self.current_location:
                    loc_text = f"Location: {self.current_location.get('address', 'Unknown')[:40]}..."
                    cv2.putText(processed_frame, loc_text, (10, processed_frame.shape[0] - 10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                # Add instructions on screen
                cv2.putText(processed_frame, "Press 'q' to quit, 'r' to refresh location", 
                           (10, processed_frame.shape[0] - 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
                
                cv2.imshow("Real-time Drowsiness Detection", processed_frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    print("Detection stopped by user.")
                    break
                elif key == ord("r"):  # Refresh location
                    self.current_location = self.get_current_location()
                    print(f"Location refreshed: {self.current_location.get('address', 'Unknown')}")
                elif key == ord("t"):  # Test notification
                    print("Testing emergency notification...")
                    self.send_emergency_notification(0.15, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        except KeyboardInterrupt:
            print("Detection interrupted by user.")
        except Exception as e:
            print(f"Error during detection: {e}")
        finally:
            print("Cleaning up resources...")
            vs.release()
            cv2.destroyAllWindows()
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()
            print("Detection stopped.")

# Global detector instance
detector = None

def start_detection():
    """Start detection function for Flask integration"""
    global detector
    detector = RealtimeDrowsinessDetector()
    detector.start_detection()

def add_emergency_contact(name, email, phone, relationship):
    """Add emergency contact to database"""
    conn = sqlite3.connect('drowsiness_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO emergency_contacts (name, email, phone, relationship) VALUES (?, ?, ?, ?)", 
             (name, email, phone, relationship))
    conn.commit()
    conn.close()

def update_user_settings(email, phone):
    """Update user settings"""
    conn = sqlite3.connect('drowsiness_data.db')
    c = conn.cursor()
    c.execute("DELETE FROM user_settings")
    c.execute("INSERT INTO user_settings (user_email, user_phone, notification_enabled) VALUES (?, ?, ?)", 
             (email, phone, 1))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    detector = RealtimeDrowsinessDetector()
    detector.start_detection()
