# MSMe Agentic AI — ADK Prototype

A runnable prototype and reference implementation of an **Agentic AI** system (ADK-style) designed to improve business workflows for small-to-medium retail MSMEs.
This project demonstrates key course concepts including multi-agent systems, LLM-powered agents, tools (custom & OpenAPI), long-running operations (pause/resume), sessions & memory, context engineering, observability, agent evaluation, the A2A protocol, and deployment patterns.

## Quickstart (local dev)

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the sample main to see a demo workflow:
   ```bash
   python -m msme_agent.main
   ```

3. Run tests:
   ```bash
   pytest -q
   ```
