"""
Main entry point for the Legal Case Analysis AI agent workflow.
"""
# pylint: disable=line-too-long, unused-import, R0903, W0611 (adjust as needed)

import os
from typing import Literal, Annotated
import json # Import json for potential argument parsing if needed

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage # Added ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
# from langgraph.types import Command # Command is not used
from copilotkit.langgraph import copilotkit_emit_state, copilotkit_customize_config # Added copilotkit_customize_config

# Import the updated state definition and supporting types
from legal_case_analyze_agent.langgraph.state import AgentState, Source # Updated import path

# Import helper functions
from legal_case_analyze_agent.langgraph.known_cases import get_known_case_url # Updated import path
from legal_case_analyze_agent.langgraph.scraper import scrape_case_text # Updated import path
from legal_case_analyze_agent.langgraph.model import get_model # Added import


# --- Tool Definition ---
@tool
def WriteReport(report: Annotated[str, "The final formatted case report in Markdown."]):
    """Writes the final formatted case report."""
    # This tool doesn't need to *do* anything in Python,
    # its purpose is to be called by the LLM.
    # The actual state update happens via emitIntermediateState.
    print(f"--- WriteReport tool called (LLM generated report) ---")
    # We might log the report length or a preview here if needed for debugging
    # print(f"Report preview (from tool call): {report[:100]}...")
    # Return the report content so the calling node can potentially use it
    return report # Modified to return the report content


# --- Node Functions ---

def retrieve_case_node(state: AgentState) -> AgentState:
    """
    Node to retrieve case text based on caseName.
    Attempts scraping for known cases, otherwise signals for manual input.
    Resets state only when starting a completely new analysis.
    """
    print("--- Executing Retrieve Case Node ---")
    case_name = state.get('caseName', '').strip()
    messages = state.get('messages', [])
    
    # Explicit reset when caseName is provided and no active analysis
    is_new_analysis = (
        (not messages or 
         len(messages) <= 1 or 
         (case_name and not state.get('report'))) and 
        case_name  # Must have case name to start new analysis
    )

    # Reset state only if it's considered a new analysis run AND a case name is provided
    if is_new_analysis and case_name:
        print("--- Resetting state for new analysis ---")
        # Keep caseName, reset others
        state['caseText'] = None
        state['reportSections'] = {}
        state['report'] = ""
        state['needsManualInput'] = False
        state['sourcesConsulted'] = []
        state['logs'] = [] # Reset logs too for new analysis
        current_logs = []
        current_sources = []
    else:
        print("--- Retaining existing state (likely chat continuation or manual input follow-up) ---")
        current_logs = state.get('logs', [])
        current_sources = state.get('sourcesConsulted', [])
        # Don't reset needsManualInput here, rely on its current value or later logic

    existing_case_text = state.get('caseText') # Check text *after* potential reset

    log_message = f"Starting retrieval/check for case: {case_name}"
    log_done = False

    # If text was provided manually (or scraped previously) and we are re-invoked, skip scraping
    if existing_case_text:
        log_message = "Processing existing case text."
        log_done = True
        needs_manual_input = False # Already have text
        state['needsManualInput'] = False # Explicitly set false if text exists
    elif not case_name and is_new_analysis: # Only error if no case name on a new analysis run
        log_message = "Error: No case name provided for new analysis."
        log_done = True
        needs_manual_input = True # Or handle as error
        state['needsManualInput'] = True
    elif case_name: # Only scrape if case_name exists and no existing_case_text
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
                current_sources.append({"url": known_url, "title": f"Source for {case_name}", "description": "Automatically scraped"})
            else:
                log_message += "\nScrape failed. Manual input required."
                log_done = True
                needs_manual_input = True
        else:
            log_message += "\nCase not found in known list. Manual input required."
            log_done = True
            needs_manual_input = True
        state['needsManualInput'] = needs_manual_input # Update based on scrape result
    else:
        # This case (no case_name, not new analysis) should ideally not happen if routing is correct
        log_message = "Warning: retrieve_case_node called without caseName during continuation."
        log_done = True
        # Don't change needsManualInput here, rely on previous state


    # Update state logs and sources
    state['logs'] = current_logs + [{"message": log_message, "done": log_done}]
    # state['needsManualInput'] is updated within the logic above
    state['sourcesConsulted'] = current_sources

    return state


