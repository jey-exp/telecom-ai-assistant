"""
Test the get_customer_context function
"""

import sys
import os
sys.path.insert(0, os.getcwd())

def test_get_customer_context():
    """Test that get_customer_context extracts user info correctly"""
    
    from orchestration.graph import get_customer_context
    
    print("🧪 Testing get_customer_context function")
    print("=" * 45)
    
    # Test Jane's context
    print("\n1. Testing Jane Smith:")
    jane_state = {
        "user_email": "jane.smith@email.com",
        "customer_info": {"email": "jane.smith@email.com"}
    }
    
    result = get_customer_context(jane_state)
    
    print(f"   Input email: {jane_state.get('user_email')}")
    print(f"   Output customer_id: {result.get('customer_id')}")
    print(f"   Output user_role: {result.get('user_role')}")
    print(f"   Expected: CUST002, customer")
    
    # Test John's context  
    print("\n2. Testing John Doe:")
    john_state = {
        "user_email": "john.doe@email.com",
        "customer_info": {"email": "john.doe@email.com"}
    }
    
    result = get_customer_context(john_state)
    
    print(f"   Input email: {john_state.get('user_email')}")
    print(f"   Output customer_id: {result.get('customer_id')}")
    print(f"   Output user_role: {result.get('user_role')}")
    print(f"   Expected: CUST001, customer")
    
    # Test Admin context
    print("\n3. Testing Admin:")
    admin_state = {
        "user_email": "admin@telecom.com",
        "customer_info": {"email": "admin@telecom.com"}
    }
    
    result = get_customer_context(admin_state)
    
    print(f"   Input email: {admin_state.get('user_email')}")
    print(f"   Output customer_id: {result.get('customer_id')}")
    print(f"   Output user_role: {result.get('user_role')}")
    print(f"   Expected: ADMIN, admin")
    
    print("\n" + "=" * 45)
    print("✅ Customer context extraction test completed!")

if __name__ == "__main__":
    test_get_customer_context()
