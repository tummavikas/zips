from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
import requests

from backend.db.database import initialize_database
from backend.db.seed import seed_vehicles
from backend.schemas import (
    Applicant, EligibilityResponse, ExplanationRequest, ExplanationResponse,
    LoanAmountRequest, LoanAmountResponse, VehicleSearchRequest,
)
from backend.services.eligibility import decide
from backend.services.loan_amount import calculate_sanction
from backend.services.vehicles import affordable_vehicles, get_vehicle
from backend.rag.retriever import explain


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    seed_vehicles()
    yield


app = FastAPI(
    title="Intelligent Vehicle Loan Advisor",
    description="Synthetic educational demo for loan eligibility, affordability, and grounded retrieval.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/predict", response_model=EligibilityResponse)
def predict(applicant: Applicant):
    try:
        return decide(applicant)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error


@app.post("/loan-amount", response_model=LoanAmountResponse)
def loan_amount(request: LoanAmountRequest):
    try:
        return calculate_sanction(request.applicant, request.decision)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/vehicles")
def vehicles(request: VehicleSearchRequest):
    return affordable_vehicles(request.budget, request.category, request.fuel_type)


@app.get("/vehicles/{vehicle_id}")
def vehicle_details(vehicle_id: str):
    vehicle = get_vehicle(vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle was not found.")
    return vehicle


@app.post("/explain", response_model=ExplanationResponse)
def explanation(request: ExplanationRequest):
    question = request.question
    if request.context:
        question = f"{question}\nApplicant/result context: {request.context}"
    try:
        return explain(question)
    except (RuntimeError, ValueError, KeyError) as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except requests.RequestException as error:
        raise HTTPException(
            status_code=502,
            detail="Gemini API request failed; verify the API key, model availability, and network connection.",
        ) from error
