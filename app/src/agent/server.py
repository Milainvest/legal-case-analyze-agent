"""
Basic FastAPI server to expose the LangGraph agent.
Integrates with CopilotKit runtime.
"""
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
# Removed sys and Path imports, and sys.path.append logic

# Import the LangGraph agent instance
from legal_case_analyze_agent.langgraph.agent import graph as langgraph_agent

# Import CopilotKit specific components
# This relies on the 'copilotkit' package being installed via Poetry
try:
    from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent # Import necessary classes
    from copilotkit.integrations.fastapi import add_fastapi_endpoint # Import FastAPI integration
except ImportError as e:
    # If this fails, check installation and package structure
    raise ImportError(f"Could not import CopilotKit components. Ensure the 'copilotkit' package is installed correctly (`poetry install`) and the virtual environment is active. Original error: {e}")

# Load environment variables (especially OPENAI_API_KEY)
load_dotenv()

# Ensure OPENAI_API_KEY is set for agent initialization if needed within LangGraph nodes
if not os.getenv("OPENAI_API_KEY"):
    print("Warning: OPENAI_API_KEY environment variable not set. LLM calls may fail.")

# --- FastAPI App Setup ---
app = FastAPI(
    title="Legal Case Analysis Agent API",
    description="API endpoint for the LangGraph-based legal analysis agent using CopilotKit.",
    version="0.1.0"
)

# --- CORS Middleware ---
# Allow requests from the frontend development server
origins = [
    "http://localhost:3000", # Default Next.js dev port
    # Add other origins if needed (e.g., deployed frontend URL)
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CopilotKit Remote Endpoint Setup ---
# Define the agent ID - MUST match the 'name' used in useCoAgent on the frontend
AGENT_ID = "research_agent"

sdk = CopilotKitRemoteEndpoint(
    agents=[
        LangGraphAgent(
            name=AGENT_ID,
            description="Agent for analyzing legal cases.", # Add a description
            graph=langgraph_agent, # Pass the compiled LangGraph instance
        ),
        # Add other agents here if needed
    ]
)

# Add the CopilotKit FastAPI endpoint - mounts routes like /copilotkit/v1/agents etc.
# The '/copilotkit' path prefix should generally match what the frontend expects.
add_fastapi_endpoint(app, sdk, "/copilotkit")
print(f"CopilotKit endpoint mounted at /copilotkit, serving agent: {AGENT_ID}")


# --- Basic Root Endpoint ---
@app.get("/")
async def root():
    return {"message": f"Legal Case Analysis Agent API ({AGENT_ID}) is running."}

# --- Run Server (for local development) ---
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000)) # Default to port 8000
    print(f"Starting FastAPI server on port {port}...")
    # Use reload=True for development to automatically pick up code changes
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
