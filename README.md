# DeepEval POC

## Overview
This Proof of Concept (POC) demonstrates how Large Language Model (LLM) responses can be automatically evaluated using **DeepEval**.
The framework reads test cases from an Excel dataset, generates AI responses using Google Gemini, and evaluates the responses using DeepEval metrics.
A Mock Provider is also available for testing when Gemini is unavailable or when API usage needs to be avoided.

# Objective
The main objective of this POC is to automate AI response validation by measuring:
- Hallucination Detection
- Answer Relevancy
- Correctness (GEval)
The framework uses an Excel based dataset and generates an Excel evaluation report.

# Technologies Used
| Technology    | Purpose                  |
|---------------|--------------------------|
| Python        | Backend Implementation   |
| Google Gemini | AI Response Generation   | 
| DeepEval      | AI Evaluation Framework  | 
| Pandas        | Excel Dataset Handling   |
| OpenPyXL      | Excel Read/Write         |
| dotenv        | Configuration Management |

# Execution Flow
Excel Dataset
      │
      ▼
 Excel Reader
      │
      ▼
AI Evaluation Service
      │
 ┌────┴────────────┐
 ▼                 ▼
Gemini Provider   Mock Provider
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

# Supported Evaluation Metrics
| Metric              | Description                                        |
| ------------------- | -------------------------------------------------- |
| Hallucination       | Detects fabricated or unsupported information      |
| Answer Relevancy    | Measures how relevant the response is to the input |
| Correctness (GEval) | Measures correctness against the expected output   |

# Configuration
The application is configured using the .env file.
GEMINI_API_KEY=YOUR_API_KEY            -> Gemini API key used for Gemini response generation and DeepEval evaluation.
GEMINI_MODEL=models/gemini-flash-latest -> Gemini model used for generating the AI response.
DEEPEVAL_GEMINI_MODEL=gemini-flash-latest -> Gemini model used by DeepEval for evaluation.

MAX_TEST_CASES=5 -> Controls the number of test cases executed from the dataset.
USE_MOCK_PROVIDER=False ->When enabled, the Mock Provider is used instead of the Gemini Provider.The Mock Provider is included for testing and for cases where Gemini API access is unavailable.

# Running the Application
Activate the virtual environment:.venv\Scripts\activate
Install dependencies:             pip install -r requirements.txt
Run the application:              python src/main.py

# Dataset
The input dataset is an Excel file located at: dataset/inputData/hallucination_dataset.xlsx
Output report is generated under: dataset/outputData/

