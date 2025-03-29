"""
Main entry point for the Legal Case Analysis AI agent workflow.
"""
# pylint: disable=line-too-long, unused-import, R0903, W0611 (adjust as needed)

import os
from typing import Literal

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage # Added AIMessage
from langchain_core.runnables import RunnableConfig # Added import
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from copilotkit.langgraph import copilotkit_emit_state # Added import

# Import the updated state definition and supporting types
from legal_case_analyze_agent.langgraph.state import AgentState, Source # Updated import path

# Import helper functions
from legal_case_analyze_agent.langgraph.known_cases import get_known_case_url # Updated import path
from legal_case_analyze_agent.langgraph.scraper import scrape_case_text # Updated import path
from legal_case_analyze_agent.langgraph.model import get_model # Added import


# --- Node Functions ---

def retrieve_case_node(state: AgentState) -> AgentState:
    """
    Node to retrieve case text based on caseName.
    Attempts scraping for known cases, otherwise signals for manual input.
    """
    print("--- Executing Retrieve Case Node ---")
    case_name = state.get('caseName', '').strip()
    existing_case_text = state.get('caseText') # Check if text exists from previous step (manual input)

    # Only reset if caseText is NOT already provided (i.e., starting fresh analysis)
    if not existing_case_text:
        print("--- Resetting state for new analysis ---")
        current_logs = []
        current_sources = []
        state['caseText'] = None
        state['reportSections'] = {}
        state['report'] = ""
        state['needsManualInput'] = False
    else:
        print("--- Retaining existing caseText (likely from manual input) ---")
        # Keep existing text, just update logs
        current_logs = state.get('logs', [])
        current_sources = state.get('sourcesConsulted', [])
        # Ensure needsManualInput is false if we have text
        state['needsManualInput'] = False


    log_message = f"Starting retrieval/check for case: {case_name}"
    log_done = False

    # If text was provided manually and we are re-invoked, skip scraping/checking known list
    if existing_case_text:
        log_message = "Processing manually provided case text."
        log_done = True
        needs_manual_input = False # Already have text
    elif not case_name:
        log_message = "Error: No case name provided."
        log_done = True
        needs_manual_input = True # Or handle as error
    else:
        # Only check known list/scrape if starting fresh (no existing_case_text)
        log_message = f"Checking known cases list for '{case_name}'..."
        known_url = get_known_case_url(case_name)

        if known_url:
            log_message += f"\nFound known URL: {known_url}. Attempting scrape..."
            scraped_text = scrape_case_text(known_url)
            if scraped_text:
                log_message += "\nScrape successful."
                log_done = True
                state['caseText'] = scraped_text # Set the scraped text
                needs_manual_input = False
                # Add URL as a source
                current_sources.append({"url": known_url, "title": f"Source for {case_name}", "description": "Automatically scraped"})
                # Log the first few characters of the scraped text for debugging
                log_message += f"\nScraped text preview: {scraped_text[:200]}..."
                # Add debug logging for text length
                log_message += f"\nTotal text length: {len(scraped_text)} characters"
            else:
                log_message += "\nScrape failed. Manual input required."
                log_done = True
                needs_manual_input = True
        else:
            log_message += "\nCase not found in known list. Manual input required."
            log_done = True
            needs_manual_input = True

    # Update state
    state['logs'] = current_logs + [{"message": log_message, "done": log_done}]
    state['needsManualInput'] = needs_manual_input
    state['sourcesConsulted'] = current_sources # Update sources if scrape was successful

    return state


