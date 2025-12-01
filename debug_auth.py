"""
Debug Authentication Issue
Test the authentication functions directly
"""

import sys
import os
sys.path.insert(0, os.getcwd())

def test_authentication_steps():
    print("🔍 Debugging Authentication Process")
    print("=" * 50)
    
    from utils.user_management import user_manager
    from services.customer_service import get_user_role
    
    # Test credentials
    test_credentials = [
        ("admin@telecom.com", "admin123", "Should work"),
        ("john.doe@email.com", "customer123", "Should work"), 
        ("jane.smith@email.com", "customer456", "Should work"),
        ("wrong@email.com", "wrong123", "Should fail")
    ]
    
    for email, password, expectation in test_credentials:
        print(f"\nTesting: {email} / {password} ({expectation})")
        print("-" * 40)
        
        # Step 1: Check if user exists
        user_role = get_user_role(email)
        print(f"1. User role from DB: {user_role}")
        
        # Step 2: Test authentication
        try:
            auth_result = user_manager.authenticate_user(email, password)
            print(f"2. Authentication result: {auth_result}")
            
            if auth_result:
                print(f"   ✅ Authentication successful for {email}")
            else:
                print(f"   ❌ Authentication failed for {email}")
                
                # Debug: Check if user exists in users table
                user_data = user_manager.get_user_by_username(email.split('@')[0])
                print(f"   Debug: User by username: {user_data is not None}")
                
                # Check if user exists by email
                from utils.database import db
                user_query = "SELECT username, email, password_hash FROM users WHERE email = ?"
                user_info = db.query_one(user_query, [email])
                
                if user_info:
                    print(f"   Debug: User found in DB - {user_info[0]}")
                    print(f"   Debug: Stored hash exists: {len(user_info[2]) > 0}")
                    
                    # Test password hashing
                    test_hash = user_manager.hash_password(password)
                    stored_hash = user_info[2]
                    print(f"   Debug: Hashes match: {test_hash == stored_hash}")
                    print(f"   Debug: Test hash: {test_hash[:20]}...")
                    print(f"   Debug: Stored hash: {stored_hash[:20]}...")
                else:
                    print(f"   Debug: User NOT found in database")
                    
        except Exception as e:
            print(f"   ❌ Authentication error: {e}")
            import traceback
            traceback.print_exc()

def test_database_users():
    """Check what users are actually in the database"""
    print("\n🗄️ Database Users Check")
    print("=" * 30)
    
    from utils.database import db
    
    try:
        users_query = "SELECT id, username, email, role, is_active FROM users"
        users = db.query(users_query)
        
        print("Users in database:")
        for user in users:
            print(f"  ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[3]}, Active: {user[4]}")
        
        print(f"\nTotal users: {len(users)}")
        
        # Check password hashes
        print("\nPassword hash check:")
        hash_query = "SELECT email, password_hash FROM users LIMIT 3"
        hash_data = db.query(hash_query)
        
        for email, hash_val in hash_data:
            print(f"  {email}: {'✓' if hash_val else '✗'} (length: {len(hash_val) if hash_val else 0})")
            
    except Exception as e:
        print(f"Database error: {e}")

def main():
    print("🧪 Authentication Debug Test")
    print("Investigating login credential issues...")
    print("=" * 60)
    
    if not os.path.exists('data/telecom.db'):
        print("❌ Database not found!")
        return
    
    test_database_users()
    test_authentication_steps()

if __name__ == "__main__":
    main()
