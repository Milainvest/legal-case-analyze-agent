"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button"; // Added for manual input submit
import {
  useCoAgent,
  useCoAgentStateRender,
  // useCopilotAction, // Removed DeleteResources action
} from "@copilotkit/react-core";
import { Progress } from "./Progress";
// import { EditResourceDialog } from "./EditResourceDialog"; // Removed
// import { AddResourceDialog } from "./AddResourceDialog"; // Removed
import { Resources } from "./Resources";
import { AgentState, Source } from "@/lib/types"; // Updated type import
import { useModelSelectorContext } from "@/lib/model-selector-provider";

export function ResearchCanvas() {
  const { model, agent } = useModelSelectorContext();

  // Ensure initial state aligns with the new AgentState structure in Main.tsx
  const { state, setState, run } = useCoAgent<AgentState>({
    name: agent,
    // initial state is primarily set in Main.tsx, but ensure defaults here if needed
    initialState: {
      model,
      caseName: "",
      caseText: "",
      reportSections: { basic_info: "", summary: "", case_brief: {}, cold_call_qa: [] },
      report: "",
      sourcesConsulted: [],
      logs: [],
      needsManualInput: false,
    },
  });

  useCoAgentStateRender({
    name: agent,
    render: ({ state, nodeName, status }) => {
      // Display logs if they exist
      if (!state.logs || state.logs.length === 0) {
        return null;
      }
      // Filter out potentially sensitive caseText from logs if desired
      const filteredLogs = state.logs; //.filter(log => !log.message.includes("caseText"));
      return <Progress logs={filteredLogs} />;
    },
  });

  // Removed useCopilotAction for DeleteResources

  const sources: Source[] = state.sourcesConsulted || [];
  // Removed setResources, addResource, removeResource, editResource logic

  // State for manual input
  const [manualCaseText, setManualCaseText] = useState("");

  const handleManualSubmit = () => {
    if (manualCaseText.trim()) {
      setState({
        ...state,
        caseText: manualCaseText,
        needsManualInput: false, // Signal that input is provided
        logs: [...(state.logs || []), { message: "Manual case text provided.", done: true }],
      });
      setManualCaseText(""); // Clear the input field
      // Explicitly trigger the agent to continue processing
      run();
    }
  };


  return (
    <div className="w-full h-full overflow-y-auto p-10 bg-[#F5F8FF]">
      <div className="space-y-8 pb-10">
        <div>
          <h2 className="text-lg font-medium mb-3 text-primary">
            Case Name
          </h2>
          <Input
            placeholder="Enter the case name (e.g., Marbury v. Madison)"
            value={state.caseName || ""}
            onChange={(e) =>
              // Only update caseName and reset results when input changes.
              // Let the backend agent determine if manual input is needed.
              setState({
                ...state,
                caseName: e.target.value,
                caseText: "", // Clear previous text
                reportSections: { basic_info: "", summary: "", case_brief: {}, cold_call_qa: [] }, // Clear previous results
                report: "", // Clear previous report
                sourcesConsulted: [], // Clear previous sources
                logs: [], // Clear previous logs
                needsManualInput: false // Reset manual input flag
              })
            }
            // TODO: Add an explicit "Analyze" button or trigger analysis on blur/enter
            // Currently, analysis might only trigger implicitly via chat or other actions.
            aria-label="Case name"
            className="bg-background px-6 py-8 border-0 shadow-none rounded-xl text-md font-extralight focus-visible:ring-0 placeholder:text-slate-400"
          />
          {/* Add Analyze button to explicitly trigger the workflow */}
          <Button onClick={() => run()} disabled={!state.caseName?.trim()} className="mt-2">
             Analyze Case
          </Button>
        </div>

        {/* Conditional Manual Input Section */}
        {state.needsManualInput && (
          <div>
            <h2 className="text-lg font-medium mb-3 text-primary text-orange-600">
              Manual Case Text Input Required
            </h2>
            <p className="text-sm text-slate-500 mb-2">
              The agent could not automatically retrieve the text for this case. Please paste the full case text below.
            </p>
            <Textarea
              placeholder="Paste the full case text here..."
              value={manualCaseText}
              onChange={(e) => setManualCaseText(e.target.value)}
              rows={15}
              aria-label="Manual case text input"
              className="bg-background px-6 py-8 border-gray-300 shadow-sm rounded-xl text-sm focus-visible:ring-1 placeholder:text-slate-400 mb-2"
            />
            <Button onClick={handleManualSubmit} disabled={!manualCaseText.trim()}>
              Submit Case Text
            </Button>
          </div>
        )}

        {/* Display Sources Consulted */}
        <div>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-medium text-primary">Sources Consulted by Agent</h2>
            {/* Removed Add/Edit Dialog buttons */}
          </div>
          {sources.length === 0 && !state.logs?.some(log => log.message.includes("Analyzing")) && (
             <div className="text-sm text-slate-400">
               Sources will appear here after analysis.
             </div>
           )}
          {sources.length > 0 && (
            <Resources
              resources={sources} // Display sourcesConsulted
              // Removed handleCardClick and removeResource props as it's read-only
            />
          )}
        </div>

        {/* Display Generated Report */}
        <div className="flex flex-col h-full">
          <h2 className="text-lg font-medium mb-3 text-primary">
            Generated Case Report
          </h2>
          <Textarea
            data-test-id="case-report"
            placeholder="The generated case report will appear here..."
            value={state.report || ""} // Bind to state.report
            readOnly // Make it read-only as it's generated content
            rows={15} // Increased rows for potentially long reports
            aria-label="Generated case report"
            className="bg-background px-6 py-8 border-0 shadow-none rounded-xl text-md font-extralight focus-visible:ring-0 placeholder:text-slate-400"
            style={{ minHeight: "300px" }} // Increased min height
          />
        </div>
      </div>
    </div>
  );
}
