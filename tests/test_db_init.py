#!/usr/bin/env python3
"""
Simple database initialization test
"""

import sqlite3
import json
from werkzeug.security import generate_password_hash

def test_db_connection():
    """Test database connection and basic operations"""
    try:
        # Load config
        with open('config.json') as data_file:
            config = json.load(data_file)
        
        print(f"✓ Config loaded: {config['database']}")
        
        # Connect to database
        conn = sqlite3.connect(config['database'])
        conn.execute('pragma foreign_keys=ON')
        conn.row_factory = sqlite3.Row
        
        print("✓ Database connected")
        
        # Test if users table exists
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        table_names = [table[0] for table in tables]
        
        print(f"✓ Found {len(table_names)} tables: {', '.join(table_names)}")
        
        # Check if admin user exists
        admin_user = conn.execute("SELECT * FROM users WHERE username = 'admin'").fetchone()
        
        if admin_user:
            print(f"✓ Admin user exists: {admin_user['username']} ({admin_user['role']})")
        else:
            print("⚠ Admin user not found, creating...")
            
            # Create admin user
            password_hash = generate_password_hash('admin123')
            user_id = conn.execute("""
                INSERT INTO users (username, email, password_hash, role, first_name, last_name, phone_number)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ('admin', 'admin@hospital.com', password_hash, 'admin', 'System', 'Administrator', '+1-555-0001')).lastrowid
            
            conn.commit()
            print(f"✓ Admin user created with ID: {user_id}")
        
        # Test other sample users
        sample_users = [
            ('dr.smith', 'doctor123', 'doctor', 'John', 'Smith'),
            ('nurse.williams', 'nurse123', 'nurse', 'Emily', 'Williams'),
            ('patient.doe', 'patient123', 'patient', 'Jane', 'Doe')
        ]
        
        for username, password, role, first_name, last_name in sample_users:
            existing = conn.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()
            
            if not existing:
                password_hash = generate_password_hash(password)
                user_id = conn.execute("""
                    INSERT INTO users (username, email, password_hash, role, first_name, last_name, phone_number)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (username, f"{username}@hospital.com", password_hash, role, first_name, last_name, f"+1-555-000{len(sample_users)+2}")).lastrowid
                
                print(f"✓ Created user: {username} ({role}) - ID: {user_id}")
            else:
                print(f"✓ User exists: {username}")
        
        conn.commit()
        
        # Count users by role
        roles = conn.execute("SELECT role, COUNT(*) as count FROM users GROUP BY role").fetchall()
        print("\n📊 User Statistics:")
        for role in roles:
            print(f"  {role['role']}: {role['count']} users")
        
        conn.close()
        print("\n✅ Database initialization test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔧 Testing Database Initialization...")
    print("="*50)
    test_db_connection()
