#!/usr/bin/env python3
"""
Test the users API to see if it's working
"""

import requests
import json

def test_users_api():
    base_url = "http://127.0.0.1:5001"
    
    print("🧪 Testing Users API")
    print("=" * 40)
    
    # First, let's try to login as admin
    print("1. Testing admin login...")
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    session = requests.Session()
    
    try:
        login_response = session.post(f"{base_url}/auth/login", json=login_data, timeout=10)
        print(f"   Login status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            print("   ✓ Admin login successful")
            
            # Now test the users endpoint
            print("\n2. Testing /users endpoint...")
            users_response = session.get(f"{base_url}/users", timeout=10)
            print(f"   Users API status: {users_response.status_code}")
            
            if users_response.status_code == 200:
                users_data = users_response.json()
                print(f"   ✓ Found {len(users_data)} users")
                
                # Show first few users
                for i, user in enumerate(users_data[:5]):
                    print(f"   User {i+1}: {user.get('username')} ({user.get('role')}) - {user.get('first_name')} {user.get('last_name')}")
                
                if len(users_data) > 5:
                    print(f"   ... and {len(users_data) - 5} more users")
                    
                return True
            else:
                print(f"   ✗ Users API failed: {users_response.text}")
                return False
        else:
            print(f"   ✗ Admin login failed: {login_response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Connection error: {e}")
        return False

def test_direct_database():
    """Test direct database access"""
    print("\n🗄️ Testing Direct Database Access")
    print("=" * 40)
    
    try:
        import sqlite3
        
        # Load config
        with open('config.json') as f:
            config = json.load(f)
        
        # Connect to database
        conn = sqlite3.connect(config['database'])
        conn.row_factory = sqlite3.Row
        
        # Get users
        users = conn.execute("SELECT user_id, username, role, first_name, last_name, is_active FROM users ORDER BY user_id").fetchall()
        
        print(f"✓ Found {len(users)} users in database:")
        for user in users:
            status = "Active" if user['is_active'] else "Inactive"
            print(f"   ID: {user['user_id']:<3} | {user['username']:<20} | {user['role']:<15} | {user['first_name']} {user['last_name']:<15} | {status}")
        
        conn.close()
        return len(users) > 0
        
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

if __name__ == "__main__":
    print("🏥 User Management Test")
    print("=" * 50)
    
    # Test database first
    db_success = test_direct_database()
    
    # Test API
    api_success = test_users_api()
    
    print("\n" + "=" * 50)
    if db_success and api_success:
        print("✅ Users are in database and API is working!")
        print("🔍 Check browser console for any JavaScript errors")
    elif db_success and not api_success:
        print("⚠️ Users are in database but API has issues")
        print("🔧 Check server logs and authentication")
    elif not db_success:
        print("❌ No users in database")
        print("🔧 Run setup_system.py to create users")
    else:
        print("❌ Multiple issues detected")
        print("🔧 Check both database and API")