def analyze_case_node(state: AgentState) -> AgentState:
    """Node to analyze caseText and generate reportSections using LLM."""
    print("--- Executing Analyze Case Node ---")
    current_logs = state.get('logs', [])
    case_text = state.get('caseText')
    case_name = state.get('caseName', 'Unknown Case')
    current_sources = state.get('sourcesConsulted', []) # Carry over sources from retrieval

    if not case_text:
        current_logs.append({"message": "Error: Cannot analyze case, no case text found.", "done": True})
        state['logs'] = current_logs
        return state

    # Add debug logging for case text
    current_logs.append({"message": f"Case text length: {len(case_text)} characters", "done": False})
    current_logs.append({"message": f"Case text preview: {case_text[:200]}...", "done": False})
    state['logs'] = current_logs

    # Clean and normalize the text
    case_text = case_text.strip()
    if not case_text:
        current_logs.append({"message": "Error: Case text is empty after cleaning.", "done": True})
        state['logs'] = current_logs
        return state

    # Add more detailed text processing
    current_logs.append({"message": "Processing case text...", "done": False})
    # Remove any HTML tags that might have been missed
    case_text = case_text.replace('<p>', '').replace('</p>', '')
    # Remove extra whitespace and normalize line breaks
    case_text = ' '.join(case_text.split())

    # Split text into paragraphs for better structure
    paragraphs = case_text.split('\n\n')
    # Clean each paragraph
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    # Rejoin with proper spacing
    case_text = '\n\n'.join(paragraphs)

    # Add section markers for better structure
    case_text = f"Case Text:\n\n{case_text}\n\nEnd of Case Text"

    # Log the processed text structure
    current_logs.append({"message": f"Processed text length: {len(case_text)} characters", "done": False})
    current_logs.append({"message": f"Number of paragraphs: {len(paragraphs)}", "done": False})
    current_logs.append({"message": f"First paragraph preview: {paragraphs[0][:200]}...", "done": False})
    state['logs'] = current_logs

    current_logs.append({"message": "Initializing LLM and prompts...", "done": False})
    state['logs'] = current_logs

    # --- LLM Setup (Requires OPENAI_API_KEY environment variable) ---
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        error_msg = "Error: OPENAI_API_KEY environment variable not set."
        print(error_msg)
        current_logs.append({"message": error_msg, "done": True}) # Append new log entry
        state['logs'] = current_logs
        # Optionally, transition to an error state here
        return state # Stop processing if key is missing

    try:
        # TODO: Allow model selection via state.model if needed
        llm = ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0) # Or another suitable model
        current_logs[-1]['message'] += "\nLLM Initialized."
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        current_logs[-1]['message'] += f"\nError initializing LLM: {e}"
        current_logs[-1]['done'] = True
        # Optionally, transition to an error state here
        return state

    # --- LLM Calls & Prompting ---
    # TODO: Further refine prompts for accuracy, robustness, and specific legal nuances.
    # TODO: Implement more sophisticated error handling (e.g., retries with backoff, validation of LLM output structure).
    # TODO: Consider parallelizing these LLM calls (e.g., using asyncio or LangChain's batch/stream capabilities) for better performance.

    report_sections = {}
    analysis_errors = []
    llm_call_successful = True # Flag to track if any LLM call failed

    # Function to safely execute an LLM chain with added logging
    def run_chain(chain, input_data, section_name):
        nonlocal llm_call_successful, current_logs # Ensure logs are updated correctly
        log_entry_index = len(current_logs) # Get index for updating later
        current_logs.append({"message": f"Generating {section_name}...", "done": False})
        state['logs'] = current_logs # Update state for logging visibility
        print(f"--- Running chain for {section_name} with input keys: {list(input_data.keys())} ---") # Log input keys
        # Log the actual input data being passed
        print(f"--- Input data for {section_name}: {input_data} ---")
        try:
            result = chain.invoke(input_data)
            print(f"--- Raw result for {section_name}: {result} ---") # Log raw result
            current_logs[log_entry_index]['done'] = True
            return result
        except Exception as e:
            print(f"Error generating {section_name}: {e}")
            error_detail = f"Error generating {section_name}: {str(e)[:100]}..." # Limit error length
            current_logs[-1]['message'] += f"\n{error_detail}"
            current_logs[-1]['done'] = True
            analysis_errors.append(section_name)
            llm_call_successful = False # Mark failure
            # Return a specific error structure or message for this section
            error_message = f"Error generating {section_name}."
            if section_name == "Case Brief":
                # Return dict with error message in each field
                return {key: error_message for key in ["Facts", "Issue", "Rule", "Holding/Reasoning"]}
            elif section_name == "Cold Call Q&A":
                 # Return list with a single error object
                return [{"question": error_message, "answer": ""}]
            else:
                 # Return simple error string for basic info and summary
                return error_message

    # 1. Basic Info - Simplified Prompt Attempt
    basic_info_prompt = ChatPromptTemplate.from_template(
        "Extract Case Name, Court, and Year from the start of this text: {case_text_snippet}. Format: 'Name | Court | Year'. Use N/A if missing."
    )
    basic_info_chain = basic_info_prompt | llm | StrOutputParser()
    report_sections['basic_info'] = run_chain(basic_info_chain, {"case_text_snippet": case_text[:2000]}, "Basic Info")

    # 2. Summary (Japanese) - Simplified Prompt Attempt (Removed Japanese constraint for debugging)
    summary_prompt = ChatPromptTemplate.from_template(
        "Summarize the main point of the following legal text in about 50 words: {case_text}"
    )
    summary_chain = summary_prompt | llm | StrOutputParser()
    report_sections['summary'] = run_chain(summary_chain, {"case_text": case_text}, "Summary") # Changed section name for clarity


    # 3. Case Brief (Structured JSON) - Previously Refined Prompt
    brief_prompt_text = """You are an expert legal assistant tasked with creating a Case Brief based *only* on the provided legal case text. Adhere strictly to the following structure and instructions:

    Analyze the provided text and extract the following components:
    1.  **Facts:** Summarize the essential procedural and substantive facts leading to the legal dispute. Include key events, parties involved, and the lower court's decision if mentioned. Be objective and concise.
    2.  **Issue:** Identify the core legal question(s) the court is being asked to resolve in this specific case. Frame it as a clear, specific question (e.g., "Whether [action] violated [law] under [circumstances]?").
    3.  **Rule:** State the specific rule(s) of law (e.g., constitutional provision, statute, common law doctrine, precedent) that the court applies to decide the issue. Quote relevant legal text if possible, otherwise paraphrase accurately.
    4.  **Holding/Reasoning:** State the court's direct answer to the Issue(s) (the holding). Then, explain the court's step-by-step legal reasoning for reaching that holding, referencing the Rule(s) and applying them to the Facts. Explain *why* the court decided the way it did.

    Format the output STRICTLY as a single JSON object with keys "Facts", "Issue", "Rule", and "Holding/Reasoning". Ensure the value for each key is a well-formatted string containing the detailed analysis for that section.

    Case Text:
    ---
    {case_text}
    ---
    """
    brief_prompt = ChatPromptTemplate.from_template(brief_prompt_text)
    # Ensure the LLM is instructed or fine-tuned to reliably output valid JSON.
    # JsonOutputParser will attempt to parse the LLM's string output as JSON.
    brief_chain = brief_prompt | llm | JsonOutputParser()
    brief_result = run_chain(brief_chain, {"case_text": case_text}, "Case Brief")
    # Ensure the result is a dict, even if run_chain returned an error structure
    report_sections['case_brief'] = brief_result if isinstance(brief_result, dict) else {"Facts": "Error", "Issue": "Error", "Rule": "Error", "Holding/Reasoning": "Error"}


    # 4. Cold Call Q&A (Structured JSON) - Refined Prompt
    qa_prompt_text = """You are simulating an experienced US law school professor preparing potential 'Cold Call' questions for students based *only* on the provided legal case text. Your goal is to test fundamental understanding of the case.

    Generate 3 to 5 insightful questions covering different key aspects:
    - The core facts or procedural history.
    - The main legal issue(s) addressed by the court.
    - The specific rule(s) of law applied or announced.
    - The court's holding and essential reasoning.
    - Potential implications or the significance of the case (if evident from the text).

    For each question generated, provide a concise and accurate answer derived *strictly* from the provided case text.

    Format the output STRICTLY as a JSON list of objects. Each object MUST have a "question" key (string) and an "answer" key (string).
    Example: [{{"question": "What was the key factual dispute between the parties?", "answer": "The dispute centered on whether..."}}, {{"question": "What rule did the court apply regarding [topic]?", "answer": "The court applied the rule that..."}}]

    Case Text:
    ---
    {case_text}
    ---
    """
    qa_prompt = ChatPromptTemplate.from_template(qa_prompt_text)
    # Ensure the LLM is instructed or fine-tuned to reliably output valid JSON.
    # JsonOutputParser will attempt to parse the LLM's string output as JSON.
    qa_chain = qa_prompt | llm | JsonOutputParser()
    # Corrected input dictionary to only include 'case_text' as defined in the prompt template
    qa_result = run_chain(qa_chain, {"case_text": case_text}, "Cold Call Q&A")
     # Ensure the result is a list, even if run_chain returned an error structure
    report_sections['cold_call_qa'] = qa_result if isinstance(qa_result, list) else [{"question": "Error generating questions.", "answer": ""}]
    # Check if the result was actually an error message string from run_chain
    if not isinstance(qa_result, list) and isinstance(qa_result, str) and "Error generating" in qa_result:
         print(f"LLM call failed for Cold Call Q&A, result: {qa_result}")


    # --- Update State ---
    # Assign the generated sections (or error messages/structures) to the state
    state['reportSections'] = report_sections

    # Source Tracking: For MVP, we associate the initially retrieved source(s)
    # with the entire analysis. More granular tracking is a future enhancement.
    state['sourcesConsulted'] = current_sources # Keep sources from retrieval step

    final_log_message = "Case analysis complete."
    if analysis_errors:
        final_log_message += f" Errors occurred in: {', '.join(analysis_errors)}."
    current_logs.append({"message": final_log_message, "done": True})
    state['logs'] = current_logs

    return state

