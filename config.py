# Configuration file for Drowsiness Detection System
# Update these settings with your actual credentials

# Email Configuration (Gmail SMTP example)
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'abcd@gmail.com',  # Update with your email
    'sender_password': 'jdhfgshthfjrjejg',   # Use app password for Gmail
    'sender_name': 'web'
}

# SMS Configuration (Twilio example)
SMS_CONFIG = {
    'account_sid': 'AC407546ba2djd83juf3347b71ea4945a',  # Update with your Twilio SID
    'auth_token': '8c9beb4ede9fh49fh5jd83h5fe8c59ad',     # Update with your Twilio auth token
    'twilio_phone_number': '+12083533542'        # Update with your Twilio phone number
}

# Detection Settings
DETECTION_CONFIG = {
    'ear_threshold': 0.25,        # Eye Aspect Ratio threshold
    'consecutive_frames': 30,      # Number of frames to confirm drowsiness
    'camera_index': 0,            # Default camera index
    'frame_width': 450,           # Frame width for processing
    'screenshot_folder': 'Screenshots'
}

# Location Settings
LOCATION_CONFIG = {
    'update_interval': 30,        # Seconds between location updates
    'location_provider': 'ipinfo', # 'ipinfo' or 'gps'
    'ipinfo_token': None          # Optional: IPInfo API token for better accuracy
}

# Database Settings
DATABASE_CONFIG = {
    'database_name': 'drowsiness_data.db',
    'backup_enabled': True,
    'backup_interval': 3600       # Seconds between backups
}

# Notification Settings
NOTIFICATION_CONFIG = {
    'email_enabled': True,
    'sms_enabled': True,
    'notification_cooldown': 300, # Seconds between notifications (5 minutes)
    'max_notifications_per_hour': 10
}

# Web Application Settings
WEB_CONFIG = {
    'secret_key': 'change_this_secret_key_in_production',
    'debug_mode': True,
    'host': '127.0.0.1',
    'port': 5000
}

# Logging Settings
LOGGING_CONFIG = {
    'log_level': 'INFO',
    'log_file': 'drowsiness_detection.log',
    'max_log_size': 10485760,     # 10MB
    'backup_count': 5
}
