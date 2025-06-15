print("Testing basic Python execution")
import sqlite3
print("SQLite3 imported successfully")
import json
print("JSON imported successfully")

# Test database connection
try:
    with open('config.json') as f:
        config = json.load(f)
    print(f"Config loaded: {config}")
    
    conn = sqlite3.connect(config['database'])
    print("Database connected successfully")
    
    # Test query
    result = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    print(f"Found {len(result)} tables")
    
    conn.close()
    print("Test completed successfully")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
