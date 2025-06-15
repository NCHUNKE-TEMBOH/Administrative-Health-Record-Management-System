#!/usr/bin/env python3
"""
Add sample data for prescriptions, medications, and other pharmacy data
"""

import sqlite3
import json
import datetime
from datetime import datetime, timedelta
import random

def add_sample_medications(conn):
    """Add sample medications to the database"""
    print("📋 Adding sample medications...")
    
    medications = [
        (1001, 'Lisinopril', 'Zestril', 'Hypertension treatment'),
        (1002, 'Metformin', 'Glucophage', 'Type 2 diabetes management'),
        (1003, 'Amlodipine', 'Norvasc', 'Blood pressure control'),
        (1004, 'Simvastatin', 'Zocor', 'Cholesterol management'),
        (1005, 'Omeprazole', 'Prilosec', 'Acid reflux treatment'),
        (1006, 'Aspirin', 'Bayer', 'Pain relief and blood thinning'),
        (1007, 'Amoxicillin', 'Amoxil', 'Bacterial infection treatment'),
        (1008, 'Ibuprofen', 'Advil', 'Pain and inflammation relief'),
        (1009, 'Acetaminophen', 'Tylenol', 'Pain and fever relief'),
        (1010, 'Hydrochlorothiazide', 'Microzide', 'Blood pressure and fluid retention')
    ]

    for code, name, brand, description in medications:
        try:
            conn.execute("""
                INSERT OR IGNORE INTO medication (code, name, brand, description)
                VALUES (?, ?, ?, ?)
            """, (code, name, brand, description))
        except Exception as e:
            print(f"   ⚠ Error adding medication {name}: {e}")
    
    conn.commit()
    print("   ✓ Sample medications added")

def add_sample_prescriptions(conn):
    """Add sample prescriptions"""
    print("💊 Adding sample prescriptions...")
    
    # Get patient and doctor IDs
    patients = conn.execute("SELECT user_id FROM users WHERE role = 'patient' LIMIT 5").fetchall()
    doctors = conn.execute("SELECT user_id FROM users WHERE role = 'doctor' LIMIT 3").fetchall()
    medications = conn.execute("SELECT code FROM medication LIMIT 10").fetchall()
    
    if not patients or not doctors or not medications:
        print("   ⚠ Missing required data (patients, doctors, or medications)")
        return
    
    prescriptions_data = [
        (1001, '10mg', 'Once daily', 'Take with food', 'active'),
        (1002, '500mg', 'Twice daily', 'Take with meals', 'active'),
        (1003, '5mg', 'Once daily', 'Take in the morning', 'active'),
        (1004, '20mg', 'Once daily at bedtime', 'Avoid grapefruit', 'active'),
        (1005, '20mg', 'Once daily before breakfast', 'Take on empty stomach', 'active'),
        (1006, '81mg', 'Once daily', 'Take with food to avoid stomach upset', 'active'),
        (1007, '500mg', 'Three times daily', 'Complete full course', 'dispensed'),
        (1008, '400mg', 'As needed for pain', 'Do not exceed 3 doses per day', 'active'),
        (1009, '500mg', 'Every 6 hours as needed', 'For fever and pain', 'dispensed'),
        (1010, '25mg', 'Once daily in morning', 'Monitor blood pressure', 'active')
    ]

    for i, (med_code, dosage, frequency, instructions, status) in enumerate(prescriptions_data):
        try:
            patient_id = patients[i % len(patients)]['user_id']
            doctor_id = doctors[i % len(doctors)]['user_id']

            # Create prescription date (within last 30 days)
            days_ago = random.randint(1, 30)
            prescribed_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')

            conn.execute("""
                INSERT INTO prescriptions (
                    pat_id, doc_id, med_code, dosage, frequency,
                    instructions, status, prescribed_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (patient_id, doctor_id, med_code, dosage, frequency, instructions, status, prescribed_date))
            
        except Exception as e:
            print(f"   ⚠ Error adding prescription {i+1}: {e}")
    
    conn.commit()
    print("   ✓ Sample prescriptions added")

def add_sample_dispensing_records(conn):
    """Add sample medication dispensing records"""
    print("🏪 Adding sample dispensing records...")
    
    # Get some prescriptions to create dispensing records
    prescriptions = conn.execute("""
        SELECT prescription_id, pat_id, med_code, dosage 
        FROM prescriptions 
        WHERE status = 'dispensed' 
        LIMIT 5
    """).fetchall()
    
    pharmacists = conn.execute("SELECT user_id FROM users WHERE role = 'pharmacist' LIMIT 2").fetchall()
    
    if not prescriptions or not pharmacists:
        print("   ⚠ No prescriptions or pharmacists found for dispensing records")
        return
    
    for prescription in prescriptions:
        try:
            pharmacist_id = pharmacists[0]['user_id']  # Use first pharmacist
            
            # Create dispensing date (within last 15 days)
            days_ago = random.randint(1, 15)
            dispensed_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')
            
            quantity = random.randint(30, 90)  # 30-90 day supply
            
            conn.execute("""
                INSERT OR IGNORE INTO medication_dispensing (
                    prescription_id, pharmacist_id, quantity_dispensed, 
                    dispensed_date, notes
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                prescription['prescription_id'],
                pharmacist_id,
                quantity,
                dispensed_date,
                f"Dispensed {quantity} tablets/capsules"
            ))
            
        except Exception as e:
            print(f"   ⚠ Error adding dispensing record: {e}")
    
    conn.commit()
    print("   ✓ Sample dispensing records added")

