from backend.schemas import Applicant

ANNUAL_INTEREST_RATE = 0.105
FOIR_LIMIT = 0.50
MAX_LTV = 0.90


def calculate_sanction(applicant: Applicant, decision: str) -> dict:
    if decision != "Approved":
        raise ValueError("A loan amount can only be calculated for an approved applicant.")
    if applicant.requested_tenure_months > 84:
        raise ValueError("Requested tenure exceeds the policy maximum of 84 months.")

    monthly_rate = ANNUAL_INTEREST_RATE / 12
    tenure = applicant.requested_tenure_months
    available_emi = max(0.0, applicant.monthly_income * FOIR_LIMIT - applicant.existing_emis)
    payment_factor = monthly_rate / (1 - (1 + monthly_rate) ** -tenure)
    repayment_capacity = available_emi / payment_factor
    estimated_vehicle_price = applicant.requested_loan_amount + applicant.down_payment
    ltv_limit = estimated_vehicle_price * MAX_LTV
    amount = min(applicant.requested_loan_amount, repayment_capacity, ltv_limit)
    emi = amount * payment_factor
    return {
        "sanctioned_amount": round(amount, 2),
        "tenure_months": tenure,
        "annual_interest_rate": ANNUAL_INTEREST_RATE,
        "estimated_monthly_emi": round(emi, 2),
        "total_vehicle_budget": round(amount + applicant.down_payment, 2),
        "calculation": [
            f"FOIR cap: monthly obligations up to ₹{applicant.monthly_income * FOIR_LIMIT:,.2f} (50% of income).",
            f"Available EMI after existing obligations: ₹{available_emi:,.2f}/month.",
            f"Repayment-capacity principal at 10.5% annual interest for {tenure} months: ₹{repayment_capacity:,.2f}.",
            f"90% LTV cap on the estimated vehicle price of ₹{estimated_vehicle_price:,.2f}: ₹{ltv_limit:,.2f}.",
            "Sanction is the minimum of requested principal, repayment capacity, and LTV principal.",
        ],
        "policy_source": "vehicle_loan_policy.md, sections 2–3",
    }
