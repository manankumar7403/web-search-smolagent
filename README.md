---
title: Web Search Smol Agent
emoji: ⚡
colorFrom: pink
colorTo: yellow
sdk: gradio
sdk_version: 5.35.0
app_file: app.py
pinned: false
tags:
- smolagents
- agent
- smolagent
- tool
- web-search
---

# Web Search Smol Agent

Welcome to **Web Search Smol Agent** – a powerful and extensible AI agent with web search capabilities, built using [Smol Agents](https://github.com/huggingface/smolagents) and deployed on Hugging Face Spaces with Gradio.

This project demonstrates how to build autonomous AI agents that can search the web, browse websites, and provide intelligent responses by combining multiple tools and reasoning capabilities.

![Hugging Face Spaces](https://img.shields.io/badge/HuggingFace-Spaces-blue?logo=huggingface)
![Gradio SDK](https://img.shields.io/badge/Gradio-5.35.0-orange?logo=python)
![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)

## Demo

Try it out on [Hugging Face Spaces](https://huggingface.co/spaces/manankumar7403/HF_Agent)

## Features

- **Web Search** - Powered by DuckDuckGo search integration
- **Webpage Browsing** - Visit and extract content from any URL
- **Smart Agent Logic** - Built on [Smol Agents](https://github.com/huggingface/smolagents) framework
- **Gradio Interface** - Easy-to-use web interface
- Ready-to-extend tool system
- Lightweight and beginner-friendly template


## Technologies Used

- **Python 3.8+**
- **[Gradio](https://gradio.app) v5.35.0** - Web interface framework
- **[Smol Agents](https://github.com/huggingface/smolagents)** - Agent framework
- **DuckDuckGo Search** - Web search functionality
- **Qwen2.5-Coder-32B** - Language model for reasoning
- **Hugging Face Spaces** - Deployment platform

## Project Structure

```
first_agent/
├── app.py                # Gradio app entry point
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
├── prompts.yaml          # Prompt templates (optional, keep at root or in /agents)
├── tools/                # Custom tools for the agent
│   ├── final_answer.py
│   ├── visit_webpage.py
│   └── web_search.py
├── agent.json            # Agent logic and configuration
├── Gradio_UI.py
└── .gitattributes
```

## Getting Started

### Fork and Clone

1. **Fork this repository** on GitHub
2. **Clone your fork**:

```bash
git clone https://github.com/manankumar7403/web-search-smolagent.git
cd web-search-smolagent
```

### Local Installation

3. **Create a virtual environment** (recommended):

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

4. **Install dependencies**:

```bash
pip install -r requirements.txt
```

**Required packages include:**
- `smolagents`
- `gradio==5.35.0`
- `duckduckgo-search`
- `requests`
- `markdownify`
- `pytz`
- `pyyaml`

5. **Run locally**:

```bash
python app.py
```

### Deploy to Hugging Face Spaces

1. Create a new Space on [Hugging Face Spaces](https://huggingface.co/spaces)
2. Choose **Gradio** as the SDK
3. Upload your files or connect your GitHub repository
4. The Space will automatically deploy using the configuration in the README header

## Usage Examples

Once running, you can ask the agent to:

- **Search the web**: "Search for the latest news about AI"
- **Browse websites**: "Visit this website and summarize its content"
- **Get current time**: "What's the current time in Tokyo?"
- **Combine tasks**: "Search for Python tutorials and visit the top result"

## Customization

### Adding New Tools

You can extend the agent's capabilities by adding new tools in the `tools/` directory. Each tool should inherit from the `Tool` class:

```python
from smolagents.tools import Tool

class YourCustomTool(Tool):
    name = "your_tool_name"
    description = "Description of what your tool does"
    inputs = {'param': {'type': 'string', 'description': 'Parameter description'}}
    output_type = "string"
    
    def forward(self, param: str) -> str:
        # Pls add your tool logic here
        return result
```

### Modifying Prompts

Edit the `prompts.yaml` file to customize the agent's behavior, system instructions, and response patterns.

### Changing the Model

In `app.py`, you can switch to different models by modifying the `model_id` parameter:

```python
model = HfApiModel(
    model_id='your-preferred-model',  # Change this
    max_tokens=2096,
    temperature=0.5,
)
```

## Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## License
This project is licensed under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/manankumar7403/web-search-smolagent/issues) page
2. Create a new issue if your problem isn't already reported
3. For general questions about Smol Agents, refer to their [documentation](https://github.com/huggingface/smolagents)
