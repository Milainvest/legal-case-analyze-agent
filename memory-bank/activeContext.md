# Active Context

## Current Focus

*   Initializing the project Memory Bank based on `docs/requirment_definition.md`.
*   Planning the initial development steps for the MVP.
*   Debugging runtime errors during initial testing.
*   Correcting import paths after directory rename.
*   Refining placeholder logic in agent nodes.
*   Fixing UI trigger for agent workflow.
*   Fixing agent workflow routing for chat vs. analysis.
*   Completing initial End-to-End testing.

## Recent Changes

*   Created initial Memory Bank files (`projectbrief.md`, `productContext.md`, `activeContext.md`, `systemPatterns.md`, `techContext.md`, `progress.md`).
*   Populated `projectbrief.md`, `productContext.md`, and `systemPatterns.md` based on requirements.
*   Updated agent state definition (`state.py`).
*   Modified UI component (`ResearchCanvas.tsx`) for case name input, report display, sources display, and manual text input.
*   Restructured agent workflow (`agent.py`) with new nodes and conditional logic (using placeholders).
*   Created `docs/task.md` outlining remaining MVP development tasks.
*   Added dependencies (`requests`, `beautifulsoup4`) to agent environment.
*   Created `known_cases.py` and `scraper.py` (with placeholder logic).
*   Implemented initial logic for `retrieve_case_node` in `agent.py` (Task 1).
*   Force reinstalled UI dependencies to resolve potential TS errors.
*   Implemented placeholder logic for `analyze_case_node` (Task 2) and `chat_node` (Task 4) in `agent.py`, including basic LangChain structure.
*   Confirmed workflow resumption logic (Task 7) relies on state updates and LangGraph checkpointer mechanism.
*   Refined placeholder logic for `analyze_case_node` (Task 2) and `format_report_node` (Task 3) in `agent.py`.
*   Refined placeholder scraping logic in `scraper.py` (Task 1 refinement).
*   Refined placeholder chat logic in `chat_node` (Task 4 refinement).
*   Refined placeholder error handling logic in `handle_error_node` (Task 5 refinement).
*   Verified UI state management structure in `Main.tsx` (Task 6).
*   Implemented initial scraping logic for Justia & CourtListener URLs in `scraper.py` (Task 1 completion).
*   Refined placeholder logic, API key check, and all prompts within `analyze_case_node` (Task 2 refinement complete).
*   Confirmed MVP source tracking logic is in place within `analyze_case_node`.
*   Reverted `server.py` to use CopilotKit runtime, aligning with frontend implementation.
*   Confirmed `copilotkit` dependency is listed in `pyproject.toml`.
*   Refined chat logic (`chat_node` - Task 4) considering CopilotKit integration.
*   Refined error handling within `analyze_case_node`'s `run_chain` (Task 2 refinement complete).
*   Corrected `copilot-runtime` import path and error message in `server.py` (removed sys.path hack).
*   Added `copilot-runtime` dependency to `pyproject.toml`.
*   Created `.env.local` file for UI API key.
*   Corrected import paths in agent files (`agent.py`, `server.py`, `demo.py`, `langgraph/*`, `crewai/*`) after directory rename.
*   Corrected `initialState` definition in `Main.tsx`.
*   Reverted agent ID in `Main.tsx` to `research_agent` to match `server.py`.
*   Added `<CopilotKit>` provider to UI layout (`layout.tsx`).
*   Corrected Q&A chain invocation in `analyze_case_node`.
*   Further refined Basic Info and Summary prompts in `analyze_case_node` (Task 2 refinement).
*   Added debug logging to `run_chain` helper in `analyze_case_node`.
*   Corrected state reset logic in `retrieve_case_node`.
*   Added "Analyze Case" button to `ResearchCanvas.tsx` to explicitly trigger workflow.
*   Successfully tested unknown case / manual input flow end-to-end.
*   Corrected LangGraph routing logic in `agent.py` (added `route_message_node`, fixed conditional edge).
*   Successfully tested chat routing logic end-to-end.

## Next Steps

*   Update `progress.md` and `docs/task.md`.
*   Begin Agent Testing (unit/integration tests - Task 8).
*   Continue refining placeholder logic (prompts, scraping, error handling) based on further testing/needs.

## Active Decisions & Considerations

*   Confirming the interpretation of requirements documented in the Memory Bank.
*   Prioritizing features for the MVP implementation.
*   Finalizing the detailed architecture for core components (e.g., AI prompt design, database schema).
*   **MVP Data Retrieval Strategy:** Decided on a hybrid approach for `retrieve_case_node`. It will first check if the `caseName` matches a predefined list (~20-30 cases) and attempt scraping. If not found or scrape fails, it will signal the UI to request manual text pasting from the user.
*   **API Key Handling:** Agent loads key from `app/src/agent/.env`. UI API route loads key from `app/src/ui/.env.local`.
*   **CopilotKit Import:** Relying on installed `copilot-runtime` package.

*(This file tracks the current state of work and immediate plans. Updated after completing initial E2E tests.)*