async def format_report_node(state: AgentState, config: RunnableConfig) -> AgentState: # Made async and added config
    """Node to format reportSections into a Markdown string and emit state."""
    print("\n=== Format Report Node Debug ===")
    print("1. Initial State Check:")
    print("- State keys:", list(state.keys()))
    print("- ReportSections present:", 'reportSections' in state)
    print("- Report present before formatting:", 'report' in state)
    
    current_logs = state.get('logs', [])
    state['logs'] = current_logs + [{"message": "Formatting report...", "done": False}]
    sections = state.get('reportSections', {})
    
    print("\n2. Report Sections Content:")
    print("- Basic Info:", sections.get('basic_info', 'N/A'))
    print("- Summary:", sections.get('summary', 'N/A'))
    print("- Case Brief Keys:", list(sections.get('case_brief', {}).keys()))
    print("- Number of Q&A items:", len(sections.get('cold_call_qa', [])))
    
    brief = sections.get('case_brief', {})
    qa = sections.get('cold_call_qa', [])

    # Ensure brief parts are strings, default to 'N/A' if missing or error
    facts = brief.get('Facts', 'N/A') if isinstance(brief.get('Facts'), str) else 'N/A'
    issue = brief.get('Issue', 'N/A') if isinstance(brief.get('Issue'), str) else 'N/A'
    rule = brief.get('Rule', 'N/A') if isinstance(brief.get('Rule'), str) else 'N/A'
    holding = brief.get('Holding/Reasoning', 'N/A') if isinstance(brief.get('Holding/Reasoning'), str) else 'N/A'

    report_md = f"""
# Case Report: {state.get('caseName', 'Unknown Case')}

## Basic Information
{sections.get('basic_info', 'N/A')}

---

## Summary (Japanese)
{sections.get('summary', 'N/A')}

---

## Case Brief

### Facts
{facts}

### Issue
{issue}

### Rule
{rule}

### Holding/Reasoning
{holding}

---

## Cold Call Prep
"""
    if isinstance(qa, list):
        for i, item in enumerate(qa):
            # Ensure question and answer are strings
            q = item.get('question', 'N/A') if isinstance(item.get('question'), str) else 'N/A'
            a = item.get('answer', 'N/A') if isinstance(item.get('answer'), str) else 'N/A'
            report_md += f"**Q{i+1}:** {q}\n**A{i+1}:** {a}\n\n"
    else:
        report_md += "Could not generate Q&A.\n\n"


    state['report'] = report_md.strip()
    
    print("\n3. Final Report Check:")
    print("- Report length:", len(state['report']))
    print("- Report preview (first 200 chars):", state['report'][:200])
    print("- Report present after formatting:", 'report' in state)
    print("- State keys after update:", list(state.keys()))
    print("=== End Format Report Node Debug ===\n")

    state['logs'][-1]['done'] = True

    # Explicitly emit the state update to CopilotKit after formatting
    print("--- Emitting final state update from format_report_node ---")
    await copilotkit_emit_state(config, state)

    return state

