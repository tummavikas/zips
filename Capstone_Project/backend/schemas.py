from typing import Literal

from pydantic import BaseModel, Field


class Applicant(BaseModel):
    monthly_income: float = Field(gt=0, le=10_000_000)
    credit_score: int = Field(ge=300, le=900)
    employment_years: float = Field(ge=0, le=60)
    employment_type: Literal["salaried", "self_employed"] = "salaried"
    existing_emis: float = Field(ge=0, le=10_000_000)
    requested_tenure_months: int = Field(ge=6, le=120)
    requested_loan_amount: float = Field(gt=0, le=100_000_000)
    down_payment: float = Field(ge=0, le=100_000_000)
    age: int = Field(ge=18, le=100)


class EligibilityResponse(BaseModel):
    decision: Literal["Approved", "Rejected"]
    model_prediction: Literal["Approved", "Rejected"]
    model_probability: float
    reasons: list[str]
    policy_source: str


class LoanAmountRequest(BaseModel):
    applicant: Applicant
    decision: Literal["Approved", "Rejected"]


class LoanAmountResponse(BaseModel):
    sanctioned_amount: float
    tenure_months: int
    annual_interest_rate: float
    estimated_monthly_emi: float
    total_vehicle_budget: float
    calculation: list[str]
    policy_source: str


class VehicleSearchRequest(BaseModel):
    budget: float = Field(gt=0, le=100_000_000)
    category: str | None = None
    fuel_type: str | None = None


class ExplanationRequest(BaseModel):
    question: str = Field(min_length=5, max_length=2000)
    context: dict = Field(default_factory=dict)


class ExplanationResponse(BaseModel):
    answer: str
    sources: list[dict]
