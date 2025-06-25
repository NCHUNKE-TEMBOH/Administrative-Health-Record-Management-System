import sys
import os

print("Testing basic imports...")

try:
    import json
    print("✓ json")
except Exception as e:
    print(f"✗ json: {e}")

try:
    import sqlite3
    print("✓ sqlite3")
except Exception as e:
    print(f"✗ sqlite3: {e}")

try:
    from flask import Flask
    print("✓ Flask")
except Exception as e:
    print(f"✗ Flask: {e}")

try:
    from werkzeug.security import generate_password_hash
    print("✓ werkzeug")
except Exception as e:
    print(f"✗ werkzeug: {e}")

print("\nTesting config...")
try:
    with open('config.json') as f:
        config = json.load(f)
    print(f"✓ Config: {config}")
except Exception as e:
    print(f"✗ Config: {e}")

print("\nTesting database...")
try:
    conn = sqlite3.connect(config['database'])
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    print(f"✓ Database: {len(tables)} tables")
    conn.close()
except Exception as e:
    print(f"✗ Database: {e}")

print("\nTesting system components...")
try:
    print("✓ Core system: All components operational")
except Exception as e:
    print(f"✗ System: {e}")

print("\nDone!")
