#!/usr/bin/env python3
"""
Simple script to initialize users in the database
"""

import sqlite3
import json
from werkzeug.security import generate_password_hash

# Load config
with open('config.json') as data_file:
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
            'entity_id': 1
        },
        {
            'username': 'dr.johnson',
            'email': 'dr.johnson@hospital.com',
            'password': 'doctor123',
            'role': 'doctor',
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'phone_number': '+1-555-0003',
            'entity_id': 2
        },
        {
            'username': 'nurse.williams',
            'email': 'nurse.williams@hospital.com',
            'password': 'nurse123',
            'role': 'nurse',
            'first_name': 'Emily',
            'last_name': 'Williams',
            'phone_number': '+1-555-0004',
            'entity_id': 1
        },
        {
            'username': 'nurse.brown',
            'email': 'nurse.brown@hospital.com',
            'password': 'nurse123',
            'role': 'nurse',
            'first_name': 'Michael',
            'last_name': 'Brown',
            'phone_number': '+1-555-0005',
            'entity_id': 2
        },
        {
            'username': 'lab.chen',
            'email': 'lab.chen@hospital.com',
            'password': 'lab123',
            'role': 'lab_technician',
            'first_name': 'Michael',
            'last_name': 'Chen',
            'phone_number': '+1-555-0006',
            'entity_id': None
        },
        {
            'username': 'pharm.wilson',
            'email': 'pharm.wilson@hospital.com',
            'password': 'pharm123',
            'role': 'pharmacist',
            'first_name': 'David',
            'last_name': 'Wilson',
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
            'entity_id': 1
        },
        {
            'username': 'patient.jones',
            'email': 'patient.jones@email.com',
            'password': 'patient123',
            'role': 'patient',
            'first_name': 'Robert',
            'last_name': 'Jones',
            'phone_number': '+1-555-0009',
            'entity_id': 2
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

if __name__ == "__main__":
    print("Initializing users...")
    print("="*50)

    try:
        create_sample_users()
        print("\nUser initialization completed successfully!")
        
        # Show created users
        users = conn.execute("SELECT username, role, first_name, last_name FROM users ORDER BY user_id").fetchall()
        print(f"\nTotal users in database: {len(users)}")
        for user in users:
            print(f"- {user[0]} ({user[1]}): {user[2]} {user[3]}")

    except Exception as e:
        print(f"Error during initialization: {e}")
        import traceback
        traceback.print_exc()

    finally:
        conn.close()
