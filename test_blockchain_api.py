#!/usr/bin/env python3
"""
Test blockchain API endpoints
"""

import requests
import json
import time

def test_blockchain_api():
    base_url = "http://127.0.0.1:5001"
    
    print("🧪 Testing Blockchain API Endpoints")
    print("=" * 50)
    
    # Test 1: Get blockchain chain
    print("\n1. Testing GET /api/blockchain/chain")
    try:
        response = requests.get(f"{base_url}/api/blockchain/chain", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Success: {len(data.get('chain', []))} blocks found")
            print(f"   Chain length: {data.get('length', 0)}")
        else:
            print(f"   ✗ Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Connection error: {e}")
    
    # Test 2: Validate blockchain
    print("\n2. Testing GET /api/blockchain/validate")
    try:
        response = requests.get(f"{base_url}/api/blockchain/validate", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Validation result: {data.get('valid', False)}")
        else:
            print(f"   ✗ Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Connection error: {e}")
    
    # Test 3: Add a test block
    print("\n3. Testing POST /api/blockchain/add")
    test_data = {
        'type': 'test',
        'message': 'API test block',
        'timestamp': time.time(),
        'test_id': 'api_test_001'
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/blockchain/add",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"   ✓ Block added successfully")
            print(f"   Block index: {data.get('block', {}).get('index', 'N/A')}")
        else:
            print(f"   ✗ Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Connection error: {e}")
    
    # Test 4: Get chain again to verify addition
    print("\n4. Testing chain after addition")
    try:
        response = requests.get(f"{base_url}/api/blockchain/chain", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Updated chain: {len(data.get('chain', []))} blocks")
        else:
            print(f"   ✗ Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Connection error: {e}")
    
    # Test 5: Test blockchain dashboard page
    print("\n5. Testing blockchain dashboard page")
    try:
        response = requests.get(f"{base_url}/blockchain/dashboard.html", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✓ Dashboard page accessible")
        else:
            print(f"   ✗ Dashboard error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Connection error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Blockchain API test completed!")

if __name__ == "__main__":
    test_blockchain_api()
