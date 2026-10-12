from pathlib import Path

import joblib
import pandas as pd

from backend.config import MODEL_PATH
from backend.schemas import Applicant

FEATURES = [
    "monthly_income", "credit_score", "employment_years", "existing_emis",
    "requested_tenure_months", "requested_loan_amount", "down_payment", "age",
    "emi_to_income",
]
POLICY_SOURCE = "vehicle_loan_policy.md, sections 1–4"


def _pipeline():
    path = Path(MODEL_PATH)
    if not path.exists():
        raise RuntimeError("Eligibility model is missing. Run `python -m backend.train_model` first.")
    return joblib.load(path)


def decide(applicant: Applicant) -> dict:
    monthly_emi = applicant.requested_loan_amount * 0.105 / 12 / (
        1 - (1 + 0.105 / 12) ** (-applicant.requested_tenure_months)
    )
    record = applicant.model_dump()
    record["emi_to_income"] = (monthly_emi + applicant.existing_emis) / applicant.monthly_income
    features = pd.DataFrame([{key: record[key] for key in FEATURES}], columns=FEATURES)
    probability = float(_pipeline().predict_proba(features)[0][1])

    reasons: list[str] = []
    minimum_experience = 1 if applicant.employment_type == "salaried" else 2
    if applicant.age < 21:
        reasons.append(f"Age {applicant.age} is below the policy minimum of 21.")
    if applicant.age + applicant.requested_tenure_months / 12 > 65:
        reasons.append("Applicant age at the end of the requested tenure would exceed 65.")
    if applicant.monthly_income < 25_000:
        reasons.append(f"Monthly income ₹{applicant.monthly_income:,.0f} is below ₹25,000.")
    if applicant.credit_score < 650:
        reasons.append(f"Credit score {applicant.credit_score} is below the minimum of 650.")
    if applicant.employment_years < minimum_experience:
        reasons.append(
            f"{applicant.employment_type.replace('_', ' ').title()} experience is below "
            f"the policy minimum of {minimum_experience} year(s)."
        )
    if applicant.requested_tenure_months > 84:
        reasons.append("Requested tenure exceeds the policy maximum of 84 months.")
    if record["emi_to_income"] > 0.50:
        reasons.append(
            f"Estimated total EMI burden is {record['emi_to_income']:.1%} of income, "
            "above the policy maximum of 50%."
        )
    return {
        "decision": "Approved" if not reasons else "Rejected",
        "model_prediction": "Approved" if probability >= 0.5 else "Rejected",
        "model_probability": round(probability, 4),
        "reasons": reasons or ["Applicant meets the implemented policy eligibility checks."],
        "policy_source": POLICY_SOURCE,
    }