async def chat_node(state: AgentState, config: RunnableConfig) -> AgentState: # Made async and added config
    """
    Node to handle chat interactions about the current case report.
    Uses the current chat history and report context.
    """
    print("--- Executing Chat Node ---")
    current_logs = state.get('logs', [])
    current_messages = state.get('messages', [])
    report_context = state.get('report', '') # Use the formatted report as primary context
    case_text_snippet = state.get('caseText', '')[:2000] # Maybe include a snippet of raw text
    case_name = state.get('caseName', 'Unknown Case') # Get case name for prompt

    if not current_messages or not isinstance(current_messages[-1], HumanMessage):
        # Only process if the last message is from the user
        print("Chat node skipped: No user message found.")
        return state

    last_user_message = current_messages[-1].content
    log_message = f"Processing chat message: '{last_user_message[:50]}...'"
    current_logs.append({"message": log_message, "done": False})
    state['logs'] = current_logs

    # --- LLM Setup (Reuse or re-init) ---
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        error_msg = "Error: OPENAI_API_KEY missing for chat."
        print(error_msg)
        current_logs[-1]['message'] += f"\n{error_msg}"
        current_logs[-1]['done'] = True
        # Add error message to chat history
        state['messages'] = current_messages + [AIMessage(content=f"Sorry, I encountered an internal error and cannot respond right now ({error_msg}).")]
        return state

    try:
        # TODO: Ensure LLM is available (might be initialized globally or passed)
        llm = ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0.7) # Allow more conversational temp
        current_logs[-1]['message'] += "\nLLM Initialized for chat."
    except Exception as e:
        error_msg = f"Error initializing LLM for chat: {e}"
        print(error_msg)
        current_logs[-1]['message'] += f"\n{error_msg}"
        current_logs[-1]['done'] = True
        # Add error message to chat history
        state['messages'] = current_messages + [AIMessage(content=f"Sorry, I encountered an internal error and cannot respond right now ({error_msg}).")]
        return state

    # --- Placeholder LLM Call for Chat ---
    # TODO: Develop a robust chat prompt that effectively uses chat history (`state['messages']`) and the report context.
    # TODO: Implement proper error handling for the chat LLM call.
    try:
        # System prompt providing context and instructions.
        # LangGraph + MessagesState should automatically include the chat history.
        system_prompt = f"""You are a helpful AI legal assistant for law students.
        You are currently discussing the case: '{case_name}'.
        Base your answers *only* on the provided Case Report Context and the ongoing conversation history.
        Be concise, accurate, and helpful. If a question cannot be answered from the provided context, clearly state that. Do not invent information.

        Case Report Context:
        ---
        {report_context}
        ---
        (Context ends here)
        """

        # Construct the messages to send (System Prompt + History)
        # LangGraph's MessagesState typically handles history automatically when invoking chains.
        # We might just need to define the chain structure.

        # Example Chain (assuming history is handled implicitly by MessagesState context):
        # prompt = ChatPromptTemplate.from_messages([
        #     SystemMessage(content=system_prompt),
        #     MessagesPlaceholder(variable_name="messages") # LangGraph uses this key
        # ])
        # chat_chain = prompt | llm | StrOutputParser()
        # response_content = chat_chain.invoke({"messages": current_messages}) # Pass full history?

        # --- Simulation ---
        # Since the exact chain invocation depends on deeper LangGraph/CopilotKit integration details,
        # we'll keep the simulation but note that the AIMessage should NOT be manually appended.
        # The actual chain invocation should return the response content string.
        print(f"Simulating LLM call for chat with system prompt and history (last message: '{last_user_message[:50]}...')")
        response_content = f"Placeholder response regarding: '{last_user_message[:30]}...' about '{case_name}'"
        print(f"Simulated chat response: {response_content}")

        # IMPORTANT: When using LangGraph with MessagesState, the node should typically return
        # a dictionary containing the response message content under a specific key (often the key
        # matching the AIMessage placeholder in the state, or just the content string if the graph
        # is configured to handle it). LangGraph then updates the 'messages' state.
        # DO NOT manually append AIMessage here in the final implementation.
        # For placeholder:
        # state['messages'] = current_messages + [AIMessage(content=response_content)]
        # Correct approach is likely returning the content for LangGraph to handle:
        # return {"messages": [AIMessage(content=response_content)]} # Or similar, check LangGraph docs

        current_logs[-1]['done'] = True
        # Return the state, assuming LangGraph handles message appending based on node output
        # If the node needs to return the message explicitly:
        # return {"messages": [AIMessage(content=response_content)]}
        # For now, just return the state as the placeholder doesn't modify messages directly
        return state # Return state directly for placeholder

    except Exception as e:
        error_msg = f"Error during chat generation: {e}"
        print(error_msg)
        current_logs[-1]['message'] += f"\n{error_msg}"
        current_logs[-1]['done'] = True
        # Add error message to chat history
        state['messages'] = current_messages + [AIMessage(content=f"Sorry, I encountered an error while generating a response: {error_msg}")]

    return state


