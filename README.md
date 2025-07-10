---
title: First HF Agent
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

# ⚡ First HF Agent Template

Welcome to **First HF Agent Template** – a simple and extensible agent setup using [Smol Agents](https://github.com/smol-ai/smol-agent), built to run on Hugging Face Spaces using Gradio.

This project serves as a minimal template to get started with building autonomous AI agents that can reason, plan, and execute tasks via tools.

![Hugging Face Spaces](https://img.shields.io/badge/HuggingFace-Spaces-blue?logo=huggingface)
![Gradio SDK](https://img.shields.io/badge/Gradio-5.35.0-orange?logo=python)

## Features

- Built using [Smol Agents](https://github.com/smol-ai/smol-agent)
- Gradio-based interface for agent interaction
- Ready-to-extend tool system
- Lightweight and beginner-friendly template

## Technologies Used

- Python
- [Gradio](https://gradio.app) `v5.35.0`
- Hugging Face Spaces
- Smol Agent (Tool-based agent framework)

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

### Running on Hugging Face Spaces

Make sure your `README.md` includes the configuration block at the top (already included above).

## Contributing

Contributions are welcome! Please fork the repo and open a pull request.

## License
This project is licensed under the [MIT License](LICENSE).
