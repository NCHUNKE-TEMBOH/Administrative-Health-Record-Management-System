import sqlite3
import json

# Load config
with open('config.json') as f:
    config = json.load(f)

# Connect to database
conn = sqlite3.connect(config['database'])

# Simple password hash (for demo purposes)
def simple_hash(password):
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

# Create users directly
users_sql = """
INSERT OR IGNORE INTO users (username, email, password_hash, role, first_name, last_name, phone_number, is_active) VALUES
('admin', 'admin@hospital.com', ?, 'admin', 'System', 'Administrator', '+1-555-0001', 1),
('dr.smith', 'dr.smith@hospital.com', ?, 'doctor', 'John', 'Smith', '+1-555-0002', 1),
('dr.johnson', 'dr.johnson@hospital.com', ?, 'doctor', 'Sarah', 'Johnson', '+1-555-0003', 1),
('nurse.williams', 'nurse.williams@hospital.com', ?, 'nurse', 'Emily', 'Williams', '+1-555-0004', 1),
('nurse.brown', 'nurse.brown@hospital.com', ?, 'nurse', 'Michael', 'Brown', '+1-555-0005', 1),
('lab.chen', 'lab.chen@hospital.com', ?, 'lab_technician', 'Michael', 'Chen', '+1-555-0006', 1),
('pharm.wilson', 'pharm.wilson@hospital.com', ?, 'pharmacist', 'David', 'Wilson', '+1-555-0007', 1),
('patient.doe', 'patient.doe@email.com', ?, 'patient', 'Jane', 'Doe', '+1-555-0008', 1),
('patient.jones', 'patient.jones@email.com', ?, 'patient', 'Robert', 'Jones', '+1-555-0009', 1),
('patient.smith', 'patient.smith@email.com', ?, 'patient', 'Mary', 'Smith', '+1-555-0010', 1)
"""

# Hash passwords
passwords = ['admin123', 'doctor123', 'doctor123', 'nurse123', 'nurse123', 'lab123', 'pharm123', 'patient123', 'patient123', 'patient123']
hashed_passwords = [simple_hash(pwd) for pwd in passwords]

try:
    conn.execute(users_sql, hashed_passwords)
    conn.commit()
    print("✓ Users created successfully!")
    
    # Show created users
    users = conn.execute("SELECT user_id, username, role, first_name, last_name, is_active FROM users ORDER BY user_id").fetchall()
    print(f"\nTotal users in database: {len(users)}")
    print("-" * 80)
    for user in users:
        status = "Active" if user[5] else "Inactive"
        print(f"ID: {user[0]:<3} | {user[1]:<20} | {user[2]:<15} | {user[3]} {user[4]:<15} | {status}")
    
    print("\n🎉 User creation completed!")
    print("\nLogin credentials:")
    print("Admin: admin / admin123")
    print("Doctor: dr.smith / doctor123")
    print("Nurse: nurse.williams / nurse123")
    print("Lab Tech: lab.chen / lab123")
    print("Pharmacist: pharm.wilson / pharm123")
    print("Patient: patient.doe / patient123")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    conn.close()
