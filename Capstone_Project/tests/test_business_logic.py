from backend.schemas import Applicant
from backend.services.loan_amount import calculate_sanction
from backend.services.vehicles import affordable_vehicles
from backend.db.seed import seed_vehicles
from backend.db.database import initialize_database


def applicant(**updates):
    values = {
        "monthly_income": 85_000, "credit_score": 745, "employment_years": 6,
        "employment_type": "salaried", "existing_emis": 12_000,
        "requested_tenure_months": 60, "requested_loan_amount": 800_000,
        "down_payment": 150_000, "age": 30,
    }
    values.update(updates)
    return Applicant(**values)


def test_sanction_respects_request_capacity_and_ltv():
    result = calculate_sanction(applicant(), "Approved")
    assert result["sanctioned_amount"] <= 800_000
    assert result["estimated_monthly_emi"] + 12_000 <= 85_000 * 0.50
    assert result["total_vehicle_budget"] == result["sanctioned_amount"] + 150_000


def test_rejected_applicant_cannot_get_amount():
    try:
        calculate_sanction(applicant(), "Rejected")
    except ValueError as error:
        assert "only be calculated" in str(error)
    else:
        raise AssertionError("Rejected applicant should not receive a sanction.")


def test_catalogue_has_at_least_25_affordable_records():
    initialize_database()
    seed_vehicles()
    vehicles = affordable_vehicles(10_000_000)
    assert len(vehicles) >= 25
    assert all(vehicle["on_road_price"] <= 10_000_000 for vehicle in vehicles)
