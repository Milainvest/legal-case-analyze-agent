"use client";

import { useState, useEffect } from "react";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button"; // Added for manual input submit
import {
  useCoAgent,
  useCoAgentStateRender,
  useCopilotContext,
} from "@copilotkit/react-core";
import { Progress } from "./Progress";
// import { EditResourceDialog } from "./EditResourceDialog"; // Removed
// import { AddResourceDialog } from "./AddResourceDialog"; // Removed
import { Resources } from "./Resources";
import { AgentState, Source } from "@/lib/types"; // Updated type import
import { useModelSelectorContext } from "@/lib/model-selector-provider";
import { useResearchState } from "@/lib/research-state-provider";

export function ResearchCanvas() {
  const { model, agent } = useModelSelectorContext();
  const { state, setState, run } = useResearchState();

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

        setState((prev) => ({
          ...prev!,
          connectionStatus
        }));

        console.log("WebSocket state:", {
          readyState,
          connectionStatus,
          bufferedAmount: ws.bufferedAmount,
          url: ws.url
        });
      } else {
        console.log("WebSocket not initialized");
        setState((prev) => ({
          ...prev!,
          connectionStatus: 'disconnected' as const
        }));
      }
    };

    // 定期的に接続状態を確認
    const interval = setInterval(checkWebSocket, 5000);
    checkWebSocket(); // 初回チェック

    return () => clearInterval(interval);
  }, []);

  // 状態更新の監視を強化
  useEffect(() => {
    if (state.report) {
      console.log("Report update detected:", {
        length: state.report.length,
        preview: state.report.slice(0, 100),
        timestamp: new Date().toISOString(),
        connectionStatus: state.connectionStatus
      });
    }
  }, [state.report]);

  // デバッグ用のログを追加
  useEffect(() => {
    console.log("\n=== ResearchCanvas State Update ===");
    console.log("State:", {
      hasReport: Boolean(state.report),
      reportLength: state.report?.length || 0,
      stateKeys: Object.keys(state),
      connectionStatus: state.connectionStatus,
      error: state.error
    });
  }, [state]);

  // 状態変更のデバッグ
  useEffect(() => {
    console.log("State change detected:", {
      hasReport: Boolean(state.report),
      reportLength: state.report?.length || 0,
      stateKeys: Object.keys(state),
      timestamp: new Date().toISOString()
    });
  }, [state]);

  // 状態の更新を監視し、必要に応じてUIを更新
  useEffect(() => {
    if (state.report) {
      console.log("Report content updated:", state.report.slice(0, 100));
    }
  }, [state.report]);

  // WebSocket接続状態の監視
  useEffect(() => {
    let reconnectAttempts = 0;
    const maxReconnectAttempts = 3;

    const checkConnection = () => {
      if (!state || reconnectAttempts >= maxReconnectAttempts) {
        console.error("Connection failed after", reconnectAttempts, "attempts");
        setState((prev) => ({
          ...prev!,
          error: "Connection failed. Please try again.",
          logs: [...(prev?.logs || []), { message: "Connection failed. Please try again.", done: true }]
        }));
        return;
      }

      reconnectAttempts++;
      console.log("Checking connection, attempt:", reconnectAttempts);
      
      // 接続状態の確認
      run().catch(error => {
        console.error("Connection check failed:", error);
        setTimeout(checkConnection, 2000); // 2秒後に再試行
      });
    };

    // 初期接続チェック
    checkConnection();

    return () => {
      reconnectAttempts = maxReconnectAttempts; // クリーンアップ時に再接続を停止
    };
  }, []);

  useCoAgentStateRender({
    name: agent,
    render: ({ state: renderState }) => {
      if (!renderState.logs || renderState.logs.length === 0) {
        return null;
      }
      return <Progress logs={renderState.logs} />;
    },
  });

  // State for manual input
  const [manualCaseText, setManualCaseText] = useState("");

  const handleManualSubmit = async () => {
    if (manualCaseText.trim()) {
      setState({
        ...state,
        caseText: manualCaseText,
        needsManualInput: false,
        logs: [...(state.logs || []), { message: "Manual case text provided.", done: true }],
      });
      setManualCaseText("");
      await run();
    }
  };

  const sources: Source[] = state.sourcesConsulted || [];
  // Removed setResources, addResource, removeResource, editResource logic

  const handleAnalyzeCase = async () => {
    console.log("Starting case analysis...");
    try {
      setState(prev => ({
        ...prev,
        error: null,
        connectionStatus: 'connecting' as const,
        logs: [...(prev.logs || []), { message: "Starting analysis...", done: false }]
      }));

      await run();
      
      console.log("Analysis completed, checking report state:", {
        hasReport: Boolean(state.report),
        reportLength: state.report?.length || 0,
        connectionStatus: state.connectionStatus
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      console.error("Error during analysis:", error);
      setState(prev => ({
        ...prev,
        error: errorMessage,
        connectionStatus: 'error' as const,
        logs: [...(prev.logs || []), { message: `Error: ${errorMessage}`, done: true, error: true }]
      }));
    }
  };

  // エラー状態のリセット関数
  const resetError = () => {
    setState(prev => ({
      ...prev,
      error: null
    }));
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
              setState({
                ...state,
                caseName: e.target.value,
                caseText: "",
                reportSections: { basic_info: "", summary: "", case_brief: {}, cold_call_qa: [] },
                report: "",
                sourcesConsulted: [],
                logs: [],
                needsManualInput: false
              })
            }
            aria-label="Case name"
            className="bg-background px-6 py-8 border-0 shadow-none rounded-xl text-md font-extralight focus-visible:ring-0 placeholder:text-slate-400"
          />
          <Button 
            onClick={handleAnalyzeCase}
            disabled={!state.caseName?.trim()} 
            className="mt-2"
          >
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

        {/* Display Generated Report with enhanced error handling */}
        <div className="flex flex-col h-full">
          <h2 className="text-lg font-medium mb-3 text-primary">
            Generated Case Report
          </h2>
          
          {/* エラー表示 */}
          {state.error && (
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

          {/* デバッグ情報 */}
          {process.env.NODE_ENV === 'development' && (
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
          )}

          <Textarea
            key={`report-${state.report ? 'present' : 'empty'}-${Date.now()}`}
            data-test-id="case-report"
            placeholder={state.error ? "An error occurred. Please try again." : "The generated case report will appear here..."}
            value={state.report || ""}
            readOnly
            rows={15}
            aria-label="Generated case report"
            className={`bg-background px-6 py-8 border-0 shadow-none rounded-xl text-md font-extralight focus-visible:ring-0 placeholder:text-slate-400 ${
              state.error ? 'border-red-200' : ''
            }`}
            style={{ minHeight: "300px" }}
          />
        </div>
      </div>
    </div>
  );
}
