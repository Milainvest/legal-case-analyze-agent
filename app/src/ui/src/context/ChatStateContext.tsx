"use client";

import { createContext, useContext, useReducer } from "react";
import { ChatMessage } from "@/lib/types";

interface ChatState {
  messages: ChatMessage[];
  currentReportContext: string | null;
  isLoading: boolean;
  error: string | null;
}

type ChatAction =
  | { type: "ADD_MESSAGE"; message: ChatMessage }
  | { type: "UPDATE_MESSAGE"; messageId: string; content: string }
  | { type: "DELETE_MESSAGE"; messageId: string }
  | { type: "CLEAR_MESSAGES" }
  | { type: "SET_REPORT_CONTEXT"; reportId: string }
  | { type: "SET_LOADING"; isLoading: boolean }
  | { type: "SET_ERROR"; error: string | null };

const initialState: ChatState = {
  messages: [],
  currentReportContext: null,
  isLoading: false,
  error: null,
};

const ChatStateContext = createContext<{
  state: ChatState;
  dispatch: React.Dispatch<ChatAction>;
}>({
  state: initialState,
  dispatch: () => null,
});

function chatReducer(state: ChatState, action: ChatAction): ChatState {
  switch (action.type) {
    case "ADD_MESSAGE":
      return { ...state, messages: [...state.messages, action.message] };
    case "UPDATE_MESSAGE":
      return {
        ...state,
        messages: state.messages.map((msg) =>
          msg.id === action.messageId ? { ...msg, content: action.content } : msg
        ),
      };
    case "DELETE_MESSAGE":
      return {
        ...state,
        messages: state.messages.filter((msg) => msg.id !== action.messageId),
      };
    case "CLEAR_MESSAGES":
      return { ...state, messages: [] };
    case "SET_REPORT_CONTEXT":
      return { ...state, currentReportContext: action.reportId };
    case "SET_LOADING":
      return { ...state, isLoading: action.isLoading };
    case "SET_ERROR":
      return { ...state, error: action.error };
    default:
      return state;
  }
}

export function ChatStateProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  return (
    <ChatStateContext.Provider value={{ state, dispatch }}>
      {children}
    </ChatStateContext.Provider>
  );
}

export function useChatState() {
  const context = useContext(ChatStateContext);

  if (!context) {
    throw new Error("useChatState must be used within a ChatStateProvider");
  }

  const { state, dispatch } = context;

  const sendMessage = async (message: string) => {
    try {
      dispatch({ type: "SET_LOADING", isLoading: true });
      dispatch({ type: "SET_ERROR", error: null });

      // Add user message first
      dispatch({
        type: "ADD_MESSAGE",
        message: {
          id: Date.now().toString(),
          content: message,
          role: "user",
          timestamp: Date.now(),
        },
      });

      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message,
          reportContext: state.currentReportContext,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to send message");
      }

      const data = await response.json();

      // Add AI response
      dispatch({
        type: "ADD_MESSAGE",
        message: {
          id: (Date.now() + 1).toString(),
          content: data.message,
          role: "assistant",
          timestamp: Date.now(),
        },
      });
    } catch (error) {
      dispatch({
        type: "SET_ERROR",
        error: `Failed to send message: ${error instanceof Error ? error.message : "Unknown error"}`,
      });
    } finally {
      dispatch({ type: "SET_LOADING", isLoading: false });
    }
  };

  return {
    state,
    dispatch,
    sendMessage,
  };
}
