#!/usr/bin/env python3
"""
Test the blockchain implementation
"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_blockchain():
    print("Testing blockchain implementation...")
    
    try:
        from package.blockchain import Blockchain
        print("✓ Blockchain module imported successfully")
        
        # Test blockchain creation
        blockchain = Blockchain()
        print("✓ Blockchain instance created")
        
        # Test adding a block
        test_data = {
            'type': 'test',
            'message': 'Test block',
            'timestamp': '2024-01-01'
        }
        
        block = blockchain.add_block(test_data)
        print(f"✓ Block added: {block.index}")
        
        # Test chain validation
        is_valid = blockchain.is_chain_valid()
        print(f"✓ Chain validation: {is_valid}")
        
        # Test chain export
        chain_list = blockchain.to_list()
        print(f"✓ Chain exported: {len(chain_list)} blocks")
        
        print("\n🎉 Blockchain test completed successfully!")
        
    except Exception as e:
        print(f"✗ Blockchain test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_blockchain()
