# MVP Development Tasks

This document outlines the remaining tasks to complete the Minimum Viable Product (MVP) for the Legal Case Analysis Agent, based on the initial setup and planning.

## Backend Agent (`app/src/agent/`)

1.  **Implement `retrieve_case_node` Logic (`agent.py` & new files):** [Completed]
    *   [X] Define the predefined list of ~20-30 known cases for initial scraping attempt (`known_cases.py` created).
    *   [X] Choose and implement a scraping library/method (`requests`, `BeautifulSoup` chosen).
    *   [X] Implement scraping logic for the known cases from designated sources (`scraper.py` implemented for Justia & CourtListener examples).
    *   [X] Implement the conditional logic: check known list -> attempt scrape -> set `state.needsManualInput = True` on failure or if not known (`agent.py` updated).
    *   [X] Ensure successful scrape populates `state.caseText` and `state.sourcesConsulted` (logic added in `agent.py`).
    *   [X] Add necessary dependencies to `pyproject.toml` and update `poetry.lock` (`requests`, `beautifulsoup4`, `copilot-runtime` added).

2.  **Implement `analyze_case_node` Logic (`agent.py` & new files):** [Refactored - Needs Testing]
    *   [X] Set up LangChain and OpenAI API client integration.
    *   [X] Develop prompts for LLM to generate report sections (Basic Info, Summary, Case Brief, Cold Call Q&A). JSON prompts improved.
    *   [X] Implement LLM calls for section generation with error handling (returns default values on JSON parse error).
    *   [X] Add prompt instructing LLM to format sections and call `WriteReport` tool.
    *   [X] Implement LLM call with `WriteReport` tool binding.
    *   [X] Extract report from tool call result and update `state.report` directly.
    *   [X] Use `copilotkit_customize_config` to manage state emission (`emitIntermediateState` removed, `emit_messages`/`emit_tool_calls` set to false).
    *   [X] Implement logic to track `state.sourcesConsulted`.

3.  **~~Implement `format_report_node` Logic (`agent.py`):~~** [Removed]
    *   ~~Refine the Markdown formatting logic.~~ (Functionality moved to LLM prompt within `analyze_case_node`).

4.  **Implement `chat_node` Logic (`agent.py` & potentially `chat.py`):** [Completed - Needs Testing]
    *   [X] Adapt the node to receive user messages via the `MessagesState`.
    *   [X] Implement LLM call logic, providing context from `state.reportSections` and `state.caseText`.
    *   [X] Ensure chat history is managed correctly (handled by `MessagesState` and LangGraph).

5.  **Refine Error Handling (`handle_error_node` in `agent.py`):** [Completed - Needs Testing]
    *   [X] Implement more robust error logging and state updates for workflow failures (Initial refinement done).

## Frontend UI (`app/src/ui/`)

6.  **Refine UI State Management (`Main.tsx`):** [Completed - Verified]
    *   [X] Created `.env.local` for UI API key.
    *   [X] Verify the `initialState` passed to `useCoAgent` fully aligns with the updated `AgentState` type.
    *   [X] Ensure UI components correctly react to state changes (e.g., displaying report, sources, manual input prompt) (Structure verified, needs runtime testing).
    *   [X] Corrected Agent ID used in `useCoAgent`.
    *   [X] Added `<CopilotKit>` provider to `layout.tsx`.

7.  **Implement Workflow Resumption Logic:** [Completed - Relies on State Update]
    *   [X] In `ResearchCanvas.tsx`, ensure `handleManualSubmit` correctly updates `state.caseText` and clears `state.needsManualInput` (Code added).
    *   [X] Determine and implement the mechanism to trigger the agent workflow to continue after manual text submission (Confirmed: State update + LangGraph checkpointer handles this).

## Testing & Integration

8.  **Agent Testing:**
    *   [ ] Write basic unit/integration tests for the implemented agent nodes (`retrieve`, `analyze`, `chat`).
9.  **End-to-End Testing:** [Completed - Basic Flow OK]
    *   [X] Manually test the full MVP flow:
        *   [X] Input known case -> Get report.
        *   [X] Input unknown case -> Get manual input prompt -> Paste text -> Get report.
        *   [X] Interact with chat about the generated report (Routing OK, response is placeholder).

## Documentation

10. **Update Memory Bank:**
    *   [X] Keep `activeContext.md` and `progress.md` updated as tasks are completed.
    *   [X] Update `systemPatterns.md` to reflect report generation refactoring.
    *   [ ] Update `techContext.md` if implementation details deviate significantly from the plan.

*(Note: Database setup (PostgreSQL/Vector DB) is deferred post-MVP based on the current plan focusing on manual input fallback and limited scraping).*
