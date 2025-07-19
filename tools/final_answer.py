from typing import Any
from smolagents.tools import Tool
from PIL import Image
import os

class FinalAnswerTool(Tool):
    name = "final_answer"
    description = "Provides a final answer to the given problem."
    inputs = {'answer': {'type': 'any', 'description': 'The final answer to the problem'}}
    output_type = "any"

    def forward(self, answer: Any) -> Any:
        if isinstance(answer, str) and os.path.exists(answer) and answer.lower().endswith((".png", ".jpg", ".jpeg")):
            try:
                return Image.open(answer)
            except Exception as e:
                return f"Error loading image: {e}"

        return answer

    def __init__(self, *args, **kwargs):
        self.is_initialized = False