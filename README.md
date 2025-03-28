# Legal Case Analysis Agent

This project provides an AI-powered agent designed to assist Japanese law students studying in the US with analyzing legal cases and preparing for class, particularly focusing on Socratic method/Cold Call scenarios.

The application consists of:

1.  **Frontend UI (`app/src/ui/`):** A Next.js application providing the user interface. Users can input a case name, view the generated report, and interact with an AI chat assistant. Built with shadcn/ui, Tailwind CSS, and CopilotKit.
2.  **Backend Agent (`app/src/agent/`):** A Python application using LangGraph, LangChain, and potentially FastAPI (or similar) to handle the core logic: retrieving case data (via scraping or manual input), analyzing the text using an LLM (e.g., OpenAI), generating structured reports, and managing chat interactions.

## Project Status (MVP Development)

The project is currently under development, focusing on the Minimum Viable Product (MVP). See `docs/task.md` for the current task list and `memory-bank/progress.md` for the latest status.

## Getting Started

### Prerequisites

*   Node.js and pnpm (for the UI)
*   Python (>=3.10, <3.13, recommend 3.12.x) and Poetry (for the Agent)
*   OpenAI API Key (set as an environment variable `OPENAI_API_KEY` for the agent)

### Running the Application

1.  **Run the Backend Agent:**
    ```bash
    cd app/src/agent
    # Activate your Python 3.12 virtual environment if not already active
    # e.g., source .venv/bin/activate
    poetry install # If dependencies changed
    # TODO: Add the command to run the agent service (e.g., uvicorn, python main.py)
    # Example placeholder:
    echo "Agent running (placeholder)... Ensure OPENAI_API_KEY is set."
    # Keep this terminal running
    ```

2.  **Run the Frontend UI:**
    ```bash
    cd app/src/ui
    pnpm install # If dependencies changed
    pnpm dev
    # Keep this terminal running
    ```

3.  Open your browser to [http://localhost:3000](http://localhost:3000) (or the configured port).

## Key Technologies

*   **Frontend:** Next.js, React, TypeScript, shadcn/ui, Tailwind CSS, CopilotKit
*   **Backend:** Python, LangGraph, LangChain, OpenAI, FastAPI (planned), Poetry
*   **Data Retrieval (MVP):** Web Scraping (`requests`, `BeautifulSoup`), Manual Input

## Documentation

*   **Requirements:** `docs/requirment_definition.md`
*   **Git Workflow:** `docs/git_workflow.md`
*   **Development Tasks:** `docs/task.md`
*   **Memory Bank:** `memory-bank/` (Contains project context, progress, etc.)

## Contributing

Please refer to the project's contribution guidelines (if available) or contact the maintainers.

## License

This repository's source code is available under the [MIT License](./LICENSE).
