import os
from dotenv import load_dotenv
from google.adk import Agent

# Load environment variables from .env
load_dotenv()

model_name = os.getenv("MODEL")

# ── Define the summarizer tool ────────────────────────────────────────────

def summarize_text(text: str) -> dict[str, str]:
    """Accepts a block of text and returns a concise summary."""
    # The agent's LLM will handle the actual summarization.
    # This function passes the text to the model via the agent instruction.
    return {"input_text": text}

# ── Define the root agent ─────────────────────────────────────────────────

root_agent = Agent(
    name="summarizer",
    model=model_name,
    description="An AI agent that summarizes any text provided by the user.",
    instruction="""
    You are a professional text summarization assistant.
    When the user provides a block of text, produce a concise summary that:
    - Captures the key points in 3-5 sentences
    - Uses clear, simple language
    - Preserves the most important facts and conclusions

    Only return the summary — do not include any preamble or explanation.
    """,
    tools=[summarize_text]
)
