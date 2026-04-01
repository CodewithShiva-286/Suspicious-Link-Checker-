You are a senior software architect and cybersecurity engineer.

I have a Product Requirements Document (PRD) already written in a markdown (.md) file in this project. Your job is to carefully read and deeply understand the PRD before doing anything else.

⚠️ IMPORTANT INSTRUCTIONS:

* Do NOT start coding
* Do NOT generate implementation yet
* First enter FULL PLAN MODE
* Think step-by-step and design the entire system before execution

---

## 🎯 PROJECT CONTEXT

We are building a **Suspicious Link Checker (Service-Based Cybersecurity Tool)**.

The system will:

* Accept a URL from the user
* Analyze it using multiple external security APIs:

  * Google Safe Browsing
  * VirusTotal
  * WHOIS (domain age)
  * SSL certificate check
* Aggregate results using a rule-based decision engine
* Return:

  * Verdict (Safe / Suspicious / Malicious)
  * Confidence score
  * Detailed reasoning
* Display results in a **futuristic frontend with step-by-step scan logs**

We are NOT training any ML model. This is a **service-integration + system design project**.

---

## 🧠 YOUR TASK (PLAN MODE)

You must produce a COMPLETE SYSTEM PLAN before coding.

---

### 1️⃣ Understand & Summarize

* Read the PRD
* Summarize the system in your own words
* Identify core components and data flow

---

### 2️⃣ Define Architecture

Design a clean architecture including:

* Frontend (React)
* Backend (FastAPI)
* External API layer
* Decision engine
* Database (MongoDB)

Create:

* High-level architecture diagram (text-based)
* Data flow from input → output

---

### 3️⃣ Define Backend Structure

Design a production-level backend structure:

* Folder structure
* Modules:

  * routes
  * services
  * utils
  * decision_engine
  * database

For each module:

* Define responsibility
* Define inputs/outputs

---

### 4️⃣ API Integration Plan

For EACH external service:

* Google Safe Browsing
* VirusTotal
* WHOIS
* SSL check

Define:

* Endpoint usage
* Request format
* Response format
* How we normalize responses into a common structure

---

### 5️⃣ Data Standardization Layer

Design a unified response format like:
{
source: string,
status: safe/suspicious/malicious,
score: number,
details: string
}

Explain how all APIs will be converted into this format.

---

### 6️⃣ Decision Engine Design

Design:

* Scoring system
* Weight distribution
* Threshold logic
* How reasons are generated

Include edge cases:

* Missing API response
* Conflicting results

---

### 7️⃣ Frontend Plan

Design UI structure:

* Components list
* Data flow from backend
* How step-by-step scan logs will work
* Animation logic (no code, just plan)

---

### 8️⃣ Database Design

* Schema for scan logs
* Fields and types
* Indexing strategy

---

### 9️⃣ Environment & Config Plan

Define:

* Required API keys
* .env structure
* How backend accesses them securely

---

### 🔟 Development Roadmap (CRITICAL)

Break the project into **clear chunks (phases)**:

For EACH chunk define:

* Goal
* What will be built
* Files/modules involved
* Dependencies

Example:
Chunk 1 → Setup
Chunk 2 → URL processing
Chunk 3 → Google API integration
...

---

### 1️⃣1️⃣ Risk & Constraints Analysis

Identify:

* API rate limits
* Failure cases
* Performance issues
* Security concerns

---

### 1️⃣2️⃣ Future Enhancements

List possible extensions:

* Browser extension
* Public API
* AI explanations
* Bulk scanning

---

## 🚫 DO NOT:

* Write actual code
* Skip planning steps
* Give shallow answers

---

## ✅ OUTPUT FORMAT

Return a **clean, structured plan** with:

* Headings
* Bullet points
* Clear explanations

Make it:

* Beginner-friendly
* But architect-level detailed

---

Take your time and think deeply before answering.
