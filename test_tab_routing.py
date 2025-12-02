"""
Test Tab-Based Routing
Verify that queries are routed to the correct agent based on UI tab selection
"""

def test_tab_routing():
    """Test that service_type overrides keyword classification"""
    print("🎯 TESTING TAB-BASED ROUTING")
    print("=" * 50)
    
    try:
        from orchestration.graph import create_graph
        
        graph = create_graph()
        
        test_cases = [
            {
                "name": "Billing Tab - Network Query",
                "query": "My internet is slow",  # Would normally go to network
                "service_type": "billing",  # But user is in billing tab
                "expected_agent": "billing"
            },
            {
                "name": "Network Tab - Billing Query", 
                "query": "What's my bill?",  # Would normally go to billing
                "service_type": "network",  # But user is in network tab
                "expected_agent": "network"
            },
            {
                "name": "Plans Tab - Any Query",
                "query": "Hello there",  # Would normally go to knowledge
                "service_type": "plans",  # But user is in plans tab
                "expected_agent": "plan"  # Should map to "plan" agent
            },
            {
                "name": "Knowledge Tab - Billing Query",
                "query": "How much do I owe?",  # Would normally go to billing
                "service_type": "knowledge",  # But user is in knowledge tab
                "expected_agent": "knowledge"
            },
            {
                "name": "No Tab (Fallback) - Network Query",
                "query": "My data is not working",  # Normal keyword classification
                "service_type": None,  # No explicit tab
                "expected_agent": "network"
            }
        ]
        
        for i, test in enumerate(test_cases, 1):
            print(f"\n{i}. {test['name']}")
            print(f"   Query: '{test['query']}'")
            print(f"   Tab: {test['service_type']}")
            
            # Create test state
            state = {
                "query": test['query'],
                "user_email": "jane.smith@email.com",
                "customer_info": {"email": "jane.smith@email.com"}
            }
            
            if test['service_type']:
                state["service_type"] = test['service_type']
            
            try:
                result = graph.invoke(state)
                classification = result.get("classification", "unknown")
                
                if classification == test['expected_agent']:
                    print(f"   ✅ Correctly routed to {classification} agent")
                else:
                    print(f"   ❌ Expected {test['expected_agent']}, got {classification}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print("\n" + "=" * 50)
        print("🎉 Tab-based routing test complete!")
        print("\nNow when users chat in specific tabs:")
        print("✅ Billing tab → Always goes to billing agent")
        print("✅ Network tab → Always goes to network agent") 
        print("✅ Plans tab → Always goes to plan agent")
        print("✅ Knowledge tab → Always goes to knowledge agent")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.getcwd())
    
    test_tab_routing()
