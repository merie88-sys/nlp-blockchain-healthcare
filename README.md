# NLP_Blockchain_Healthcare – Automated Medical Claims Validation System

## Description
This project presents a proof-of-concept (POC) system that automates the validation of medical reports and triggers insurance reimbursements using a combination of **Natural Language Processing (NLP)**, an **AI-powered Oracle**, and a **Smart Contract simulation**. The system extracts key information from unstructured medical reports (free text), validates it against insurance rules via an AI oracle, and simulates a blockchain-based smart contract to automate decision-making. This architecture bridges off-chain data and on-chain execution, ensuring transparency, traceability, and automation in healthcare insurance processes.

## Dataset Information
Currently, this project uses **synthetic medical reports** for demonstration purposes. No real clinical dataset is integrated yet.  
- Example report: `"The patient underwent a brain MRI on April 10, 2025."`  
- Purpose: To test NLP extraction and rule-based validation.  
- Future plan: Integrate publicly available datasets such as MIMIC-III (after anonymization and translation) or French MedNLP Corpus for multilingual support.  
- Data format: Plain text files (`.txt`) and structured YAML rules.

## Code Information
The project consists of three core Python modules simulating the full pipeline:

1. **`medical_nlp_extractor.py`**  
   - Extracts medical entities (e.g., exam type, date) from free-text reports using spaCy NLP.
   - Supports English (en_core_web_sm) with plans to add French (fr_core_news_sm).

2. **`simulate_oracle.py`**  
   - Simulates an AI-powered oracle using FastAPI.
   - Validates extracted data against business rules defined in `config/rules.yaml`.
   - Exposes a REST API endpoint (`/valider`) for external validation requests.

3. **`simulate_smart_contract.py`**  
   - Simulates a smart contract logic in Python.
   - Receives validation results and "executes" a reimbursement decision.
   - Logs the outcome (approved/rejected) and amount.

## Usage Instructions
1. **Clone the repository:**
   ```bash
   git clone https://github.com/merie88-sys/nlp-blockchain-healthcare
## Set up a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Linux/macOS
# or
venv\Scripts\activate     # On Windows
 ## Install dependencies
 pip install -r requirements.txt
python -m spacy download en_core_web_sm
 ## Run the components:
1. **Test NLP extraction**
   python medical_nlp_extractor.py
2. **Launch the AI Oracle API:**
   uvicorn simulate_oracle:app --reload
3. **Simulate smart contract execution**
   python simulate_smart_contract.py
## Requirements
Python 3.8 or higher 
Libraries:
   spacy (for NLP)
   fastapi, uvicorn (for API/oracle)
   pyyaml (for rule configuration)
spaCy English model: en_core_web_sm
Optional tools: VS Code, Anaconda, Postman (for API testing)
## To install all dependencies at once:
pip install spacy fastapi uvicorn pyyaml
python -m spacy download en_core_web_sm
   
   
