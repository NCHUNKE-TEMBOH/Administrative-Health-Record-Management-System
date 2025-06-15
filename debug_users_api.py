#!/usr/bin/env python3
"""
Debug the Users API to find the exact error
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_users_api_directly():
    """Test the Users API code directly"""
    print("🔍 Testing Users API directly...")
    
    try:
        # Import required modules
        from package.model import conn
        from package.auth import generate_password_hash
        
        print("✓ Imports successful")
        
        # Test database connection
        users_rows = conn.execute("""
            SELECT user_id, username, email, role, first_name, last_name,
                   phone_number, is_active, created_date, last_login, entity_id
            FROM users
            ORDER BY created_date DESC
        """).fetchall()
        
        print(f"✓ Database query successful: {len(users_rows)} users found")
        
        # Convert Row objects to dictionaries (like the API does)
        users = []
        for row in users_rows:
            users.append({
                'user_id': row['user_id'],
                'username': row['username'],
                'email': row['email'],
                'role': row['role'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'phone_number': row['phone_number'],
                'is_active': row['is_active'],
                'created_date': row['created_date'],
                'last_login': row['last_login'],
                'entity_id': row['entity_id']
            })
        
        print(f"✓ Data conversion successful: {len(users)} users processed")
        
        # Show first few users
        for i, user in enumerate(users[:3]):
            print(f"   User {i+1}: {user['username']} ({user['role']}) - {user['first_name']} {user['last_name']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_auth_functions():
    """Test authentication functions"""
    print("\n🔐 Testing authentication functions...")
    
    try:
        from package.auth import role_required, get_current_user, log_access
        print("✓ Auth imports successful")
        
        # Test password hashing
        from werkzeug.security import generate_password_hash, check_password_hash
        test_password = "test123"
        hashed = generate_password_hash(test_password)
        is_valid = check_password_hash(hashed, test_password)
        print(f"✓ Password hashing works: {is_valid}")
        
        return True
        
    except Exception as e:
        print(f"❌ Auth error: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_simple_users_endpoint():
    """Create a simple users endpoint that bypasses authentication"""
    print("\n🛠️ Creating simple users endpoint...")
    
    try:
        from flask import Flask, jsonify
        from package.model import conn
        
        app = Flask(__name__)
        
        @app.route('/api/users-simple', methods=['GET'])
        def get_users_simple():
            try:
                users_rows = conn.execute("""
                    SELECT user_id, username, email, role, first_name, last_name,
                           phone_number, is_active, created_date, last_login, entity_id
                    FROM users
                    WHERE is_active = 1
                    ORDER BY created_date DESC
                """).fetchall()
                
                users = []
                for row in users_rows:
                    users.append({
                        'user_id': row['user_id'],
                        'username': row['username'],
                        'email': row['email'],
                        'role': row['role'],
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                        'phone_number': row['phone_number'],
                        'is_active': row['is_active'],
                        'created_date': row['created_date'],
                        'last_login': row['last_login'],
                        'entity_id': row['entity_id']
                    })
                
                return jsonify(users)
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        print("✓ Simple endpoint created")
        print("   You can test it at: http://127.0.0.1:5001/api/users-simple")
        
        return app
        
    except Exception as e:
        print(f"❌ Endpoint creation error: {e}")
        return None

if __name__ == "__main__":
    print("🏥 Users API Debug Tool")
    print("=" * 50)
    
    # Test database and API code
    db_success = test_users_api_directly()
    auth_success = test_auth_functions()
    
    if db_success and auth_success:
        print("\n✅ All components working correctly!")
        print("🔍 The issue might be with authentication or session management")
        print("\n💡 Suggestions:")
        print("1. Check if admin login is working properly")
        print("2. Check browser console for authentication errors")
        print("3. Verify the session/token is being sent with requests")
        
        # Create simple endpoint
        app = create_simple_users_endpoint()
        if app:
            print("\n🚀 Starting simple test server...")
            try:
                app.run(host='127.0.0.1', port=5002, debug=True)
            except Exception as e:
                print(f"Server error: {e}")
    else:
        print("\n❌ Found issues with core components")
        print("🔧 Fix the errors above before proceeding")
