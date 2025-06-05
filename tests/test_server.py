#!/usr/bin/env python3
"""
Simple test server for PulseCare to verify page accessibility
"""

from flask import Flask, send_from_directory
import os
import json

# Load config
with open('config.json') as data_file:
    config = json.load(data_file)

app = Flask(__name__, static_url_path='')
app.secret_key = config.get('secret_key', 'test-secret-key')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/home.html')
def home_page():
    return app.send_static_file('index.html')

@app.route('/login.html')
def login_page():
    return app.send_static_file('login.html')

@app.route('/signup.html')
def signup_page():
    return app.send_static_file('signup.html')

@app.route('/dashboard.html')
def dashboard_page():
    return app.send_static_file('dashboard.html')

@app.route('/about_us.html')
def about_us():
    return app.send_static_file('about_us.html')

# Admin portal routes
@app.route('/admin/users.html')
def admin_users():
    return app.send_static_file('admin/users.html')

@app.route('/admin/patients.html')
def admin_patients():
    return app.send_static_file('admin/patients.html')

@app.route('/admin/health-records.html')
def admin_health_records():
    return app.send_static_file('admin/health-records.html')

# Doctor portal routes
@app.route('/doctor/patients.html')
def doctor_patients():
    return app.send_static_file('doctor/patients.html')

@app.route('/doctor/prescriptions.html')
def doctor_prescriptions():
    return app.send_static_file('doctor/prescriptions.html')

@app.route('/doctor/appointments.html')
def doctor_appointments():
    return app.send_static_file('doctor/appointments.html')

@app.route('/doctor/lab-tests.html')
def doctor_lab_tests():
    return app.send_static_file('doctor/lab-tests.html')

@app.route('/doctor/medical-notes.html')
def doctor_medical_notes():
    return app.send_static_file('doctor/medical-notes.html')

# Nurse portal routes
@app.route('/nurse/patients.html')
def nurse_patients():
    return app.send_static_file('nurse/patients.html')

@app.route('/nurse/vital-signs.html')
def nurse_vital_signs():
    return app.send_static_file('nurse/vital-signs.html')

@app.route('/nurse/assignments.html')
def nurse_assignments():
    return app.send_static_file('nurse/assignments.html')

@app.route('/nurse/nursing-notes.html')
def nurse_nursing_notes():
    return app.send_static_file('nurse/nursing-notes.html')

# Lab Technician portal routes
@app.route('/lab/tests.html')
def lab_tests():
    return app.send_static_file('lab/tests.html')

@app.route('/lab/pending-tests.html')
def lab_pending_tests():
    return app.send_static_file('lab/pending-tests.html')

@app.route('/lab/in-progress-tests.html')
def lab_in_progress_tests():
    return app.send_static_file('lab/in-progress-tests.html')

@app.route('/lab/test-results.html')
def lab_test_results():
    return app.send_static_file('lab/test-results.html')

@app.route('/lab/enter-results.html')
def lab_enter_results():
    return app.send_static_file('lab/enter-results.html')

# Pharmacist portal routes
@app.route('/pharmacy/prescriptions.html')
def pharmacy_prescriptions():
    return app.send_static_file('pharmacy/prescriptions.html')

@app.route('/pharmacy/dispense.html')
def pharmacy_dispense():
    return app.send_static_file('pharmacy/dispense.html')

@app.route('/pharmacy/inventory.html')
def pharmacy_inventory():
    return app.send_static_file('pharmacy/inventory.html')

@app.route('/pharmacy/history.html')
def pharmacy_history():
    return app.send_static_file('pharmacy/history.html')

# Patient portal routes
@app.route('/patient/health-records.html')
def patient_health_records():
    return app.send_static_file('patient/health-records.html')

@app.route('/patient/prescriptions.html')
def patient_prescriptions():
    return app.send_static_file('patient/prescriptions.html')

@app.route('/patient/appointments.html')
def patient_appointments():
    return app.send_static_file('patient/appointments.html')

@app.route('/patient/vital-signs.html')
def patient_vital_signs():
    return app.send_static_file('patient/vital-signs.html')

@app.route('/patient/lab-results.html')
def patient_lab_results():
    return app.send_static_file('patient/lab-results.html')

# Mock API endpoints for testing
@app.route('/common')
def common_api():
    return {"message": "Common API endpoint working"}

@app.route('/medication')
def medication_api():
    return [
        {"code": 1, "name": "Aspirin", "description": "Pain reliever"},
        {"code": 2, "name": "Ibuprofen", "description": "Anti-inflammatory"},
        {"code": 3, "name": "Acetaminophen", "description": "Pain reliever"}
    ]

@app.route('/department')
def department_api():
    return [
        {"department_id": 1, "name": "Cardiology"},
        {"department_id": 2, "name": "Neurology"},
        {"department_id": 3, "name": "Emergency"}
    ]

if __name__ == '__main__':
    print("🏥 Starting PulseCare Test Server...")
    print(f"Server will run on http://{config['host']}:{config['port']}")
    app.run(debug=True, host=config['host'], port=config['port'])
