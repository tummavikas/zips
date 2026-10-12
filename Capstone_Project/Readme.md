AI ENGINEER PROGRAM | CAPSTONE PROJECT 

Intelligent Vehicle Loan Advisor 

Candidate Brief: design it, build it, defend it 

1. Background 

A customer walking into a dealership or a bank wants answers to a chain of questions: Will I get a vehicle loan? How much will I be given? Which vehicles can I actually afford with that amount? What exactly does each of those vehicles offer? Today these answers come from different people, different documents and different systems, and customers are often told "rejected" with no reason. 

In this capstone you will build one working system that answers the whole chain, end to end, and that can explain its answers by referring to the lender’s written lending policy. 

2. Problem Statement 

The challenge 

Build an intelligent vehicle loan advisor that, from an applicant’s details, decides whether the loan is Approved or Rejected; if approved, determines how much loan is sanctioned; based on that amount, shows which vehicles the applicant can buy; and retrieves the details of any specific vehicle the applicant picks. 

 

Every decision must be explainable. Rejections, and the sanctioned amount, must be justified from the policy documents rather than from the system’s imagination. Vehicle information must come from your vehicle catalogue, not be invented. 

3. The Required Flow 

The applicant journey below is fixed. How each step is implemented within the technology stack is your design. 

1 

Applicant details 

The applicant provides financial and personal parameters (for example income, credit score, employment experience, existing loan obligations, requested tenure and down payment). You decide the full parameter set and justify it. 

2 

Eligibility decision 

The system decides Approved or Rejected based on those parameters. 

3 

Sanctioned loan amount 

If approved, the system states how much loan is sanctioned (and the terms that go with it). This can be lower than what the applicant hoped for. If rejected, the system stops here and explains why. 

4 

Affordable vehicles 

Based on the sanctioned amount (and the down payment, if any), the system shows which vehicles the applicant can buy. 

5 

Vehicle details 

The applicant selects a vehicle and the system returns its specific details: price, variants, specifications, features and anything else a buyer needs to decide. 

 

4. Example Scenarios 

These illustrate the expected behaviour and are not test data. All figures and vehicle names are made up. 

4.1 Approved applicant 

Applicant detail 

Value 

Monthly income 

₹85,000 

Credit score 

745 

Employment experience 

6 years 

Existing EMIs 

₹12,000 per month 

Requested tenure 

5 years 

Down payment available 

₹1,50,000 

 

Decision: Approved 

Sanctioned loan: ₹8,00,000 for 5 years, with the policy rules that set this limit. 

Vehicles within budget: a shortlist, for example "Hatchback X", "Compact Sedan Y" and "Compact SUV Z", each with price and estimated EMI. 

Details for the selected vehicle: specifications, variants, mileage, features and price breakdown for the one the applicant chooses. 

4.2 Rejected applicant 

Applicant detail 

Value 

Monthly income 

₹22,000 

Credit score 

580 

Employment experience 

1 year 

Existing EMIs 

₹9,000 per month, 2 active loans 

Requested tenure 

5 years 

 

Decision: Rejected 

Explanation (illustrative): “The application was rejected because the credit score and the ratio of existing EMIs to income do not meet the eligibility requirements in the vehicle loan policy.” 

Source: the policy document and the specific section the reasoning is based on. 

Your explanations are expected to be more specific than these samples, for example naming the policy threshold alongside the applicant’s actual value. 

5. What You Must Deliver 

5.1 Eligibility decision 

A model trained on historical loan data that predicts Approved or Rejected for a new applicant. 

Evidence of data exploration and preparation, a comparison of more than one modelling approach, and stated reasons for your final choice. 

Evaluation that fits the business problem. Think about which mistakes are costly for a lender and which for a customer, and let that guide your metrics. 

5.2 Sanctioned loan amount 

For approved applicants the system must produce a specific sanctioned amount. You choose how: a learned model, policy rules, or a combination. Justify the choice. 

The amount must be consistent with the applicant’s repayment capacity and with the limits in your policy. It must never exceed what the policy allows. 

The system should show how the amount was arrived at. 

5.3 Vehicle recommendation 

