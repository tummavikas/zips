import time

import requests

from backend.config import GEMINI_API_KEY, GEMINI_EMBEDDING_MODEL, GEMINI_GENERATION_MODEL

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"


def _require_key() -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured. Add it to your .env file.")
    return GEMINI_API_KEY


def _post(url: str, payload: dict, timeout: int) -> requests.Response:
    response = None
    for attempt in range(3):
        response = requests.post(
            url,
            headers={"x-goog-api-key": _require_key()},
            json=payload,
            timeout=timeout,
        )
        if response.status_code not in {429, 500, 502, 503, 504} or attempt == 2:
            break
        time.sleep(2**attempt)
    response.raise_for_status()
    return response


def embed_text(text: str) -> list[float]:
    response = _post(
        f"{BASE_URL}/{GEMINI_EMBEDDING_MODEL}:embedContent",
        {"model": f"models/{GEMINI_EMBEDDING_MODEL}", "content": {"parts": [{"text": text}]}},
        60,
    )
    return response.json()["embedding"]["values"]


def generate_grounded_answer(question: str, context: str) -> str:
    prompt = (
        "Answer the user's question using only the source passages below. "
        "If they do not contain the answer, say you do not have enough information. "
        "Do not invent financial or vehicle facts.\n\n"
        f"Source passages:\n{context}\n\nQuestion: {question}"
    )
    response = _post(
        f"{BASE_URL}/{GEMINI_GENERATION_MODEL}:generateContent",
        {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.1},
        },
        90,
    )
    candidates = response.json().get("candidates", [])
    if not candidates:
        raise RuntimeError("Gemini returned no answer candidates.")
    return "".join(part.get("text", "") for part in candidates[0]["content"].get("parts", []))
