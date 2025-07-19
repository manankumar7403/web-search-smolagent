from typing import Any
from smolagents.tools import Tool
import requests
import markdownify
import re
from smolagents.utils import truncate_content
from requests.exceptions import RequestException

class VisitWebpageTool(Tool):
    name = "visit_webpage"
    description = "Visits a webpage at the given URL and reads its content as a markdown string. Use this to browse webpages."
    inputs = {'url': {'type': 'string', 'description': 'The URL of the webpage to visit.'}}
    output_type = "string"

    def __init__(self, *args, **kwargs):
        super().__init__()

    def forward(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()

            # Convert HTML to Markdown
            markdown_content = markdownify.markdownify(response.text).strip()

            # Clean up formatting
            markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)

            return truncate_content(markdown_content, 10000)

        except requests.exceptions.Timeout:
            return "The request timed out. Please try again later or check the URL."
        except RequestException as e:
            return f"Error fetching the webpage: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
