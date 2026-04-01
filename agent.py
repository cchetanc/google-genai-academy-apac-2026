import os
import logging
import google.cloud.logging
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# --- Setup Logging and Environment ---
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()
model_name = os.getenv("MODEL")

# TOOL 1: Save student's prompt to shared state
def add_prompt_to_state(
    tool_context: ToolContext, prompt: str
) -> dict[str, str]:
    """Saves the student's placement query to shared state."""
    tool_context.state["PROMPT"] = prompt
    logging.info(f"[State updated] Student prompt: {prompt}")
    return {"status": "success"}

# TOOL 2: Mock Company Database
def get_company_info(
    tool_context: ToolContext, company_name: str
) -> dict:
    """Returns placement info for a given company from internal DB."""
    company_db = {
        "google": {
            "rounds": ["Online Coding Test", "Technical Interview x2", "Googleyness Interview"],
            "ctc": "30-45 LPA",
            "skills": ["DSA", "System Design", "Python/Java", "Problem Solving"],
            "tip": "Focus on LeetCode Medium/Hard. Practice STAR method for behavioural rounds."
        },
        "microsoft": {
            "rounds": ["Coding Assessment", "Technical Interview x3", "HR Round"],
            "ctc": "20-40 LPA",
            "skills": ["DSA", "OOP", "System Design", "Azure basics"],
            "tip": "Strong emphasis on OOP concepts. Be ready to code on a whiteboard."
        },
        "amazon": {
            "rounds": ["OA (2 coding + work simulation)", "Technical x2", "Bar Raiser"],
            "ctc": "18-35 LPA",
            "skills": ["DSA", "Leadership Principles", "System Design"],
            "tip": "Know all 16 Leadership Principles by heart. Every answer should use STAR format."
        },
        "tcs": {
            "rounds": ["TCS NQT", "Technical Interview", "HR Interview"],
            "ctc": "3.5-7 LPA",
            "skills": ["Programming basics", "Aptitude", "Communication"],
            "tip": "Clear TCS NQT with a good score. Focus on verbal and quantitative sections."
        },
        "infosys": {
            "rounds": ["InfyTQ / Hackwithinfy", "Technical Interview", "HR"],
            "ctc": "3.6-9 LPA",
            "skills": ["Python", "Logical reasoning", "Database basics"],
            "tip": "InfyTQ certification gives an edge. Practice SQL and Python fundamentals."
        }
    }
    key = company_name.lower().strip()
    if key in company_db:
        info = company_db[key]
        logging.info(f"[company_db] Found info for: {company_name}")
        return {"company": company_name, "found": True, **info}
    else:
        return {
            "company": company_name,
            "found": False,
            "message": f"No internal data for {company_name}. Using general advice."
        }

# Wikipedia Tool 
wikipedia_tool = LangchainTool(
    tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
)

# AGENT 1: Resume & Company Analyst 
resume_analyst = Agent(
    name="resume_analyst",
    model=model_name,
    description="Researches the target company and provides resume + preparation tips.",
    instruction="""
    You are an expert campus placement advisor.
    The student's query is in: { PROMPT }

    Your tasks:
    1. Use the 'get_company_info' tool with the company name from the prompt.
    2. Use 'wikipedia_tool' to find general info about the company
       (industry, products, founding, culture).
    3. Based on both sources, provide:
       - Key skills the student should highlight on their resume
       - Interview rounds breakdown
       - One actionable preparation tip

    Be specific and concise. Output the data as structured text.
    """,
    tools=[get_company_info, wikipedia_tool],
    output_key="company_research"
)

# AGENT 2: Interview Coach
interview_coach = Agent(
    name="interview_coach",
    model=model_name,
    description="Generates practice interview questions tailored to the target company.",
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

# AGENT 3: Response Formatter 
response_formatter = Agent(
    name="response_formatter",
    model=model_name,
    description="Presents all placement guidance in a clear, motivating format.",
    instruction="""
    You are a friendly placement cell coordinator.
    Combine the research and interview questions into one helpful response.

    Structure your response as:
    1. Company Snapshot
    2. Resume Tips (skills to highlight)
    3. Interview Process
    4. Top 5 Practice Questions with Hints
    5. One motivational closing tip

    Data:
    Company Research: { company_research }
    Interview Questions: { interview_questions }

    Be warm, clear, and encouraging.
    """
)

# WORKFLOW 
placement_workflow = SequentialAgent(
    name="placement_workflow",
    description="Runs the full placement preparation pipeline for a student.",
    sub_agents=[
        resume_analyst,       # Step 1: Research company
        interview_coach,      # Step 2: Generate questions
        response_formatter,   # Step 3: Format final guidance
    ]
)

# ROOT AGENT
root_agent = Agent(
    name="placement_greeter",
    model=model_name,
    description="Entry point for the Campus Placement Assistant.",
    instruction="""
    Greet the student warmly and introduce yourself as their
    AI-powered Campus Placement Assistant.
    Ask them: Which company are they preparing for?
    Once they respond, use 'add_prompt_to_state' to save their answer,
    then hand off to the placement_workflow agent.
    """,
    tools=[add_prompt_to_state],
    sub_agents=[placement_workflow]
)
# End of File
##############
