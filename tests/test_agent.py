import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Check if database file exists (in root, assuming run from root or tests dir)
# We want to use the one in root if possible.
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "notebook.db")

print(f"Checking DB at {db_path}")

if not os.path.exists(db_path):
    print("Initializing database...")
    from src.core.database import init_db
    # This init_db uses "notebook.db" relative path.
    # If run from tests dir, it creates tests/notebook.db.
    # If run from root, it creates notebook.db.
    # ideally we should configure DB path in config.py
    init_db()

# Test Executor
print("Testing Executor...")
from src.core.executor import CodeExecutor
executor = CodeExecutor()
res = executor.execute("print('Hello from Test')")
if res['output'].strip() == "Hello from Test":
    print("Executor Test Passed!")
else:
    print(f"Executor Test Failed: {res}")

# Test Agent (mocking API key if needed, or assuming env)
print("Testing Agent (dry run)...")
try:
    from src.agent.graph import app
    print("Agent Graph Compiled Successfully!")
except Exception as e:
    print(f"Agent Import Failed: {e}")
