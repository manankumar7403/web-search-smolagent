from typing import Any
from smolagents.tools import Tool

class DuckDuckGoSearchTool(Tool):
    name = "web_search"
    description = "Performs a DuckDuckGo web search based on your query and returns the top search results."
    inputs = {'query': {'type': 'string', 'description': 'The search query to perform.'}}
    output_type = "string"

    def __init__(self, max_results=10, **kwargs):
        super().__init__()
        self.max_results = max_results
        try:
            from duckduckgo_search import DDGS
            self.DDGS = DDGS
        except ImportError as e:
            raise ImportError(
                "Install `duckduckgo_search` with `pip install duckduckgo-search`."
            ) from e

    def forward(self, query: str) -> str:
        with self.DDGS() as ddgs:
            results = ddgs.text(query, max_results=self.max_results)
            if not results:
                return "No results found for this query."

            formatted = [
                f"[{r['title']}]({r['href']})\n{r.get('body', '')}" for r in results
            ]
            return "## Search Results\n\n" + "\n\n".join(formatted)