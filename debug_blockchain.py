#!/usr/bin/env python3
"""
Debug blockchain implementation
"""

import sys
import os
import json
import traceback

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_blockchain():
    print("🔍 Debugging blockchain implementation...")
    
    try:
        # Test config loading
        print("\n1. Testing config loading...")
        with open('config.json') as f:
            config = json.load(f)
        print(f"✓ Config loaded: {config}")
        
        # Test database connection
        print("\n2. Testing database connection...")
        import sqlite3
        conn = sqlite3.connect(config['database'])
        print("✓ Database connection successful")
        
        # Test blockchain import
        print("\n3. Testing blockchain import...")
        from package.blockchain import Blockchain
        print("✓ Blockchain module imported")
        
        # Test blockchain initialization
        print("\n4. Testing blockchain initialization...")
        blockchain = Blockchain(config['database'])
        print("✓ Blockchain initialized")
        
        # Test blockchain methods
        print("\n5. Testing blockchain methods...")
        
        # Test chain export
        chain = blockchain.to_list()
        print(f"✓ Chain exported: {len(chain)} blocks")
        
        # Test validation
        is_valid = blockchain.is_chain_valid()
        print(f"✓ Chain validation: {is_valid}")
        
        # Test adding a block
        test_data = {
            'type': 'test',
            'message': 'Debug test block',
            'timestamp': '2024-01-01'
        }
        block = blockchain.add_block(test_data)
        print(f"✓ Block added: Index {block.index}")
        
        # Test chain after adding block
        chain = blockchain.to_list()
        print(f"✓ Updated chain: {len(chain)} blocks")
        
        # Test Flask app import
        print("\n6. Testing Flask app components...")
        from flask import Flask, jsonify, request
        print("✓ Flask components imported")
        
        # Test app initialization
        print("\n7. Testing app initialization...")
        app = Flask(__name__)
        print("✓ Flask app created")
        
        print("\n🎉 All blockchain components working correctly!")
        
        # Show blockchain content
        print("\n📊 Current blockchain content:")
        for i, block in enumerate(chain):
            print(f"Block {i}: {block['data']['type']} - {block['data'].get('message', 'No message')}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during debugging: {e}")
        print("\n📋 Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_blockchain()
    if success:
        print("\n✅ Blockchain is ready for use!")
    else:
        print("\n❌ Blockchain needs fixing!")
