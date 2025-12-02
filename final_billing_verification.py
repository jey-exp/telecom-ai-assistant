"""
Final Verification: Billing Context Fix
Tests the complete workflow to ensure Jane gets her own billing data
"""

def verify_billing_fix():
    """Complete end-to-end test of billing fix"""
    
    print("🎯 FINAL BILLING FIX VERIFICATION")
    print("=" * 50)
    
    try:
        # Import required components
        print("1. Testing imports...")
        from orchestration.graph import create_graph, get_customer_context
        from services.customer_service import get_customer_profile
        print("   ✅ All imports successful")
        
        # Test customer context extraction
        print("\n2. Testing customer context extraction...")
        
        jane_state = {
            "user_email": "jane.smith@email.com",
            "customer_info": {"email": "jane.smith@email.com"}
        }
        
        result = get_customer_context(jane_state)
        jane_customer_id = result.get('customer_id')
        
        print(f"   Jane's customer_id: {jane_customer_id}")
        
        if jane_customer_id == "CUST002":
            print("   ✅ Jane gets correct customer ID")
        else:
            print("   ❌ Jane gets wrong customer ID")
            return False
            
        # Test direct billing data lookup
        print("\n3. Testing direct billing data...")
        from agents.billing_agents import get_customer_billing_details
        
        jane_billing = get_customer_billing_details("CUST002")
        john_billing = get_customer_billing_details("CUST001")
        
        if jane_billing:
            print(f"   Jane's bill: ${jane_billing[7]} (Expected: $80.99)")
        if john_billing:
            print(f"   John's bill: ${john_billing[7]} (Expected: $45.99)")
            
        # Test complete graph workflow
        print("\n4. Testing complete workflow...")
        graph = create_graph()
        
        workflow_state = {
            "query": "What is my bill?",
            "user_email": "jane.smith@email.com",
            "customer_info": {"email": "jane.smith@email.com"}
        }
        
        workflow_result = graph.invoke(workflow_state)
        final_response = workflow_result.get("final_response", "")
        
        print(f"   Final response preview: {final_response[:100]}...")
        
        # Check if Jane's bill amount appears in response
        if "80.99" in final_response:
            print("   ✅ Jane's correct bill amount found in response")
            success = True
        elif "45.99" in final_response:
            print("   ❌ John's bill amount found in response (WRONG!)")
            success = False
        else:
            print("   ⚠️  No clear bill amount found in response")
            success = False
            
        print("\n" + "=" * 50)
        if success:
            print("🎉 SUCCESS: Billing fix is working correctly!")
            print("✅ Jane will now see her own bill ($80.99)")
            print("✅ Complete workflow tested and verified")
        else:
            print("❌ FAILED: Billing fix needs more work")
            
        return success
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.getcwd())
    
    verify_billing_fix()
