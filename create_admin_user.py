#!/usr/bin/env python3
"""
Create admin user directly in the database
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

def create_admin_user():
    """Create admin user if it doesn't exist"""
    
    # Check if admin user already exists
    existing = conn.execute(
        "SELECT user_id FROM users WHERE username = 'admin' OR email = 'admin@hospital.com'"
    ).fetchone()
    
    if existing:
        print("Admin user already exists")
        return
    
    # Create admin user
    password_hash = generate_password_hash('admin123')
    
    try:
        user_id = conn.execute("""
            INSERT INTO users (username, email, password_hash, role, first_name, last_name, phone_number)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            'admin',
            'admin@hospital.com',
            password_hash,
            'admin',
            'System',
            'Administrator',
            '+1-555-0001'
        )).lastrowid
        
        conn.commit()
        print(f"Admin user created successfully with ID: {user_id}")
        print("Login credentials:")
        print("Username: admin")
        print("Password: admin123")
        
    except Exception as e:
        print(f"Error creating admin user: {e}")

if __name__ == "__main__":
    print("Creating admin user...")
    create_admin_user()
    conn.close()
    print("Done!")
