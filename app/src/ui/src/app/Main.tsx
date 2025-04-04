import { ResearchCanvas } from "@/components/ResearchCanvas";
// import { useModelSelectorContext } from "@/lib/model-selector-provider"; // Removed context import
import { AgentState } from "@/lib/types";
import { useCoAgent } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import { useCopilotChatSuggestions } from "@copilotkit/react-ui";
import { useEffect } from "react";

// Define the agent ID consistent with the backend server.py
const AGENT_ID = "research_agent"; // Reverted to match server.py

export default function Main() {
  // const { model, agent } = useModelSelectorContext(); // Removed context usage
  const { state, setState, run } = useCoAgent<AgentState>({
    name: AGENT_ID,
    initialState: {
      model: "openai",
      caseName: "",
      caseText: "",
      reportSections: { basic_info: "", summary: "", case_brief: {}, cold_call_qa: [] },
      report: "",
      sourcesConsulted: [],
      logs: [],
      needsManualInput: false,
    },
  });

  // デバッグ用のログを追加
  useEffect(() => {
    console.log("\n=== Main Component State Update ===");
    console.log("State:", state);
    console.log("=== End Main Component State Update ===\n");
  }, [state]);

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
            onSubmitMessage={async (message) => {
              console.log("Chat submitted:", message);
              await run();
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
