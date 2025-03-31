import { ResearchCanvas } from "@/components/ResearchCanvas";
import { useCoAgent } from "@copilotkit/react-core"; // Only useCoAgent
import { Role, TextMessage } from "@copilotkit/runtime-client-gql";
import { CopilotChat } from "@copilotkit/react-ui";
import { useCopilotChatSuggestions } from "@copilotkit/react-ui";
import { useEffect } from "react";
import { ResearchStateProvider } from "@/lib/research-state-provider";
import { AgentState, Message } from "@/lib/types"; // Import AgentState and Message types

// Define the agent ID consistent with the backend server.py
const AGENT_ID = "research_agent";

export default function Main() {
  // Use useCoAgent for both state management and chat interactions
  const coAgent = useCoAgent<AgentState>({
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
      messages: [], // Ensure messages are part of the AgentState
      connectionStatus: 'disconnected',
      error: null,
    },
  });

  // Determine if a report exists based on the coAgent state for UI logic
  const hasReportCoAgent = Boolean(coAgent.state.report?.trim());

  // Suggestions based on report status from coAgent state
  useCopilotChatSuggestions({
    instructions: hasReportCoAgent
      ? "The case report is displayed. Ask questions or give further instructions." // General instruction after report
      : "Enter a case name to analyze",
    // disabled: hasReportCoAgent, // 'disabled' prop is not valid
  });

   // Debug log for coAgent state
   useEffect(() => {
    console.log("\n=== useCoAgent State Update (Main.tsx) ===");
    console.log("State:", {
        reportLength: coAgent.state.report?.length || 0,
        logsCount: coAgent.state.logs?.length || 0,
        needsInput: coAgent.state.needsManualInput,
        error: coAgent.state.error,
        connection: coAgent.state.connectionStatus,
        messagesCount: coAgent.state.messages?.length || 0, // Log message count
    });
    console.log("Is Running:", coAgent.running);
    console.log("=== End useCoAgent State Update ===\n");
  }, [coAgent.state, coAgent.running]);

  return (
    // Pass coAgent state/functions to the provider for ResearchCanvas
    <ResearchStateProvider
      initialState={coAgent.state}
      setState={coAgent.setState}
      run={coAgent.run}
    >
      <h1 className="flex h-[60px] bg-[#0E103D] text-white items-center px-10 text-2xl font-medium">
        Research Helper
      </h1>

      <div
        className="flex flex-1 border"
        style={{ height: "calc(100vh - 60px)" }}
      >
        <div className="flex-1 overflow-hidden">
          {/* ResearchCanvas gets state via useResearchState from the provider */}
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
          {/* Pass state and functions from useCoAgent to CopilotChat */}
          <CopilotChat
            className="h-full"
            // Let CopilotChat manage its internal message display based on the context
            onSubmitMessage={async (messageContent: string) => { // Use onSubmitMessage
              console.log("Chat submitted via CopilotChat, updating coAgent state and running agent");
              const newUserMessage: Message = { role: 'user', content: messageContent };
              // Update coAgent state with the new user message
              coAgent.setState(prevState => {
                const currentMessages = prevState?.messages || [];
                // Define a default state structure if prevState is undefined
                const defaultState: AgentState = {
                  model: "openai", caseName: "", caseText: "", reportSections: { basic_info: "", summary: "", case_brief: {}, cold_call_qa: [] }, report: "", sourcesConsulted: [], logs: [], needsManualInput: false, messages: [], connectionStatus: 'disconnected', error: null
                };
                return {
                  ...(prevState || defaultState), // Use defaultState if prevState is undefined
                  messages: [...currentMessages, newUserMessage], // Add the new Message object
                };
              });
              // Trigger agent run to process the new message
              await coAgent.run(); // Call run to send the message to the backend
            }}
            // isLoading prop is not accepted by CopilotChat
            // isLoading={coAgent.running}
            labels={{
              initial: hasReportCoAgent
                ? "Ask questions about the case analysis above"
                : "Enter a case name above to start analysis.",
            }}
          />
        </div>
      </div>
    </ResearchStateProvider>
  );
}
