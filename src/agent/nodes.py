import os
from langchain_google_genai import ChatGoogleGenerativeAI
from src.agent.state import AgentState
from src.core.database import add_cell, get_last_state
from src.core.shared import get_global_executor
from src.core.config import load_config

load_config()

# Initialize Gemini
if "GOOGLE_API_KEY" not in os.environ:
    # This might fail in production if key is missing, but for now we pass.
    pass

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

def planner_node(state: AgentState):
    """Generates Python code based on the user query and previous state."""
    messages = state["messages"]
    last_state = get_last_state()
    
    prompt = f"""
    You are a Data Science AI Assistant.
    Your goal is to generate executable Python code to solve the user's request.
    
    Current Variable State:
    {last_state}
    
    User Query:
    {messages[-1]}
    
    Requirements:
    1. Return ONLY executable Python code.
    2. NO markdown, NO explanations.
    3. Assume 'pandas' is imported as 'pd', 'numpy' as 'np', 'matplotlib.pyplot' as 'plt'.
    4. Use existing variables if available.
    5. If plotting, use plt.show() or simply create the plot.
    """
    
    result = llm.invoke(prompt)
    code = result.content.strip().replace("```python", "").replace("```", "")
    return {"code": code}

def executor_node_run(state: AgentState):
    """Executes the generated code using the global executor."""
    code = state["code"]
    executor = get_global_executor()
    result = executor.execute(code)
    return {"output": result["output"], "variables": result["variables"]}

def state_updater_node(state: AgentState):
    """Updates the database with the execution results."""
    code = state["code"]
    output = state["output"]
    variables = state["variables"]
    
    add_cell(code, output, variables)
    return {"output": output}