def handle_error_node(state: AgentState) -> AgentState:
    """Node to handle errors detected during the workflow."""
    print("--- Executing Error Handling Node ---")
    current_logs = state.get('logs', [])
    # TODO: Implement more specific error logging based on where the error occurred (if possible to determine from state).
    # For now, just log a generic error message.
    error_message = "An unexpected error occurred during processing."
    print(f"Error: {error_message}") # Log to console/server logs
    current_logs.append({"message": error_message, "done": True})

    # Update state to reflect the error clearly for the UI if needed
    # state['report'] = f"Error: {error_message}" # Example: Update report field
    # state['reportSections'] = {} # Clear sections

    state['logs'] = current_logs
    # The workflow currently ends after this node. Recovery logic could be added later.
    return state


async def send_proactive_message_node(state: AgentState, config: RunnableConfig) -> AgentState:
    """Generates a proactive follow-up message after report generation."""
    print("--- Executing Send Proactive Message Node ---")
    current_logs = state.get('logs', [])
    current_messages = state.get('messages', [])
    report_preview = state.get('report', '')[:500] # Get a preview for context

    log_message = "Generating proactive follow-up message..."
    current_logs.append({"message": log_message, "done": False})
    state['logs'] = current_logs

    # Simple proactive message for now
    proactive_message_content = "The case report has been generated. What aspects would you like to discuss further, or shall we move on to Cold Call practice?"

    # Add the proactive message as an AIMessage
    # IMPORTANT: This message should ideally be generated by an LLM based on the report,
    # but for now, we use a static message.
    proactive_ai_message = AIMessage(content=proactive_message_content)

    # Update state
    state['messages'] = current_messages + [proactive_ai_message]
    current_logs[-1]['done'] = True
    state['logs'] = current_logs

    # Emit state so the UI shows the proactive message
    print("--- Emitting state update from send_proactive_message_node ---")
    await copilotkit_emit_state(config, state)

    return state


