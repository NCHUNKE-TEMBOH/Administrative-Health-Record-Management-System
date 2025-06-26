from flask import Flask, send_from_directory, request, jsonify
from flask_restful import Api
from prometheus_flask_exporter import PrometheusMetrics
import json
import os

# Load config once
with open('config.json') as data_file:
    config = json.load(data_file)

# Initialize Flask app once
app = Flask(__name__, static_url_path='')

# Set secret key
app.secret_key = config.get('secret_key', 'your-secret-key-change-this')

# Initialize Flask RESTful API on this app
api = Api(app)

# Import modules AFTER app created
from package.patient import Patients, Patient
from package.doctor import Doctors, Doctor
from package.appointment import Appointments, Appointment
from package.common import Common
from package.medication import Medication, Medications
from package.department import Departments, Department
from package.nurse import Nurse, Nurses
from package.room import Room, Rooms
from package.procedure import Procedure, Procedures
from package.prescribes import Prescribes, Prescribe
from package.undergoes import Undergoess, Undergoes

from package.user_management import UserLogin, UserProfile, Users, User, ChangePassword, UserRegistration
from package.health_records import HealthRecords, HealthRecord, VitalSigns
from package.lab_results import LabTests, LabTest, LabTestsByPatient, PendingLabTests
from package.prescriptions_enhanced import Prescriptions as PrescriptionsEnhanced, Prescription as PrescriptionEnhanced, MedicationDispensing
from package.medical_notes import MedicalNotes, MedicalNote, NursingNotes, PatientAssignments

from package.blockchain import Blockchain
import package.health_records as health_records_module

# Initialize blockchain once
blockchain = Blockchain(config['database'])
print(f"🔗 Blockchain initialized with {len(blockchain.chain)} blocks")

# Set blockchain instance for health records module
health_records_module.set_blockchain_instance(blockchain)

# Register API resources
api.add_resource(Patients, '/patient', '/patients')
api.add_resource(Patient, '/patient/<int:id>', '/patients/<int:id>')
api.add_resource(Doctors, '/doctor')
api.add_resource(Doctor, '/doctor/<int:id>')
api.add_resource(Appointments, '/appointment', '/appointments')
api.add_resource(Appointment, '/appointment/<int:id>', '/appointments/<int:id>')
api.add_resource(Common, '/common')
api.add_resource(Medications, '/medication')
api.add_resource(Medication, '/medication/<int:code>')
api.add_resource(Departments, '/department')
api.add_resource(Department, '/department/<int:department_id>')
api.add_resource(Nurses, '/nurse')
api.add_resource(Nurse, '/nurse/<int:id>')
api.add_resource(Rooms, '/room')
api.add_resource(Room, '/room/<int:room_no>')
api.add_resource(Procedures, '/procedure')
api.add_resource(Procedure, '/procedure/<int:code>')
api.add_resource(Prescribes, '/prescribes')
api.add_resource(Undergoess, '/undergoes')

api.add_resource(UserLogin, '/auth/login')
api.add_resource(UserRegistration, '/auth/register')
api.add_resource(UserProfile, '/auth/profile')
api.add_resource(ChangePassword, '/auth/change-password')
api.add_resource(Users, '/users')
api.add_resource(User, '/users/<int:user_id>')

api.add_resource(HealthRecords, '/health-records')
api.add_resource(HealthRecord, '/health-records/<int:record_id>')
api.add_resource(VitalSigns, '/vital-signs')

api.add_resource(LabTests, '/lab-tests')
api.add_resource(LabTest, '/lab-tests/<int:test_id>')
api.add_resource(LabTestsByPatient, '/lab-tests/patient/<int:patient_id>')
api.add_resource(PendingLabTests, '/lab-tests/pending')

api.add_resource(PrescriptionsEnhanced, '/prescriptions')
api.add_resource(PrescriptionEnhanced, '/prescriptions/<int:prescription_id>')
api.add_resource(MedicationDispensing, '/medication-dispensing')

api.add_resource(MedicalNotes, '/medical-notes')
api.add_resource(MedicalNote, '/medical-notes/<int:note_id>')
api.add_resource(NursingNotes, '/nursing-notes')
api.add_resource(PatientAssignments, '/patient-assignments')

# Static file routes
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
@app.route('/home.html')
def index():
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

# Debug Users endpoint
@app.route('/api/users-debug')
def get_users_debug():
    try:
        from package.model import conn
        users_rows = conn.execute("""
            SELECT user_id, username, email, role, first_name, last_name,
                   phone_number, is_active, created_date, last_login, entity_id
            FROM users
            WHERE is_active = 1
            ORDER BY created_date DESC
        """).fetchall()

        users = []
        for row in users_rows:
            users.append({
                'user_id': row['user_id'],
                'username': row['username'],
                'email': row['email'],
                'role': row['role'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'phone_number': row['phone_number'],
                'is_active': row['is_active'],
                'created_date': row['created_date'],
                'last_login': row['last_login'],
                'entity_id': row['entity_id']
            })

        return jsonify(users)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Blockchain API endpoints
@app.route('/api/blockchain/chain')
def get_blockchain_chain():
    try:
        if blockchain:
            return jsonify({
                'chain': blockchain.to_list(),
                'length': len(blockchain.chain),
                'valid': blockchain.is_chain_valid()
            })
        else:
            return jsonify({'error': 'Blockchain not initialized'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/blockchain/validate')
def validate_blockchain():
    try:
        if blockchain:
            is_valid = blockchain.is_chain_valid()
            stats = blockchain.get_blockchain_stats()
            return jsonify({
                'valid': is_valid,
                'stats': stats
            })
        else:
            return jsonify({'error': 'Blockchain not initialized'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/blockchain/stats')
def get_blockchain_stats():
    try:
        if blockchain:
            stats = blockchain.get_blockchain_stats()
            db_stats = blockchain.get_database_stats()
            return jsonify({
                'blockchain_stats': stats,
                'database_stats': db_stats
            })
        else:
            return jsonify({'error': 'Blockchain not initialized'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/blockchain/add', methods=['POST'])
def add_to_blockchain():
    try:
        if not blockchain:
            return jsonify({'error': 'Blockchain not initialized'}), 500

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        block = blockchain.add_block(data)
        return jsonify({
            'message': 'Block added successfully',
            'block': block.to_dict()
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Prometheus metrics setup
metrics = PrometheusMetrics(app, path="/metrics")

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', config.get('host', '0.0.0.0'))
    port = int(os.getenv('FLASK_PORT', config.get('port', 5001)))
    debug = os.getenv('FLASK_ENV', 'production') != 'production'

    print(f" Starting medicare Health Record Management System...")
    print(f" Server: http://{host}:{port}")
    print(f" Environment: {'Development' if debug else 'Production'}")

    app.run(host=host, port=port, debug=debug)
