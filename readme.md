# AI-Powered Cloud Cost Optimizer (LLM-Driven)

## 📌 Project Overview

This project is an **AI-powered Cloud Cost Optimizer** that helps users understand and optimize cloud costs based on a **plain-English project description**.

Instead of manually estimating infrastructure costs, the system:

1. Extracts a structured project profile using an LLM  
2. Generates realistic, budget-aware synthetic cloud billing  
3. Analyzes costs against the budget  
4. Produces actionable, multi-cloud cost optimization recommendations  
5. Operates through a **menu-driven CLI**

The project demonstrates **backend development**, **LLM integration**, and **robust handling of probabilistic AI outputs**.

---

## 🏗️ High-Level Architecture & Design

AI-Powered Cloud Cost Optimizer (LLM-Driven)
📌 Project Overview

This project is an AI-powered Cloud Cost Optimizer that helps users understand and optimize cloud costs based on a plain-English project description.

Instead of manually estimating infrastructure costs, the system:

Extracts a structured project profile using an LLM

Generates realistic, budget-aware synthetic cloud billing

Analyzes costs against the budget

Produces actionable, multi-cloud cost optimization recommendations

Operates through a menu-driven CLI

The project demonstrates backend development, LLM integration, and robust handling of probabilistic AI outputs.



---

## 🧠 Key Design Decisions

### 1️⃣ Separation of Concerns

Each responsibility is isolated into its own module:

- **Profile Extraction** → LLM-based
- **Billing Generation** → LLM-based
- **Cost Analysis** → Pure Python (deterministic)
- **Recommendations** → LLM-based
- **CLI** → Orchestration only (no business logic)

This ensures the system is **modular, testable, and production-oriented**.

---

### 2️⃣ Dual LLM Call Strategy (Important Design Choice)

Different LLM decoding strategies behave differently.  
To ensure reliability, **two LLM call modes** are used intentionally.

| Task | LLM Call Type | Reason |
|----|----|----|
| Project Profile Extraction | Streaming (`chat_stream`) | Small output, conservative JSON |
| Synthetic Billing | Non-streaming (`chat`) | Large structured JSON arrays |
| Recommendations | Non-streaming (`chat`) | Reasoning-heavy, long output |

This avoids JSON corruption and empty outputs — a **real-world LLM engineering concern**.

---

### 3️⃣ Defensive Validation of LLM Outputs

Because LLMs are probabilistic:

- All LLM outputs are validated
- Empty or malformed JSON is rejected early
- Corrupted artifacts are never propagated to downstream stages

This guarantees **pipeline stability**.

---

### 4️⃣ Absolute Paths for Artifacts

All file paths are resolved from the project root to ensure consistent behavior across:

- CLI execution
- Test scripts
- Windows environments

---

## 📁 Project Structure

.
├── artifacts/
│   ├── project_description.txt
│   ├── project_profile.json
│   ├── mock_billing.json
│   └── cost_optimization_report.json
│
├── config/
│   ├── profile_prompt.yaml
│   ├── billing_prompt.yaml
│   ├── recommendation_prompt.yaml
│   └── summary_prompt.yaml
│
├── src/
│   ├── components/
│   │   ├── profile_extractor.py
│   │   ├── billing_generator.py
│   │   ├── cost_analyzer.py
│   │   └── recommendation_engine.py
│   │
│   ├── pipeline/
│   │   ├── profile_pipeline.py
│   │   ├── billing_pipeline.py
│   │   ├── cost_analysis_pipeline.py
│   │   └── recommendation_pipeline.py
│   │
│   ├── utils/
│   │   └── llm_client.py
│   │
│   ├── constant/
│   │   └── paths.py
│   │
│   └── exception.py
│
├── cost_optimizer.py        # CLI entry point
├── test_profile_pipeline.py
├── test_billing_pipeline.py
├── test_cost_analysis_pipeline.py
├── test_recommendation_pipeline.py
├── requirements.txt
├── .env_example
└── README.md



⚙️ Setup Instructions
1️⃣ Clone the Repository
git clone <your-repository-url>
cd OpenText_project

2️⃣ Create and Activate Virtual Environment (Recommended: Conda)
conda create -n cloud-opt python=3.10 -y
conda activate cloud-opt


3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment Variables

Create a .env file using .env_example as reference:

MISTRAL_API_KEY=your_mistral_api_key_here


▶️ How to Run the Project
Start the CLI
python cost_optimizer.py

CLI Menu Options
1. Enter new project description
2. Run Complete Cost Analysis
3. View Recommendations
4. Export Report
5. Exit

Example Workflow

1️⃣ Enter a project description in plain English
2️⃣ Run complete cost analysis
3️⃣ View optimization recommendations
4️⃣ Export the final report

All generated artifacts are saved in the artifacts/ directory.



| File                          | Description                      |
| ----------------------------- | -------------------------------- |
| project_description.txt       | Raw user input                   |
| project_profile.json          | Structured project profile       |
| mock_billing.json             | Synthetic cloud billing          |
| cost_optimization_report.json | Final analysis & recommendations |


# LLM Usage & Academic Integrity

LLMs are used only where reasoning or generation is required

Deterministic logic (cost calculations) is handled in Python

Different decoding strategies are used intentionally

All LLM outputs are validated

# Tools Used

Mistral API – LLM inference - Not used Hugging face as mistral was not working but when i used mistral api from it's officaial website it was working fine

Python 3.10

dotenv

PyYAML

ChatGPT


