#!/usr/bin/env python3
"""
Initialize the database with sample users for testing the Health Record Management System
"""

import sqlite3
import json
from werkzeug.security import generate_password_hash

# Load config
with open('../config.json') as data_file:
    config = json.load(data_file)

# Connect to database
conn = sqlite3.connect(config['database'])
conn.execute('pragma foreign_keys=ON')

def create_sample_users():
    """Create sample users for each role"""
    
    sample_users = [
        {
            'username': 'admin',
            'email': 'admin@hospital.com',
            'password': 'admin123',
            'role': 'admin',
            'first_name': 'System',
            'last_name': 'Administrator',
            'phone_number': '+1-555-0001',
            'entity_id': None
        },
        {
            'username': 'dr.smith',
            'email': 'dr.smith@hospital.com',
            'password': 'doctor123',
            'role': 'doctor',
            'first_name': 'John',
            'last_name': 'Smith',
            'phone_number': '+1-555-0002',
            'entity_id': 1  # Links to doctor table
        },
        {
            'username': 'dr.johnson',
            'email': 'dr.johnson@hospital.com',
            'password': 'doctor123',
            'role': 'doctor',
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'phone_number': '+1-555-0003',
            'entity_id': 2  # Links to doctor table
        },
        {
            'username': 'nurse.williams',
            'email': 'nurse.williams@hospital.com',
            'password': 'nurse123',
            'role': 'nurse',
            'first_name': 'Emily',
            'last_name': 'Williams',
            'phone_number': '+1-555-0004',
            'entity_id': 1  # Links to nurse table
        },
        {
            'username': 'nurse.brown',
            'email': 'nurse.brown@hospital.com',
            'password': 'nurse123',
            'role': 'nurse',
            'first_name': 'Michael',
            'last_name': 'Brown',
            'phone_number': '+1-555-0005',
            'entity_id': 2  # Links to nurse table
        },
        {
            'username': 'lab.tech1',
            'email': 'lab.tech1@hospital.com',
            'password': 'lab123',
            'role': 'lab_technician',
            'first_name': 'David',
            'last_name': 'Wilson',
            'phone_number': '+1-555-0006',
            'entity_id': None
        },
        {
            'username': 'pharmacist1',
            'email': 'pharmacist1@hospital.com',
            'password': 'pharm123',
            'role': 'pharmacist',
            'first_name': 'Lisa',
            'last_name': 'Davis',
            'phone_number': '+1-555-0007',
            'entity_id': None
        },
        {
            'username': 'patient.doe',
            'email': 'patient.doe@email.com',
            'password': 'patient123',
            'role': 'patient',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'phone_number': '+1-555-0008',
            'entity_id': 1  # Links to patient table
        },
        {
            'username': 'patient.jones',
            'email': 'patient.jones@email.com',
            'password': 'patient123',
            'role': 'patient',
            'first_name': 'Robert',
            'last_name': 'Jones',
            'phone_number': '+1-555-0009',
            'entity_id': 2  # Links to patient table
        }
    ]
    
    print("Creating sample users...")
    
    for user_data in sample_users:
        # Check if user already exists
        existing = conn.execute(
            "SELECT user_id FROM users WHERE username = ? OR email = ?",
            (user_data['username'], user_data['email'])
        ).fetchone()
        
        if existing:
            print(f"User {user_data['username']} already exists, skipping...")
            continue
        
        # Hash password
        password_hash = generate_password_hash(user_data['password'])
        
        # Insert user
        try:
            user_id = conn.execute("""
                INSERT INTO users (username, email, password_hash, role, first_name, last_name, phone_number, entity_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_data['username'],
                user_data['email'],
                password_hash,
                user_data['role'],
                user_data['first_name'],
                user_data['last_name'],
                user_data['phone_number'],
                user_data['entity_id']
            )).lastrowid
            
            print(f"Created user: {user_data['username']} ({user_data['role']}) - ID: {user_id}")
            
        except Exception as e:
            print(f"Error creating user {user_data['username']}: {e}")
    
    conn.commit()

def create_sample_data():
    """Create some sample data for testing"""
    
    print("\nCreating sample data...")
    
    # Sample doctors (if not exist)
    sample_doctors = [
        ('John', 'Smith', '+1-555-0002', '123 Medical St'),
        ('Sarah', 'Johnson', '+1-555-0003', '456 Health Ave')
    ]
    
    for doc in sample_doctors:
        existing = conn.execute(
            "SELECT doc_id FROM doctor WHERE doc_first_name = ? AND doc_last_name = ?",
            (doc[0], doc[1])
        ).fetchone()
        
        if not existing:
            doc_id = conn.execute(
                "INSERT INTO doctor (doc_first_name, doc_last_name, doc_ph_no, doc_address) VALUES (?, ?, ?, ?)",
                doc
            ).lastrowid
            print(f"Created doctor: {doc[0]} {doc[1]} - ID: {doc_id}")
    
    # Sample nurses (if not exist)
    sample_nurses = [
        ('Emily', 'Williams', '+1-555-0004', '789 Care Blvd'),
        ('Michael', 'Brown', '+1-555-0005', '321 Nursing Way')
    ]
    
    for nurse in sample_nurses:
        existing = conn.execute(
            "SELECT nur_id FROM nurse WHERE nur_first_name = ? AND nur_last_name = ?",
            (nurse[0], nurse[1])
        ).fetchone()
        
        if not existing:
            nurse_id = conn.execute(
                "INSERT INTO nurse (nur_first_name, nur_last_name, nur_ph_no, nur_address) VALUES (?, ?, ?, ?)",
                nurse
            ).lastrowid
            print(f"Created nurse: {nurse[0]} {nurse[1]} - ID: {nurse_id}")
    
    # Sample patients (if not exist)
    sample_patients = [
        ('Jane', 'Doe', 'INS001', '+1-555-0008', '111 Patient St'),
        ('Robert', 'Jones', 'INS002', '+1-555-0009', '222 Health Rd')
    ]
    
    for patient in sample_patients:
        existing = conn.execute(
            "SELECT pat_id FROM patient WHERE pat_first_name = ? AND pat_last_name = ?",
            (patient[0], patient[1])
        ).fetchone()
        
        if not existing:
            pat_id = conn.execute(
                "INSERT INTO patient (pat_first_name, pat_last_name, pat_insurance_no, pat_ph_no, pat_address) VALUES (?, ?, ?, ?, ?)",
                patient
            ).lastrowid
            print(f"Created patient: {patient[0]} {patient[1]} - ID: {pat_id}")
    
    # Sample medications (if not exist)
    sample_medications = [
        (1001, 'Aspirin', 'Bayer', 'Pain reliever and anti-inflammatory'),
        (1002, 'Amoxicillin', 'Generic', 'Antibiotic for bacterial infections'),
        (1003, 'Lisinopril', 'Prinivil', 'ACE inhibitor for blood pressure'),
        (1004, 'Metformin', 'Glucophage', 'Diabetes medication'),
        (1005, 'Ibuprofen', 'Advil', 'Pain reliever and anti-inflammatory')
    ]
    
    for med in sample_medications:
        existing = conn.execute("SELECT code FROM medication WHERE code = ?", (med[0],)).fetchone()
        
        if not existing:
            conn.execute(
                "INSERT INTO medication (code, name, brand, description) VALUES (?, ?, ?, ?)",
                med
            )
            print(f"Created medication: {med[1]} ({med[2]}) - Code: {med[0]}")
    
    # Sample departments (if not exist)
    sample_departments = [
        (1, 'Cardiology', 1),
        (2, 'Emergency Medicine', 2),
        (3, 'Internal Medicine', 1)
    ]
    
    for dept in sample_departments:
        existing = conn.execute("SELECT department_id FROM department WHERE department_id = ?", (dept[0],)).fetchone()
        
        if not existing:
            conn.execute(
                "INSERT INTO department (department_id, name, head_id) VALUES (?, ?, ?)",
                dept
            )
            print(f"Created department: {dept[1]} - ID: {dept[0]}")
    
    # Sample rooms (if not exist)
    sample_rooms = [
        (101, 'ICU', 1),
        (102, 'General Ward', 1),
        (201, 'Emergency Room', 1),
        (202, 'Surgery Room', 0)
    ]
    
    for room in sample_rooms:
        existing = conn.execute("SELECT room_no FROM room WHERE room_no = ?", (room[0],)).fetchone()
        
        if not existing:
            conn.execute(
                "INSERT INTO room (room_no, room_type, available) VALUES (?, ?, ?)",
                room
            )
            print(f"Created room: {room[0]} ({room[1]})")
    
    conn.commit()

def create_patient_assignments():
    """Create sample patient assignments for nurses"""
    
    print("\nCreating patient assignments...")
    
    # Get nurse and patient IDs
    nurses = conn.execute("SELECT user_id FROM users WHERE role = 'nurse'").fetchall()
    patients = conn.execute("SELECT pat_id FROM patient").fetchall()
    
    if nurses and patients:
        # Assign first patient to first nurse
        if len(nurses) > 0 and len(patients) > 0:
            existing = conn.execute(
                "SELECT assignment_id FROM patient_assignments WHERE nurse_id = ? AND pat_id = ?",
                (nurses[0][0], patients[0][0])
            ).fetchone()
            
            if not existing:
                conn.execute(
                    "INSERT INTO patient_assignments (nurse_id, pat_id, shift, notes) VALUES (?, ?, ?, ?)",
                    (nurses[0][0], patients[0][0], 'day', 'Primary care assignment')
                )
                print(f"Assigned patient {patients[0][0]} to nurse {nurses[0][0]}")
        
        # Assign second patient to second nurse (if available)
        if len(nurses) > 1 and len(patients) > 1:
            existing = conn.execute(
                "SELECT assignment_id FROM patient_assignments WHERE nurse_id = ? AND pat_id = ?",
                (nurses[1][0], patients[1][0])
            ).fetchone()
            
            if not existing:
                conn.execute(
                    "INSERT INTO patient_assignments (nurse_id, pat_id, shift, notes) VALUES (?, ?, ?, ?)",
                    (nurses[1][0], patients[1][0], 'evening', 'Evening shift care')
                )
                print(f"Assigned patient {patients[1][0]} to nurse {nurses[1][0]}")
    
    conn.commit()

def print_login_credentials():
    """Print login credentials for testing"""
    
    print("\n" + "="*60)
    print("SAMPLE LOGIN CREDENTIALS FOR TESTING")
    print("="*60)
    
    users = conn.execute("""
        SELECT username, role, first_name, last_name 
        FROM users 
        ORDER BY role, username
    """).fetchall()
    
    role_passwords = {
        'admin': 'admin123',
        'doctor': 'doctor123',
        'nurse': 'nurse123',
        'lab_technician': 'lab123',
        'pharmacist': 'pharm123',
        'patient': 'patient123'
    }
    
    current_role = None
    for user in users:
        username, role, first_name, last_name = user
        
        if role != current_role:
            print(f"\n{role.upper().replace('_', ' ')}:")
            print("-" * 30)
            current_role = role
        
        password = role_passwords.get(role, 'password123')
        print(f"Username: {username:<15} Password: {password:<12} ({first_name} {last_name})")
    
    print("\n" + "="*60)
    print("Access the system at: http://127.0.0.1:5001/login.html")
    print("="*60)

if __name__ == "__main__":
    print("Initializing Health Record Management System with sample data...")
    print("="*60)

    try:
        create_sample_users()
        create_sample_data()
        create_patient_assignments()
        print_login_credentials()

        print("\nDatabase initialization completed successfully!")

    except Exception as e:
        print(f"Error during initialization: {e}")
        import traceback
        traceback.print_exc()

    finally:
        conn.close()
