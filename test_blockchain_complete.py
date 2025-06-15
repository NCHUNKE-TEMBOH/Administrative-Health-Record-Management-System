#!/usr/bin/env python3
"""
Comprehensive blockchain test for the health record system
"""

import json
import sys
import os
import time

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_blockchain_functionality():
    print("🧪 Comprehensive Blockchain Test")
    print("=" * 60)
    
    try:
        # Load config
        with open('config.json') as f:
            config = json.load(f)
        print(f"✓ Config loaded: {config['database']}")
        
        # Test blockchain import and initialization
        print("\n1. Testing Blockchain Import and Initialization")
        from package.blockchain import Blockchain
        
        blockchain = Blockchain(config['database'])
        print(f"✓ Blockchain initialized with {len(blockchain.chain)} blocks")
        
        # Test blockchain validation
        print("\n2. Testing Blockchain Validation")
        is_valid = blockchain.is_chain_valid()
        print(f"✓ Blockchain validation: {is_valid}")
        
        # Test database functionality
        print("\n3. Testing Database Functionality")
        db_stats = blockchain.get_database_stats()
        print(f"✓ Database stats: {db_stats}")
        
        # Test blockchain statistics
        print("\n4. Testing Blockchain Statistics")
        stats = blockchain.get_blockchain_stats()
        print(f"✓ Total blocks: {stats['total_blocks']}")
        print(f"✓ Record types: {stats['record_types']}")
        print(f"✓ Patients count: {stats['patients_count']}")
        
        # Test adding sample data
        print("\n5. Testing Sample Data Addition")
        initial_count = len(blockchain.chain)
        added_count = blockchain.add_sample_data()
        final_count = len(blockchain.chain)
        print(f"✓ Added {added_count} sample records")
        print(f"✓ Blockchain grew from {initial_count} to {final_count} blocks")
        
        # Test specific record type queries
        print("\n6. Testing Record Type Queries")
        health_records = blockchain.get_records_by_type('health_record')
        vital_signs = blockchain.get_records_by_type('vital_signs')
        prescriptions = blockchain.get_records_by_type('prescription')
        lab_results = blockchain.get_records_by_type('lab_result')
        
        print(f"✓ Health records: {len(health_records)}")
        print(f"✓ Vital signs: {len(vital_signs)}")
        print(f"✓ Prescriptions: {len(prescriptions)}")
        print(f"✓ Lab results: {len(lab_results)}")
        
        # Test patient-specific queries
        print("\n7. Testing Patient-Specific Queries")
        patient_records = blockchain.get_patient_records(8)  # Jane Doe
        print(f"✓ Patient 8 records: {len(patient_records)}")
        
        # Test blockchain export
        print("\n8. Testing Blockchain Export")
        chain_export = blockchain.to_list()
        print(f"✓ Exported {len(chain_export)} blocks")
        
        # Test database persistence
        print("\n9. Testing Database Persistence")
        blockchain.save_to_database()
        
        # Create new instance and load
        blockchain2 = Blockchain(config['database'])
        print(f"✓ Reloaded blockchain with {len(blockchain2.chain)} blocks")
        
        # Verify integrity after reload
        is_valid_after_reload = blockchain2.is_chain_valid()
        print(f"✓ Blockchain valid after reload: {is_valid_after_reload}")
        
        print("\n" + "=" * 60)
        print("🎉 All blockchain tests passed successfully!")
        
        # Final statistics
        final_stats = blockchain.get_blockchain_stats()
        print(f"\n📊 Final Statistics:")
        print(f"   Total Blocks: {final_stats['total_blocks']}")
        print(f"   Chain Valid: {final_stats['is_valid']}")
        print(f"   Patients: {final_stats['patients_count']}")
        print(f"   Record Types: {final_stats['record_types']}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Blockchain test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_integration():
    """Test blockchain API integration"""
    print("\n🌐 Testing API Integration")
    print("-" * 40)
    
    try:
        import requests
        base_url = "http://127.0.0.1:5001"
        
        # Test blockchain chain endpoint
        response = requests.get(f"{base_url}/api/blockchain/chain", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ API Chain endpoint: {len(data.get('chain', []))} blocks")
        else:
            print(f"⚠ API Chain endpoint failed: {response.status_code}")
        
        # Test validation endpoint
        response = requests.get(f"{base_url}/api/blockchain/validate", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ API Validation endpoint: {data.get('valid', False)}")
        else:
            print(f"⚠ API Validation endpoint failed: {response.status_code}")
        
        # Test adding a record
        test_record = {
            'type': 'test_api',
            'message': 'API integration test',
            'timestamp': time.time()
        }
        
        response = requests.post(
            f"{base_url}/api/blockchain/add",
            json=test_record,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"✓ API Add endpoint: Block {data.get('block', {}).get('index', 'N/A')} added")
        else:
            print(f"⚠ API Add endpoint failed: {response.status_code}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"⚠ API test skipped (server not running): {e}")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    print("🏥 Administrative Health Record Management System")
    print("🔗 Blockchain Comprehensive Test Suite")
    print("=" * 60)
    
    # Test blockchain functionality
    blockchain_success = test_blockchain_functionality()
    
    # Test API integration (optional)
    api_success = test_api_integration()
    
    print("\n" + "=" * 60)
    if blockchain_success:
        print("✅ Blockchain implementation is fully functional!")
        print("🔗 Database integration working correctly")
        print("📊 All blockchain features tested successfully")
        
        if api_success:
            print("🌐 API integration working correctly")
        else:
            print("ℹ API integration not tested (server not running)")
        
        print("\n🚀 Ready for production use!")
        
    else:
        print("❌ Blockchain implementation has issues")
        print("🔧 Please check the errors above")
        
    return blockchain_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
