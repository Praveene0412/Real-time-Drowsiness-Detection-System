#!/usr/bin/env python3
"""
Database initialization script for Drowsiness Detection System
"""

import sqlite3
import os

def init_database():
    """Initialize the database with all required tables"""
    
    # Remove existing database if it exists
    if os.path.exists('drowsiness_data.db'):
        os.remove('drowsiness_data.db')
        print("Removed existing database")
    
    # Create new database connection
    conn = sqlite3.connect('drowsiness_data.db')
    c = conn.cursor()
    
    # Create user settings table
    c.execute('''CREATE TABLE user_settings (
                 id INTEGER PRIMARY KEY,
                 user_email TEXT,
                 user_phone TEXT,
                 notification_enabled BOOLEAN DEFAULT 1
                 )''')
    print("✓ Created user_settings table")
    
    # Create emergency contacts table
    c.execute('''CREATE TABLE emergency_contacts (
                 id INTEGER PRIMARY KEY,
                 name TEXT NOT NULL,
                 email TEXT,
                 phone TEXT,
                 relationship TEXT
                 )''')
    print("✓ Created emergency_contacts table")
    
    # Create drowsiness detection table
    c.execute('''CREATE TABLE drowsiness (
                 id INTEGER PRIMARY KEY,
                 timestamp DATETIME,
                 eye_aspect_ratio REAL,
                 location TEXT,
                 notified BOOLEAN DEFAULT 0
                 )''')
    print("✓ Created drowsiness table")
    
    # Insert default user settings
    c.execute("INSERT INTO user_settings (user_email, user_phone, notification_enabled) VALUES (?, ?, ?)", 
             ("", "", 1))
    print("✓ Inserted default user settings")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print("🎉 Database initialization completed successfully!")

def test_database():
    """Test database operations"""
    conn = sqlite3.connect('drowsiness_data.db')
    c = conn.cursor()
    
    # Test adding emergency contact
    c.execute("INSERT INTO emergency_contacts (name, email, phone, relationship) VALUES (?, ?, ?, ?)", 
             ("Test Contact", "test@example.com", "+1234567890", "Friend"))
    print("✓ Test emergency contact added")
    
    # Test updating user settings
    c.execute("DELETE FROM user_settings")
    c.execute("INSERT INTO user_settings (user_email, user_phone, notification_enabled) VALUES (?, ?, ?)", 
             ("user@example.com", "+0987654321", 1))
    print("✓ Test user settings updated")
    
    # Test adding drowsiness alert
    c.execute("INSERT INTO drowsiness (timestamp, eye_aspect_ratio, location, notified) VALUES (?, ?, ?, ?)", 
             ("2023-01-01 12:00:00", 0.15, "Test Location", 1))
    print("✓ Test drowsiness alert added")
    
    # View all data
    print("\n📊 Database Contents:")
    
    c.execute("SELECT * FROM user_settings")
    print("User Settings:", c.fetchone())
    
    c.execute("SELECT * FROM emergency_contacts")
    print("Emergency Contacts:", c.fetchall())
    
    c.execute("SELECT * FROM drowsiness")
    print("Drowsiness Alerts:", c.fetchall())
    
    conn.commit()
    conn.close()
    print("\n✅ Database test completed successfully!")

if __name__ == "__main__":
    print("🚀 Initializing Drowsiness Detection Database...")
    print("=" * 50)
    
    init_database()
    test_database()
    
    print("\n🎯 Database is ready for use!")
    print("You can now run the Flask application.")
