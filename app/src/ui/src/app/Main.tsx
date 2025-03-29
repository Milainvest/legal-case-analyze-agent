import { ResearchCanvas } from "@/components/ResearchCanvas";
// import { useModelSelectorContext } from "@/lib/model-selector-provider"; // Removed context import
import { AgentState } from "@/lib/types";
import { useCoAgent } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import { useCopilotChatSuggestions } from "@copilotkit/react-ui";

// Define the agent ID consistent with the backend server.py
const AGENT_ID = "research_agent"; // Reverted to match server.py

export default function Main() {
  // const { model, agent } = useModelSelectorContext(); // Removed context usage
  const { state, setState } = useCoAgent<AgentState>({
    name: AGENT_ID, // Use the fixed agent ID
    // Updated initialState to match the new AgentState structure
    initialState: {
      // model: model, // Model selection might need to be handled differently now
      model: "openai", // Hardcode default model or manage differently
      // Removed duplicate model line below
      caseName: "",
      caseText: "",
      reportSections: { basic_info: "", summary: "", case_brief: {}, cold_call_qa: [] },
      report: "",
      sourcesConsulted: [],
      logs: [],
      needsManualInput: false,
    },
  });

  // TODO: Update or remove chat suggestions if needed
  useCopilotChatSuggestions({
    instructions: "Ask about the case facts", // Example suggestion
  });

  return (
    <>
      <h1 className="flex h-[60px] bg-[#0E103D] text-white items-center px-10 text-2xl font-medium">
        Research Helper
      </h1>

      <div
        className="flex flex-1 border"
        style={{ height: "calc(100vh - 60px)" }}
      >
        <div className="flex-1 overflow-hidden">
          <ResearchCanvas />
        </div>
        <div
          className="w-[500px] h-full flex-shrink-0"
          style={
            {
              "--copilot-kit-background-color": "#E0E9FD",
              "--copilot-kit-secondary-color": "#6766FC",
              "--copilot-kit-separator-color": "#b8b8b8",
              "--copilot-kit-primary-color": "#FFFFFF",
              "--copilot-kit-contrast-color": "#000000",
              "--copilot-kit-secondary-contrast-color": "#000",
            } as any
          }
        >
          <CopilotChat
            className="h-full"
            // TODO: Review onSubmitMessage logic. Clearing logs might be okay,
            // but consider if other state resets are needed when starting a new case analysis.
            onSubmitMessage={async (message) => {
              // For now, just pass the message. Agent handles context.
              // If starting a new case analysis via chat is desired, more logic is needed here.
              console.log("Chat submitted:", message);
              // Original log clearing logic:
              // setState({ ...state, logs: [] });
              // await new Promise((resolve) => setTimeout(resolve, 30));
            }}
            labels={{
              initial: "Enter a case name above to start analysis, or ask questions about the current report.",
            }}
          />
        </div>
      </div>
    </>
  );
}
