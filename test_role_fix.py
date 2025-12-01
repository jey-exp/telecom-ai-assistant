"""
Test Role-Based Access Fix
Tests admin vs customer access to ensure proper separation
"""

import sys
import os
sys.path.insert(0, os.getcwd())

from services.customer_service import get_customer_profile, get_user_role

def test_admin_access():
    """Test that admin gets admin dashboard, not customer details"""
    print("🔧 Testing Admin Access:")
    print("-" * 30)
    
    admin_email = "admin@telecom.com"
    admin_role = get_user_role(admin_email)
    print(f"Admin role: {admin_role}")
    
    customer_id, customer_data = get_customer_profile(admin_email)
    print(f"Admin customer_id: {customer_id}")
    
    if customer_id == "ADMIN" and isinstance(customer_data, dict):
        print("✅ SUCCESS: Admin gets dashboard data")
        print(f"   Dashboard type: {customer_data.get('type')}")
        print(f"   Total customers: {customer_data.get('total_customers')}")
    else:
        print(f"❌ FAILED: Admin still gets customer data: {customer_id}")
    
    print()

def test_customer_access():
    """Test that customers get their own data"""
    print("👤 Testing Customer Access:")
    print("-" * 30)
    
    # Test John Doe
    john_email = "john.doe@email.com"
    john_role = get_user_role(john_email)
    print(f"John's role: {john_role}")
    
    customer_id, customer_data = get_customer_profile(john_email)
    print(f"John's customer_id: {customer_id}")
    
    if customer_id == "CUST001" and customer_data and len(customer_data) > 1:
        print(f"✅ SUCCESS: John gets his data - {customer_data[1]}")
    else:
        print(f"❌ FAILED: John doesn't get proper data")
    
    # Test Jane Smith
    jane_email = "jane.smith@email.com"
    jane_role = get_user_role(jane_email)
    print(f"Jane's role: {jane_role}")
    
    customer_id, customer_data = get_customer_profile(jane_email)
    print(f"Jane's customer_id: {customer_id}")
    
    if customer_id == "CUST002" and customer_data and len(customer_data) > 1:
        print(f"✅ SUCCESS: Jane gets her data - {customer_data[1]}")
    else:
        print(f"❌ FAILED: Jane doesn't get proper data")
    
    print()

def test_network_agent():
    """Test network agent role-based responses"""
    print("📡 Testing Network Agent:")
    print("-" * 30)
    
    from agents.network_agents import process_network_query
    
    # Test admin query
    print("Testing admin network query...")
    admin_response = process_network_query("Network status overview", "admin@telecom.com")
    print(f"Admin response: {admin_response[:100]}...")
    
    # Test customer query
    print("\nTesting customer network query...")
    customer_response = process_network_query("My internet is slow", "john.doe@email.com")
    print(f"Customer response: {customer_response[:100]}...")

def main():
    print("🧪 Role-Based Access Test")
    print("=" * 50)
    
    # Check if database exists
    if not os.path.exists('data/telecom.db'):
        print("❌ Database not found! Run complete_setup.py first.")
        return
    
    try:
        test_admin_access()
        test_customer_access()
        test_network_agent()
        
        print("🎉 Role-based access testing completed!")
        print("\nKey fixes:")
        print("- Removed hardcoded CUST001 fallback")
        print("- Added role-based data access")
        print("- Admin gets dashboard, customers get their own data")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
