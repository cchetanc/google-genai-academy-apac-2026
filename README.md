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

```
summarizer_agent/
├── __init__.py
├── agent.py
├── requirements.txt
├── .env.example
├── .gitignore
```

---

## 🚀 Key Improvements

* Upgraded from single-task summarizer → multi-capability agent
* Added question answering and classification
* Introduced intelligent request routing
* Fully aligned with hackathon requirements

---

## 📖 Reference

Updated deployment guide: 


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
