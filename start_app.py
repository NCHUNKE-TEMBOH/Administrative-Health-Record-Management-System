#!/usr/bin/env python3
"""
Start the application with proper initialization
"""

import os
import sys
import sqlite3
import json
from werkzeug.security import generate_password_hash

def initialize_database():
    """Initialize database with sample users"""
    print("🔧 Initializing database...")
    
    try:
        # Load config
        with open('config.json') as f:
            config = json.load(f)
        
        # Connect to database
        conn = sqlite3.connect(config['database'])
        conn.execute('pragma foreign_keys=ON')
        
        # Check if admin user exists
        existing = conn.execute("SELECT user_id FROM users WHERE username = 'admin'").fetchone()
        
        if not existing:
            print("   Creating admin user...")
            password_hash = generate_password_hash('admin123')
            user_id = conn.execute("""
                INSERT INTO users (username, email, password_hash, role, first_name, last_name, phone_number)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ('admin', 'admin@hospital.com', password_hash, 'admin', 'System', 'Administrator', '+1-555-0001')).lastrowid
            
            conn.commit()
            print(f"   ✓ Admin user created (ID: {user_id})")
        else:
            print("   ✓ Admin user already exists")
        
        # Create a few sample users
        sample_users = [
            ('dr.smith', 'dr.smith@hospital.com', 'doctor123', 'doctor', 'John', 'Smith'),
            ('nurse.williams', 'nurse.williams@hospital.com', 'nurse123', 'nurse', 'Emily', 'Williams'),
            ('patient.doe', 'patient.doe@email.com', 'patient123', 'patient', 'Jane', 'Doe')
        ]
        
        for username, email, password, role, first_name, last_name in sample_users:
            existing = conn.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()
            if not existing:
                password_hash = generate_password_hash(password)
                user_id = conn.execute("""
                    INSERT INTO users (username, email, password_hash, role, first_name, last_name, phone_number, entity_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (username, email, password_hash, role, first_name, last_name, '+1-555-0000', 1)).lastrowid
                
                conn.commit()
                print(f"   ✓ User {username} created (ID: {user_id})")
        
        conn.close()
        print("✅ Database initialization completed!")
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def start_application():
    """Start the Flask application"""
    print("🚀 Starting application...")
    
    try:
        # Import and run the app
        from app import app, config
        
        host = config.get('host', '127.0.0.1')
        port = config.get('port', 5001)
        
        print(f"🏥 Administrative Health Record Management System")
        print(f"🌐 Server: http://{host}:{port}")
        print(f"🔐 Login credentials:")
        print(f"   Admin: admin / admin123")
        print(f"   Doctor: dr.smith / doctor123")
        print(f"   Nurse: nurse.williams / nurse123")
        print(f"   Patient: patient.doe / patient123")
        print(f"🏥 Health Records Dashboard: http://{host}:{port}/dashboard.html")
        print("=" * 60)
        
        app.run(host=host, port=port, debug=True)
        
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        import traceback
        traceback.print_exc()

def main():
    print("🏥 Administrative Health Record Management System")
    print("=" * 60)
    
    # Initialize database
    if not initialize_database():
        print("❌ Cannot start application due to database initialization failure")
        return
    
    # Start application
    start_application()

if __name__ == "__main__":
    main()
