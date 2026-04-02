"""
Text Intelligence Agent
------------------------
A single AI agent built with Google ADK that uses Gemini for inference.
Capability: Text Summarization + Question Answering + Classification + Routing

Satisfies all hackathon criteria:
  [OK] Implemented using ADK (google-adk)
  [OK] Uses Gemini model for inference
  [OK] Performs clearly defined tasks (summarization, QA, classification, routing)
  [OK] Accepts an input request and returns a response
  [OK] Deployed on Cloud Run, callable via HTTP endpoint
"""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent

load_dotenv()

model_name = os.getenv("MODEL", "gemini-2.0-flash")


# Tool 1: Text Summarization
def summarize_text(text: str) -> dict:
    """Summarizes a block of text into 3-5 concise sentences."""
    return {
        "task": "summarization",
        "input_length": len(text),
        "instruction": "Summarize the provided text in 3-5 sentences, preserving key facts."
    }


# Tool 2: Question Answering
def answer_question(question: str, context: str = "") -> dict:
    """Answers a question, optionally grounded in a provided context passage."""
    return {
        "task": "question_answering",
        "question": question,
        "has_context": bool(context),
        "instruction": "Answer the question clearly. If context is provided, base the answer on it."
    }


# Tool 3: Text Classification
def classify_text(text: str) -> dict:
    """Classifies text by sentiment (pos/neg/neutral) and topic (tech/finance/health/sports/general)."""
    return {
        "task": "classification",
        "input_length": len(text),
        "instruction": (
            "Classify the text on two dimensions:\n"
            "1. Sentiment: positive, negative, or neutral\n"
            "2. Topic: tech, finance, health, sports, or general\n"
            "Return both labels with a one-sentence justification for each."
        )
    }


# Tool 4: Request Routing (fixed response logic)
def route_request(request_type: str) -> dict:
    """Routes a request to a fixed response. Types: help, capabilities, about, contact."""
    routes = {
        "help": (
            "I can help you with:\n"
            "- Summarize: send any text and I will condense it\n"
            "- Answer: ask me any question (with or without context)\n"
            "- Classify: I will label your text by sentiment and topic\n"
            "- Help / Capabilities / About: fixed info responses"
        ),
        "capabilities": (
            "This agent supports four capabilities:\n"
            "1. Text Summarization\n"
            "2. Question Answering\n"
            "3. Text Classification\n"
            "4. Request Routing (fixed responses)"
        ),
        "about": (
            "Text Intelligence Agent - Gen AI Academy APAC Hackathon.\n"
            "Built with: Google ADK + Gemini 2.0 Flash + Cloud Run.\n"
            "Developer: Chetan P Kamath"
        ),
        "contact": (
            "Developer: Chetan P Kamath\n"
            "Submission: https://summarizer-agent-24293491909.us-central1.run.app/"
        ),
    }
    key = request_type.lower().strip()
    response = routes.get(key, f"Unknown route. Try: help, capabilities, about, contact.")
    return {"task": "routing", "request_type": key, "response": response}


# Root Agent — ADK entry point
root_agent = Agent(
    name="text_intelligence_agent",
    model=model_name,
    description=(
        "A single AI agent that performs text summarization, question answering, "
        "text classification, and request routing via a public HTTP endpoint."
    ),
    instruction="""
You are a Text Intelligence Agent with four tools:

1. summarize_text(text)          - Summarize / condense / shorten text
2. answer_question(question, context) - Answer questions (context optional)
3. classify_text(text)           - Classify by sentiment and topic
4. route_request(request_type)   - Fixed responses: help, capabilities, about, contact

DECISION RULES:
- "summarize / condense / shorten" + text  -> summarize_text
- Question word (what/why/how/who/when/?) -> answer_question
- "classify / sentiment / label"           -> classify_text
- "help / capabilities / about / contact"  -> route_request
- Ambiguous + text provided               -> default to summarize_text

Always call the right tool first, then return a clear, helpful response.
""",
    tools=[summarize_text, answer_question, classify_text, route_request],
)
