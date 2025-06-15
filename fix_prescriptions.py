#!/usr/bin/env python3
"""
Fix prescriptions data and add more sample data
"""

import sqlite3
import json
import datetime
from datetime import datetime, timedelta
import random

def add_prescriptions_with_duration(conn):
    """Add prescriptions with proper duration field"""
    print("💊 Adding prescriptions with duration...")
    
    # Get patient and doctor IDs
    patients = conn.execute("SELECT user_id FROM users WHERE role = 'patient' LIMIT 5").fetchall()
    doctors = conn.execute("SELECT user_id FROM users WHERE role = 'doctor' LIMIT 3").fetchall()
    
    if not patients or not doctors:
        print("   ⚠ Missing patients or doctors")
        return
    
    prescriptions_data = [
        (1001, '10mg', 'Once daily', '30 days', 'Take with food', 'active'),
        (1002, '500mg', 'Twice daily', '90 days', 'Take with meals', 'active'),
        (1003, '5mg', 'Once daily', '30 days', 'Take in the morning', 'active'),
        (1004, '20mg', 'Once daily at bedtime', '30 days', 'Avoid grapefruit', 'active'),
        (1005, '20mg', 'Once daily before breakfast', '30 days', 'Take on empty stomach', 'active'),
        (1006, '81mg', 'Once daily', '90 days', 'Take with food to avoid stomach upset', 'active'),
        (1007, '500mg', 'Three times daily', '10 days', 'Complete full course', 'dispensed'),
        (1008, '400mg', 'As needed for pain', '30 days', 'Do not exceed 3 doses per day', 'active'),
        (1009, '500mg', 'Every 6 hours as needed', '7 days', 'For fever and pain', 'dispensed'),
        (1010, '25mg', 'Once daily in morning', '30 days', 'Monitor blood pressure', 'active'),
        (145, '500mg', 'Every 8 hours', '5 days', 'Take with water', 'active'),
        (423, '300mg', 'Every 8 weeks', '1 year', 'Infusion therapy', 'active'),
        (673, '1000mg', 'Twice daily', '90 days', 'Take with meals', 'active'),
        (1001, '5mg', 'Once daily', '30 days', 'Monitor blood pressure', 'pending'),
        (1002, '850mg', 'Twice daily', '90 days', 'Take with food', 'pending')
    ]
    
    for i, (med_code, dosage, frequency, duration, instructions, status) in enumerate(prescriptions_data):
        try:
            patient_id = patients[i % len(patients)]['user_id']
            doctor_id = doctors[i % len(doctors)]['user_id']
            
            # Create prescription date (within last 30 days)
            days_ago = random.randint(1, 30)
            prescribed_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
            
            # Calculate start and end dates
            start_date = prescribed_date
            if 'days' in duration:
                days = int(duration.split()[0])
                end_date = (datetime.strptime(prescribed_date, '%Y-%m-%d') + timedelta(days=days)).strftime('%Y-%m-%d')
            elif 'weeks' in duration:
                weeks = int(duration.split()[0])
                end_date = (datetime.strptime(prescribed_date, '%Y-%m-%d') + timedelta(weeks=weeks)).strftime('%Y-%m-%d')
            elif 'year' in duration:
                end_date = (datetime.strptime(prescribed_date, '%Y-%m-%d') + timedelta(days=365)).strftime('%Y-%m-%d')
            else:
                end_date = (datetime.strptime(prescribed_date, '%Y-%m-%d') + timedelta(days=30)).strftime('%Y-%m-%d')
            
            refills = random.randint(0, 3) if status == 'active' else 0
            
            conn.execute("""
                INSERT INTO prescriptions (
                    pat_id, doc_id, med_code, dosage, frequency, duration,
                    instructions, status, prescribed_date, start_date, end_date, refills_remaining
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (patient_id, doctor_id, med_code, dosage, frequency, duration, 
                  instructions, status, prescribed_date, start_date, end_date, refills))
            
            print(f"   ✓ Added prescription {i+1}: {med_code} for patient {patient_id}")
            
        except Exception as e:
            print(f"   ⚠ Error adding prescription {i+1}: {e}")
    
    conn.commit()
    print("   ✓ Prescriptions added successfully")

def main():
    print("🏥 Fixing Prescriptions Data")
    print("=" * 40)
    
    try:
        # Load config
        with open('config.json') as f:
            config = json.load(f)
        
        # Connect to database
        conn = sqlite3.connect(config['database'])
        conn.row_factory = sqlite3.Row
        
        # Add prescriptions with duration
        add_prescriptions_with_duration(conn)
        
        # Show summary
        print("\n📊 Updated Summary:")
        
        # Count prescriptions by status
        status_counts = conn.execute("""
            SELECT status, COUNT(*) as count 
            FROM prescriptions 
            GROUP BY status
        """).fetchall()
        
        total_prescriptions = sum(row['count'] for row in status_counts)
        print(f"   Total Prescriptions: {total_prescriptions}")
        
        for status in status_counts:
            print(f"   - {status['status']}: {status['count']}")
        
        # Count users by role
        user_counts = conn.execute("""
            SELECT role, COUNT(*) as count 
            FROM users 
            WHERE is_active = 1
            GROUP BY role
        """).fetchall()
        
        total_users = sum(row['count'] for row in user_counts)
        print(f"\n   Total Active Users: {total_users}")
        
        for role in user_counts:
            print(f"   - {role['role']}: {role['count']}")
        
        conn.close()
        
        print("\n✅ Data fixed successfully!")
        print("🏪 Pharmacist dashboard should now show prescriptions")
        print("👥 Admin dashboard should show all users")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
