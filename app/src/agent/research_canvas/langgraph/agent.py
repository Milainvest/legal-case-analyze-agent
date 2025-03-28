"""
Main entry point for the Legal Case Analysis AI agent workflow.
"""
# pylint: disable=line-too-long, unused-import, R0903, W0611 (adjust as needed)

from typing import Literal

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# Import the updated state definition and supporting types
from research_canvas.langgraph.state import AgentState, Source

# Import helper functions
from research_canvas.langgraph.known_cases import get_known_case_url
from research_canvas.langgraph.scraper import scrape_case_text


# --- Node Functions ---

def retrieve_case_node(state: AgentState) -> AgentState:
    """
    Node to retrieve case text based on caseName.
    Attempts scraping for known cases, otherwise signals for manual input.
    """
    print("--- Executing Retrieve Case Node ---")
    case_name = state.get('caseName', '').strip()
    current_logs = state.get('logs', [])
    current_sources = state.get('sourcesConsulted', [])
    case_text = None
    needs_manual_input = False
    log_message = f"Starting retrieval for case: {case_name}"
    log_done = False

    if not case_name:
        log_message = "Error: No case name provided."
        log_done = True
        needs_manual_input = True # Or handle as error
    elif state.get('caseText'):
        # If text was already provided (e.g., manually submitted earlier)
        log_message = "Case text already present in state."
        log_done = True
        needs_manual_input = False
        case_text = state['caseText'] # Ensure it's carried forward
    else:
        log_message = f"Checking known cases list for '{case_name}'..."
        known_url = get_known_case_url(case_name)

        if known_url:
            log_message += f"\nFound known URL: {known_url}. Attempting scrape..."
            scraped_text = scrape_case_text(known_url)
            if scraped_text:
                log_message += "\nScrape successful (Simulated/Actual)."
                log_done = True
                case_text = scraped_text
                needs_manual_input = False
                # Add URL as a source
                current_sources.append({"url": known_url, "title": f"Source for {case_name}", "description": "Automatically scraped"})
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
    if case_text:
        state['caseText'] = case_text
    state['sourcesConsulted'] = current_sources # Update sources if scrape was successful

