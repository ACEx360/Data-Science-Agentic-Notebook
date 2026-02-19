from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    messages: List[str] # User query and history
    code: str
    output: str
    variables: Dict[str, Any]
