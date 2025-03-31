import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Import the LangGraph agent instance
from legal_case_analyze_agent.langgraph.agent import graph as langgraph_agent

try:
    from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent
    from copilotkit.integrations.fastapi import add_fastapi_endpoint
except ImportError as e:
    raise ImportError(f"Could not import CopilotKit components. Ensure the 'copilotkit' package is installed correctly (`poetry install`) and the virtual environment is active. Original error: {e}")

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    print("Warning: OPENAI_API_KEY environment variable not set. LLM calls may fail.")

app = FastAPI(
    title="Legal Case Analysis Agent API",
    description="API endpoint for the LangGraph-based legal analysis agent using CopilotKit.",
    version="0.1.0"
)

origins = [
    "http://localhost:3000",  # Default Next.js dev port
    # Add other origins if needed
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the agent ID - MUST match the 'name' used in useCoAgent/useCopilotChat on the frontend
AGENT_ID = "research_agent"

# Create the CopilotKit endpoint with LangGraph integration
sdk = CopilotKitRemoteEndpoint(
    agents=[
        LangGraphAgent(
            name=AGENT_ID,
            description="Agent for analyzing legal cases.",
            graph=langgraph_agent,  # Pass the compiled graph with SQLite checkpointer
        ),
    ],
)

# Add CopilotKit endpoint
add_fastapi_endpoint(app, sdk, "/copilotkit/")
print(f"CopilotKit endpoint mounted at /copilotkit/, serving agent: {AGENT_ID}")

# Ensure FastAPI handles root path correctly
@app.get("/")
async def root():
    return {"message": f"Legal Case Analysis Agent API ({AGENT_ID}) is running."}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Starting FastAPI server on port {port}...")
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
