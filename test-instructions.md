To test the application, please follow these steps:

1. **Start the Backend Agent:**
    - Open a terminal.
    - Navigate to the agent directory: `cd app/src/agent`
    - Activate your Python virtual environment (e.g., `source .venv/bin/activate`).
    - Ensure your `OPENAI_API_KEY` is correctly set in the `.env` file within this directory.
    - Run the FastAPI server using: `uvicorn server:app --reload --port 8000`
    - Keep this terminal open and observe the logs printed by the agent nodes.
2. **Start the Frontend UI:**
    - Open a *second* terminal.
    - Navigate to the UI directory: `cd app/src/ui`
    - Run the development server: `pnpm dev`
    - Keep this terminal open.
3. **Test in Browser:**
    - Open your web browser and go to `http://localhost:3000`.
    - **Test Case 1 (Known Case):**
        - Enter `marbury v. madison` into the "Case Name" input field.
        - Observe: Does the backend log show "Scrape successful (Simulated fallback)" or "Scrape successful (Justia structure found)"? Does the UI eventually display a placeholder report in the "Generated Case Report" area? Does the "Sources Consulted" section show the Justia URL?
    - **Test Case 2 (Unknown Case -> Manual Input):**
        - Refresh the page or clear the state if necessary.
        - Enter `my unknown test case` into the "Case Name" input field.
        - Observe: Does the backend log show "Case not found in known list"? Does the "Manual Case Text Input Required" section appear in the UI?
        - Paste some sample text (e.g., "This is the manually provided text for the test case.") into the manual input textarea and click "Submit Case Text".
        - Observe: Does the backend log show the analysis and formatting nodes running? Does the UI display a placeholder report based on the manual text?
    - **Test Case 3 (Chat):**
        - After a report is generated (from either test case 1 or 2), type a question into the chat input on the right side (e.g., "What are the facts?") and submit it.
        - Observe: Does the backend log show "Processing chat message..."? Does a placeholder response appear in the chat UI?

Please perform these tests and report back any errors you encounter in the terminals or browser console, or any unexpected behavior in the UI. This will help identify what needs refinement.