# Added imports for LangChain/OpenAI
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.messages import SystemMessage, HumanMessage


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
        # Optionally, transition to an error state here
        return state

    current_logs.append({"message": "Initializing LLM and prompts...", "done": False})
    state['logs'] = current_logs

    # --- LLM Setup (Requires OPENAI_API_KEY in environment) ---
    try:
        # TODO: Allow model selection via state.model if needed
        llm = ChatOpenAI(model="gpt-4o", temperature=0) # Or another suitable model
        current_logs[-1]['message'] += "\nLLM Initialized."
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        current_logs[-1]['message'] += f"\nError initializing LLM: {e}"
        current_logs[-1]['done'] = True
        # Optionally, transition to an error state here
        return state

    # --- Placeholder LLM Calls & Prompting ---
    # TODO: Develop robust prompts for each section.
    # TODO: Implement proper error handling for LLM calls.
    # TODO: Consider parallel execution for efficiency if possible.

    report_sections = {}
    analysis_errors = []

    # 1. Basic Info (Example: Simple extraction prompt)
    try:
        current_logs.append({"message": "Generating Basic Info...", "done": False})
        state['logs'] = current_logs
        basic_info_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="Extract the basic case information (Case Name, Parties, Court, Year) from the following text. Output only the extracted information concisely."),
            HumanMessage(content=case_text[:4000]) # Limit context for this simple task
        ])
        basic_info_chain = basic_info_prompt | llm | StrOutputParser()
        report_sections['basic_info'] = basic_info_chain.invoke({}) # Pass empty dict if prompt doesn't need variables
        current_logs[-1]['done'] = True
    except Exception as e:
        print(f"Error generating Basic Info: {e}")
        current_logs[-1]['message'] += f"\nError: {e}"
        current_logs[-1]['done'] = True
        analysis_errors.append("Basic Info")
        report_sections['basic_info'] = "Error generating Basic Info."

    # 2. Summary (Japanese)
    try:
        current_logs.append({"message": "Generating Summary (Japanese)...", "done": False})
        state['logs'] = current_logs
        summary_prompt = ChatPromptTemplate.from_messages([
             SystemMessage(content="Summarize the following legal case text in Japanese, within 150 characters."),
             HumanMessage(content=case_text)
        ])
        summary_chain = summary_prompt | llm | StrOutputParser()
        report_sections['summary'] = summary_chain.invoke({})
        current_logs[-1]['done'] = True
    except Exception as e:
        print(f"Error generating Summary: {e}")
        current_logs[-1]['message'] += f"\nError: {e}"
        current_logs[-1]['done'] = True
        analysis_errors.append("Summary")
        report_sections['summary'] = "Error generating Summary."

    # 3. Case Brief (Example: Structured output prompt)
    try:
        current_logs.append({"message": "Generating Case Brief...", "done": False})
        state['logs'] = current_logs
        brief_prompt_text = """Analyze the provided legal case text and extract the following components for a Case Brief:
        - Facts: Key background facts of the case.
        - Issue: The main legal question(s) the court addressed.
        - Rule: The rule of law applied or established by the court.
        - Holding/Reasoning: The court's decision and the reasoning behind it.

        Format the output as a JSON object with keys "Facts", "Issue", "Rule", "Holding/Reasoning".

        Case Text:
        {case_text}"""
        brief_prompt = ChatPromptTemplate.from_template(brief_prompt_text)
        # Using JsonOutputParser requires the LLM to reliably output JSON
        brief_chain = brief_prompt | llm | JsonOutputParser()
        report_sections['case_brief'] = brief_chain.invoke({"case_text": case_text})
        current_logs[-1]['done'] = True
    except Exception as e:
        print(f"Error generating Case Brief: {e}")
        current_logs[-1]['message'] += f"\nError: {e}"
        current_logs[-1]['done'] = True
        analysis_errors.append("Case Brief")
        report_sections['case_brief'] = {"Facts": "Error", "Issue": "Error", "Rule": "Error", "Holding/Reasoning": "Error"}


    # 4. Cold Call Q&A
    try:
        current_logs.append({"message": "Generating Cold Call Q&A...", "done": False})
        state['logs'] = current_logs
        qa_prompt_text = """Based on the provided legal case text, generate 3-5 potential 'Cold Call' style questions a professor might ask about this case, along with concise, accurate answers based *only* on the text.

        Format the output as a JSON list of objects, where each object has a "question" key and an "answer" key. Example: [{"question": "What was the main issue?", "answer": "The main issue was..."}]

        Case Text:
        {case_text}"""
        qa_prompt = ChatPromptTemplate.from_template(qa_prompt_text)
        qa_chain = qa_prompt | llm | JsonOutputParser()
        report_sections['cold_call_qa'] = qa_chain.invoke({"case_text": case_text})
        current_logs[-1]['done'] = True
    except Exception as e:
        print(f"Error generating Cold Call Q&A: {e}")
        current_logs[-1]['message'] += f"\nError: {e}"
        current_logs[-1]['done'] = True
        analysis_errors.append("Cold Call Q&A")
        report_sections['cold_call_qa'] = [{"question": "Error generating questions.", "answer": ""}]


    # --- Update State ---
    state['reportSections'] = report_sections
    # TODO: Implement actual source tracking based on LLM responses or retrieval step
    # For now, just keep any sources found during retrieval
    state['sourcesConsulted'] = current_sources

    final_log_message = "Case analysis complete."
    if analysis_errors:
        final_log_message += f" Errors occurred in: {', '.join(analysis_errors)}."
    current_logs.append({"message": final_log_message, "done": True})
    state['logs'] = current_logs

    return state

def format_report_node(state: AgentState) -> AgentState:
    """Node to format reportSections into a Markdown string."""
    print("--- Executing Format Report Node ---")
    # TODO: Implement Markdown formatting logic
    state['logs'].append({"message": "Formatting report...", "done": False})
    sections = state.get('reportSections', {})
    brief = sections.get('case_brief', {})
    qa = sections.get('cold_call_qa', [])
    report_md = f"""
# Case Report: {state.get('caseName', 'Unknown Case')}

## Basic Information
{sections.get('basic_info', 'N/A')}

## Summary (Japanese)
{sections.get('summary', 'N/A')}

## Case Brief
**Facts:** {brief.get('Facts', 'N/A')}
**Issue:** {brief.get('Issue', 'N/A')}
**Rule:** {brief.get('Rule', 'N/A')}
**Holding/Reasoning:** {brief.get('Holding/Reasoning', 'N/A')}

## Cold Call Prep
"""
    for item in qa:
        report_md += f"**Q:** {item.get('question', 'N/A')}\n**A:** {item.get('answer', 'N/A')}\n\n"

    state['report'] = report_md.strip()
    state['logs'][-1]['done'] = True
    return state

