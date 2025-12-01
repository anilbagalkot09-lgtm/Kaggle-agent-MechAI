# Agentic AI for MSME Inventory (Google ADK)

This repository contains a full, submission-ready Agentic AI project built for the Google ADK coursework.
It implements a multi-agent system that optimizes inventory workflows for MSMEs using a Gemini-enabled ForecastAgent,
ReorderAgent, OrderAgent (long-running), OpsAgent, tools (MCP-style Inventory, Supplier OpenAPI), sessions, memory, and observability.

## Quickstart (local)
1. Create venv and install deps:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. (Optional) Provide Gemini API key in `.env`:
   ```bash
   LLM_PROVIDER=gemini
   GEMINI_API_KEY=YOUR_KEY_HERE
   GEMINI_MODEL=models/text-bison-001
   GEMINI_API_BASE=https://generativelanguage.googleapis.com/v1beta2
   ```
3. Start mock supplier (separate terminal):
   ```bash
   python mock_supplier.py
   ```
4. Run demo:
   ```bash
   python -m msme_adk.main_gemini
   ```
5. Run tests:
   ```bash
   pytest -q
   ```

## Repo layout
See `flow_adk_web.png` for architecture diagram (replace placeholder with your image).
