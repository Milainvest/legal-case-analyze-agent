"use client";

import { useCoAgent } from "@copilotkit/react-core";
import Main from "./Main";
import { ResearchStateProvider } from "@/lib/research-state-provider";
import { AgentState } from "@/lib/types";
import {
  ModelSelectorProvider,
  useModelSelectorContext,
} from "@/lib/model-selector-provider";
import { ModelSelector } from "@/components/ModelSelector";

// Define a default initial state for the agent
const initialAgentState: AgentState = {
  model: "",
  messages: [],
  caseName: "",
  caseText: "",
  report: "",
  reportSections: { basic_info: "", summary: "", case_brief: {}, cold_call_qa: [] },
  sourcesConsulted: [],
  logs: [],
  needsManualInput: false,
  error: null,
  connectionStatus: 'disconnected',
};

export default function ModelSelectorWrapper() {
  return (
    <ModelSelectorProvider>
      <Home />
      <ModelSelector />
    </ModelSelectorProvider>
  );
}

function Home() {
  const { agent } = useModelSelectorContext();
  
  // Manage agent state using useCoAgent
  const { state, setState, run } = useCoAgent<AgentState>({
    name: agent,
    initialState: initialAgentState,
  });

  return (
    <ResearchStateProvider
      initialState={state}
      setState={setState as React.Dispatch<React.SetStateAction<AgentState>>}
      run={run}
    >
      <Main />
    </ResearchStateProvider>
  );
}
