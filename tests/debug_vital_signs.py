#!/usr/bin/env python3
"""
Debug script to test vital signs endpoint specifically
"""

import requests
import json

base_url = "http://127.0.0.1:5001"

# Login as nurse
login_data = {"username": "nurse.williams", "password": "nurse123"}
response = requests.post(f"{base_url}/auth/login", json=login_data)

if response.status_code == 200:
    token = response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    print("✓ Logged in as nurse successfully")
    
    # Get patient assignments first
    assignments_response = requests.get(f"{base_url}/patient-assignments", headers=headers)
    if assignments_response.status_code == 200:
        assignments = assignments_response.json()
        print(f"✓ Retrieved {len(assignments)} patient assignments")
        
        if assignments:
            patient_id = assignments[0]['pat_id']
            print(f"Testing vital signs for patient ID: {patient_id}")
            
            # Test vital signs endpoint
            vital_response = requests.get(f"{base_url}/vital-signs?patient_id={patient_id}", headers=headers)
            print(f"Vital signs response status: {vital_response.status_code}")
            print(f"Vital signs response: {vital_response.text}")
            
        else:
            print("No patient assignments found")
    else:
        print(f"Failed to get assignments: {assignments_response.status_code}")
        print(f"Response: {assignments_response.text}")
else:
    print(f"Login failed: {response.status_code}")
    print(f"Response: {response.text}")
