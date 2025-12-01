import sqlite3
import os

# Simple test to create database and add users
db_path = "data/telecom.db"
print(f"Database path: {db_path}")
print(f"Database exists: {os.path.exists(db_path)}")

try:
    # Create connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create a simple table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            role TEXT
        )
    """)
    
    # Insert test data
    cursor.execute("INSERT INTO test_users (username, role) VALUES (?, ?)", ("admin", "admin"))
    cursor.execute("INSERT INTO test_users (username, role) VALUES (?, ?)", ("customer1", "customer"))
    
    conn.commit()
    
    # Query back
    cursor.execute("SELECT * FROM test_users")
    users = cursor.fetchall()
    
    print("Users created:")
    for user in users:
        print(f"  - {user}")
        
    conn.close()
    print("Test completed successfully!")
    
except Exception as e:
    print(f"Error: {e}")
    if conn:
        conn.close()
