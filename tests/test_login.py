#!/usr/bin/env python3
"""
Test script to verify login functionality
"""

import requests
import json

# Test login with admin credentials
def test_login():
    url = "http://127.0.0.1:5001/auth/login"
    
    # Test data
    test_credentials = [
        {"username": "admin", "password": "admin123", "expected_role": "admin"},
        {"username": "dr.smith", "password": "doctor123", "expected_role": "doctor"},
        {"username": "nurse.williams", "password": "nurse123", "expected_role": "nurse"},
        {"username": "lab.tech1", "password": "lab123", "expected_role": "lab_technician"},
        {"username": "pharmacist1", "password": "pharm123", "expected_role": "pharmacist"},
        {"username": "patient.doe", "password": "patient123", "expected_role": "patient"}
    ]
    
    print("Testing login functionality...")
    print("="*50)
    
    for cred in test_credentials:
        try:
            response = requests.post(url, json={
                "username": cred["username"],
                "password": cred["password"]
            })
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ {cred['username']} login successful - Role: {data['user']['role']}")
                
                # Test if we can access profile
                token = data['token']
                profile_response = requests.get(
                    "http://127.0.0.1:5001/auth/profile",
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                if profile_response.status_code == 200:
                    print(f"  ✓ Profile access successful")
                else:
                    print(f"  ✗ Profile access failed: {profile_response.status_code}")
                    
            else:
                print(f"✗ {cred['username']} login failed: {response.status_code}")
                if response.status_code != 404:
                    try:
                        error_data = response.json()
                        print(f"  Error: {error_data.get('error', 'Unknown error')}")
                    except:
                        print(f"  Error: {response.text}")
                        
        except requests.exceptions.ConnectionError:
            print(f"✗ Connection failed - Is the server running?")
            break
        except Exception as e:
            print(f"✗ {cred['username']} test failed: {e}")
    
    print("="*50)

if __name__ == "__main__":
    test_login()
