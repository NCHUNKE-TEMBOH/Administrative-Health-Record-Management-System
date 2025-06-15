import sqlite3
import json
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from werkzeug.security import generate_password_hash
    print("✓ Werkzeug imported successfully")
except ImportError:
    print("✗ Werkzeug not available, using simple hash")
    def generate_password_hash(password):
        return f"simple_hash_{password}"

def main():
    print("Setting up users for Health Record Management System...")
    
    # Load config
    try:
        with open('config.json') as f:
            config = json.load(f)
        print(f"✓ Config loaded: {config['database']}")
    except Exception as e:
        print(f"✗ Error loading config: {e}")
        return
    
    # Connect to database
    try:
        conn = sqlite3.connect(config['database'])
        conn.execute('pragma foreign_keys=ON')
        print("✓ Database connected")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return
    
    # Create admin user
    try:
        # Check if admin exists
        existing = conn.execute("SELECT user_id FROM users WHERE username = 'admin'").fetchone()
        
        if existing:
            print("ℹ Admin user already exists")
        else:
            password_hash = generate_password_hash('admin123')
            user_id = conn.execute("""
                INSERT INTO users (username, email, password_hash, role, first_name, last_name, phone_number)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ('admin', 'admin@hospital.com', password_hash, 'admin', 'System', 'Administrator', '+1-555-0001')).lastrowid
            
            conn.commit()
            print(f"✓ Admin user created with ID: {user_id}")
            print("  Username: admin")
            print("  Password: admin123")
    
    except Exception as e:
        print(f"✗ Error creating admin user: {e}")
    
    # Create sample users
    sample_users = [
        ('dr.smith', 'dr.smith@hospital.com', 'doctor123', 'doctor', 'John', 'Smith', '+1-555-0002', 1),
        ('nurse.williams', 'nurse.williams@hospital.com', 'nurse123', 'nurse', 'Emily', 'Williams', '+1-555-0004', 1),
        ('lab.chen', 'lab.chen@hospital.com', 'lab123', 'lab_technician', 'Michael', 'Chen', '+1-555-0006', None),
        ('patient.doe', 'patient.doe@email.com', 'patient123', 'patient', 'Jane', 'Doe', '+1-555-0008', 1)
    ]
    
    for username, email, password, role, first_name, last_name, phone, entity_id in sample_users:
        try:
            existing = conn.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()
            
            if existing:
                print(f"ℹ User {username} already exists")
            else:
                password_hash = generate_password_hash(password)
                user_id = conn.execute("""
                    INSERT INTO users (username, email, password_hash, role, first_name, last_name, phone_number, entity_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (username, email, password_hash, role, first_name, last_name, phone, entity_id)).lastrowid
                
                conn.commit()
                print(f"✓ User {username} ({role}) created with ID: {user_id}")
        
        except Exception as e:
            print(f"✗ Error creating user {username}: {e}")
    
    # Show all users
    try:
        users = conn.execute("SELECT user_id, username, role, first_name, last_name FROM users ORDER BY user_id").fetchall()
        print(f"\n📊 Total users in database: {len(users)}")
        print("=" * 60)
        for user in users:
            print(f"ID: {user[0]:<3} | {user[1]:<15} | {user[2]:<15} | {user[3]} {user[4]}")
    except Exception as e:
        print(f"✗ Error listing users: {e}")
    
    conn.close()
    print("\n✅ Setup completed!")

if __name__ == "__main__":
    main()