# --- Conditional Edge Logic ---

def should_analyze(state: AgentState) -> Literal["analyze_case_node", "wait_for_manual_input", "handle_error_node"]:
    """Determines if analysis can proceed or if manual input is needed."""
    print("--- Checking Condition: Should Analyze? ---")
    needs_manual = state.get('needsManualInput', False) # Default to False if not set
    case_text = state.get('caseText') # Get caseText without default value
    has_text = bool(case_text and case_text.strip()) # Check if text exists and is not just whitespace

    if needs_manual and not has_text:
        print("Decision: Wait for manual input.")
        # Interrupt the graph. UI should show input field.
        # When user submits, UI updates state.caseText and state.needsManualInput=False,
        # then re-invokes the graph.
        return "wait_for_manual_input" # This edge leads to END for now.
    elif has_text:
        print("Decision: Proceed to analysis.")
        # Ensure needsManualInput is false if we have text
        state['needsManualInput'] = False
        return "analyze_case_node"
    else:
        # This case should ideally not be reached if retrieve_case_node logic is correct
        # (it should either set caseText or set needsManualInput=True)
        print("Decision: Error - No case text and not waiting for manual input.")
        return "handle_error_node"

# --- New Router Node ---
def route_message(state: AgentState) -> Literal["chat_node", "retrieve_case_node"]:
    """
    Determines the next node based on the last message.
    Returns the *name* of the next node, not a state update.
    The node itself should return an empty dict or state updates if needed.
    """
    print("--- Routing Message ---")
    messages = state.get('messages', [])
    if messages and isinstance(messages[-1], HumanMessage):
        print("Decision: Route to chat_node")
        return "chat_node"
    else:
        # If no messages or last message is not Human, start/continue analysis flow
        print("Decision: Route to retrieve_case_node")
        return "retrieve_case_node"

