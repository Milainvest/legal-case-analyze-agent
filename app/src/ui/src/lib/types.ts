// Renamed from Resource
export type Source = {
  url: string;
  title: string; // Agent should attempt to find/generate a title
  description: string; // Optional brief note from agent
};

export type Log = {
  message: string;
  done: boolean;
};

// Structure for the generated report parts (matching backend)
export type ReportSections = {
  basic_info: string; // Case Name, Parties, Court, Year
  summary: string; // ~150 chars Japanese summary
  case_brief: { [key: string]: string }; // Keys: Facts, Issue, Rule, Holding/Reasoning
  cold_call_qa: Array<{ question: string; answer: string }>; // List of {"question": "...", "answer": "..."}
};

// Updated AgentState to match backend state.py
export type AgentState = {
  model: string; // LLM identifier
  caseName: string; // Input case name
  caseText: string; // Raw text of the case fetched/provided
  reportSections: ReportSections; // Structured data for the report
  report: string; // Formatted Markdown version of reportSections for UI display
  sourcesConsulted: Source[]; // List of sources found by agent
  logs: Log[]; // For tracking agent progress
  needsManualInput?: boolean | null; // Optional field to signal UI for manual input
  // Implicitly includes chat history via MessagesState on backend
};
