import sys
import io
import contextlib
import pandas as pd
import matplotlib.pyplot as plt

class CodeExecutor:
    def __init__(self):
        self.globals = {}
        # Pre-import common libraries
        self.execute("import pandas as pd")
        self.execute("import numpy as np")
        self.execute("import matplotlib.pyplot as plt")

    def execute(self, code):
        """
        Executes the provided Python code and captures the output.
        Returns a dictionary containing the output and the current state of variables.
        """
        # Capture stdout and stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
            try:
                exec(code, self.globals)
                output = stdout_capture.getvalue()
                error = stderr_capture.getvalue()
            except Exception as e:
                output = stdout_capture.getvalue()
                error = str(e)

        # specific output logic
        pass 
        if error:
            output += f"\nError: {error}"

        # Extract variable summary
        variables = self._get_variable_summary()
        
        return {
            "output": output.strip(),
            "variables": variables
        }

    def _get_variable_summary(self):
        """
        Extracts a summary of the defined variables.
        """
        summary = {}
        for name, value in self.globals.items():
            if name.startswith("_") or name in ["pd", "np", "plt", "io", "sys", "contextlib"]:
                continue
            
            type_name = type(value).__name__
            info = str(value)[:50]  # Truncate long values

            if isinstance(value, pd.DataFrame):
                info = f"DataFrame shape: {value.shape}, Columns: {list(value.columns)}"
            elif isinstance(value, pd.Series):
                 info = f"Series shape: {value.shape}"
            
            summary[name] = {
                "type": type_name,
                "info": info
            }
        return summary

if __name__ == "__main__":
    executor = CodeExecutor()
    result = executor.execute("print('Hello, World!')\nx = 10\ndf = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})")
    print("Output:", result["output"])
    print("Variables:", result["variables"])
