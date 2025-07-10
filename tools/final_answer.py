from typing import Any, Optional
from smolagents.tools import Tool
from smolagents.agent_types import AgentText, AgentImage, AgentAudio

class FinalAnswerTool(Tool):
    name = "final_answer"
    description = "Provides a final answer to the given problem."
    inputs = {'answer': {'type': 'any', 'description': 'The final answer to the problem'}}
    output_type = "any"

    def forward(self, answer: Any) -> Any:
        if isinstance(answer, str) and answer.startswith("http"):
            if any(answer.endswith(ext) for ext in [".png", ".jpg", ".jpeg"]):
                return AgentImage(path=answer)
            return AgentText(answer)
        elif isinstance(answer, (int, float)):
            return AgentText(str(answer))
        else:
            return AgentText(str(answer))

    def __init__(self, *args, **kwargs):
        self.is_initialized = False
