import sqlite3
import json

# Load config
with open('config.json') as f:
    config = json.load(f)

# Connect to database
conn = sqlite3.connect(config['database'])

# Read and execute SQL
with open('insert_users.sql', 'r') as f:
    sql_script = f.read()

# Execute the SQL script
conn.executescript(sql_script)
conn.commit()

# Check results
users = conn.execute("SELECT user_id, username, role, first_name, last_name FROM users ORDER BY user_id").fetchall()
print(f"Total users: {len(users)}")
for user in users:
    print(f"  {user[0]}: {user[1]} ({user[2]}) - {user[3]} {user[4]}")

# Check system tables
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print(f"\nSystem tables: {len(tables)} total")

conn.close()
print("Done!")
