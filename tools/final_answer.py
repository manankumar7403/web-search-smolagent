from typing import Any
from smolagents.tools import Tool
import re

class FinalAnswerTool(Tool):
    name = "final_answer"
    description = "Provides a final answer to the given problem in a human-readable, conversational format."
    inputs = {
        'answer': {'type': 'any', 'description': 'The final answer to the problem'},
        'task': {'type': 'string', 'description': 'The original task for context (optional)', 'default': ''}
    }
    output_type = "string"

    def forward(self, answer: Any, task: str = '') -> str:
        # Default fallback for unrecognized task formats
        default_response = f"{str(answer)}"

        if not task:
            return default_response

        # Normalize task string for easier matching
        task_lower = task.lower().strip()

        # Handle "age of" questions, e.g., "What is the age of Elon Musk?"
        age_match = re.match(r".*age of\s+(.+?)(?:\?|$)", task_lower)
        if age_match and isinstance(answer, (int, float)):
            subject = age_match.group(1).strip()
            # Capitalize the subject for proper formatting
            subject = ' '.join(word.capitalize() for word in subject.split())
            return f"The age of {subject} is {answer}."

        # Handle "who is" questions, e.g., "Who is the current head coach of the Indian national cricket team?"
        who_match = re.match(r"who is\s+(.+?)(?:\?|$)", task_lower)
        if who_match:
            subject = who_match.group(1).strip()
            return f"The {subject} is {str(answer)}."

        # Handle "what is" questions (excluding "age of"), e.g., "What is the capital of France?"
        what_match = re.match(r"what is\s+(.+?)(?:\?|$)", task_lower)
        if what_match and "age of" not in task_lower:
            subject = what_match.group(1).strip()
            return f"The {subject} is {str(answer)}."

        # Handle "image" tasks (unchanged)
        if "image" in task_lower and isinstance(answer, str):
            return f"Here is the result for '{task}': {answer}"

        # Fallback for other cases
        return f"The answer to '{task}' is: {str(answer)}"

    def __init__(self, *args, **kwargs):
        self.is_initialized = True