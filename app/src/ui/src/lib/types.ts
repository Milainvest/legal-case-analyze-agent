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

export interface CaseBrief {
  facts?: string;
  issue?: string;
  holding?: string;
  reasoning?: string;
}

export interface ReportSections {
  basic_info: string;
  summary: string;
  case_brief: CaseBrief;
  cold_call_qa: string[];
}

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: number;
}

// Updated AgentState to match backend state.py
export interface AgentState {
  model: string;
  caseName: string;
  caseText: string;
  reportSections: ReportSections;
  report: string;
  sourcesConsulted: Source[];
  logs: Log[];
  needsManualInput: boolean;
  messages: Message[];
  connectionStatus?: 'connecting' | 'connected' | 'disconnected' | 'error';
  error?: string | null;
}