# Modify analyze_case_node again
async def analyze_case_node(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    Node to analyze caseText, generate report sections,
    instruct LLM to call WriteReport tool, and update report state directly.
    """
    print("--- Executing Analyze Case Node ---")
    # --- Customize config to suppress messages/tool calls ---
    # We will update the state directly in this node's return value
    config = copilotkit_customize_config(
        config,
        emit_messages=False,
        emit_tool_calls=False,
        # emit_intermediate_state=[] # Remove this
    )

    current_logs = state.get('logs', [])
    case_text = state.get('caseText')
    case_name = state.get('caseName', 'Unknown Case')
    current_sources = state.get('sourcesConsulted', [])

    if not case_text:
        current_logs.append({"message": "Error: Cannot analyze case, no case text found.", "done": True})
        state['logs'] = current_logs
        return state # Return early with error log

    # ... (text cleaning/processing remains the same) ...
    case_text = case_text.strip()
    if not case_text:
        current_logs.append({"message": "Error: Case text is empty after cleaning.", "done": True})
        state['logs'] = current_logs
        return state
    current_logs.append({"message": "Processing case text...", "done": False})
    case_text = case_text.replace('<p>', '').replace('</p>', '')
    case_text = ' '.join(case_text.split())
    paragraphs = case_text.split('\n\n')
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    case_text = '\n\n'.join(paragraphs)
    case_text = f"Case Text:\n\n{case_text}\n\nEnd of Case Text"

    current_logs.append({"message": "Initializing LLM and prompts...", "done": False})
    state['logs'] = current_logs

    # --- LLM Setup ---
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        error_msg = "Error: OPENAI_API_KEY environment variable not set."
        print(error_msg)
        current_logs.append({"message": error_msg, "done": True})
        state['logs'] = current_logs
        state['report'] = error_msg # Set error in report state
        return state # Return early

    try:
        llm = ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0)
        current_logs[-1]['message'] += "\nLLM Initialized."
    except Exception as e:
        error_msg = f"Error initializing LLM: {e}"
        print(error_msg)
        current_logs[-1]['message'] += f"\n{error_msg}"
        current_logs[-1]['done'] = True
        state['report'] = error_msg # Set error in report state
        return state # Return early

    # --- Generate Report Sections ---
    report_sections = state.get('reportSections', {}) # Initialize from state if exists
    analysis_errors = []
    llm_call_successful = True

    # Function to safely execute an LLM chain (with improved error handling for JSON)
    def run_chain(chain, input_data, section_name):
        nonlocal llm_call_successful, current_logs, analysis_errors
        log_entry_index = len(current_logs)
        current_logs.append({"message": f"Generating {section_name}...", "done": False})
        state['logs'] = current_logs
        print(f"--- Running chain for {section_name} ---")
        try:
            result = chain.invoke(input_data)
            current_logs[log_entry_index]['done'] = True
            return result
        except Exception as e:
            print(f"Error generating {section_name}: {e}")
            error_detail = f"Error generating {section_name}: {str(e)[:100]}..."
            current_logs[-1]['message'] += f"\n{error_detail}"
            current_logs[-1]['done'] = True
            analysis_errors.append(section_name)
            llm_call_successful = False # Mark failure for overall success tracking

            # Check if it's a JSON parsing error specifically
            is_json_parsing_error = "Invalid json output" in str(e) or isinstance(e, json.JSONDecodeError)

            # Return default structure on JSON error, otherwise an error message/structure
            if section_name == "Case Brief":
                # Return empty dict on JSON error, otherwise error dict
                return {} if is_json_parsing_error else {"Facts": "Error", "Issue": "Error", "Rule": "Error", "Holding/Reasoning": "Error"}
            elif section_name == "Cold Call Q&A":
                 # Return empty list on JSON error, otherwise error list
                return [] if is_json_parsing_error else [{"question": "Error", "answer": ""}]
            else:
                 # For StrOutputParser sections, return error message
                 return f"Error generating {section_name}."

    # Define chains for sections (with improved JSON instructions)
    basic_info_prompt = ChatPromptTemplate.from_template("Extract Case Name, Court, and Year from the start of this text: {case_text_snippet}. Format: 'Name | Court | Year'. Use N/A if missing.")
    basic_info_chain = basic_info_prompt | llm | StrOutputParser()

    summary_prompt = ChatPromptTemplate.from_template("Summarize the main point of the following legal text in about 50 words: {case_text}")
    summary_chain = summary_prompt | llm | StrOutputParser()

    brief_prompt_text = """You are an expert legal assistant tasked with creating a Case Brief based *only* on the provided legal case text. Adhere strictly to the following structure and instructions:

    Analyze the provided text and extract the following components:
    1.  **Facts:** Summarize the essential procedural and substantive facts leading to the legal dispute. Include key events, parties involved, and the lower court's decision if mentioned. Be objective and concise.
    2.  **Issue:** Identify the core legal question(s) the court is being asked to resolve in this specific case. Frame it as a clear, specific question (e.g., "Whether [action] violated [law] under [circumstances]?").
    3.  **Rule:** State the specific rule(s) of law (e.g., constitutional provision, statute, common law doctrine, precedent) that the court applies to decide the issue. Quote relevant legal text if possible, otherwise paraphrase accurately.
    4.  **Holding/Reasoning:** State the court's direct answer to the Issue(s) (the holding). Then, explain the court's step-by-step legal reasoning for reaching that holding, referencing the Rule(s) and applying them to the Facts. Explain *why* the court decided the way it did.

    Format the output STRICTLY as a single valid JSON object with keys "Facts", "Issue", "Rule", and "Holding/Reasoning".
    Ensure the entire output is ONLY the JSON object, starting with {{ and ending with }}. Do not include any text before or after the JSON.

    Case Text:
    ---
    {case_text}
    ---
    """
    brief_prompt = ChatPromptTemplate.from_template(brief_prompt_text)
    brief_chain = brief_prompt | llm | JsonOutputParser()

    qa_prompt_text = """You are simulating an experienced US law school professor preparing potential 'Cold Call' questions for students based *only* on the provided legal case text. Your goal is to test fundamental understanding of the case.

    Generate 3 to 5 insightful questions covering different key aspects:
    - The core facts or procedural history.
    - The main legal issue(s) addressed by the court.
    - The specific rule(s) of law applied or announced.
    - The court's holding and essential reasoning.
    - Potential implications or the significance of the case (if evident from the text).

    For each question generated, provide a concise and accurate answer derived *strictly* from the provided case text.

    Format the output STRICTLY as a valid JSON list of objects. Each object MUST have a "question" key (string) and an "answer" key (string).
    Ensure the entire output is ONLY the JSON list, starting with [ and ending with ]. Do not include any text before or after the JSON list.
    Example: [{{ "question": "...", "answer": "..." }}, {{ "question": "...", "answer": "..." }}]

    Case Text:
    ---
    {case_text}
    ---
    """
    qa_prompt = ChatPromptTemplate.from_template(qa_prompt_text)
    qa_chain = qa_prompt | llm | JsonOutputParser()

    # Run chains
    report_sections['basic_info'] = run_chain(basic_info_chain, {"case_text_snippet": case_text[:2000]}, "Basic Info")
    report_sections['summary'] = run_chain(summary_chain, {"case_text": case_text}, "Summary")
    brief_result = run_chain(brief_chain, {"case_text": case_text}, "Case Brief")
    report_sections['case_brief'] = brief_result # Will be {} if JSON parsing failed
    qa_result = run_chain(qa_chain, {"case_text": case_text}, "Cold Call Q&A")
    report_sections['cold_call_qa'] = qa_result # Will be [] if JSON parsing failed


    # --- Instruct LLM to Format and Call WriteReport Tool ---
    # Proceed even if some sections failed, but indicate errors if present.
    # Use default values for failed sections in the final prompt.
    current_logs.append({"message": "Instructing LLM to format report and call WriteReport tool...", "done": False})
    state['logs'] = current_logs
    print("--- Instructing LLM to call WriteReport tool ---")

    final_report_prompt_text = """
    You have analyzed a legal case and generated the following sections (some may contain errors or be empty if generation failed):

    Basic Info: {basic_info}
    Summary: {summary}
    Case Brief: {case_brief}
    Cold Call Q&A: {cold_call_qa}

    Now, format these sections into a single, well-structured Markdown report. If a section contains an error message or is empty, indicate that clearly in the report (e.g., "Case Brief: [Error during generation]").
    Then, call the 'WriteReport' tool with the complete Markdown report as the 'report' argument.
    Do not add any extra commentary before or after calling the tool. Just call the tool with the formatted report.
    """
    final_report_prompt = ChatPromptTemplate.from_messages([("system", final_report_prompt_text)])
    llm_with_tool = llm.bind_tools([WriteReport], tool_choice="WriteReport")
    final_chain = final_report_prompt | llm_with_tool

    final_report_content = "Error: Report generation failed." # Default error message
    llm_response = None # Initialize llm_response

    try:
        llm_response = await final_chain.ainvoke({
            "basic_info": report_sections.get('basic_info', '[Not Generated]'),
            "summary": report_sections.get('summary', '[Not Generated]'),
            "case_brief": json.dumps(report_sections.get('case_brief', {'Error': 'Brief generation failed'}), indent=2),
            "cold_call_qa": json.dumps(report_sections.get('cold_call_qa', [{'question': 'Error', 'answer': 'Q&A generation failed'}]), indent=2)
        }, config=config)

        print("--- LLM response (should contain WriteReport tool call):", llm_response)

        if llm_response.tool_calls and llm_response.tool_calls[0]['name'] == 'WriteReport':
            final_report_content = llm_response.tool_calls[0]['args'].get('report', 'Error: Could not extract report from tool call.')
            print(f"--- Extracted report content. Length: {len(final_report_content)} ---")
            current_logs[-1]['message'] += "\nLLM called WriteReport successfully."
            current_logs[-1]['done'] = True
        else:
            print("--- Error: LLM did not call WriteReport tool as expected. ---")
            current_logs[-1]['message'] += "\nError: LLM failed to call WriteReport tool."
            current_logs[-1]['done'] = True
            analysis_errors.append("WriteReport Tool Call Failed")
            final_report_content = "Error: Failed to generate final report via tool call."

    except Exception as e:
        error_msg = f"Error instructing LLM to call WriteReport: {e}"
        print(error_msg)
        current_logs[-1]['message'] += f"\n{error_msg}"
        current_logs[-1]['done'] = True
        analysis_errors.append("WriteReport Tool Call Exception")
        final_report_content = f"Error: Exception during final report generation - {e}"


    # --- Final State Update ---
    final_log_message = "Case analysis node finished."
    if analysis_errors:
        final_log_message += f" Errors occurred in: {', '.join(analysis_errors)}."
    current_logs.append({"message": final_log_message, "done": True})

    # Update the state dictionary to be returned
    updated_state = {
        "logs": current_logs,
        "sourcesConsulted": current_sources,
        "reportSections": report_sections, # Keep sections for potential debug/retry
        "report": final_report_content # Set the final report content (or error)
    }

    # Explicitly emit the final report state for the UI
    print("--- Emitting final report state update from analyze_case_node ---")
    state_to_emit_final = {
        "report": final_report_content,
        "logs": current_logs,
        "sourcesConsulted": current_sources,
        "caseName": case_name,
        "needsManualInput": state.get('needsManualInput', False),
        "analysis_complete": updated_state.get("analysis_complete", False)
    }
    await copilotkit_emit_state(config, state_to_emit_final)


    # Return the state dictionary directly. The graph will handle the next step based on route_message.
    # Add the AIMessage and ToolMessage (if successful) to the state's messages list.
    final_messages = state.get('messages', [])
    if llm_response:
        final_messages.append(llm_response)
        # Only add ToolMessage if analysis is being marked complete
        if llm_call_successful and not analysis_errors and 'WriteReport Tool Call Failed' not in analysis_errors:
            tool_message = ToolMessage(
                tool_call_id=llm_response.tool_calls[0]['id'],
                content="Report generated successfully.",
                name="WriteReport"
            )
            final_messages.append(tool_message)
            print("--- Added ToolMessage to state ---")

    # Mark analysis as complete if successful
    if llm_call_successful and not analysis_errors:
        updated_state["analysis_complete"] = True
        print("--- Analysis marked as complete ---")
    else:
        updated_state["analysis_complete"] = False
        print("--- Analysis not complete due to errors ---")

    updated_state["messages"] = final_messages
    print(f"Final message count: {len(final_messages)}")
    print("--- Returning updated state from analyze_case_node ---")
    print(f"Final state: {{"
          f"'analysis_complete': {updated_state.get('analysis_complete', False)}, "
          f"'report_exists': {bool(updated_state.get('report'))}, "
          f"'message_count': {len(final_messages)}}}")
    return updated_state


# chat_node remains the same
async def chat_node(state: AgentState, config: RunnableConfig) -> AgentState:
    # ... (chat_node implementation remains the same) ...
    print("--- Executing Chat Node ---")
    current_logs = state.get('logs', [])
    current_messages = state.get('messages', [])
    report_context = state.get('report', '') # Use the formatted report as primary context
    case_text_snippet = state.get('caseText', '')[:2000] # Maybe include a snippet of raw text
    case_name = state.get('caseName', 'Unknown Case') # Get case name for prompt

    if not current_messages or not isinstance(current_messages[-1], HumanMessage):
        # Only process if the last message is from the user
        print("Chat node skipped: No user message found.")
        # Return unchanged state or minimal update if needed
        return {"logs": current_logs} # Avoid returning full state if no action taken

    last_user_message = current_messages[-1].content
    log_message = f"Processing chat message: '{last_user_message[:50]}...'"
    current_logs.append({"message": log_message, "done": False})
    # state['logs'] = current_logs # Update logs within the returned dict

    # --- LLM Setup (Reuse or re-init) ---
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        error_msg = "Error: OPENAI_API_KEY missing for chat."
        print(error_msg)
        current_logs[-1]['message'] += f"\n{error_msg}"
        current_logs[-1]['done'] = True
        # Add error message to chat history and preserve report
        return {
            "messages": current_messages + [AIMessage(content=f"Sorry, I encountered an internal error and cannot respond right now ({error_msg}).")],
            "report": state.get('report', ''),
            "logs": current_logs
        }

    try:
        llm = ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0.7)
        current_logs[-1]['message'] += "\nLLM Initialized for chat."
    except Exception as e:
        error_msg = f"Error initializing LLM for chat: {e}"
        print(error_msg)
        current_logs[-1]['message'] += f"\n{error_msg}"
        current_logs[-1]['done'] = True
        # Add error message to chat history and preserve report
        return {
             "messages": current_messages + [AIMessage(content=f"Sorry, I encountered an internal error and cannot respond right now ({error_msg}).")],
             "report": state.get('report', ''),
             "logs": current_logs
        }

    # --- LLM Call for Chat ---
    try:
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
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=system_prompt),
        ])
        chat_chain = prompt | llm | StrOutputParser()
        response_content = chat_chain.invoke({"messages": current_messages}) # Pass history implicitly via MessagesState
        print(f"LLM chat response: {response_content}")
        current_logs[-1]['done'] = True

        # Return the response content and explicitly maintain the existing report state
        return {
            "messages": [AIMessage(content=response_content)],
            "report": state.get('report', ''), # Ensure report state is preserved
            "logs": current_logs
        }

    except Exception as e:
        error_msg = f"Error during chat generation: {e}"
        print(error_msg)
        current_logs[-1]['message'] += f"\n{error_msg}"
        current_logs[-1]['done'] = True
        # Add error message to chat history and preserve report
        return {
            "messages": current_messages + [AIMessage(content=f"Sorry, I encountered an error while generating a response: {error_msg}")],
            "report": state.get('report', ''), # Preserve report state on error
            "logs": current_logs
        }


# handle_error_node remains the same
def handle_error_node(state: AgentState) -> AgentState:
    # ... (handle_error_node implementation remains the same) ...
    print("--- Executing Error Handling Node ---")
    current_logs = state.get('logs', [])
    error_message = "An unexpected error occurred during processing."
    print(f"Error: {error_message}")
    current_logs.append({"message": error_message, "done": True})
    # Return minimal state update
    return {"logs": current_logs, "report": f"Error: {error_message}"}


# --- Conditional Edge Logic ---
# should_analyze remains the same
def should_analyze(state: AgentState) -> Literal["analyze_case_node", "wait_for_manual_input", "handle_error_node"]:
    # ... (should_analyze implementation remains the same) ...
    print("--- Checking Condition: Should Analyze? ---")
    needs_manual = state.get('needsManualInput', False)
    case_text = state.get('caseText')
    has_text = bool(case_text and case_text.strip())

    if needs_manual and not has_text:
        print("Decision: Wait for manual input.")
        return "wait_for_manual_input"
    elif has_text:
        print("Decision: Proceed to analysis.")
        # state['needsManualInput'] = False # Let analyze_case_node handle this if needed
        return "analyze_case_node"
    else:
        print("Decision: Error - No case text and not waiting for manual input.")
        return "handle_error_node"

# Updated route_message logic
def route_message(state: AgentState) -> Literal["chat_node", "retrieve_case_node", "handle_error_node", END]:
    """Routes logic based on the last message and current state."""
    print("--- Routing Message ---")
    messages = state.get('messages', [])
    has_report = bool(state.get('report', '').strip())
    case_name = state.get('caseName', '').strip()
    analysis_complete = state.get('analysis_complete', False)

    # Debug log current state
    print(f"Routing Debug - Case: {case_name}, Report: {has_report}, Complete: {analysis_complete}")
    if messages:
        print(f"Last message type: {type(messages[-1]).__name__}")

    # Case 1: Analysis already completed
    if analysis_complete:
        print("Decision: Analysis already complete - proceeding to chat")
        return "chat_node"
        
    # Case 2: Analysis not yet started (no report, case name exists)
    if case_name and not has_report:
        if messages:
            last_message = messages[-1]
            if isinstance(last_message, HumanMessage):
                last_msg = last_message.content.lower()
                if "analyze" in last_msg or "start" in last_msg:
                    print("Decision: Starting new analysis from human message (retrieve_case_node)")
                    return "retrieve_case_node"
                else:
                    print("Decision: Defaulting to analysis for human message with case name")
                    return "retrieve_case_node"
            elif isinstance(last_message, AIMessage):
                last_msg = last_message.content.lower()
                if "analyze" in last_msg or "proceed" in last_msg:
                    print("Decision: Starting new analysis from AI response (retrieve_case_node)")
                    return "retrieve_case_node"
            elif isinstance(last_message, ToolMessage):
                print("Decision: Processing ToolMessage as analysis trigger")
                return "retrieve_case_node"
        
        print(f"Decision: Defaulting to analysis for case '{case_name}'")
        return "retrieve_case_node"

    # Case 2: Analysis completed and report exists
    if has_report and analysis_complete:
        if messages and isinstance(messages[-1], HumanMessage):
            print("Decision: User message after analysis - continuing in chat mode (chat_node)")
            return "chat_node"
        elif messages and isinstance(messages[-1], AIMessage):
            print("Decision: AI message after analysis - ending flow")
            return END
        elif messages and isinstance(messages[-1], ToolMessage):
            print("Decision: ToolMessage after analysis - proceeding to chat mode (chat_node)")
            return "chat_node"
        print("Decision: Defaulting to chat mode after analysis completion")
        return "chat_node"

    # Case 3: Default chat behavior for human messages
    if messages and isinstance(messages[-1], HumanMessage):
        print("Decision: Default chat behavior for human message (chat_node)")
        return "chat_node"

    # Case 4: Error or unexpected state
    print("Decision: Ending flow due to unexpected state")
    return END

# route_message_node remains the same
def route_message_node(state: AgentState) -> dict:
     # ... (route_message_node implementation remains the same) ...
     print("--- Executing Router Node (no state change) ---")
     return {}

# --- Workflow Definition ---

workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("retrieve_case_node", retrieve_case_node)
workflow.add_node("analyze_case_node", analyze_case_node) # analyze_case_node now handles report update
workflow.add_node("chat_node", chat_node)
workflow.add_node("handle_error_node", handle_error_node)
workflow.add_node("route_message", route_message_node)

# Set entry point
workflow.set_entry_point("route_message")

# Define edges
workflow.add_conditional_edges(
    "route_message",
    route_message,
    {
        "chat_node": "chat_node",
        "retrieve_case_node": "retrieve_case_node",
        "handle_error_node": "handle_error_node",
        END: END
    }
)

workflow.add_conditional_edges(
    "retrieve_case_node",
    should_analyze,
    {
        "analyze_case_node": "analyze_case_node",
        "wait_for_manual_input": END,
        "handle_error_node": "handle_error_node"
    }
)
# analyze_case_node returns a state dict. The graph implicitly transitions
# back to the entry point ('route_message') after a node returns a state dict.
# No explicit edge needed here for the success case.
# workflow.add_edge("analyze_case_node", END) # Remove this edge

# chat_node should also end the flow after responding
workflow.add_edge("chat_node", END)
workflow.add_edge("handle_error_node", END) # Error node also ends the flow


# Compile the graph
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)

# ... (Remaining TODOs) ...
