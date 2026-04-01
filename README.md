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

The **Summarizer Agent** is a simple yet powerful AI agent that takes any input text and generates a concise summary using **Gemini 2.5 Flash**.

It demonstrates the fundamentals of building an AI agent using **Google ADK**, including tool integration, prompt design, and deployment to Cloud Run.

## ⚙️ Features

* Accepts long-form text input
* Generates concise 3–5 sentence summaries
* Uses clear and simple language
* Fully deployable as an HTTP endpoint

## 🏗️ Architecture

* **Root Agent**: Handles all incoming requests
* **Tool**: `summarize_text` (passes input to LLM)
* **Model**: Gemini 2.5 Flash

## 🚀 Deployment

The agent is deployed using:

* Google Cloud Run
* Artifact Registry
* Cloud Build
* Vertex AI (Gemini)

## 🧪 Example Use Case

Input:

```
Artificial intelligence is transforming industries...
```

Output:

```
AI is transforming industries by enabling automation and solving complex problems...
```

## 📖 Reference

Implementation based on the ADK deployment guide 

---

# 🎓 Project 2: Campus Placement Assistant

## 📌 Overview

The **Placement Assistant** is a **multi-agent AI system** designed to help students prepare for campus placements. It provides:

* Resume guidance
* Company-specific preparation tips
* Interview questions
* HR round strategies

This project extends the ADK framework into a real-world, high-impact use case for students.

## 💡 Key Idea

Students can interact conversationally with the agent and receive **end-to-end placement preparation guidance** tailored to a specific company.

## 🏗️ Architecture (Multi-Agent Workflow)

The system uses a **Sequential Agent pipeline**:

1. **Greeter (Root Agent)**

   * Captures user intent
   * Routes workflow

2. **Resume Analyst**

   * Fetches company data
   * Suggests resume improvements

3. **Interview Coach**

   * Generates interview questions
   * Provides answer hints

4. **Response Formatter**

   * Produces structured final output

## 🧰 Tools Used

* `company_db_tool` (custom internal database)
* `wikipedia_tool` (for company insights)
* Shared state management via ADK

## ⚙️ Features

* Company-specific preparation guidance
* Resume improvement suggestions
* Real interview questions with hints
* Motivational and structured responses
* Works for companies like Google, Amazon, Microsoft, TCS, Infosys

## 🧪 Example Queries

* "I am preparing for Google"
* "Help me with Amazon placement"
* "What about TCS NQT?"

## 📊 Output Includes

* Company snapshot
* Required skills
* Interview process
* 5 practice questions with hints
* Final motivational tip

## ☁️ Deployment

* Hosted on **Google Cloud Run**
* Uses **Gemini 2.5 Flash via Vertex AI**
* Built and deployed using **ADK CLI**

## 🌍 Why This Project Matters

* Solves a real student problem in the APAC region
* Highly interactive and demo-friendly
* Extensible to real job platforms and resume parsing

## 📖 Reference

Detailed implementation from project submission document 

---

# ☁️ Tech Stack

* **Google ADK (Agent Development Kit)**
* **Gemini 2.5 Flash (Vertex AI)**
* **Python 3.11+**
* **Cloud Run**
* **Cloud Build**
* **Artifact Registry**
* **LangChain (Wikipedia Tool)**

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone <your-repo-link>
cd GenAI-Academy-Apac-2026
```

## 2. Set Up Environment

* Create a `.env` file with:

```
MODEL="gemini-2.5-flash"
```

## 3. Install Dependencies

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## 4. Deploy (Example)

```bash
uvx --from google-adk==1.14.0 adk deploy cloud_run ...
```

---

# 🧪 Testing

After deployment:

* Open Cloud Run service URL
* Use ADK UI chat interface
* Try sample prompts for both agents

---

# 📌 Notes

* `.env` file should NOT be committed to GitHub
* Uses only free-tier compatible GCP services
* Easily extensible with additional tools and APIs

---

# 🙌 Acknowledgment

Built as part of **GenAI Academy APAC 2026 – Track 1: Build & Deploy AI Agents**

---

# 📬 Future Improvements

* Resume PDF parsing (Document AI)
* Integration with job portals (LinkedIn, Naukri)
* Voice-based mock interviews
* Personalized learning paths

---

⭐ If you found this project interesting, feel free to star the repo!
