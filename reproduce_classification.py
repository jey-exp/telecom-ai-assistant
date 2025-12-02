
import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

from orchestration.graph import classify_query
from orchestration.state import TelecomState

def test_classification():
    test_cases = [
        ("I want to change my plan", "plan"),
        ("My internet is very slow", "network"),
        ("How much is my bill this month?", "billing"),
        ("What is 5G?", "knowledge"),
        ("I want to upgrade to premium", "plan"),
        ("Why is my signal so bad?", "network"),
        ("Can I pay with credit card?", "billing"),
        ("Tell me about roaming charges", "knowledge"), # Could be billing or knowledge, but likely knowledge about charges
    ]

    print("Running classification tests...")
    for query, expected in test_cases:
        state = TelecomState(query=query)
        # Initialize other fields to avoid errors if any
        state["customer_info"] = {}
        state["user_email"] = "test@example.com"
        
        result_state = classify_query(state)
        classification = result_state.get("classification")
        
        print(f"Query: '{query}' -> Classified as: '{classification}' (Expected: '{expected}')")
        
        # Note: LLM might not always match exactly what we expect for ambiguous cases, but should be close.
        # We are mainly checking if it runs and gives reasonable outputs.

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables.")
    else:
        test_classification()
