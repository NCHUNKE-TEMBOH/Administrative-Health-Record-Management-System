#!/usr/bin/env python3
"""
Initialize users for the system
"""

import sqlite3
import json
import hashlib

def simple_hash(password):
    """Simple password hashing for testing"""
    return hashlib.sha256(password.encode()).hexdigest()

def main():
    print("Initializing users...")
    
    # Load config
    with open('config.json') as f:
        config = json.load(f)
    
    # Connect to database
    conn = sqlite3.connect(config['database'])
    
    # Sample users
    users = [
        ('admin', 'admin@hospital.com', 'admin123', 'admin', 'System', 'Administrator', '+1-555-0001'),
        ('dr.smith', 'dr.smith@hospital.com', 'doctor123', 'doctor', 'John', 'Smith', '+1-555-0002'),
        ('nurse.williams', 'nurse.williams@hospital.com', 'nurse123', 'nurse', 'Emily', 'Williams', '+1-555-0003'),
        ('lab.chen', 'lab.chen@hospital.com', 'lab123', 'lab_technician', 'Michael', 'Chen', '+1-555-0004'),
        ('pharm.wilson', 'pharm.wilson@hospital.com', 'pharm123', 'pharmacist', 'David', 'Wilson', '+1-555-0005'),
        ('patient.doe', 'patient.doe@email.com', 'patient123', 'patient', 'Jane', 'Doe', '+1-555-0006'),
    ]
    
    for username, email, password, role, first_name, last_name, phone in users:
        # Check if user exists
        existing = conn.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()
        
        if not existing:
            try:
                # Try werkzeug first
                try:
                    from werkzeug.security import generate_password_hash
                    password_hash = generate_password_hash(password)
                except ImportError:
                    password_hash = simple_hash(password)
                
                user_id = conn.execute("""
                    INSERT INTO users (username, email, password_hash, role, first_name, last_name, phone_number, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 1)
                """, (username, email, password_hash, role, first_name, last_name, phone)).lastrowid
                
                conn.commit()
                print(f"✓ Created user: {username} ({role}) - ID: {user_id}")
                
            except Exception as e:
                print(f"✗ Error creating {username}: {e}")
        else:
            print(f"ℹ User {username} already exists")
    
    # Show all users
    users = conn.execute("SELECT user_id, username, role, first_name, last_name FROM users ORDER BY user_id").fetchall()
    print(f"\nTotal users: {len(users)}")
    for user in users:
        print(f"  {user[0]}: {user[1]} ({user[2]}) - {user[3]} {user[4]}")
    
    conn.close()
    print("\nUsers initialized!")

if __name__ == "__main__":
    main()