def add_sample_inventory(conn):
    """Add sample pharmacy inventory"""
    print("📦 Adding sample inventory...")
    
    medications = conn.execute("SELECT code, name FROM medication").fetchall()
    
    for medication in medications:
        try:
            stock_quantity = random.randint(50, 500)
            reorder_level = random.randint(20, 50)
            unit_cost = round(random.uniform(0.50, 25.00), 2)
            
            # Create expiry date (6 months to 2 years from now)
            days_future = random.randint(180, 730)
            expiry_date = (datetime.now() + timedelta(days=days_future)).strftime('%Y-%m-%d')
            
            conn.execute("""
                INSERT OR IGNORE INTO pharmacy_inventory (
                    med_code, stock_quantity, reorder_level, unit_cost,
                    expiry_date, last_updated
                )
                VALUES (?, ?, ?, ?, ?, datetime('now'))
            """, (
                medication['code'],
                stock_quantity,
                reorder_level,
                unit_cost,
                expiry_date
            ))
            
        except Exception as e:
            print(f"   ⚠ Error adding inventory for {medication['name']}: {e}")
    
    conn.commit()
    print("   ✓ Sample inventory added")

def create_pharmacy_tables(conn):
    """Create pharmacy-related tables if they don't exist"""
    print("🏗️ Creating pharmacy tables...")
    
    # Pharmacy inventory table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pharmacy_inventory (
            inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
            med_code TEXT NOT NULL,
            stock_quantity INTEGER NOT NULL DEFAULT 0,
            reorder_level INTEGER NOT NULL DEFAULT 10,
            unit_cost DECIMAL(10,2),
            expiry_date DATE,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (med_code) REFERENCES medication(med_code)
        )
    """)
    
    print("   ✓ Pharmacy tables created")

def main():
    print("🏥 Adding Sample Data for Pharmacy Dashboard")
    print("=" * 60)
    
    try:
        # Load config
        with open('config.json') as f:
            config = json.load(f)
        
        # Connect to database
        conn = sqlite3.connect(config['database'])
        conn.row_factory = sqlite3.Row
        
        # Create tables
        create_pharmacy_tables(conn)
        
        # Add sample data
        add_sample_medications(conn)
        add_sample_prescriptions(conn)
        add_sample_dispensing_records(conn)
        add_sample_inventory(conn)
        
        # Show summary
        print("\n📊 Summary:")
        
        # Count medications
        med_count = conn.execute("SELECT COUNT(*) as count FROM medication").fetchone()['count']
        print(f"   Medications: {med_count}")
        
        # Count prescriptions
        presc_count = conn.execute("SELECT COUNT(*) as count FROM prescriptions").fetchone()['count']
        print(f"   Prescriptions: {presc_count}")
        
        # Count by status
        status_counts = conn.execute("""
            SELECT status, COUNT(*) as count 
            FROM prescriptions 
            GROUP BY status
        """).fetchall()
        
        for status in status_counts:
            print(f"   - {status['status']}: {status['count']}")
        
        # Count dispensing records
        disp_count = conn.execute("SELECT COUNT(*) as count FROM medication_dispensing").fetchone()['count']
        print(f"   Dispensing records: {disp_count}")
        
        # Count inventory items
        inv_count = conn.execute("SELECT COUNT(*) as count FROM pharmacy_inventory").fetchone()['count']
        print(f"   Inventory items: {inv_count}")
        
        conn.close()
        
        print("\n✅ Sample data added successfully!")
        print("🏪 Pharmacy dashboard should now show data")
        print("👥 Admin dashboard should show all users")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
