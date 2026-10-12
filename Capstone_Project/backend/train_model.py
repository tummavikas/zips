from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from backend.config import MODEL_PATH, PROJECT_ROOT
from backend.services.eligibility import FEATURES


def make_synthetic_dataset(rows: int = 5000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    income = rng.uniform(20_000, 250_000, rows)
    score = rng.integers(500, 851, rows)
    experience = rng.uniform(0, 25, rows)
    existing = rng.uniform(0, income * 0.55)
    tenure = rng.choice([12, 24, 36, 48, 60, 72, 84], rows)
    requested = rng.uniform(200_000, 4_000_000, rows)
    down_payment = rng.uniform(50_000, 1_000_000, rows)
    age = rng.integers(21, 61, rows)
    rate = 0.105 / 12
    emi = requested * rate / (1 - (1 + rate) ** (-tenure))
    emi_to_income = (emi + existing) / income
    noise = rng.normal(0, 0.45, rows)
    latent = (
        (score - 650) / 70
        + np.log1p(income / 25_000) * 0.45
        + np.minimum(experience, 10) * 0.06
        - emi_to_income * 2.0
        - np.maximum(0, requested - down_payment * 9) / 2_000_000
        + noise
    )
    approved = (
        (score >= 650)
        & (income >= 25_000)
        & (experience >= 1)
        & (emi_to_income <= 0.5)
        & (tenure <= 84)
        & (latent > 0.75)
    ).astype(int)
    return pd.DataFrame(
        {
            "monthly_income": income,
            "credit_score": score,
            "employment_years": experience,
            "existing_emis": existing,
            "requested_tenure_months": tenure,
            "requested_loan_amount": requested,
            "down_payment": down_payment,
            "age": age,
            "emi_to_income": emi_to_income,
            "approved": approved,
        }
    )


def train() -> dict:
    data = make_synthetic_dataset()
    raw_path = PROJECT_ROOT / "data" / "raw" / "synthetic_loan_applications.csv"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(raw_path, index=False)
    X, y = data[FEATURES], data["approved"]
    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    candidates = {
        "logistic_regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, class_weight="balanced")),
        "random_forest": RandomForestClassifier(
            n_estimators=250, max_depth=12, min_samples_leaf=3,
            class_weight="balanced", random_state=42, n_jobs=-1,
        ),
    }
    reports = {}
    for name, model in candidates.items():
        model.fit(x_train, y_train)
        probabilities = model.predict_proba(x_test)[:, 1]
        reports[name] = {
            "accuracy": accuracy_score(y_test, probabilities >= 0.5),
            "roc_auc": roc_auc_score(y_test, probabilities),
            "classification_report": classification_report(
                y_test, probabilities >= 0.5, output_dict=True, zero_division=0
            ),
        }
    chosen_name = max(reports, key=lambda name: reports[name]["roc_auc"])
    chosen = candidates[chosen_name]
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(chosen, MODEL_PATH)
    report_path = PROJECT_ROOT / "models" / "evaluation.json"
    report_path.write_text(
        __import__("json").dumps({"selected_model": chosen_name, "models": reports}, indent=2),
        encoding="utf-8",
    )
    print(f"Saved {chosen_name} to {MODEL_PATH}; data: {raw_path}")
    print(f"Model comparison written to {report_path}")
    return reports


if __name__ == "__main__":
    train()
