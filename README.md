# Kaggle-agent-MechAI
Mech AI generates optimized CNC programs for simple aerospace components.
# MSMe Agentic AI — ADK Prototype

A runnable prototype and reference implementation of an **Agentic AI** system (ADK-style) designed to improve business workflows for small-to-medium retail MSMEs.  
This project demonstrates key course concepts including multi-agent systems, LLM-powered agents, tools (custom & OpenAPI), long-running operations (pause/resume), sessions & memory, context engineering, observability, agent evaluation, the A2A protocol, and deployment patterns.

> Folder structure in this repo matches the preferred GitHub layout:
>
> ```
> root/
> ├── msme_agent/
> ├── tests/
> ├── .gitignore
> ├── LICENSE
> ├── README.md
> ├── flow_adk_web.png
> ├── requirements.txt
> └── thumbnail.png
> ```

---

## Project overview

**Use case:** Optimize inventory ordering, supplier interactions, and fulfillment for a retail MSME. Agents forecast demand, calculate reorder points, place orders with suppliers, and coordinate operations — all while keeping sessions, long-term memory, and observability.

**Core Agents**
- `ForecastAgent` — LLM-powered forecasting agent; uses loop/iterative refinement and context compaction.
- `ReorderAgent` — computes reorder points and quantities using forecasts, inventory state, and safety stock rules.
- `OrderAgent` — places supplier orders via an OpenAPI tool and implements pause/resume for long-running order lifecycle.
- `OpsAgent` — orchestrator and human-in-the-loop coordinator; receives notifications and handles approvals.

**Tools**
- `InventoryDBTool` — MCP-style custom tool to read/write inventory.
- `SupplierOpenAPITool` — OpenAPI client that places orders and reads statuses.
- `SearchTool` — built-in style tool (mockable) for market/product signals.
- `CodeExecTool` — executes small verification scripts (e.g., compute EOQ, sanity checks).

**Core Infrastructure**
- `A2A` message envelope & router for agent-to-agent communication.
- `InMemorySessionService` for workflow persistence (pause/resume).
- `MemoryBank` for long-term storage and embedding-enabled retrieval (placeholder).
- Observability module for structured logging, traces, and Prometheus metrics.
- Evaluation harness (scenario-based testing & KPIs).

---

## Requirements

This prototype is written in **Python 3.10+** (optional conversion to Node/TS is straightforward). See `requirements.txt` for Python dependencies.

---

## Quickstart (local dev)

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

