import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

try:
    from config.config import config
    print("✓ Config imported successfully")
    print(f"Database path: {config.DB_PATH}")
except Exception as e:
    print(f"✗ Error importing config: {e}")

try:
    import sqlite3
    print("✓ SQLite3 available")
    
    # Test database connection
    conn = sqlite3.connect(config.DB_PATH)
    print("✓ Database connection successful")
    conn.close()
except Exception as e:
    print(f"✗ Database error: {e}")

try:
    from utils.database import db
    print("✓ Database utility imported")
except Exception as e:
    print(f"✗ Error importing database utility: {e}")

print("Environment test completed!")
