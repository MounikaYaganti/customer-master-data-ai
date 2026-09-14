# 🤖 Customer Master Data AI Assistant

An AI-assisted Master Data Management application designed to validate customer master data, detect potential duplicate customer records, provide AI-powered analysis, and support human reviewer decisions.

This project demonstrates how deterministic data quality rules and duplicate detection can be combined with Generative AI and Human-in-the-Loop decision-making for enterprise Master Data Management.

---

## 🚀 Features

### ✅ Customer Data Validation

Validates customer master data before processing.

Validation includes:

- Customer Name
- Country
- City
- Postal Code
- Customer Type
- Sales Organization

---

### 🔍 Duplicate Detection

The application compares a new customer record against existing customer master data.

Duplicate detection uses:

- Customer Name Similarity
- City Match
- Country Match
- Postal Code Match
- Customer Type Match
- Sales Organization Match

---

### 📊 Weighted Similarity Scoring

The duplicate detection engine calculates a weighted similarity score using multiple master data attributes.

| Attribute | Weight |
|---|---:|
| Customer Name | 50% |
| City | 15% |
| Country | 10% |
| Postal Code | 10% |
| Customer Type | 5% |
| Sales Organization | 10% |

---

### 🚨 Risk Classification

Potential duplicates are classified into risk levels:

- 🔴 HIGH — Similarity ≥ 85%
- 🟡 MEDIUM — Similarity between 70% and 84.99%
- 🟢 LOW — Similarity below 70%

---

### 🤖 AI Duplicate Analysis

The project uses a locally running Large Language Model through Ollama.

The AI provides:

- Duplicate risk analysis
- Match evidence
- Business-friendly explanation
- Recommended action

The LLM does not make the final Master Data decision.

---

### 👨‍💼 Human-in-the-Loop Review

The Master Data reviewer makes the final decision:

- ✅ Duplicate Confirmed
- ❌ Not a Duplicate
- 🔎 Further Investigation

This ensures that AI recommendations remain advisory.

---

### 📝 Audit Logging

Reviewer decisions are stored with:

- Timestamp
- Customer Name
- Potential Duplicate
- Similarity Score
- Risk Level
- Customer Master Attributes
- Reviewer Decision

---

### 📋 Review History

The Review History page allows users to:

- Search customer reviews
- Filter by Risk Level
- Filter by Reviewer Decision
- View historical decisions
- Download an audit report

---

### 📊 Dashboard

The Dashboard provides:

- Total Reviews
- High Risk Records
- Medium Risk Records
- Low Risk Records
- Reviewer Decision Metrics
- Duplicate Risk Distribution
- Reviewer Decision Distribution
- Similarity Score Analysis
- Recent Review Activity

---

## 🏗️ Project Architecture

```text
Customer Master Data
        │
        ▼
Data Validation
        │
        ▼
Duplicate Detection Engine
        │
        ▼
Weighted Similarity Score
        │
        ▼
Risk Classification
        │
        ▼
AI Recommendation
        │
        ▼
Qwen LLM Analysis
        │
        ▼
Human MDM Reviewer Decision
        │
        ▼
Audit Logging
        │
        ├───────────────┐
        ▼               ▼
Review History      Dashboard

🛠️ Technologies Used
Python
Streamlit
Pandas
Ollama
Qwen 2.5
SequenceMatcher
CSV
Generative AI
Large Language Models (LLMs)


📁 Project Structure
customer-master-ai/
│
├── data/
│   ├── customer_master.csv
│   └── review_decisions.csv
│
├── src/
│   ├── pages/
│   │   ├── Dashboard.py
│   │   └── Review_History.py
│   │
│   ├── streamlit_app.py
│   ├── validation.py
│   ├── duplicate.py
│   ├── llm.py
│   ├── data_loader.py
│   └── audit_logger.py
│
├── .gitignore
├── requirements.txt
└── README.md


⚙️ Installation
1. Clone the repository
git clone <your-repository-url>
2. Navigate to the project
cd customer-master-ai
3. Create a virtual environment
python -m venv venv
4. Activate the virtual environment
Windows
venv\Scripts\activate
5. Install dependencies
pip install -r requirements.txt


🤖 Ollama Setup

Install Ollama and download the Qwen model:

ollama pull qwen2.5:3b

Make sure Ollama is running before starting the application.



▶️ Run the Application

From the project root:

streamlit run src/streamlit_app.py


💡 Key Design Principle

The project separates:

Deterministic Logic

Used for:

Data Validation
Similarity Calculation
Duplicate Detection
Risk Classification
Generative AI

Used for:

Explaining duplicate risk
Summarizing match evidence
Providing business-friendly recommendations
Human Decision

Used for:

Final Master Data approval
Duplicate confirmation
Further investigation

This architecture helps ensure that Generative AI remains an advisory component rather than making autonomous Master Data decisions.


🔮 Future Improvements

Possible future enhancements include:

Fuzzy matching algorithms
Embedding-based duplicate detection
Vector database integration
RAG for Master Data policies
SAP MDG integration
Database storage
Role-based access control
Automated data quality scoring
👤 Author

MounikaYaganti

Enterprise Data Operations | SAP MDG | Master Data Management | Generative AI



⭐ If you found this project useful, feel free to star the repository!


---

## ⚠️ One small thing before saving

In this section:

```markdown
**MounikaYaganti**


Then press:

Ctrl + S
