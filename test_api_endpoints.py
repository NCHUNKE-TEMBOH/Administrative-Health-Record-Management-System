#!/usr/bin/env python3
"""
Test API endpoints to ensure they return data
"""

import requests
import json

def test_endpoints():
    base_url = "http://127.0.0.1:5001"
    
    print("🧪 Testing API Endpoints")
    print("=" * 50)
    
    # Test without authentication first
    endpoints_to_test = [
        ('/users', 'Users'),
        ('/prescriptions', 'Prescriptions'),
        ('/patient', 'Patients'),
        ('/doctor', 'Doctors'),
        ('/nurse', 'Nurses')
    ]
    
    session = requests.Session()
    
    # Try to login as admin first
    print("1. Testing admin login...")
    login_data = {'username': 'admin', 'password': 'admin123'}
    
    try:
        login_response = session.post(f"{base_url}/auth/login", json=login_data, timeout=10)
        print(f"   Login status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            print("   ✓ Admin login successful")
            
            # Test each endpoint
            for endpoint, name in endpoints_to_test:
                print(f"\n2. Testing {name} endpoint ({endpoint})...")
                try:
                    response = session.get(f"{base_url}{endpoint}", timeout=10)
                    print(f"   Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            if isinstance(data, list):
                                print(f"   ✓ {name}: {len(data)} items found")
                                if len(data) > 0:
                                    print(f"   Sample: {data[0] if data else 'None'}")
                            else:
                                print(f"   ✓ {name}: Data received (not a list)")
                        except json.JSONDecodeError:
                            print(f"   ⚠ {name}: Response not JSON")
                    else:
                        print(f"   ✗ {name}: Failed with status {response.status_code}")
                        print(f"   Response: {response.text[:200]}")
                        
                except requests.exceptions.RequestException as e:
                    print(f"   ✗ {name}: Connection error - {e}")
        else:
            print(f"   ✗ Login failed: {login_response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Login connection error: {e}")

def test_database_direct():
    """Test database directly"""
    print("\n🗄️ Testing Database Directly")
    print("=" * 50)
    
    try:
        import sqlite3
        
        with open('config.json') as f:
            config = json.load(f)
        
        conn = sqlite3.connect(config['database'])
        conn.row_factory = sqlite3.Row
        
        # Test users
        users = conn.execute("SELECT COUNT(*) as count FROM users WHERE is_active = 1").fetchone()
        print(f"✓ Active users in database: {users['count']}")
        
        # Test prescriptions
        prescriptions = conn.execute("SELECT COUNT(*) as count FROM prescriptions").fetchone()
        print(f"✓ Total prescriptions in database: {prescriptions['count']}")
        
        # Test by status
        active_presc = conn.execute("SELECT COUNT(*) as count FROM prescriptions WHERE status = 'active'").fetchone()
        print(f"✓ Active prescriptions: {active_presc['count']}")
        
        # Test medications
        medications = conn.execute("SELECT COUNT(*) as count FROM medication").fetchone()
        print(f"✓ Medications in database: {medications['count']}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

if __name__ == "__main__":
    print("🏥 API and Database Test")
    print("=" * 60)
    
    # Test database first
    db_success = test_database_direct()
    
    if db_success:
        print("\n" + "="*60)
        # Test API endpoints
        test_endpoints()
    
    print("\n" + "="*60)
    print("🏁 Test completed!")
    print("\nIf APIs are working:")
    print("✅ Admin dashboard should show user counts")
    print("✅ Pharmacist dashboard should show prescription counts")
    print("\nIf APIs are not working:")
    print("🔧 Check server logs and authentication")