Given the sanctioned amount (and down payment if you include it), return the vehicles the applicant can reasonably buy. 

Decide how affordability is defined and be explicit about it. For example, whether price, EMI or total cost is the deciding factor. 

Make the shortlist useful: allow narrowing by what a buyer cares about, and order results in a way you can defend. 

If no vehicle fits the budget, say so clearly and help the applicant understand what could change that. 

5.4 Vehicle details 

For any vehicle in the shortlist, return its specific details from your vehicle information, including price, variants, specifications and features. 

Answers about a vehicle must come from your vehicle information. If something is not in the data, the system must say it does not know instead of guessing. 

Your vehicle information should include both structured facts and descriptive material of the kind found in brochures, so that detail questions are a real retrieval problem. 

5.5 Policy-grounded explanation 

Rejections and sanctioned amounts must be explained in plain language, grounded in your loan policy documents. 

Every explanation shows its sources: which document and which section or passage supports each reason. 

If the policy does not contain enough to justify a reason, the system must say so. 

5.6 Service layer 

Every capability above must be available to other software through a well-defined interface, not only through your user interface. 

The interface validates inputs, returns clear errors, and is documented well enough for another developer to use without asking you questions. 

5.7 User application 

A usable front end that walks the applicant through the full flow: enter details, see the decision, see the sanctioned amount, browse the vehicles, and open the details of one vehicle. 

A loan officer who is not a data scientist should be able to use it and understand the results, including the policy sources behind them. 

6. Data and Documents 

Nothing is supplied. Sourcing or creating the following is part of the exercise. 

Loan data. A public loan or credit dataset, or a realistic synthetic one. State where it came from, what each field means and its limitations. 

Loan policy documents. Author your own realistic vehicle loan policy: eligibility criteria, credit score rules, income and obligation limits, maximum loan-to-value, tenure rules, exceptions and documentation. It should have several distinct sections and some rules that apply to only some applicants. 

Vehicle information. A realistic catalogue of at least 25 vehicles across several price bands and types, with variants and details. It should include both structured data and descriptive documents. Cite your sources if the data is based on real vehicles, or mark it as synthetic. 

Consistency. The patterns your model learns, the rules in your policy and the amounts you sanction should not contradict each other. Decide how to handle conflicts and document it. 

No real personal data. Do not use real customer data or confidential company documents. 

7. Technology Stack 

Build the solution using the technologies taught in this course. Everything below has been covered in the program, so no outside frameworks are required. 

Layer 

Technology 

Used for 

Language 

Python 3 

All backend, ML, RAG and frontend code. 

Data handling and EDA 

Pandas, NumPy, Matplotlib / Seaborn 

Loading, cleaning and exploring the loan and vehicle data; missing values, outliers, encoding and feature engineering. 

Machine learning 

Scikit-learn 

Training and comparing classification models for the approve / reject decision (for example Logistic Regression, Decision Tree, Random Forest, XGBoost), and regression for the loan amount if you use a model. Includes train/test split, scaling, cross-validation and hyperparameter tuning. 

Model explainability (optional) 

SHAP / LIME 

Showing which applicant attributes drove a decision. 

Embeddings and retrieval 

OpenAI or Gemini Embeddings, similarity search over a vector store 

Chunking the policy documents and vehicle brochures, embedding them and retrieving the most relevant passages. 

LLM 

OpenAI or Gemini API 

Writing the policy-grounded explanation and the vehicle detail answers from retrieved passages. Prompt design and guardrails are your responsibility. 

Data storage 

SQLite (plus files for documents) 

Vehicle catalogue, and optionally a log of applications and decisions. 

Backend 

FastAPI, Pydantic, Uvicorn 

REST API with input validation and automatic documentation. 

Frontend 

Streamlit 

Interactive application for the complete applicant flow. 

Packaging and tooling 

requirements file, environment variables (.env), Docker and Docker Compose 

Version control, reproducible setup, keeping secrets out of the code, and running backend and frontend together. 

 

Rules for the stack 

•  The backend (FastAPI) and the frontend (Streamlit) must be separate applications. The frontend talks to the backend only through the API. 

•  Trained models are saved to disk and loaded by the backend. Training must not happen when the API starts. 

