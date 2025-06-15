print("Python is working!")
print("Testing imports...")

try:
    import sqlite3
    print("✓ sqlite3 imported")
except Exception as e:
    print(f"✗ sqlite3 error: {e}")

try:
    import json
    print("✓ json imported")
except Exception as e:
    print(f"✗ json error: {e}")

try:
    from flask import Flask
    print("✓ Flask imported")
except Exception as e:
    print(f"✗ Flask error: {e}")

print("Test completed!")
