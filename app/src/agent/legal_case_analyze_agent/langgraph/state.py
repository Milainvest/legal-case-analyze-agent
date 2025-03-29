"""
This is the state definition for the AI.
It defines the state of the agent and the state of the conversation.
"""

from typing import List, TypedDict, Dict # Added Dict
from langgraph.graph import MessagesState

class Source(TypedDict): # Renamed from Resource for clarity
    """
    Represents a source consulted by the agent during analysis.
    """
    url: str
    title: str # Agent should attempt to find/generate a title
    description: str # Optional brief note from agent

class Log(TypedDict):
    """
    Represents a log of an action performed by the agent.
    """
    message: str
    done: bool

# Structure for the generated report parts
class ReportSections(TypedDict):
    basic_info: str # Case Name, Parties, Court, Year
    summary: str # ~150 chars Japanese summary
    case_brief: Dict[str, str] # Keys: Facts, Issue, Rule, Holding/Reasoning
    cold_call_qa: List[Dict[str, str]] # List of {"question": "...", "answer": "..."}

class AgentState(MessagesState):
    """
    State for the Legal Case Analysis Agent.
    Inherits from MessagesState to handle chat history implicitly.
    """
    model: str # LLM identifier
    caseName: str # Input case name
    caseText: str # Raw text of the case fetched/provided
    reportSections: ReportSections # Structured data for the report
    report: str # Formatted Markdown version of reportSections for UI display
    sourcesConsulted: List[Source] # List of sources found by agent
    logs: List[Log] # For tracking agent progress
    # Optional field to signal UI for manual input
    needsManualInput: bool | None = None
