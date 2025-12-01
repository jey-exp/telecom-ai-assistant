"""
Test Login Flow - Simulates the Streamlit authentication process
"""

import sys
import os
sys.path.insert(0, os.getcwd())

def simulate_login(email, password):
    """Simulate the complete login process"""
    print(f"🔑 Simulating login for: {email}")
    
    from utils.user_management import user_manager
    from services.customer_service import get_user_role, get_customer_profile
    
    # Step 1: Authenticate (like sidebar does)
    if user_manager.authenticate_user(email, password):
        print("  ✅ Authentication successful")
        
        # Step 2: Get user role (like sidebar does)
        user_role = get_user_role(email)
        print(f"  📋 User role: {user_role}")
        
        # Step 3: Get profile data (like dashboard does)
        customer_id, customer_data = get_customer_profile(email)
        print(f"  📊 Profile data: {customer_id}")
        
        if user_role == 'admin' and customer_id == 'ADMIN':
            print("  🎯 ADMIN LOGIN SUCCESS: Gets admin dashboard")
            return True
        elif user_role == 'customer' and customer_data and len(customer_data) > 1:
            print(f"  🎯 CUSTOMER LOGIN SUCCESS: Gets own data - {customer_data[1]}")
            return True
        else:
            print("  ❌ Login succeeded but data access failed")
            return False
    else:
        print("  ❌ Authentication failed")
        return False

def main():
    print("🧪 End-to-End Login Test")
    print("Simulating the complete Streamlit login flow")
    print("=" * 50)
    
    # Test all user types
    test_cases = [
        ("admin@telecom.com", "admin123", "Admin"),
        ("john.doe@email.com", "customer123", "John Doe"),
        ("jane.smith@email.com", "customer456", "Jane Smith")
    ]
    
    all_passed = True
    
    for email, password, name in test_cases:
        print(f"\n{name} Login Test:")
        print("-" * 30)
        
        success = simulate_login(email, password)
        if not success:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL LOGINS WORKING CORRECTLY!")
        print("✅ The authentication issue is fully fixed")
        print("\n📱 You can now start the app and login successfully:")
        print("   streamlit run app.py")
    else:
        print("❌ Some login issues remain")

if __name__ == "__main__":
    main()
