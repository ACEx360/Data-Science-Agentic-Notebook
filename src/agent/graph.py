from langgraph.graph import StateGraph, END
from src.agent.state import AgentState
from src.agent.nodes import planner_node, executor_node_run, state_updater_node

workflow = StateGraph(AgentState)

workflow.add_node("planner", planner_node)
workflow.add_node("executor", executor_node_run)
workflow.add_node("state_updater", state_updater_node)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "executor")
workflow.add_edge("executor", "state_updater")
workflow.add_edge("state_updater", END)

app = workflow.compile()
