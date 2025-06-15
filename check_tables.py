import sqlite3
import json

# Load config
with open('config.json') as f:
    config = json.load(f)

# Connect to database
conn = sqlite3.connect(config['database'])

# Get all table names
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("📋 Database Tables:")
for table in tables:
    print(f"   - {table[0]}")

print("\n🔍 Table Structures:")

# Check medication table structure
print("\n📊 MEDICATION table:")
try:
    medication_info = conn.execute("PRAGMA table_info(medication)").fetchall()
    for col in medication_info:
        print(f"   {col[1]} ({col[2]})")
except:
    print("   Table doesn't exist")

# Check prescriptions table structure
print("\n💊 PRESCRIPTIONS table:")
try:
    prescriptions_info = conn.execute("PRAGMA table_info(prescriptions)").fetchall()
    for col in prescriptions_info:
        print(f"   {col[1]} ({col[2]})")
except:
    print("   Table doesn't exist")

# Check users table
print("\n👥 USERS table:")
try:
    users_info = conn.execute("PRAGMA table_info(users)").fetchall()
    for col in users_info:
        print(f"   {col[1]} ({col[2]})")
except:
    print("   Table doesn't exist")

# Show sample data
print("\n📊 Sample Data:")

# Show medications
try:
    medications = conn.execute("SELECT * FROM medication LIMIT 3").fetchall()
    print(f"\nMedications ({len(medications)} shown):")
    for med in medications:
        print(f"   {med}")
except Exception as e:
    print(f"   Medications error: {e}")

# Show users count by role
try:
    user_counts = conn.execute("SELECT role, COUNT(*) as count FROM users GROUP BY role").fetchall()
    print(f"\nUsers by role:")
    for role in user_counts:
        print(f"   {role[0]}: {role[1]}")
except Exception as e:
    print(f"   Users error: {e}")

conn.close()
