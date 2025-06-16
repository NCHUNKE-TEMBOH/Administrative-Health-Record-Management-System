#!/usr/bin/env python3
"""
Fix blockchain database schema
"""

import sqlite3
import json

def fix_blockchain_schema():
    print("🔧 Fixing Blockchain Database Schema")
    print("=" * 50)
    
    try:
        with open('config.json') as f:
            config = json.load(f)
        
        conn = sqlite3.connect(config['database'])
        
        # Check current schema
        columns = conn.execute("PRAGMA table_info(blockchain_blocks)").fetchall()
        existing_columns = [col[1] for col in columns]
        print(f"Existing columns: {existing_columns}")
        
        # Add missing columns if they don't exist
        required_columns = [
            ('record_type', 'TEXT'),
            ('patient_id', 'INTEGER'),
            ('created_by', 'INTEGER')
        ]
        
        for col_name, col_type in required_columns:
            if col_name not in existing_columns:
                try:
                    conn.execute(f"ALTER TABLE blockchain_blocks ADD COLUMN {col_name} {col_type}")
                    print(f"✅ Added column: {col_name}")
                except Exception as e:
                    print(f"⚠ Column {col_name} might already exist: {e}")
        
        conn.commit()
        conn.close()
        
        print("✅ Blockchain schema fixed")
        return True
        
    except Exception as e:
        print(f"❌ Schema fix error: {e}")
        return False

if __name__ == "__main__":
    fix_blockchain_schema()
