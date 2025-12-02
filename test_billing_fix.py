"""
Test Billing Fix - Verify Jane gets her own bill, not John's
"""

import sys
import os
sys.path.insert(0, os.getcwd())

def test_billing_by_user():
    """Test that each user gets their own billing data"""
    print("💰 Testing Billing Data by User")
    print("=" * 40)
    
    from orchestration.graph import create_graph
    
    # Create the graph
    graph = create_graph()
    
    # Test cases
    test_cases = [
        {
            "name": "John Doe",
            "email": "john.doe@email.com",
            "expected_customer_id": "CUST001",
            "expected_bill": 45.99
        },
        {
            "name": "Jane Smith", 
            "email": "jane.smith@email.com",
            "expected_customer_id": "CUST002",
            "expected_bill": 80.99
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🧪 Testing {test_case['name']}:")
        print("-" * 25)
        
        # Simulate the billing query
        state = {
            "query": "What is my bill?",
            "user_email": test_case["email"],
            "customer_info": {"email": test_case["email"]}
        }
        
        try:
            result = graph.invoke(state)
            
            # Check if we got the customer context
            customer_id = result.get("customer_id")
            final_response = result.get("final_response", "")
            
            print(f"Customer ID: {customer_id}")
            print(f"Response: {final_response[:100]}...")
            
            # Check if the correct customer ID was used
            if customer_id == test_case["expected_customer_id"]:
                print(f"✅ Correct customer ID: {customer_id}")
                
                # Check if the bill amount appears in response
                expected_bill_str = str(test_case["expected_bill"])
                if expected_bill_str in final_response:
                    print(f"✅ Correct bill amount found: ${expected_bill_str}")
                else:
                    print(f"⚠️  Expected bill ${expected_bill_str} not clearly found in response")
                    
            else:
                print(f"❌ Wrong customer ID: got {customer_id}, expected {test_case['expected_customer_id']}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

def test_database_billing_data():
    """Verify what billing data is in the database for each customer"""
    print("\n🗄️ Database Billing Data Check")
    print("=" * 35)
    
    from agents.billing_agents import get_customer_billing_details
    
    customers = [
        ("CUST001", "John Doe"),
        ("CUST002", "Jane Smith")
    ]
    
    for customer_id, name in customers:
        print(f"\n{name} ({customer_id}):")
        
        billing_data = get_customer_billing_details(customer_id)
        
        if billing_data:
            print(f"  Name: {billing_data[0]}")
            print(f"  Email: {billing_data[1]}")
            print(f"  Bill Amount: ${billing_data[7]}")
            print(f"  Data Used: {billing_data[3]} GB")
            print(f"  Plan Cost: ${billing_data[8]}")
        else:
            print(f"  ❌ No billing data found")

def main():
    print("🧪 Billing Fix Verification")
    print("Testing that Jane gets her bill ($80.99) not John's ($45.99)")
    print("=" * 60)
    
    if not os.path.exists('data/telecom.db'):
        print("❌ Database not found! Run complete_setup.py first.")
        return
    
    # First check what's in the database
    test_database_billing_data()
    
    # Then test the full workflow
    test_billing_by_user()
    
    print("\n" + "=" * 60)
    print("💡 If Jane still gets John's bill, the issue is in the workflow")
    print("💡 If database shows correct data, the fix should work")

if __name__ == "__main__":
    main()
