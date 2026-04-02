"""
agent.py — Campus Placement Assistant v2
Upgraded for Track 2: Multi-agent + MCP + Firestore + Multi-step workflow + API deployment

Requirements met:
  ✅ Primary agent coordinating sub-agents (SequentialAgent pattern)
  ✅ Structured data stored/retrieved from Firestore via MCP
  ✅ MCP tool integration (placement_mcp_server.py)
  ✅ Multi-step workflow (greet → research → coach → format)
  ✅ API-based deployment (Cloud Run)
"""
import os
import sys
import logging
import google.cloud.logging
from dotenv import load_dotenv

from google.adk.agents import Agent, SequentialAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams
from mcp import StdioServerParameters

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# ── Setup ────────────────────────────────────────────────────────────────────
try:
    cloud_logging_client = google.cloud.logging.Client()
    cloud_logging_client.setup_logging()
except Exception:
    logging.basicConfig(level=logging.INFO)

load_dotenv()
model_name = os.getenv("MODEL", "gemini-2.5-flash")

MCP_SERVER_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "placement_mcp_server.py")
)

# ── MCP Toolset (connects to placement_mcp_server.py via stdio) ───────────────
placement_mcp_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable,
            args=[MCP_SERVER_PATH],
        )
    )
)

# ── Wikipedia Tool ────────────────────────────────────────────────────────────
wikipedia_tool = LangchainTool(
    tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
)

# ── State Tool ────────────────────────────────────────────────────────────────
def add_prompt_to_state(tool_context: ToolContext, prompt: str) -> dict:
    """Save the student's placement query to shared agent state."""
    tool_context.state["PROMPT"] = prompt
    logging.info(f"[State] Student prompt saved: {prompt}")
    return {"status": "success"}

# ── AGENT 1: Resume & Company Analyst ────────────────────────────────────────
resume_analyst = Agent(
    name="resume_analyst",
    model=model_name,
    description="Researches the target company using MCP database and Wikipedia, provides resume tips.",
    instruction="""
        You are an expert campus placement advisor.
        The student's query is in: { PROMPT }

        Your tasks:
        1. Use the 'get_company_info' MCP tool with the company name from the prompt.
           This retrieves structured data from the Firestore database.
        2. Use 'wikipedia_tool' to find general info about the company
           (industry, products, founding, culture).
        3. Based on both sources, provide:
           - Key skills the student should highlight on their resume
           - Interview rounds breakdown with CTC range
           - One actionable preparation tip

        Be specific and concise. Output as structured text.
    """,
    tools=[placement_mcp_toolset, wikipedia_tool],
    output_key="company_research"
)

# ── AGENT 2: Interview Coach ──────────────────────────────────────────────────
interview_coach = Agent(
    name="interview_coach",
    model=model_name,
    description="Generates 5 targeted practice interview questions for the company.",
    instruction="""
        You are a senior technical interviewer.
        Use the COMPANY_RESEARCH below to generate 5 targeted practice questions
        (mix of technical + HR) a student should prepare for this company.
        For each question, provide a 1-2 sentence model answer hint.

        COMPANY_RESEARCH:
        { company_research }
    """,
    output_key="interview_questions"
)

# ── AGENT 3: Session Saver ────────────────────────────────────────────────────
session_saver = Agent(
    name="session_saver",
    model=model_name,
    description="Saves the student's session to the Firestore database via MCP.",
    instruction="""
        You are responsible for persisting the student's session to the database.

        Use the 'save_student_session' MCP tool to save this session with:
        - student_id: generate a simple id like "student_001"
        - company: extract the company name from { PROMPT }
        - notes: summarize key tips from { company_research }

        This ensures the session is stored in Firestore for future reference.
        After saving, confirm with a brief message.
    """,
    tools=[placement_mcp_toolset],
    output_key="session_saved"
)

# ── AGENT 4: Response Formatter ───────────────────────────────────────────────
response_formatter = Agent(
    name="response_formatter",
    model=model_name,
    description="Combines all research and questions into a clean, encouraging final response.",
    instruction="""
        You are a friendly placement cell coordinator.
        Combine the research and interview questions into one comprehensive response.

        Structure your response as:
        1. 🏢 Company Snapshot (domain, CTC, overview)
        2. 📄 Resume Tips (top skills to highlight)
        3. 🔁 Interview Process (rounds breakdown)
        4. 🎯 Top 5 Practice Questions with Model Answer Hints
        5. 💾 Session Saved confirmation
        6. 🚀 One motivational closing tip

        Data:
        Company Research: { company_research }
        Interview Questions: { interview_questions }
        Session Status: { session_saved }

        Be warm, clear, and encouraging.
    """
)

# ── SEQUENTIAL WORKFLOW ───────────────────────────────────────────────────────
placement_workflow = SequentialAgent(
    name="placement_workflow",
    description="Full placement preparation pipeline: research → coach → save → format.",
    sub_agents=[
        resume_analyst,    # Step 1: Fetch from MCP/Firestore + Wikipedia
        interview_coach,   # Step 2: Generate Q&As
        session_saver,     # Step 3: Persist to Firestore via MCP
        response_formatter # Step 4: Format final response
    ]
)

# ── ROOT AGENT ────────────────────────────────────────────────────────────────
root_agent = Agent(
    name="placement_greeter",
    model=model_name,
    description="Entry point for the Campus Placement Assistant.",
    instruction="""
        Greet the student warmly and introduce yourself as their
        AI-powered Campus Placement Assistant (powered by Google ADK + MCP + Firestore).

        Ask them: Which company are you preparing for?
        Once they respond, use 'add_prompt_to_state' to save their answer,
        then hand off to the placement_workflow agent.
    """,
    tools=[add_prompt_to_state],
    sub_agents=[placement_workflow]
)
