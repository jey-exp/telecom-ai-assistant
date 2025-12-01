"""
Database Reset Script - Drops existing database and recreates it with correct schema
"""

import os
import sys
sys.path.insert(0, os.getcwd())

from utils.database import db

def reset_database():
    """Drop the existing database file and recreate it"""
    db_path = db.db_path
    
    # Remove existing database file
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")
    
    # Create new database with correct schema
    print("Creating new database with correct schema...")
    db.create_tables()
    
    print("Database reset completed successfully!")

if __name__ == "__main__":
    reset_database()
