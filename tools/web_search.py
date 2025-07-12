from typing import Any, Optional
from smolagents.tools import Tool
from ddgs import DDGS  # Updated import

class DuckDuckGoSearchTool(Tool):
    name = "web_search"
    description = "Performs a DuckDuckGo web search based on your query (think a Google search) then returns the top search results."
    inputs = {'query': {'type': 'string', 'description': 'The search query to perform.'}}
    output_type = "string"

    def __init__(self, max_results=10, **kwargs):
        super().__init__()
        self.max_results = max_results
        try:
            from ddgs import DDGS
        except ImportError as e:
            raise ImportError(
                "You must install package `ddgs` to run this tool: run `pip install ddgs`."
            ) from e
        self.ddgs = DDGS(**kwargs)

    def forward(self, query: str) -> str:
        results = self.ddgs.text(query, max_results=self.max_results)
        if len(results) == 0:
            raise Exception("No results found! Try a less restrictive/shorter query.")
        postprocessed_results = [f"[{result['title']}]({result['href']})\n{result['body']}" for result in results]
        return "## Search Results\n\n" + "\n\n".join(postprocessed_results)