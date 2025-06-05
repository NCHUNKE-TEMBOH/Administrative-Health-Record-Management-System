#!/usr/bin/env python3
"""
Database Schema Test for PulseCare Hospital Management System
Verifies all required tables exist and have proper structure
"""

import sqlite3
import json

# Load config
with open('config.json') as data_file:
    config = json.load(data_file)

def test_database_schema():
    """Test database schema and table structure"""
    print("🗄️ PulseCare Database Schema Test")
    print("="*50)
    
    # Connect to database
    conn = sqlite3.connect(config['database'])
    conn.row_factory = sqlite3.Row
    
    # Expected tables
    expected_tables = [
        'users', 'patient', 'doctor', 'nurse', 'appointment', 'medication',
        'department', 'room', 'procedure', 'prescribes', 'undergoes',
        'health_records', 'vital_signs', 'lab_tests', 'medical_notes',
        'nursing_notes', 'patient_assignments', 'prescriptions',
        'medication_dispensing', 'access_logs'
    ]
    
    # Get all tables
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    existing_tables = [table['name'] for table in tables]
    
    print(f"📋 Found {len(existing_tables)} tables in database:")
    for table in existing_tables:
        print(f"  ✓ {table}")
    
    # Check for missing tables
    missing_tables = [table for table in expected_tables if table not in existing_tables]
    if missing_tables:
        print(f"\n⚠️ Missing tables: {missing_tables}")
    else:
        print(f"\n✅ All expected tables present!")
    
    # Test table structures
    print(f"\n🔍 Testing table structures...")
    
    # Test users table
    try:
        users = conn.execute("SELECT COUNT(*) as count FROM users").fetchone()
        print(f"✓ Users table: {users['count']} records")
    except Exception as e:
        print(f"✗ Users table error: {e}")
    
    # Test patient table
    try:
        patients = conn.execute("SELECT COUNT(*) as count FROM patient").fetchone()
        print(f"✓ Patient table: {patients['count']} records")
    except Exception as e:
        print(f"✗ Patient table error: {e}")
    
    # Test health_records table
    try:
        health_records = conn.execute("SELECT COUNT(*) as count FROM health_records").fetchone()
        print(f"✓ Health records table: {health_records['count']} records")
    except Exception as e:
        print(f"✗ Health records table error: {e}")
    
    # Test vital_signs table
    try:
        vital_signs = conn.execute("SELECT COUNT(*) as count FROM vital_signs").fetchone()
        print(f"✓ Vital signs table: {vital_signs['count']} records")
    except Exception as e:
        print(f"✗ Vital signs table error: {e}")
    
    # Test prescriptions table
    try:
        prescriptions = conn.execute("SELECT COUNT(*) as count FROM prescriptions").fetchone()
        print(f"✓ Prescriptions table: {prescriptions['count']} records")
    except Exception as e:
        print(f"✗ Prescriptions table error: {e}")
    
    # Test lab_tests table
    try:
        lab_tests = conn.execute("SELECT COUNT(*) as count FROM lab_tests").fetchone()
        print(f"✓ Lab tests table: {lab_tests['count']} records")
    except Exception as e:
        print(f"✗ Lab tests table error: {e}")
    
    # Test patient_assignments table
    try:
        assignments = conn.execute("SELECT COUNT(*) as count FROM patient_assignments").fetchone()
        print(f"✓ Patient assignments table: {assignments['count']} records")
    except Exception as e:
        print(f"✗ Patient assignments table error: {e}")
    
    # Test foreign key constraints
    print(f"\n🔗 Testing foreign key relationships...")
    try:
        # Test user-patient relationship
        user_patients = conn.execute("""
            SELECT COUNT(*) as count 
            FROM users u 
            JOIN patient p ON u.entity_id = p.pat_id 
            WHERE u.role = 'patient'
        """).fetchone()
        print(f"✓ User-Patient relationships: {user_patients['count']} linked")
        
        # Test user-doctor relationship
        user_doctors = conn.execute("""
            SELECT COUNT(*) as count 
            FROM users u 
            JOIN doctor d ON u.entity_id = d.doc_id 
            WHERE u.role = 'doctor'
        """).fetchone()
        print(f"✓ User-Doctor relationships: {user_doctors['count']} linked")
        
        # Test user-nurse relationship
        user_nurses = conn.execute("""
            SELECT COUNT(*) as count 
            FROM users u 
            JOIN nurse n ON u.entity_id = n.nur_id 
            WHERE u.role = 'nurse'
        """).fetchone()
        print(f"✓ User-Nurse relationships: {user_nurses['count']} linked")
        
    except Exception as e:
        print(f"✗ Foreign key test error: {e}")
    
    # Summary
    print(f"\n📊 Database Schema Test Summary")
    print("="*50)
    print(f"Total tables found: {len(existing_tables)}")
    print(f"Expected tables: {len(expected_tables)}")
    print(f"Missing tables: {len(missing_tables)}")
    
    if len(missing_tables) == 0:
        print("✅ Database schema is complete and ready!")
    else:
        print("⚠️ Database schema has missing tables")
    
    conn.close()

if __name__ == "__main__":
    test_database_schema()