•  API keys and other secrets live in environment variables and never in the code or the repository. 

•  Docker and Docker Compose are expected for running the whole system; they should start both applications with one command. 

 

8. Project Structure 

Organise your repository along these lines. Names can differ, but the separation between data, notebooks, model code, retrieval code, backend and frontend must stay clear. 

vehicle-loan-advisor/ 

|-- README.md                  setup, run and usage instructions 

|-- requirements.txt           Python dependencies 

|-- .env.example               names of required variables (no real keys) 

|-- docker-compose.yml         runs backend and frontend together 

|-- data/ 

|   |-- raw/                   loan dataset, vehicle catalogue (structured) 

|   |-- processed/             cleaned and feature-engineered data 

|   `-- documents/ 

|       |-- policy/            vehicle loan policy documents 

|       `-- vehicles/          brochures and descriptive vehicle documents 

|-- notebooks/                 EDA, model training and comparison, evaluation 

|-- models/                    saved trained models and preprocessing objects 

|-- vectorstore/               stored embeddings of the documents 

|-- backend/ 

|   |-- Dockerfile 

|   |-- main.py                FastAPI app and route definitions 

|   |-- schemas.py             Pydantic request and response models 

|   |-- services/ 

|   |   |-- eligibility.py     approve / reject prediction 

|   |   |-- loan_amount.py     sanctioned amount and terms 

|   |   |-- vehicles.py        affordability filter and vehicle lookup 

|   |   `-- explain.py         retrieval and LLM explanation 

|   |-- rag/                   ingestion, chunking, embeddings, retriever 

|   `-- db/                    SQLite setup and queries 

|-- frontend/ 

|   |-- Dockerfile 

|   `-- app.py                 Streamlit application 

|-- tests/                     API and logic tests 

`-- docs/                      design document, evaluation report, screenshots 

 

8.1 Backend API 

Expose at least the following endpoints. Request and response shapes are yours to design and must be validated and documented. 

Endpoint 

Purpose 

POST /predict 

Takes applicant details and returns Approved or Rejected, with the model’s confidence. 

POST /loan-amount 

For an approved applicant, returns the sanctioned amount and loan terms. 

POST /vehicles 

Takes the sanctioned amount (and down payment) and returns the vehicles the applicant can afford. 

GET /vehicles/{id} 

Returns the full details of one vehicle. 

POST /explain 

Retrieves policy passages and returns a grounded explanation for the decision or amount, with sources. 

GET /health 

Reports that the service is running. 

 

8.2 Frontend pages 

Applicant form: enter details and submit. 

Decision view: Approved or Rejected, the sanctioned amount, the explanation and its policy sources. 

Vehicle shortlist: vehicles within the sanctioned amount, with price and estimated EMI. 

Vehicle detail view: full details of the selected vehicle. 

9. Working implementation in this repository

The capstone starter implementation in this repository uses Python, SQLite, FastAPI, Streamlit, scikit-learn, and the Gemini API. It is a synthetic educational demo, not a real credit decision system.

Setup from the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Set GEMINI_API_KEY in .env, then prepare the model and retrieval index:

```powershell
python -m backend.train_model
python -m backend.db.seed
python -m backend.rag.ingest
```

Training writes synthetic loan examples, compares Logistic Regression with Random Forest, saves the chosen model, and records metrics. Ingestion makes Gemini embedding API calls for policy passages and vehicle descriptions. Each explanation request embeds its question, retrieves matching SQLite passages, and calls Gemini to generate a source-grounded answer. Gemini calls can incur API usage charges.

Run the applications in separate terminals:

```powershell
uvicorn backend.main:app --reload
```

```powershell
streamlit run frontend/app.py
```

The Streamlit app is available at http://localhost:8501, and the FastAPI documentation is available at http://localhost:8000/docs. Run automated checks with `pytest`.

The classifier returns a prediction and probability for evaluation and decision support. The displayed Approved/Rejected outcome is determined by the implemented written-policy checks; policy rules and repayment limits remain authoritative. The included policy, generated loan data, and 25-vehicle catalogue are synthetic, so the system is not suitable for actual lending or financial advice.