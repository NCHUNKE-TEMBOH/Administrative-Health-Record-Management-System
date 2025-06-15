#!/usr/bin/env python3
"""
Check existing users in the database
"""

import sqlite3
import json

try:
    # Load config
    with open('config.json') as data_file:
        config = json.load(data_file)
    
    # Connect to database
    conn = sqlite3.connect(config['database'])
    conn.row_factory = sqlite3.Row
    
    # Check users
    users = conn.execute("SELECT user_id, username, role, first_name, last_name, is_active FROM users ORDER BY user_id").fetchall()
    
    print(f"Found {len(users)} users in database:")
    print("-" * 60)
    
    if users:
        for user in users:
            status = "Active" if user['is_active'] else "Inactive"
            print(f"ID: {user['user_id']:<3} | {user['username']:<15} | {user['role']:<15} | {user['first_name']} {user['last_name']} | {status}")
    else:
        print("No users found in database")
    
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
