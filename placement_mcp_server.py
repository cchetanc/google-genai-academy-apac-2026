"""
placement_mcp_server.py
MCP stdio server that exposes company placement data from Firestore.
Falls back to built-in data if Firestore is unavailable.
"""
import asyncio
import json
import os
import logging

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

app = Server("placement-data-server")

# ── Built-in seed data (also written to Firestore on first run) ──────────────
COMPANY_DB = {
    "google": {
        "rounds": ["Online Coding Test", "Technical Interview x2", "Googleyness Interview"],
        "ctc": "30-45 LPA",
        "skills": ["DSA", "System Design", "Python/Java", "Problem Solving"],
        "tip": "Focus on LeetCode Medium/Hard. Practice STAR method for behavioural rounds.",
        "domain": "Technology / Cloud"
    },
    "microsoft": {
        "rounds": ["Coding Assessment", "Technical Interview x3", "HR Round"],
        "ctc": "20-40 LPA",
        "skills": ["DSA", "OOP", "System Design", "Azure basics"],
        "tip": "Strong emphasis on OOP concepts. Be ready to code on a whiteboard.",
        "domain": "Technology / Cloud"
    },
    "amazon": {
        "rounds": ["OA (2 coding + work simulation)", "Technical x2", "Bar Raiser"],
        "ctc": "18-35 LPA",
        "skills": ["DSA", "Leadership Principles", "System Design"],
        "tip": "Know all 16 Leadership Principles by heart. Every answer should use STAR format.",
        "domain": "E-Commerce / Cloud"
    },
    "tcs": {
        "rounds": ["TCS NQT", "Technical Interview", "HR Interview"],
        "ctc": "3.5-7 LPA",
        "skills": ["Programming basics", "Aptitude", "Communication"],
        "tip": "Clear TCS NQT with a good score. Focus on verbal and quantitative sections.",
        "domain": "IT Services"
    },
    "infosys": {
        "rounds": ["InfyTQ / Hackwithinfy", "Technical Interview", "HR"],
        "ctc": "3.6-9 LPA",
        "skills": ["Python", "Logical reasoning", "Database basics"],
        "tip": "InfyTQ certification gives an edge. Practice SQL and Python fundamentals.",
        "domain": "IT Services"
    },
    "wipro": {
        "rounds": ["NLTH Test", "Technical Interview", "HR Round"],
        "ctc": "3.5-6.5 LPA",
        "skills": ["Core CS", "Communication", "Aptitude"],
        "tip": "Score well in the NLTH test. Prepare OS, DBMS, and networking basics.",
        "domain": "IT Services"
    },
    "goldman sachs": {
        "rounds": ["HackerRank Test", "Technical x3", "HR + Culture Fit"],
        "ctc": "25-45 LPA",
        "skills": ["DSA", "C++/Java", "Probability", "Finance basics"],
        "tip": "Be strong in algorithms and probability. Know basic finance concepts.",
        "domain": "Finance / Technology"
    }
}


def get_firestore_client():
    """Return a Firestore client or None if unavailable."""
    try:
        from google.cloud import firestore
        return firestore.Client()
    except Exception as e:
        logging.warning(f"Firestore unavailable: {e}. Using built-in data.")
        return None


def seed_firestore(db):
    """Write seed data to Firestore if collection is empty."""
    try:
        col = db.collection("companies")
        existing = list(col.limit(1).stream())
        if not existing:
            for company, data in COMPANY_DB.items():
                col.document(company).set(data)
                logging.info(f"Seeded Firestore: {company}")
    except Exception as e:
        logging.warning(f"Could not seed Firestore: {e}")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_company_info",
            description=(
                "Retrieve placement data for a company from the database. "
                "Returns interview rounds, CTC range, required skills, and prep tips."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": "Company name e.g. Google, Amazon, TCS"
                    }
                },
                "required": ["company_name"]
            }
        ),
        types.Tool(
            name="list_companies",
            description="List all companies available in the placement database.",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="save_student_session",
            description=(
                "Save a student's session data (target company, skills, notes) to the database "
                "for future reference."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "student_id": {"type": "string", "description": "Unique student identifier"},
                    "company": {"type": "string", "description": "Target company"},
                    "notes": {"type": "string", "description": "Session notes or tips"},
                },
                "required": ["student_id", "company"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    db = get_firestore_client()
    if db:
        seed_firestore(db)

    if name == "get_company_info":
        company_name = arguments["company_name"].lower().strip()

        # Try Firestore first
        if db:
            try:
                doc = db.collection("companies").document(company_name).get()
                if doc.exists:
                    data = doc.to_dict()
                    data["company"] = arguments["company_name"]
                    data["found"] = True
                    data["source"] = "firestore"
                    return [types.TextContent(type="text", text=json.dumps(data))]
            except Exception as e:
                logging.warning(f"Firestore read failed: {e}")

        # Fallback to built-in data
        if company_name in COMPANY_DB:
            data = {**COMPANY_DB[company_name], "company": arguments["company_name"],
                    "found": True, "source": "built-in"}
            return [types.TextContent(type="text", text=json.dumps(data))]

        return [types.TextContent(type="text", text=json.dumps({
            "company": arguments["company_name"],
            "found": False,
            "message": f"No data found for {arguments['company_name']}. Using general guidance."
        }))]

    elif name == "list_companies":
        companies = list(COMPANY_DB.keys())
        if db:
            try:
                docs = db.collection("companies").stream()
                companies = [doc.id for doc in docs]
            except Exception:
                pass
        return [types.TextContent(type="text", text=json.dumps({"companies": companies}))]

    elif name == "save_student_session":
        record = {
            "student_id": arguments["student_id"],
            "company": arguments["company"],
            "notes": arguments.get("notes", ""),
            "timestamp": str(asyncio.get_event_loop().time())
        }
        if db:
            try:
                db.collection("student_sessions").document(
                    arguments["student_id"]
                ).set(record, merge=True)
                return [types.TextContent(type="text", text=json.dumps(
                    {"status": "saved", "record": record}))]
            except Exception as e:
                return [types.TextContent(type="text", text=json.dumps(
                    {"status": "error", "message": str(e)}))]
        return [types.TextContent(type="text", text=json.dumps(
            {"status": "saved_locally", "record": record}))]

    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream, write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
