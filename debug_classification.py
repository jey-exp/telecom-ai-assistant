
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

print("Starting import...")
try:
    from orchestration.graph import classify_query
    print("Import successful.")
except Exception as e:
    print(f"Import failed: {e}")

from orchestration.state import TelecomState
print("State imported.")

if __name__ == "__main__":
    print("Running single test...")
    state = TelecomState(query="test query")
    state["customer_info"] = {}
    state["user_email"] = "test@example.com"
    # Mock client if needed, but let's see if it runs
    try:
        result = classify_query(state)
        print(f"Result: {result.get('classification')}")
    except Exception as e:
        print(f"Execution failed: {e}")