# --- Node function for the router (returns empty dict as it only routes) ---
def route_message_node(state: AgentState) -> dict:
     """This node function simply returns an empty dict. Routing is handled by conditional edges."""
     print("--- Executing Router Node (no state change) ---")
     return {}

# --- Workflow Definition ---

workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("retrieve_case_node", retrieve_case_node)
workflow.add_node("analyze_case_node", analyze_case_node)
workflow.add_node("format_report_node", format_report_node)
workflow.add_node("chat_node", chat_node)
workflow.add_node("handle_error_node", handle_error_node)
workflow.add_node("route_message", route_message_node) # Add the new router node function
workflow.add_node("send_proactive_message_node", send_proactive_message_node) # Add the proactive message node

# Set entry point to the new router
workflow.set_entry_point("route_message") # Changed entry point

# Define edges
workflow.add_conditional_edges(
    "route_message", # The source node name
    route_message,   # The function that decides which node to go to next
    {
        "chat_node": "chat_node", # Map the decision string to the target node name
        "retrieve_case_node": "retrieve_case_node"
    }
)

workflow.add_conditional_edges(
    "retrieve_case_node",
    should_analyze,
    {
        "analyze_case_node": "analyze_case_node",
        "wait_for_manual_input": END, # Interrupt workflow; UI handles manual input submission & re-invocation
        "handle_error_node": "handle_error_node"
    }
)
workflow.add_edge("analyze_case_node", "format_report_node")
# workflow.add_edge("format_report_node", END) # OLD: End after formatting
workflow.add_edge("format_report_node", "send_proactive_message_node") # NEW: Go to proactive message node
workflow.add_edge("send_proactive_message_node", END) # NEW: End after sending proactive message

# After chat node finishes, loop back to router to decide next step (could be END or another node)
# For now, let chat simply end the current invocation. CopilotKit will likely trigger a new one for the next message.
workflow.add_edge("chat_node", END)

workflow.add_edge("handle_error_node", END)


# Compile the graph
memory = MemorySaver()
# The graph should only interrupt if the conditional edge leads to END (wait_for_manual_input).
graph = workflow.compile(checkpointer=memory) # Removed interrupt_after

# TODO: Implement actual scraping logic in scraper.py
# TODO: Implement robust prompt engineering in analyze_case_node and chat_node.
# TODO: Implement source tracking logic in analyze_case_node.
# TODO: Implement detailed error handling and potentially retries.
# TODO: Verify the mechanism for resuming the graph after manual input with CopilotKit.
# TODO: Verify how CopilotKit invokes the graph for chat messages vs. explicit run() calls.
