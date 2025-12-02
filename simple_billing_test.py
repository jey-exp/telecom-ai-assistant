"""
Simple test for customer context function
"""

import sys
import os
sys.path.insert(0, os.getcwd())

def test_customer_context_function():
    """Test the get_customer_context function directly"""
    
    from orchestration.graph import get_customer_context
    
    # Test Jane's context
    state = {
        "user_email": "jane.smith@email.com",
        "customer_info": {"email": "jane.smith@email.com"}
    }
    
    result = get_customer_context(state)
    
    print("Jane's context:")
    print(f"  Customer ID: {result.get('customer_id')}")
    print(f"  User email: {result.get('user_email')}")
    print(f"  User role: {result.get('user_role')}")
    
    # Test John's context
    state = {
        "user_email": "john.doe@email.com", 
        "customer_info": {"email": "john.doe@email.com"}
    }
    
    result = get_customer_context(state)
    
    print("\nJohn's context:")
    print(f"  Customer ID: {result.get('customer_id')}")
    print(f"  User email: {result.get('user_email')}")
    print(f"  User role: {result.get('user_role')}")

if __name__ == "__main__":
    test_customer_context_function()
