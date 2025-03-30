"use client";

import { useState, useEffect } from "react";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button"; // Added for manual input submit
import {
  useCoAgent,
  useCoAgentStateRender,
  useCopilotContext,
  useCopilotAction
} from "@copilotkit/react-core";
import { Progress } from "./Progress";
// import { EditResourceDialog } from "./EditResourceDialog"; // Removed
// import { AddResourceDialog } from "./AddResourceDialog"; // Removed
import { Resources } from "./Resources";
import { AgentState, Source } from "@/lib/types"; // Updated type import
import { useModelSelectorContext } from "@/lib/model-selector-provider";
import { useResearchState } from "@/lib/research-state-provider";

// Define initialAgentState outside the component function
const initialAgentState: AgentState = {
  model: "openai",
  caseName: "",
  caseText: "",
  reportSections: { basic_info: "", summary: "", case_brief: {}, cold_call_qa: [] },
  report: "",
  sourcesConsulted: [],
  logs: [],
  needsManualInput: false,
  messages: [],
  connectionStatus: 'disconnected',
  error: null,
};

export function ResearchCanvas() {
  const { model, agent } = useModelSelectorContext();
  const { state, setState, run } = useResearchState();
  const copilot = useCopilotContext();

  // WebSocketの接続状態を監視
  useEffect(() => {
    const checkWebSocket = () => {
      // @ts-ignore - WebSocketの状態を確認
      const ws = window._copilotkit_ws;
      if (ws) {
        const readyState = ws.readyState;
        const connectionStatus =
          readyState === WebSocket.CONNECTING ? ('connecting' as const) :
          readyState === WebSocket.OPEN ? ('connected' as const) :
          readyState === WebSocket.CLOSING || readyState === WebSocket.CLOSED ? ('disconnected' as const) :
          ('error' as const);

        // Only update connectionStatus if prevState exists and status changed
        setState((prevState) => {
          const currentBaseState = prevState ?? initialAgentState;
          // Avoid unnecessary state updates if status hasn't changed
          if (currentBaseState.connectionStatus === connectionStatus) {
            return currentBaseState; // Return previous state to prevent re-render
          }
          // Ensure a valid AgentState object is always returned
          return {
            ...(currentBaseState as AgentState), // Type assertion might be needed if TS still complains
            connectionStatus
          };
        });

        // console.log("WebSocket state:", { // Reduce logging frequency if needed
        //   readyState,
        //   connectionStatus,
        //   bufferedAmount: ws.bufferedAmount,
        //   url: ws.url
        // });
      } else {
        // console.log("WebSocket not initialized");
        // Only update connectionStatus, preserve other state fields
        setState((prevState) => {
           // Ensure we have a valid previous state to spread, fallback to initialAgentState
          const currentBaseState = prevState ?? initialAgentState;
           // Avoid unnecessary state updates if status hasn't changed
           if (currentBaseState.connectionStatus === 'disconnected') {
             return currentBaseState;
           }
          // Ensure a valid AgentState object is always returned
          return {
            ...(currentBaseState as AgentState), // Type assertion might be needed
            connectionStatus: 'disconnected' as const
          };
        });
      }
    };

    // 定期的に接続状態を確認
    const interval = setInterval(checkWebSocket, 5000);
    checkWebSocket(); // 初回チェック

    return () => clearInterval(interval);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [setState]); // Only depend on setState

  // 状態更新の監視を強化 (Commented out for debugging)
  // useEffect(() => {
  //   if (state?.report) { // Add null check
  //     console.log("Report update detected:", {
  //       length: state.report.length,
  //       preview: state.report.slice(0, 100),
  //       timestamp: new Date().toISOString(),
  //       connectionStatus: state.connectionStatus
  //     });
  //   }
  // }, [state?.report, state?.connectionStatus]); // Add null checks to dependencies

  // デバッグ用のログを追加 (Commented out for debugging)
  // useEffect(() => {
  //   console.log("\n=== ResearchCanvas State Update ===");
  //   console.log("State:", {
  //     hasReport: Boolean(state?.report), // Add null check
  //     reportLength: state?.report?.length || 0, // Add null check
  //     stateKeys: state ? Object.keys(state) : [], // Add null check
  //     connectionStatus: state?.connectionStatus, // Add null check
  //     error: state?.error // Add null check
  //   });
  // }, [state]);

  // 状態変更のデバッグ (Commented out for debugging)
  // useEffect(() => {
  //   console.log("State change detected:", {
  //     hasReport: Boolean(state?.report), // Add null check
  //     reportLength: state?.report?.length || 0, // Add null check
  //     stateKeys: state ? Object.keys(state) : [], // Add null check
  //     timestamp: new Date().toISOString()
  //   });
  // }, [state]);

  // 状態の更新を監視し、必要に応じてUIを更新 (Commented out for debugging)
  // useEffect(() => {
  //   if (state?.report) { // Add null check
  //     console.log("Report content updated:", state.report.slice(0, 100));
  //   }
  // }, [state?.report]); // Add null check

  // WebSocket接続状態の監視 (Commented out for debugging - potential cause)
  // useEffect(() => {
  //   let reconnectAttempts = 0;
  //   const maxReconnectAttempts = 3;

  //   const checkConnection = () => {
  //     if (!state || reconnectAttempts >= maxReconnectAttempts) {
  //       console.error("Connection failed after", reconnectAttempts, "attempts");
  //       // Ensure prevState is handled correctly
  //       setState((prevState) => {
  //         const currentBaseState = prevState ?? initialAgentState;
  //         return {
  //           ...currentBaseState,
  //           error: "Connection failed. Please try again.",
  //           logs: [...(currentBaseState.logs || []), { message: "Connection failed. Please try again.", done: true }]
  //         };
  //       });
  //       return;
  //     }

  //     reconnectAttempts++;
  //     console.log("Checking connection, attempt:", reconnectAttempts);
      // 接続状態の確認 - run() はここでは呼び出さない
      // run().catch(error => {
      //   console.error("Connection check failed:", error);
      //   setTimeout(checkConnection, 2000); // 2秒後に再試行
      // });
      // 代わりにWebSocketの状態を直接確認する (checkWebSocket内で行われている)
  //     console.log("Initial connection check relies on WebSocket state.");
  //   };

    // 初期接続チェック
  //   checkConnection();

  //   return () => {
  //     reconnectAttempts = maxReconnectAttempts; // クリーンアップ時に再接続を停止
  //   };
  // }, []); // Removed state from dependency array if checkConnection doesn't need it directly

  useCoAgentStateRender({
    name: agent,
    render: ({ state: renderState }) => {
      // Ensure renderState and renderState.logs exist before accessing length
      if (!renderState?.logs || renderState.logs.length === 0) {
        return null;
      }
      return <Progress logs={renderState.logs} />;
    },
  });

  // State for manual input
  const [manualCaseText, setManualCaseText] = useState("");

  const handleManualSubmit = async () => {
    if (manualCaseText.trim()) {
      setState((prevState) => { // Use functional update
        const currentBaseState = prevState ?? initialAgentState;
        return {
          ...currentBaseState,
          caseText: manualCaseText,
          needsManualInput: false,
          logs: [...(currentBaseState.logs || []), { message: "Manual case text provided.", done: true }],
        };
      });
      setManualCaseText("");
      await run();
    }
  };

  const sources: Source[] = state?.sourcesConsulted || []; // Add null check for state
  // Removed setResources, addResource, removeResource, editResource logic

  useCopilotAction({
    name: "generateReport",
    description: "Generate a legal case analysis report",
    available: "remote",
    parameters: [
      {
        name: "caseName",
        type: "string",
        description: "The name of the case to analyze",
        required: true,
      },
      {
        name: "caseText",
        type: "string",
        description: "The text content of the case",
        required: true,
      }
    ],
    handler: async ({ caseName, caseText }) => {
      try {
        // Ensure prevState is handled correctly
        setState(prevState => {
          const currentBaseState = prevState ?? initialAgentState;
          return {
            ...currentBaseState,
            error: null,
            connectionStatus: 'connecting',
            logs: [...(currentBaseState.logs || []), { message: "Starting analysis...", done: false }]
          };
        });

        // This fetch call seems incorrect for triggering the backend agent.
        // We should use the `run` function provided by `useResearchState` (originally from `useCoAgent`).
        // The `run` function handles communication with the backend agent.
        // await run({ /* Pass necessary context if needed, e.g., caseName */ });

        // The following fetch logic might be for a different purpose or needs removal/refactoring
        // if it's intended to trigger the agent.

        // const response = await fetch('/api/copilotkit/agent', { // This endpoint might not exist or be correct
        //   method: 'POST',
        //   headers: {
        //     'Content-Type': 'application/json',
        //   },
        //   body: JSON.stringify({
        //     action: "generateReport", // Backend might not expect this structure
        //     parameters: {
        //       caseName,
        //       caseText
        //     }
        //   })
        // });

        // if (!response.ok) {
        //   throw new Error(`HTTP error! status: ${response.status}`);
        // }

        // const result = await response.json();

        // // State updates should happen based on backend emissions via useCoAgent, not directly here
        // setState(prevState => ({
        //   ...(prevState || initialAgentState),
        //   report: result.report,
        //   reportSections: result.sections,
        //   connectionStatus: 'connected',
        //   logs: [...(prevState?.logs || []), { message: "Analysis completed.", done: true }]
        // }));

        // return result; // The handler might not need to return anything if state is managed via backend emissions

        console.log("generateReport action handler called (currently does nothing, relies on backend)");
        return "Action triggered, backend processing..."; // Placeholder return

      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
        console.error("Error in generateReport action handler:", error);
        // Ensure prevState is handled correctly
        setState(prevState => {
          const currentBaseState = prevState ?? initialAgentState;
          return {
            ...currentBaseState,
            error: errorMessage,
            connectionStatus: 'error',
            logs: [...(currentBaseState.logs || []), { message: `Error: ${errorMessage}`, done: true, error: true }]
          };
        });
        throw error; // Re-throw error for potential higher-level handling
      }
    }
  });

  const handleAnalyzeCase = async () => {
    console.log("Starting case analysis via run()...");
    // Reset relevant parts of the state before starting a new analysis
    setState(prevState => {
      const currentBaseState = prevState ?? initialAgentState;
      return {
        ...currentBaseState,
        report: "", // Clear previous report
        reportSections: { basic_info: "", summary: "", case_brief: {}, cold_call_qa: [] },
        sourcesConsulted: [],
        logs: [{ message: `Analyzing case: ${currentBaseState.caseName || 'Unknown'}...`, done: false }], // Start with an initial log
        needsManualInput: false,
        error: null,
        // Keep messages? Decide based on desired behavior. Resetting might be cleaner.
        // messages: [],
      };
    });
    try {
       // Ensure the latest caseName is included in the state update for the run
       // The run function itself doesn't take arguments here; it uses the current state.
      await run();
    } catch (error) {
      console.error("Error in handleAnalyzeCase:", error);
       setState(prevState => {
         const currentBaseState = prevState ?? initialAgentState;
         return {
           ...currentBaseState,
           error: error instanceof Error ? error.message : "Analysis failed",
           logs: [...(currentBaseState.logs || []), { message: `Analysis failed: ${error}`, done: true, error: true }]
         };
       }); // Added missing parenthesis and semicolon
    }
  };

  // エラー状態のリセット関数
  const resetError = () => {
    // Ensure prevState is handled correctly
    setState(prevState => {
      const currentBaseState = prevState ?? initialAgentState;
      return {
        ...currentBaseState,
        error: null
      };
    });
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
            value={state?.caseName || ""} // Add null check
            onChange={(e) =>
              // Only update caseName, do not reset other state here
              setState((prevState) => { // Use functional update
                const currentBaseState = prevState ?? initialAgentState;
                return {
                  ...currentBaseState, // Use initial state as fallback
                  caseName: e.target.value,
                };
              })
            }
            aria-label="Case name"
            className="bg-background px-6 py-8 border-0 shadow-none rounded-xl text-md font-extralight focus-visible:ring-0 placeholder:text-slate-400"
          />
          <Button
            onClick={handleAnalyzeCase}
            disabled={!state?.caseName?.trim()} // Add null check
            className="mt-2"
          >
            Analyze Case
          </Button>
        </div>

        {/* Conditional Manual Input Section */}
        {state?.needsManualInput && ( // Add null check
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
          {sources.length === 0 && !state?.logs?.some(log => log.message.includes("Analyzing")) && ( // Add null check
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

        {/* Display Generated Report with enhanced error handling */}
        <div className="flex flex-col h-full">
          <h2 className="text-lg font-medium mb-3 text-primary">
            Generated Case Report
          </h2>

          {/* エラー表示 */}
          {state?.error && ( // Add null check
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-600 text-sm">
                Error: {state.error}
              </p>
              <Button
                onClick={resetError}
                className="mt-2 text-xs bg-red-100 hover:bg-red-200 text-red-600"
              >
                Dismiss
              </Button>
            </div>
          )}

          {/* デバッグ情報削除 */}
          {/* {process.env.NODE_ENV === 'development' && state && ( // Add null check
            <div className="mb-2 p-2 bg-gray-100 rounded text-xs">
              <p>Debug Info:</p>
              <p>Report State: {state.report ? 'Present' : 'Empty'}</p>
              <p>Report Length: {state.report?.length || 0}</p>
              <p>Report Type: {typeof state.report}</p>
              <p>Report Preview: {state.report?.slice(0, 100)}</p>
              <p>State Keys: {Object.keys(state).join(', ')}</p>
              <p>Error State: {state.error || 'None'}</p>
              <p>Connection Status: {state.connectionStatus || 'Unknown'}</p>
            </div>
          )} */}

          <Textarea
            key={`report-${state?.report ? 'present' : 'empty'}-${Date.now()}`} // Add null check
            data-test-id="case-report"
            placeholder={state?.error ? "An error occurred. Please try again." : "The generated case report will appear here..."} // Add null check
            value={state?.report || ""} // Add null check
            readOnly={true} // Add readOnly back
            rows={15}
            aria-label="Generated case report"
            className={`bg-background px-6 py-8 border-0 shadow-none rounded-xl text-md font-extralight focus-visible:ring-0 placeholder:text-slate-400 overflow-y-auto ${ // Add overflow-y-auto
              state?.error ? 'border-red-200' : '' // Add null check
            }`}
            style={{ minHeight: "300px" }}
          />
        </div>
      </div>
    </div>
  );
}
