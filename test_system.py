#!/usr/bin/env python3
"""
Test script for the Real-time Drowsiness Detection System
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import cv2
        print("✓ OpenCV imported successfully")
    except ImportError as e:
        print(f"✗ OpenCV import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ NumPy imported successfully")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False
    
    try:
        import imutils
        print("✓ Imutils imported successfully")
    except ImportError as e:
        print(f"✗ Imutils import failed: {e}")
        return False
    
    try:
        import requests
        print("✓ Requests imported successfully")
    except ImportError as e:
        print(f"✗ Requests import failed: {e}")
        return False
    
    try:
        from geopy.geocoders import Nominatim
        print("✓ Geopy imported successfully")
    except ImportError as e:
        print(f"✗ Geopy import failed: {e}")
        return False
    
    try:
        import dlib
        print("✓ Dlib imported successfully")
    except ImportError as e:
        print(f"✗ Dlib import failed: {e}")
        return False
    
    try:
        from playsound import playsound
        print("✓ Playsound imported successfully")
    except ImportError as e:
        print(f"✗ Playsound import failed: {e}")
        return False
    
    try:
        import sqlite3
        print("✓ SQLite3 imported successfully")
    except ImportError as e:
        print(f"✗ SQLite3 import failed: {e}")
        return False
    
    return True

def test_database():
    """Test database creation and operations"""
    print("\nTesting database...")
    
    try:
        import sqlite3
        
        # Test database connection
        conn = sqlite3.connect('drowsiness_data.db')
        print("✓ Database connection successful")
        
        # Test table creation
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS test_table (
                     id INTEGER PRIMARY KEY,
                     test_data TEXT
                     )''')
        print("✓ Table creation successful")
        
        # Test data insertion
        c.execute("INSERT INTO test_table (test_data) VALUES (?)", ("test_data",))
        conn.commit()
        print("✓ Data insertion successful")
        
        # Test data retrieval
        c.execute("SELECT * FROM test_table")
        data = c.fetchone()
        print(f"✓ Data retrieval successful: {data}")
        
        # Clean up
        c.execute("DROP TABLE test_table")
        conn.commit()
        conn.close()
        print("✓ Database cleanup successful")
        
        return True
        
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_geolocation():
    """Test geolocation functionality"""
    print("\nTesting geolocation...")
    
    try:
        from geopy.geocoders import Nominatim
        import requests
        
        # Test IP-based geolocation
        response = requests.get('https://ipinfo.io/json', timeout=5)
        if response.status_code == 200:
            data = response.json()
            location_str = f"{data.get('city', 'Unknown')}, {data.get('region', 'Unknown')}"
            print(f"✓ IP-based geolocation successful: {location_str}")
        else:
            print("✗ IP-based geolocation failed")
            return False
        
        # Test Nominatim (optional)
        try:
            geolocator = Nominatim(user_agent="test_agent")
            location = geolocator.geocode("New York, NY")
            if location:
                print(f"✓ Nominatim geocoding successful: {location.address}")
            else:
                print("⚠ Nominatim geocoding returned no results")
        except Exception as e:
            print(f"⚠ Nominatim test failed (non-critical): {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ Geolocation test failed: {e}")
        return False

def test_camera():
    """Test camera access"""
    print("\nTesting camera access...")
    
    try:
        import cv2
        
        # Test camera initialization
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✓ Camera access successful")
            
            # Test frame capture
            ret, frame = cap.read()
            if ret:
                print(f"✓ Frame capture successful: {frame.shape}")
            else:
                print("✗ Frame capture failed")
                cap.release()
                return False
            
            cap.release()
            return True
        else:
            print("✗ Camera access failed - camera may be in use")
            return False
            
    except Exception as e:
        print(f"✗ Camera test failed: {e}")
        return False

def test_dlib_model():
    """Test dlib face landmark model"""
    print("\nTesting dlib model...")
    
    try:
        import dlib
        import os
        
        model_path = "shape_predictor_68_face_landmarks.dat"
        if os.path.exists(model_path):
            detector = dlib.get_frontal_face_detector()
            predictor = dlib.shape_predictor(model_path)
            print("✓ Dlib model loaded successfully")
            return True
        else:
            print(f"✗ Dlib model file not found: {model_path}")
            return False
            
    except Exception as e:
        print(f"✗ Dlib model test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("REAL-TIME DROWSINESS DETECTION SYSTEM TEST")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Database Test", test_database),
        ("Geolocation Test", test_geolocation),
        ("Camera Test", test_camera),
        ("Dlib Model Test", test_dlib_model)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
