from src.core.executor import CodeExecutor

_executor = None

def set_global_executor(executor: CodeExecutor):
    """Sets the global executor instance to be used by the agent."""
    global _executor
    _executor = executor

def get_global_executor() -> CodeExecutor:
    """Gets the global executor or creates a new one if not set."""
    global _executor
    if _executor is None:
        _executor = CodeExecutor()
    return _executor
