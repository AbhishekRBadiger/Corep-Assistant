#  COREP Regulatory Reporting Assistant

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Groq](https://img.shields.io/badge/Groq-AI%20Powered-purple.svg)

**AI-Powered Prototype for PRA COREP Compliance Reporting**  
*Internship Selection Project - 2026*

---

##  Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation Guide](#installation-guide)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Example Queries](#example-queries)
- [Limitations](#limitations)

---

## 🎯 Project Overview

The **COREP Regulatory Reporting Assistant** is an AI-powered web application designed to help UK banks streamline their Common Reporting (COREP) submissions to the Prudential Regulation Authority (PRA). 

This prototype demonstrates how Large Language Models (LLMs) can be leveraged to automate complex regulatory compliance tasks, reducing manual effort and minimizing errors in financial reporting.

### Key Statistics

- **~600 lines** of Python code
- **4 main components** (Backend, Frontend, Template Generator, Rules Database)
- **Full-stack implementation** (Python Flask + HTML/CSS/JavaScript)
- **AI Integration** using Groq's Llama 3.3 70B model
- **End-to-end workflow** from query to formatted output

---

## 🔍 Problem Statement

### The Real-World Challenge

UK banks subject to the PRA Rulebook must submit COREP regulatory returns that accurately reflect their:
- Capital adequacy
- Risk exposures  
- Prudential metrics

**Current Pain Points:**

1. **Complexity**: COREP forms contain 100+ fields with intricate calculations
2. **Time-Intensive**: Analysts spend hours interpreting dense regulatory rulebooks
3. **Error-Prone**: Manual data entry leads to mistakes and compliance issues
4. **Frequent Changes**: Rules and templates are updated regularly
5. **Audit Requirements**: Every entry must be traceable to specific regulations

### Business Impact

- **Manual Processing Time**: 40-80 hours per reporting cycle
- **Error Rate**: 15-25% of submissions require corrections
- **Compliance Risk**: Fines for incorrect submissions can reach millions
- **Resource Cost**: Senior analysts tied up with routine compliance tasks

---

## ✨ Solution

This prototype provides an **intelligent assistant** that:

1. **Understands Natural Language**: Ask questions in plain English
2. **Retrieves Relevant Rules**: Automatically finds applicable PRA regulations
3. **Generates Structured Output**: Uses AI to populate COREP fields correctly
4. **Provides Audit Trail**: Shows which rules justified each entry
5. **Validates Data**: Flags potential errors and inconsistencies

### Scope

**Focused on**: Own Funds (C 01.00) COREP template, specifically Common Equity Tier 1 (CET1) capital calculations

**Demonstrates**: End-to-end LLM-assisted regulatory reporting workflow

---

## 🚀 Features

### ✅ Core Functionality

- **Natural Language Query Processing**: Ask questions conversationally
- **Intelligent Rule Retrieval**: Finds relevant PRA regulations from knowledge base
- **AI-Powered Analysis**: Uses Groq's Llama 3.3 70B for understanding and generation
- **Structured JSON Output**: Consistent, parseable responses
- **COREP Template Formatting**: Converts AI output to readable regulatory forms
- **Field Validation**: Basic business rule checks
- **Audit Trail**: Documents which rules were applied and why
- **Web-Based Interface**: Clean, responsive UI accessible via browser

### 🎨 User Experience

- **Responsive Design**: Works on desktop and mobile
- **Real-Time Processing**: Live AI response generation
- **Example Queries**: Pre-loaded questions to get started
- **Error Handling**: Graceful fallbacks when AI fails
- **Loading Indicators**: Clear feedback during processing
- **Clean Output**: Professional table formatting with color coding

---

## 🛠️ Technology Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8+ | Core programming language |
| **Flask** | 3.0.0 | Web framework for API and routing |
| **Groq SDK** | 0.4.2 | LLM API integration |
| **python-dotenv** | 1.0.0 | Environment variable management |

### Frontend

| Technology | Purpose |
|------------|---------|
| **HTML5** | Page structure |
| **CSS3** | Styling and animations |
| **JavaScript (ES6+)** | Interactivity and API calls |

### AI Model

| Component | Details |
|-----------|---------|
| **Provider** | Groq Cloud |
| **Model** | Llama 3.3 70B Versatile |
| **Context Window** | 32,768 tokens |
| **Response Format** | JSON Mode |

### Why These Choices?

- **Flask**: Lightweight, perfect for prototypes, easy to learn
- **Groq**: Free tier, extremely fast inference, no credit card required
- **Llama 3.3**: Open-source, powerful, good at structured outputs
- **No Database**: Simplified deployment, easy to run locally

---

## 📁 Project Structure

```
corep-assistant/
│
├── app_groq.py              # Main Flask application
├── template_generator.py    # COREP template formatting module
├── rules.txt               # PRA regulatory rules database
├── requirements.txt        # Python dependencies
├── .env                    # API keys (not in repo)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

### File Descriptions

#### `app_groq.py` (Main Application)
- Flask web server setup
- API route handlers (`/` and `/ask`)
- AI prompt engineering
- Rule retrieval logic
- Fallback response generation
- HTML/CSS/JavaScript frontend code (embedded)

#### `template_generator.py` (Formatter)
- Converts JSON to HTML tables
- Generates COREP form extracts
- Applies styling and formatting
- Basic field validation
- Audit trail formatting

#### `rules.txt` (Knowledge Base)
- Simplified PRA Rulebook content
- COREP field definitions
- Capital adequacy regulations
- Deduction rules
- Plain text format for easy editing

#### `requirements.txt` (Dependencies)
- Lists all Python packages needed
- Pinned versions for reproducibility
- Used by `pip install -r requirements.txt`

#### `.env` (Configuration)
- Stores API keys securely
- Not committed to version control
- Required: `GROQ_API_KEY`

---

## 📥 Installation Guide

### Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher** installed ([Download here](https://www.python.org/downloads/))
- **pip** (Python package installer - comes with Python)
- **Git** (optional, for cloning)
- A **Groq API key** ([Get free key here](https://console.groq.com))

### Step 1: Get the Code

**Option A: Clone with Git**
```bash
git clone https://github.com/AbhishekRBadiger/corep-assistant.git
cd corep-assistant
```

**Option B: Download ZIP**
1. Download this repository as ZIP
2. Extract to a folder
3. Open terminal/command prompt in that folder

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear in your terminal.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- Groq (AI SDK)
- python-dotenv (environment variables)

### Step 4: Get Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up (free, no credit card required)
3. Navigate to **API Keys** section
4. Click **Create API Key**
5. Copy the key (starts with `gsk_...`)

### Step 5: Configure Environment

Create a file named `.env` in the project root:

```bash
# Windows
type nul > .env

# Mac/Linux
touch .env
```

Open `.env` and add:
```
GROQ_API_KEY=gsk_your_actual_api_key_here
```

**Important**: Replace `gsk_your_actual_api_key_here` with your real key!

### Step 6: Run the Application

```bash
python app_groq.py
```

You should see:
```
==================================================
COREP Assistant Starting (Groq Version)...
==================================================
📍 Server: http://localhost:5000
==================================================
```

### Step 7: Open in Browser

Navigate to: **http://localhost:5000**

You should see the COREP Assistant interface!

---

## 💻 Usage

### Basic Workflow

1. **Open the application** in your browser (http://localhost:5000)
2. **Type your question** in the text area
3. **Click "Get AI Assistance"** button
4. **Wait 2-5 seconds** for AI processing
5. **Review the results** - populated COREP template, audit trail, and validation notes

### Keyboard Shortcuts

- `Ctrl + Enter` (while in text area): Submit question
- `Clear` button: Reset the form

### Tips for Best Results

✅ **Be Specific**: "Calculate CET1 for a bank with £100M shares" works better than "Tell me about capital"

✅ **Include Numbers**: When you have specific values, include them in your question

✅ **Ask One Thing**: Focus questions get better answers than multi-part questions

✅ **Use Keywords**: Mention "CET1", "capital", "deductions", "COREP" to trigger relevant rules

---

## 🔄 How It Works

### Architecture Overview

```
┌─────────────┐
│   Browser   │
│   (User)    │
└──────┬──────┘
       │ HTTP Request
       ↓
┌─────────────────────────┐
│   Flask Web Server      │
│   - Receives question   │
│   - Loads rules         │
│   - Calls AI            │
│   - Formats response    │
└──────┬──────────────────┘
       │ API Call
       ↓
┌─────────────────────────┐
│   Groq Cloud API        │
│   - Llama 3.3 70B       │
│   - Processes prompt    │
│   - Returns JSON        │
└──────┬──────────────────┘
       │ JSON Response
       ↓
┌─────────────────────────┐
│   Template Generator    │
│   - Parses JSON         │
│   - Creates HTML table  │
│   - Validates fields    │
└──────┬──────────────────┘
       │ Formatted HTML
       ↓
┌─────────────┐
│   Browser   │
│   (Display) │
└─────────────┘
```

### Step-by-Step Flow

**1. User Input**
```
User types: "Our bank has £100M ordinary shares, 
            £20M retained earnings, and £5M intangibles. 
            Calculate CET1."
```

**2. Backend Processing**
```python
# app_groq.py receives the question
question = "Our bank has £100M ordinary shares..."

# Loads regulatory rules from rules.txt
rules = load_rules()  # Returns PRA regulations

# Finds relevant sections (currently returns all for simplicity)
relevant_rules = find_relevant_rules(question, rules)
```

**3. AI Prompt Construction**
```python
# Creates structured prompt
prompt = f"""
You are a UK banking regulatory expert.

RULES: {relevant_rules}
QUESTION: {question}

Respond with JSON containing:
- applicable_rules
- required_fields (with field_name, value, rule_reference)
- validation_notes
- audit_trail
"""
```

**4. Groq API Call**
```python
# Sends to Groq's Llama 3.3 70B
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
    response_format={"type": "json_object"}
)
```

**5. AI Response**
```json
{
  "applicable_rules": ["RULE 1: CET1 Components", "RULE 2: Deductions"],
  "required_fields": [
    {
      "field_name": "Ordinary Shares",
      "value": "100000",
      "rule_reference": "RULE 1: CET1 includes capital instruments"
    },
    {
      "field_name": "Retained Earnings",
      "value": "20000",
      "rule_reference": "RULE 1: CET1 includes retained earnings"
    },
    {
      "field_name": "Intangible Assets (deduction)",
      "value": "-5000",
      "rule_reference": "RULE 2: Intangible assets deducted from CET1"
    },
    {
      "field_name": "TOTAL CET1 Capital",
      "value": "115000",
      "rule_reference": "Calculated: 100,000 + 20,000 - 5,000"
    }
  ],
  "validation_notes": "Calculation verified: £115M CET1",
  "audit_trail": "Applied RULE 1 for positive items, RULE 2 for deductions"
}
```

**6. Template Generation**
```python
# template_generator.py converts JSON to HTML
formatted_output = generate_corep_template(llm_response)
# Creates styled table with all fields
```

**7. Display to User**
```
Browser shows:
┌─────────────────────────────────┬────────────┬─────────────────────────┐
│ Field Name                      │ Amount     │ Rule Reference          │
├─────────────────────────────────┼────────────┼─────────────────────────┤
│ Ordinary Shares                 │ £100,000   │ RULE 1: CET1 includes...│
│ Retained Earnings               │ £20,000    │ RULE 1: CET1 includes...│
│ Intangible Assets (deduction)   │ -£5,000    │ RULE 2: Deduct...       │
│ TOTAL CET1 Capital              │ £115,000   │ Sum of above            │
└─────────────────────────────────┴────────────┴─────────────────────────┘
```


## 💡 Example Queries

### Query 1: Calculation Question

**Input:**
```
How do I calculate Common Equity Tier 1 capital?
```

**Output:**
- Step-by-step calculation methodology
- Components to add (ordinary shares, retained earnings, reserves)
- Components to subtract (intangibles, deferred tax assets)
- Formula: CET1 = (Positive Items) - (Deductions)
- Rule references for each component

---

### Query 2: Deduction-Focused Question

**Input:**
```
What are the deductions from CET1?
```

**Output:**
- Intangible assets (explanation + rule reference)
- Deferred tax assets (explanation + rule reference)
- Current year losses (explanation + rule reference)
- Expected loss shortfalls (explanation + rule reference)
- Note: All entered as negative amounts

---

### Query 3: Calculation with Specific Numbers

**Input:**
```
Our bank has £100M ordinary shares, £20M retained earnings, 
and £5M intangibles. Calculate CET1.
```

**Output:**
```
Ordinary Shares:              £100,000 (thousands)
Retained Earnings:            £20,000 (thousands)
Intangible Assets (deduct):   -£5,000 (thousands)
────────────────────────────────────────────────
TOTAL CET1 Capital:           £115,000 (thousands)

Calculation: £100M + £20M - £5M = £115M
```

---

### Query 4: COREP Fields Question

**Input:**
```
What fields are required for Own Funds COREP reporting?
```

**Output:**
- C 01.00 - Row 010: Capital instruments eligible as CET1
- C 01.00 - Row 030: Share premium
- C 01.00 - Row 050: Retained earnings
- C 01.00 - Row 070: Accumulated other comprehensive income
- C 01.00 - Row 090: Other reserves
- C 01.00 - Row 210: Intangible assets (deduction)
- C 01.00 - Row 230: Deferred tax assets (deduction)
- C 01.00 - Row 290: Common Equity Tier 1 Capital (total)

---

## ⚠️ Limitations

### Current Constraints

1. **Simplified Rule Set**
   - Uses basic PRA rules, not the complete rulebook
   - Real system would need comprehensive regulatory database
   - Missing edge cases and complex scenarios

2. **Single Template Focus**
   - Only handles Own Funds (C 01.00) template
   - Production system needs 50+ COREP templates
   - Limited to CET1 calculations

3. **No File Generation**
   - Displays results in browser only
   - Doesn't generate actual Excel COREP files
   - No export functionality

4. **Basic Validation**
   - Simple business rule checks only
   - Missing complex cross-field validations
   - No regulatory compliance verification

5. **No Persistence**
   - Doesn't save queries or results
   - No user accounts or history
   - Each session is isolated

6. **Rule Retrieval**
   - Currently returns all rules (not smart filtering)
   - Production needs vector embeddings for relevance
   - No semantic search

7. **AI Limitations**
   - Occasional JSON formatting errors
   - May hallucinate rules that don't exist
   - Requires fallback mechanisms

8. **Single User**
   - No authentication
   - No multi-user support
   - Not production-ready security

---


*Last Updated: February 2026*  
*Version: 1.0.0*  
*Status: Prototype - Educational Use Only*
