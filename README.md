# 🚀 GenAI Academy APAC 2026 – AI Agents Project

This repository contains two AI agent projects built as part of the **GenAI Academy APAC 2026 (Track 1: Build & Deploy AI Agents)** program. Both projects leverage **Google ADK (Agent Development Kit)**, **Gemini 2.5 Flash**, and **Google Cloud Run** for deployment.

---

## 📂 Project Structure

```
GenAI-Academy-Apac-2026
├── Project 1 - Summarizer agent/
│   ├── __init__.py
│   ├── agent.py
│   └── requirements.txt
├── Project 2 - Placement assistant/
│   ├── __init__.py
│   ├── agent.py
│   └── requirements.txt
└── README.md
```

---

# 🧠 Project 1: Summarizer Agent

## 📌 Overview

The **Summarizer Agent** has been upgraded into a **Text Intelligence Agent** that goes beyond basic summarization.

It is built using **Google ADK** and powered by **Gemini 2.0 Flash**, supporting multiple natural language processing capabilities within a single agent.

---

## ⚙️ Features

* 📝 Summarizes long text into concise insights
* ❓ Answers user questions (with or without context)
* 🏷️ Classifies text (sentiment + topic)
* 🔀 Handles fixed queries like help, about, and capabilities
* 🌐 Deployable as a Cloud Run HTTP endpoint

---

## 🏗️ Architecture

### 🔹 Root Agent

* `text_intelligence_agent`
* Handles all incoming requests
* Routes tasks intelligently to the correct tool

### 🔹 Tools (4 Total)

1. **summarize_text**

   * Generates concise summaries (3–5 sentences)

2. **answer_question**

   * Answers user queries clearly
   * Supports optional context-based answers

3. **classify_text**

   * Provides:

     * Sentiment → positive / negative / neutral
     * Topic → tech / finance / health / sports / general

4. **route_request**

   * Handles:

     * `help`, `capabilities`, `about`, `contact`

---

## 🧠 How It Works

* The agent receives input via API or UI
* Uses instruction-based reasoning to:

  * Identify user intent
  * Select the correct tool
* Gemini generates the final response

---

## 🔁 Decision Logic

* "summarize / condense" → summarization
* Question-based input → question answering
* "classify / sentiment" → classification
* "help / about / capabilities" → routing
* Default → summarization

---

## ☁️ Deployment

* **Framework**: Google ADK (`google-adk==1.14.0`)
* **Model**: Gemini 2.0 Flash *(updated)*
* **Platform**: Google Cloud Run

---

## 📦 Dependencies

```txt
google-adk==1.14.0
python-dotenv==1.0.1
```

---

## 🧪 Example Use Cases

**Summarization**

```
Summarize: AI is transforming industries...
```

**Question Answering**

```
What is machine learning?
```

**Classification**

```
Classify: The company reported record profits this quarter.
```

**Routing**

```
capabilities
```

---

## 🔄 Redeployment

```bash
source .env
uvx --from google-adk==1.14.0 adk deploy cloud_run ...
```

* Zero-downtime updates
* Same service URL retained

---

## 📁 Project Structure

🎓 Project 2: Campus Placement Assistant (v2 – Multi-Agent + MCP + Firestore)
📌 Overview

The Placement Assistant v2 is an upgraded multi-agent AI system designed to help students prepare for campus placements with real-time data, persistent storage, and tool integration.

It extends the v1 solution by introducing:

MCP-based tool integration
Firestore database for storage
Session tracking and persistence

This makes the system production-ready and fully aligned with advanced AI agent workflows.

💡 Key Idea

Provide a personalized, end-to-end placement preparation assistant that:

Understands user queries
Fetches company-specific data
Generates interview guidance
Stores user progress for future use
🏗️ Architecture (Multi-Agent Workflow)

The system uses a Sequential Multi-Agent pipeline with MCP integration:

Greeter (Primary Agent)
Captures user intent
Routes workflow
Resume Analyst
Fetches company data via MCP + Firestore
Performs additional research
Interview Coach
Generates interview questions & answers
Session Saver (NEW)
Saves session data using MCP → Firestore
Response Formatter
Produces structured final output
🔌 MCP Tools (NEW)

The system integrates external tools using MCP:

get_company_info → Fetch company data from Firestore
list_companies → Retrieve available companies
save_student_session → Store user session data
🗄️ Database Integration (NEW)

Uses Firestore (Native Mode) with two collections:

companies → Stores company placement data
student_sessions → Stores user interaction history

This enables persistent memory and real-time data retrieval.

⚙️ Features
Multi-agent AI system with orchestration
Company-specific interview preparation
AI-generated interview Q&A
MCP-based tool integration
Firestore-backed persistent storage
Session tracking and history
Multi-step workflow execution
Structured and personalized responses
Scalable API deployment
🧪 Example Queries
"I am preparing for Google"
"Help me prepare for Amazon"
"What about TCS NQT?"
"List all companies"
📊 Output Includes
Company insights (rounds, skills, tips)
Interview questions with guidance
Preparation strategy
Stored session for future reference
☁️ Deployment
Platform: Google Cloud Run
AI Model: Gemini 2.5 Flash (Vertex AI)
Framework: Google ADK
Database: Firestore
Protocol: MCP (Model Context Protocol)
🌍 Why This Project Matters
Solves real placement challenges for students
Demonstrates multi-agent + tool + database integration
Shows production-ready AI system design
Highly scalable and extensible for ed-tech platforms
🚀 Key Improvements (v2)
Added MCP server for tool integration
Introduced Firestore for persistent storage
Added session_saver agent
Enabled real-time data + memory
Fully meets advanced hackathon requirements
