"""
Test configuration and fixtures for the Administrative Health Record Management System
"""

import pytest
import tempfile
import os
import json
import sqlite3
from unittest.mock import patch
import sys

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from package.auth import generate_token


@pytest.fixture(scope="session")
def test_config():
    """Test configuration fixture"""
    return {
        "database": ":memory:",  # Use in-memory database for tests
        "secret_key": "test_secret_key_for_testing_only",
        "jwt_secret": "test_jwt_secret_for_testing_only",
        "testing": True
    }


@pytest.fixture(scope="session")
def test_database():
    """Create a test database with schema"""
    # Create temporary database file
    db_fd, db_path = tempfile.mkstemp()
    
    try:
        # Create database schema
        conn = sqlite3.connect(db_path)
        
        # Create all necessary tables
        schema_sql = """
        -- Users table
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            phone_number TEXT,
            is_active BOOLEAN DEFAULT 1,
            entity_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Patient table
        CREATE TABLE IF NOT EXISTS patient (
            pat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pat_first_name TEXT NOT NULL,
            pat_last_name TEXT NOT NULL,
            pat_insurance_no TEXT,
            pat_ph_no TEXT,
            pat_address TEXT,
            pat_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Doctor table
        CREATE TABLE IF NOT EXISTS doctor (
            doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_first_name TEXT NOT NULL,
            doc_last_name TEXT NOT NULL,
            doc_specialization TEXT,
            doc_ph_no TEXT,
            doc_address TEXT
        );

        -- Nurse table
        CREATE TABLE IF NOT EXISTS nurse (
            nurse_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nurse_first_name TEXT NOT NULL,
            nurse_last_name TEXT NOT NULL,
            nurse_ph_no TEXT,
            nurse_address TEXT
        );

        -- Appointment table
        CREATE TABLE IF NOT EXISTS appointment (
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_id INTEGER,
            appointment_date DATE,
            appointment_time TIME,
            status TEXT DEFAULT 'scheduled',
            reason TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patient(pat_id),
            FOREIGN KEY (doctor_id) REFERENCES doctor(doc_id)
        );

        -- Prescriptions table
        CREATE TABLE IF NOT EXISTS prescriptions (
            prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_id INTEGER,
            medication_name TEXT NOT NULL,
            dosage TEXT,
            frequency TEXT,
            duration TEXT,
            instructions TEXT,
            status TEXT DEFAULT 'active',
            prescribed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            start_date DATE,
            end_date DATE,
            FOREIGN KEY (patient_id) REFERENCES patient(pat_id),
            FOREIGN KEY (doctor_id) REFERENCES doctor(doc_id)
        );

        -- Lab tests table
        CREATE TABLE IF NOT EXISTS lab_tests (
            test_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            test_type TEXT,
            test_name TEXT,
            status TEXT DEFAULT 'pending',
            priority TEXT DEFAULT 'normal',
            ordered_by INTEGER,
            ordered_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_date TIMESTAMP,
            results TEXT,
            notes TEXT,
            FOREIGN KEY (patient_id) REFERENCES patient(pat_id),
            FOREIGN KEY (ordered_by) REFERENCES doctor(doc_id)
        );

        -- Health records table
        CREATE TABLE IF NOT EXISTS health_records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_id INTEGER,
            record_type TEXT,
            diagnosis TEXT,
            treatment TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patient(pat_id),
            FOREIGN KEY (doctor_id) REFERENCES doctor(doc_id)
        );

        -- Vital signs table
        CREATE TABLE IF NOT EXISTS vital_signs (
            vital_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            temperature REAL,
            blood_pressure_systolic INTEGER,
            blood_pressure_diastolic INTEGER,
            heart_rate INTEGER,
            respiratory_rate INTEGER,
            oxygen_saturation INTEGER,
            recorded_by INTEGER,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patient(pat_id),
            FOREIGN KEY (recorded_by) REFERENCES users(user_id)
        );

        -- Department table
        CREATE TABLE IF NOT EXISTS department (
            department_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            head_id INTEGER,
            FOREIGN KEY (head_id) REFERENCES doctor(doc_id)
        );

        -- Medication table
        CREATE TABLE IF NOT EXISTS medication (
            code INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            dosage_form TEXT,
            strength TEXT,
            manufacturer TEXT
        );

        -- Room table
        CREATE TABLE IF NOT EXISTS room (
            room_no INTEGER PRIMARY KEY,
            room_type TEXT,
            capacity INTEGER,
            status TEXT DEFAULT 'available',
            floor INTEGER,
            department_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES department(department_id)
        );

        -- Procedure table
        CREATE TABLE IF NOT EXISTS procedure (
            code INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT,
            duration INTEGER,
            cost REAL
        );
        """
        
        conn.executescript(schema_sql)
        conn.commit()
        conn.close()
        
        yield db_path
        
    finally:
        os.close(db_fd)
        os.unlink(db_path)


