# System Patterns

## Architecture Overview

*   The system utilizes a **Frontend-Backend Architecture** for the MVP, with plans for a Microservices Architecture later. (Ref: docs/requirment_definition.md Section 4.2, 4.3)
*   **Frontend:** Next.js (AppRouter) using CopilotKit for agent interaction.
*   **Backend:** FastAPI serving a LangGraph agent via CopilotKit integration.
*   **AI Processing:** LangGraph orchestrates the flow, using LangChain and OpenAI API for analysis and generation.
*   **State Management:** LangGraph's `MemorySaver` (in-memory checkpointer) persists state between agent runs. `useCoAgent` hook syncs state with the frontend.
*   **Data Retrieval:** Primarily web scraping (`requests`, `BeautifulSoup`) for known cases, with manual text input as fallback. Database integration (PostgreSQL, Vector DB) is deferred post-MVP.

*   **MVP Agent Workflow (LangGraph):**
    ```mermaid
    graph TD
        A[route_message] --> B{Last Msg Human?};
        B -- Yes --> C{Report Exists?};
        B -- No --> Z[END];
        C -- Yes --> D[chat_node];
        C -- No --> E[retrieve_case_node];
        D --> Z;
        E --> F{Text Available?};
        F -- Yes --> G[analyze_case_node];
        F -- No --> H{Manual Input Needed?};
        F -- Error --> Y[handle_error_node];
        G -- Calls WriteReport Tool --> G; # Internal loop for tool call
        G -- Updates state.report --> Z; # Node finishes after updating state
        H -- Yes --> Z;
        H -- No --> Y;
        Y --> Z;
    ```
    *   **Nodes:**
        *   `route_message` (Entry Point): Determines flow based on message history and report status.
        *   `retrieve_case_node`: Fetches case text (scrape or signals manual input). Refined reset logic.
        *   `analyze_case_node`: Analyzes `caseText`, generates `reportSections`, then instructs the LLM to call the `WriteReport` tool with the formatted Markdown report. Updates `state.report` directly from the tool call result before ending. Uses `copilotkit_customize_config` to suppress direct message/tool call emissions.
        *   `chat_node`: Handles user queries about the generated report using `state.report` and `state.messages` as context. Preserves `report` state.
        *   `handle_error_node`: Logs errors and potentially updates state to indicate failure.
    *   **Conditional Edges:** Logic based on message type, report existence, text availability, and manual input flags.
    *   **State Update for Report:** `analyze_case_node` updates `state.report` directly after the LLM calls the `WriteReport` tool. A final `copilotkit_emit_state` call sends necessary UI state updates.

## Key Technical Decisions

*   **Backend Framework:** FastAPI chosen for Python backend. (Ref: 5.1)
*   **Frontend Framework:** Next.js (AppRouter) selected for the TypeScript frontend. (Ref: 5.2)
*   **AI Orchestration:** LangGraph used for defining the agent workflow. LangChain used for LLM interactions within nodes. (Implementation Detail)
*   **Agent-UI Communication:** CopilotKit SDK (`useCoAgent`, `<CopilotChat>`, `copilotkit_customize_config`, `copilotkit_emit_state`) manages state synchronization and interaction flow. (Implementation Detail)
*   **Report Generation:** Shifted from node-based formatting (`format_report_node`) to LLM calling a `WriteReport` tool within `analyze_case_node`, aligning with CopilotKit examples. (Implementation Detail)
*   **Databases:** Deferred post-MVP. (Ref: 5.1)
*   **Asynchronous Processing:** Not implemented for MVP (RabbitMQ deferred). (Ref: 5.1)

## Design Patterns

*   **State Machine:** LangGraph implements a state machine pattern for the agent workflow. (Implementation Detail)
*   **Tools / Function Calling:** LangChain tools (`@tool` decorator) are used, including `WriteReport`, invoked by the LLM. (Implementation Detail)
*   **Dependency Injection:** Supported by FastAPI. (Ref: 5.1)
*   **ORM:** SQLAlchemy planned but deferred. (Ref: 5.1)
*   [Other patterns TBD]

## Component Relationships

*   **Frontend (`Main.tsx`, `ResearchCanvas.tsx`) <-> Backend API (`/api/copilotkit/route.ts`):** CopilotKit runtime handles communication via WebSockets.
*   **Backend API (`route.ts`) -> Agent Server (`demo.py`):** CopilotKit runtime forwards requests to the FastAPI server hosting the LangGraph agent.
*   **Agent Server (`demo.py`) -> LangGraph (`agent.py`):** Executes the defined LangGraph workflow (`graph.stream` or `graph.invoke`).
*   **LangGraph Nodes -> AI Services:** API calls to OpenAI via LangChain wrappers (`ChatOpenAI`).
*   **LangGraph Nodes -> External Sources:** Web scraping via `requests`/`BeautifulSoup` in `scraper.py`.

*(This file documents the technical blueprint based on requirements and current implementation details. Updated after refactoring report generation.)*
