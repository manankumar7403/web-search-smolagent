from typing import Any
from smolagents.tools import Tool

class FinalAnswerTool(Tool):
    name = "final_answer"
    description = "Provides a final answer to the given problem in a human-readable format."
    inputs = {'answer': {'type': 'any', 'description': 'The final answer to the problem'},
              'task': {'type': 'string', 'description': 'The original task for context (optional)', 'default': ''}}
    output_type = "string"

    def forward(self, answer: Any, task: str = '') -> str:
        # Format the answer based on the task context
        if "age" in task.lower() and isinstance(answer, (int, float)):
            return f"The answer to the task '{task}' is: {answer} years old."
        elif "image" in task.lower() and isinstance(answer, str):
            return f"Here is the result for '{task}': {answer}"
        else:
            return f"The answer to the task '{task}' is: {str(answer)}"

    def __init__(self, *args, **kwargs):
        self.is_initialized = True