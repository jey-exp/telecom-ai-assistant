"""
Test graph.py import and basic functionality
"""

import sys
import os
sys.path.insert(0, os.getcwd())

try:
    from orchestration.graph import create_graph, get_customer_context, classify_query
    print("✅ Successfully imported graph functions")
    
    # Test creating the graph
    graph = create_graph()
    print("✅ Successfully created graph")
    
    # Test basic state processing
    test_state = {
        "query": "What is my bill?",
        "user_email": "jane.smith@email.com",
        "customer_info": {"email": "jane.smith@email.com"}
    }
    
    result = graph.invoke(test_state)
    print("✅ Successfully invoked graph")
    
    print(f"\nResults:")
    print(f"Customer ID: {result.get('customer_id')}")
    print(f"Classification: {result.get('classification')}")
    print(f"Final Response: {result.get('final_response', 'No response')[:100]}...")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
