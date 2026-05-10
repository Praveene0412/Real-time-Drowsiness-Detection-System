from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
import sqlite3
import threading
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this for production

# Initialize database if it doesn't exist
def init_db():
    if not os.path.exists('drowsiness_data.db'):
        from init_database import init_database
        init_database()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/setup')
def setup():
    try:
        # Get user settings and contacts
        conn = sqlite3.connect('drowsiness_data.db')
        c = conn.cursor()
        
        # Get user settings
        c.execute("SELECT * FROM user_settings LIMIT 1")
        user_settings = c.fetchone()
        
        # Get emergency contacts
        c.execute("SELECT * FROM emergency_contacts ORDER BY id")
        contacts = c.fetchall()
        
        conn.close()
        
        return render_template('setup.html', 
                             user_settings=user_settings,
                             contacts=contacts)
    except Exception as e:
        print(f"Setup error: {e}")
        flash(f"Error loading setup page: {str(e)}", 'error')
        return render_template('setup.html', 
                             user_settings=None,
                             contacts=[])

@app.route('/dashboard')
def dashboard():
    try:
        # Get user settings and contacts
        conn = sqlite3.connect('drowsiness_data.db')
        c = conn.cursor()
        
        # Get user settings
        c.execute("SELECT * FROM user_settings LIMIT 1")
        user_settings = c.fetchone()
        
        # Get emergency contacts
        c.execute("SELECT * FROM emergency_contacts ORDER BY id")
        contacts = c.fetchall()
        
        # Get total count of alerts
        c.execute("SELECT COUNT(*) FROM drowsiness")
        total_alerts = c.fetchone()[0]
        
        # Get recent drowsiness alerts (last 10)
        c.execute("SELECT * FROM drowsiness ORDER BY timestamp DESC LIMIT 10")
        alerts = c.fetchall()
        
        conn.close()
        
        return render_template('dashboard.html', 
                             user_settings=user_settings,
                             contacts=contacts,
                             alerts=alerts)
    except Exception as e:
        print(f"Dashboard error: {e}")
        flash(f"Error loading dashboard: {str(e)}", 'error')
        return render_template('dashboard.html', 
                             user_settings=None,
                             contacts=[],
                             alerts=[])

@app.route('/start_detection')
def start_detection_route():
    try:
        # Import here to avoid circular imports
        from realtime_detection import start_detection
        
        # Start detection in a separate thread
        detection_thread = threading.Thread(target=start_detection)
        detection_thread.daemon = True
        detection_thread.start()
        
        # Return JSON for AJAX calls
        return jsonify({"message": "Real-time drowsiness detection started with geolocation and emergency notifications.", "status": "success"})
    except Exception as e:
        return jsonify({"error": f"Failed to start detection: {str(e)}", "status": "error"}), 500

@app.route('/detection_page')
def detection_page():
    """Dedicated page showing detection interface"""
    return render_template('detection_interface.html')

@app.route('/get_recent_alerts')
def get_recent_alerts():
    """Get recent alerts for dashboard auto-refresh"""
    try:
        conn = sqlite3.connect('drowsiness_data.db')
        c = conn.cursor()
        
        # Get total count of alerts
        c.execute("SELECT COUNT(*) FROM drowsiness")
        total_alerts = c.fetchone()[0]
        
        # Get recent 10 alerts
        c.execute("SELECT * FROM drowsiness ORDER BY timestamp DESC LIMIT 10")
        recent_alerts = c.fetchall()
        
        conn.close()
        
        # Format alerts for JSON response
        formatted_alerts = []
        for alert in recent_alerts:
            formatted_alerts.append({
                'timestamp': alert[1] if alert[1] else 'Unknown',
                'ear': alert[2] if alert[2] else 'N/A',
                'location': alert[3] if alert[3] else 'Unknown location'
            })
        
        return jsonify({
            'total_alerts': total_alerts,
            'recent_alerts': formatted_alerts
        })
    except Exception as e:
        print(f"Error getting recent alerts: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/add_contact', methods=['POST'])
def add_contact():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        relationship = request.form.get('relationship')
        
        print(f"Adding contact: {name}, {email}, {phone}, {relationship}")
        
        if name and (email or phone):
            # Import here to avoid circular imports
            from realtime_detection import add_emergency_contact
            add_emergency_contact(name, email, phone, relationship)
            flash('Emergency contact added successfully!', 'success')
            print("Contact added successfully")
        else:
            flash('Please provide at least name and either email or phone number.', 'error')
            print("Validation failed")
        
        return redirect(url_for('setup'))
    except Exception as e:
        print(f"Error adding contact: {e}")
        flash(f'Error adding contact: {str(e)}', 'error')
        return redirect(url_for('setup'))

@app.route('/update_settings', methods=['POST'])
def update_settings():
    try:
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        print(f"Updating settings: {email}, {phone}")
        
        # Import here to avoid circular imports
        from realtime_detection import update_user_settings
        update_user_settings(email, phone)
        flash('User settings updated successfully!', 'success')
        print("Settings updated successfully")
        
        return redirect(url_for('setup'))
    except Exception as e:
        print(f"Error updating settings: {e}")
        flash(f'Error updating settings: {str(e)}', 'error')
        return redirect(url_for('setup'))

@app.route('/delete_contact/<int:contact_id>', methods=['POST'])
def delete_contact(contact_id):
    try:
        conn = sqlite3.connect('drowsiness_data.db')
        c = conn.cursor()
        c.execute("DELETE FROM emergency_contacts WHERE id = ?", (contact_id,))
        conn.commit()
        conn.close()
        
        flash('Emergency contact deleted successfully!', 'success')
        print(f"Contact {contact_id} deleted successfully")
    except Exception as e:
        print(f"Error deleting contact: {e}")
        flash(f'Error deleting contact: {str(e)}', 'error')
    
    return redirect(url_for('setup'))

@app.route('/get_location')
def get_location():
    from realtime_detection import RealtimeDrowsinessDetector
    detector = RealtimeDrowsinessDetector()
    location = detector.get_current_location()
    return jsonify(location)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
