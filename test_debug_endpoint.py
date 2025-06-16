#!/usr/bin/env python3
"""
Test the debug endpoint and blockchain
"""

import requests
import json

def test_debug_endpoints():
    base_url = "http://127.0.0.1:5001"
    
    print("🧪 Testing Debug and Blockchain Endpoints")
    print("=" * 60)
    
    try:
        # Test debug users endpoint
        print("1. Testing debug users endpoint...")
        response = requests.get(f"{base_url}/api/users-debug", timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            users = response.json()
            print(f"   ✓ Debug endpoint: {len(users)} users found")
            for i, user in enumerate(users[:3]):
                print(f"   User {i+1}: {user['username']} ({user['role']}) - {user['first_name']} {user['last_name']}")
        else:
            print(f"   ✗ Debug endpoint failed: {response.text}")
        
        # Test blockchain endpoints
        print("\n2. Testing blockchain endpoints...")
        
        # Test blockchain chain
        response = requests.get(f"{base_url}/api/blockchain/chain", timeout=10)
        print(f"   Blockchain chain status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Blockchain: {data.get('length', 0)} blocks, valid: {data.get('valid', False)}")
        
        # Test blockchain stats
        response = requests.get(f"{base_url}/api/blockchain/stats", timeout=10)
        print(f"   Blockchain stats status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            blockchain_stats = data.get('blockchain_stats', {})
            print(f"   ✓ Blockchain stats: {blockchain_stats.get('total_blocks', 0)} blocks")
            print(f"   Record types: {blockchain_stats.get('record_types', {})}")
        
        # Test blockchain validation
        response = requests.get(f"{base_url}/api/blockchain/validate", timeout=10)
        print(f"   Blockchain validate status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Blockchain valid: {data.get('valid', False)}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Connection error: {e}")
        return False

if __name__ == "__main__":
    success = test_debug_endpoints()
    
    if success:
        print("\n✅ Debug endpoints working!")
        print("🔧 Now update the admin dashboard to use the debug endpoint")
    else:
        print("\n❌ Debug endpoints failed")
        print("🔧 Check server logs")
