import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.executor import CodeExecutor
from src.core.shared import set_global_executor, get_global_executor

def test_manual_execution_persistence():
    print("Testing manual execution persistence...")
    
    # 1. Create a shared executor
    shared_executor = CodeExecutor()
    set_global_executor(shared_executor)
    
    # 2. Simulate Manual Execution (like in app.py)
    print("Executing manual code: 'x = 42'")
    shared_executor.execute("x = 42")
    
    # 3. Simulate Agent Execution (checking if it sees 'x')
    print("Invoking Agent to print 'x'...")
    
    retrieved_executor = get_global_executor()
    if retrieved_executor is shared_executor:
        print("SUCCESS: shared_executor is correctly retrieved.")
    else:
        print("FAILURE: retrieved_executor is DIFFERENT.")
        
    # Test variable persistence
    res = retrieved_executor.execute("print(x)")
    # Since print output goes to stdout capture in executor 
    # and "42" should be in the output string
    if "42" in res["output"]:
        print(f"SUCCESS: Variable 'x' persisted. Output: {res['output']}")
    else:
        print(f"FAILURE: Variable 'x' NOT found. Output: {res['output']}")

if __name__ == "__main__":
    test_manual_execution_persistence()
