#!/usr/bin/env python3
"""
Complete system setup: Users + Blockchain
"""

import sqlite3
import json
import hashlib
import time
import sys
import os

def simple_hash(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

def setup_users(conn):
    """Setup users in the database"""
    print("🔧 Setting up users...")
    
    # Create users table if it doesn't exist (just in case)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone_number TEXT,
            is_active INTEGER DEFAULT 1,
            entity_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Sample users data
    users_data = [
        ('admin', 'admin@hospital.com', 'admin123', 'admin', 'System', 'Administrator', '+1-555-0001', None),
        ('dr.smith', 'dr.smith@hospital.com', 'doctor123', 'doctor', 'John', 'Smith', '+1-555-0002', 1),
        ('dr.johnson', 'dr.johnson@hospital.com', 'doctor123', 'doctor', 'Sarah', 'Johnson', '+1-555-0003', 2),
        ('dr.williams', 'dr.williams@hospital.com', 'doctor123', 'doctor', 'Michael', 'Williams', '+1-555-0004', 1),
        ('nurse.emily', 'nurse.emily@hospital.com', 'nurse123', 'nurse', 'Emily', 'Davis', '+1-555-0005', 1),
        ('nurse.brown', 'nurse.brown@hospital.com', 'nurse123', 'nurse', 'Robert', 'Brown', '+1-555-0006', 2),
        ('nurse.wilson', 'nurse.wilson@hospital.com', 'nurse123', 'nurse', 'Lisa', 'Wilson', '+1-555-0007', 1),
        ('lab.chen', 'lab.chen@hospital.com', 'lab123', 'lab_technician', 'Michael', 'Chen', '+1-555-0008', None),
        ('lab.garcia', 'lab.garcia@hospital.com', 'lab123', 'lab_technician', 'Maria', 'Garcia', '+1-555-0009', None),
        ('pharm.wilson', 'pharm.wilson@hospital.com', 'pharm123', 'pharmacist', 'David', 'Wilson', '+1-555-0010', None),
        ('pharm.taylor', 'pharm.taylor@hospital.com', 'pharm123', 'pharmacist', 'Jennifer', 'Taylor', '+1-555-0011', None),
        ('patient.doe', 'patient.doe@email.com', 'patient123', 'patient', 'Jane', 'Doe', '+1-555-0012', 1),
        ('patient.jones', 'patient.jones@email.com', 'patient123', 'patient', 'Robert', 'Jones', '+1-555-0013', 2),
        ('patient.smith', 'patient.smith@email.com', 'patient123', 'patient', 'Mary', 'Smith', '+1-555-0014', 1),
        ('patient.davis', 'patient.davis@email.com', 'patient123', 'patient', 'James', 'Davis', '+1-555-0015', 2),
        ('patient.miller', 'patient.miller@email.com', 'patient123', 'patient', 'Patricia', 'Miller', '+1-555-0016', 1)
    ]
    
    created_count = 0
    for username, email, password, role, first_name, last_name, phone, entity_id in users_data:
        # Check if user exists
        existing = conn.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()
        
        if not existing:
            try:
                password_hash = simple_hash(password)
                user_id = conn.execute('''
                    INSERT INTO users (username, email, password_hash, role, first_name, last_name, phone_number, entity_id, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
                ''', (username, email, password_hash, role, first_name, last_name, phone, entity_id)).lastrowid
                
                created_count += 1
                print(f"   ✓ Created: {username} ({role}) - ID: {user_id}")
                
            except Exception as e:
                print(f"   ✗ Error creating {username}: {e}")
        else:
            print(f"   ℹ Exists: {username}")
    
    conn.commit()
    
    # Show all users
    users = conn.execute("SELECT user_id, username, role, first_name, last_name, is_active FROM users ORDER BY user_id").fetchall()
    print(f"\n📊 Total users in database: {len(users)}")
    print("   " + "="*70)
    
    role_counts = {}
    for user in users:
        role = user[2]
        role_counts[role] = role_counts.get(role, 0) + 1
        status = "Active" if user[5] else "Inactive"
        print(f"   ID: {user[0]:<3} | {user[1]:<20} | {user[2]:<15} | {user[3]} {user[4]:<15} | {status}")
    
    print(f"\n📈 Users by role:")
    for role, count in role_counts.items():
        print(f"   {role}: {count}")
    
    return len(users)

# Blockchain functionality removed

def main():
    print("🏥 Administrative Health Record Management System Setup")
    print("="*70)
    
    try:
        # Load config
        with open('config.json') as f:
            config = json.load(f)
        print(f"✓ Config loaded: {config['database']}")
        
        # Connect to database
        conn = sqlite3.connect(config['database'])
        conn.execute('pragma foreign_keys=ON')
        print("✓ Database connected")
        
        # Setup users
        user_count = setup_users(conn)
        
        # Blockchain functionality removed
        
        conn.close()
        
        print("\n" + "="*70)
        print("🎉 System setup completed successfully!")
        print(f"📊 {user_count} users available in the system")
        
        print("\n🔐 Login credentials for testing:")
        print("   Admin: admin / admin123")
        print("   Doctor: dr.smith / doctor123")
        print("   Nurse: nurse.emily / nurse123")
        print("   Lab Tech: lab.chen / lab123")
        print("   Pharmacist: pharm.wilson / pharm123")
        print("   Patient: patient.doe / patient123")
        
        print("\n🌐 Access the system:")
        print("   Main App: http://127.0.0.1:5001")
        print("   Login: http://127.0.0.1:5001/login.html")
        print("   Dashboard: http://127.0.0.1:5001/dashboard.html")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Ready to start the application!")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)
