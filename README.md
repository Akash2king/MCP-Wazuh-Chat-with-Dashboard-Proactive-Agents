# MCP Server Basic Example

A basic implementation of a **Model Context Protocol (MCP)** server that demonstrates core functionality, including tools and resources. This guide will walk you through the steps to initialize, inspect, and integrate the server.

## Getting Started

Before you begin, ensure you have the following installed:

- **Python** (Version 3.8 or later)
- **uv CLI**

To verify your installation, run:
```bash
    python --version
    uv --version
```

### Initialization

To initialize the project, navigate to a local folder of your choice and launch your terminal (PowerShell or CMD). Then, run:

```bash
    uv init mcp-ai-chat-langchain
``` 

### To add a new dependency 

```bash
    uv add langchain-groq
    uv addlangchain-openai
    uv add mcp-use
``` 

### To execute the project

```bash
    uv run app.py
```

This will set up the project directory and install the necessary dependencies.