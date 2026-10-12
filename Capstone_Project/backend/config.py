import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")
DATABASE_PATH = Path(os.getenv("DATABASE_PATH", PROJECT_ROOT / "data" / "advisor.sqlite3"))
MODEL_PATH = Path(os.getenv("MODEL_PATH", PROJECT_ROOT / "models" / "eligibility.joblib"))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_EMBEDDING_MODEL = "gemini-embedding-001"
GEMINI_GENERATION_MODEL = "gemini-3.6-flash"
POLICY_DIR = PROJECT_ROOT / "data" / "documents" / "policy"
VEHICLE_DOC_DIR = PROJECT_ROOT / "data" / "documents" / "vehicles"
