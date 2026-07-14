# DeepEval POC

## Overview

This Proof of Concept (POC) demonstrates how Large Language Model (LLM) responses can be automatically evaluated using **DeepEval**.

Instead of manually validating AI responses, the framework evaluates generated responses against predefined expectations using AI evaluation metrics.

---

# Objective

The primary objective of this POC is to automate AI response validation by measuring:

- Hallucination Detection
- Answer Relevancy
- Correctness (GEval)

The framework is designed to be reusable, configurable, and independent of the AI provider.

---

# Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Backend Implementation |
| Google Gemini | AI Response Generation |
| DeepEval | AI Evaluation Framework |
| Pandas | Excel Dataset Handling |
| OpenPyXL | Excel Read/Write |
| dotenv | Configuration Management |

---

# Architecture

![Architecture](architecture.png)

---

# Execution Flow

```
Excel Dataset
      │
      ▼
 Excel Reader
      │
      ▼
AI Evaluation Service
      │
 ┌────┴────────┐
 ▼             ▼
Gemini     Mock Provider
Provider
      │
      ▼
 DeepEval Runner
      │
 ┌────┼───────────────────┐
 ▼    ▼                   ▼
Hallucination
Answer Relevancy
Correctness (GEval)
      │
      ▼
 Report Writer
      │
      ▼
evaluation_report.xlsx
```

---

# Project Structure

```
DeepEval-POC

src
│
├── config
├── data
├── evaluators
├── exceptions
├── providers
├── reports
├── services
└── tests

dataset
│
├── inputData
└── outputData
```

---

# Features

- Excel driven AI evaluation
- Gemini Integration
- Mock Provider Support
- DeepEval Integration
- Hallucination Detection
- Answer Relevancy Evaluation
- Correctness Evaluation (GEval)
- Exception Handling
- Retry Mechanism
- Configurable Execution
- Excel Report Generation

---

# Supported Evaluation Metrics

| Metric | Description |
|---------|-------------|
| Hallucination | Detects fabricated or unsupported information |
| Answer Relevancy | Measures how relevant the response is to the prompt |
| Correctness (GEval) | Measures factual correctness against the expected output |

---

# Configuration

The application is configured using the `.env` file.

Example:

```
GEMINI_API_KEY=YOUR_API_KEY
GEMINI_MODEL=models/gemini-flash-latest
DEEPEVAL_GEMINI_MODEL=gemini-flash-latest
MAX_TEST_CASES=5
USE_MOCK_PROVIDER=True
```

---

# Running the Application

Activate Virtual Environment

```
.venv\Scripts\activate
```

Run

```
python src/main.py
```

---

# Sample Output

The framework generates an evaluation report containing:

- AI Response
- Hallucination Score
- Answer Relevancy Score
- Correctness Score
- Result
- Remarks

---

# Current Capabilities

- AI Response Generation
- AI Evaluation using DeepEval
- Gemini Integration
- Mock Provider Support
- Excel Based Dataset Execution
- Configurable Number of Test Cases
- Exception Handling
- Execution Summary
- Excel Report Generation

---

# Future Enhancements

- HTML Dashboard
- CI/CD Integration
- Support for Multiple LLM Providers
- Azure OpenAI Integration
- Claude Integration
- Interactive Analytics Dashboard
- Additional DeepEval Metrics

---

# Author

**Shivani Rampally**

QA Engineer

DeepEval AI Hallucination Evaluation POC