@pytest.fixture
def app_client(test_config, test_database):
    """Create a test client for the Flask app"""
    # Patch the config to use test database
    with patch('package.model.conn') as mock_conn:
        mock_conn.return_value = sqlite3.connect(test_database)

        app.config['TESTING'] = True
        app.config['DATABASE'] = test_database

        with app.test_client() as client:
            with app.app_context():
                yield client


@pytest.fixture
def sample_users():
    """Sample user data for testing"""
    return [
        {
            "username": "admin_test",
            "email": "admin@test.com",
            "password": "admin123",
            "role": "admin",
            "first_name": "Admin",
            "last_name": "User"
        },
        {
            "username": "doctor_test",
            "email": "doctor@test.com",
            "password": "doctor123",
            "role": "doctor",
            "first_name": "Dr. John",
            "last_name": "Smith"
        },
        {
            "username": "nurse_test",
            "email": "nurse@test.com",
            "password": "nurse123",
            "role": "nurse",
            "first_name": "Jane",
            "last_name": "Nurse"
        },
        {
            "username": "patient_test",
            "email": "patient@test.com",
            "password": "patient123",
            "role": "patient",
            "first_name": "John",
            "last_name": "Patient"
        }
    ]


@pytest.fixture
def sample_patients():
    """Sample patient data for testing"""
    return [
        {
            "pat_first_name": "Jane",
            "pat_last_name": "Doe",
            "pat_insurance_no": "INS123456",
            "pat_ph_no": "+1234567890",
            "pat_address": "123 Main St, City, State"
        },
        {
            "pat_first_name": "John",
            "pat_last_name": "Smith",
            "pat_insurance_no": "INS789012",
            "pat_ph_no": "+1234567891",
            "pat_address": "456 Oak Ave, City, State"
        }
    ]


@pytest.fixture
def sample_doctors():
    """Sample doctor data for testing"""
    return [
        {
            "doc_first_name": "Dr. John",
            "doc_last_name": "Smith",
            "doc_specialization": "Cardiology",
            "doc_ph_no": "+1234567890",
            "doc_address": "Hospital Address"
        },
        {
            "doc_first_name": "Dr. Sarah",
            "doc_last_name": "Johnson",
            "doc_specialization": "Neurology",
            "doc_ph_no": "+1234567891",
            "doc_address": "Hospital Address"
        }
    ]


@pytest.fixture
def auth_headers():
    """Generate authentication headers for testing"""
    def _auth_headers(user_data=None):
        if user_data is None:
            user_data = {
                "user_id": 1,
                "username": "admin_test",
                "role": "admin"
            }
        
        token = generate_token(user_data)
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    return _auth_headers


@pytest.fixture
def db_connection(test_database):
    """Provide a database connection for tests"""
    conn = sqlite3.connect(test_database)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


# Test data insertion helpers
def insert_test_user(conn, user_data):
    """Insert a test user into the database"""
    from werkzeug.security import generate_password_hash
    
    hashed_password = generate_password_hash(user_data['password'])
    
    cursor = conn.execute("""
        INSERT INTO users (username, email, password_hash, role, first_name, last_name)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_data['username'],
        user_data['email'],
        hashed_password,
        user_data['role'],
        user_data['first_name'],
        user_data['last_name']
    ))
    
    conn.commit()
    return cursor.lastrowid


def insert_test_patient(conn, patient_data):
    """Insert a test patient into the database"""
    cursor = conn.execute("""
        INSERT INTO patient (pat_first_name, pat_last_name, pat_insurance_no, pat_ph_no, pat_address)
        VALUES (?, ?, ?, ?, ?)
    """, (
        patient_data['pat_first_name'],
        patient_data['pat_last_name'],
        patient_data['pat_insurance_no'],
        patient_data['pat_ph_no'],
        patient_data['pat_address']
    ))
    
    conn.commit()
    return cursor.lastrowid


def insert_test_doctor(conn, doctor_data):
    """Insert a test doctor into the database"""
    cursor = conn.execute("""
        INSERT INTO doctor (doc_first_name, doc_last_name, doc_specialization, doc_ph_no, doc_address)
        VALUES (?, ?, ?, ?, ?)
    """, (
        doctor_data['doc_first_name'],
        doctor_data['doc_last_name'],
        doctor_data['doc_specialization'],
        doctor_data['doc_ph_no'],
        doctor_data['doc_address']
    ))
    
    conn.commit()
    return cursor.lastrowid