def chat_node(state: AgentState) -> AgentState:
    """Node to handle chat interactions about the current case report."""
    print("--- Executing Chat Node ---")
    # TODO: Implement LLM call using state['messages'] and context (reportSections, caseText)
    # This node will likely modify state['messages'] implicitly via MessagesState
    state['logs'].append({"message": "Processing chat message...", "done": False})
    # Placeholder: Just log receipt for now
    last_message = state['messages'][-1].content if state['messages'] else "No message"
    print(f"Received chat message: {last_message}")
    # Simulate AI response (normally added by LangGraph/LLM)
    # state['messages'].append(AIMessage(content="Placeholder chat response."))
    state['logs'][-1]['done'] = True
    return state

def handle_error_node(state: AgentState) -> AgentState:
    """Node to handle errors during the workflow."""
    print("--- Executing Error Handling Node ---")
    # TODO: Implement error logging and potentially update state to reflect error
    state['logs'].append({"message": "An error occurred.", "done": True})
    # Decide if workflow should end or try to recover
    return state

# --- Conditional Edge Logic ---

def should_analyze(state: AgentState) -> Literal["analyze_case_node", "wait_for_manual_input", "handle_error_node"]:
    """Determines if analysis can proceed or if manual input is needed."""
    print("--- Checking Condition: Should Analyze? ---")
    if state.get('needsManualInput'):
        print("Decision: Wait for manual input.")
        # We will interrupt the graph after retrieve_case_node if this is true.
        # The UI needs to detect needsManualInput=True and provide the text area.
        # When the user submits text, the UI should update state.caseText and
        # potentially re-invoke the graph or signal the agent to continue.
        # For LangGraph, interrupting and then re-invoking with updated state is common.
        return "wait_for_manual_input" # This path leads to END in the graph for now.
    if state.get('caseText'):
        print("Decision: Proceed to analysis.")
        return "analyze_case_node"
    print("Decision: Error - No case text and not waiting for manual.")
    return "handle_error_node" # Or handle error state appropriately

# --- Workflow Definition ---

workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("retrieve_case_node", retrieve_case_node)
workflow.add_node("analyze_case_node", analyze_case_node)
workflow.add_node("format_report_node", format_report_node)
workflow.add_node("chat_node", chat_node) # Keep chat node definition, even if not in main flow
workflow.add_node("handle_error_node", handle_error_node)

# Set entry point
# The workflow starts when the user provides a caseName (likely via UI state change triggering agent)
workflow.set_entry_point("retrieve_case_node")

# Define edges for the main analysis flow
workflow.add_conditional_edges(
    "retrieve_case_node",
    should_analyze,
    {
        "analyze_case_node": "analyze_case_node",
        "wait_for_manual_input": END, # Interrupt workflow; UI handles manual input submission
        "handle_error_node": "handle_error_node"
    }
)
workflow.add_edge("analyze_case_node", "format_report_node")
workflow.add_edge("format_report_node", END) # Main analysis flow ends after formatting report
workflow.add_edge("handle_error_node", END)

# Chat interactions are handled separately, likely by invoking the graph
# with the 'chat_node' as the target or by managing chat state outside this main flow.
# The CopilotKit integration likely handles invoking the agent for chat messages.

# Compile the graph
memory = MemorySaver()
# Interrupt after retrieve_case_node if manual input is needed, allowing UI to react
graph = workflow.compile(checkpointer=memory, interrupt_after=["retrieve_case_node"])

# TODO: Implement the actual logic within the placeholder node functions.
# TODO: Refine how the workflow resumes after manual input is provided.
#       Typically, the UI updates the state (adds caseText) and re-invokes the graph.
