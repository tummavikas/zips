import json

import numpy as np

from backend.db.database import connect
from backend.gemini import embed_text, generate_grounded_answer


def retrieve(question: str, limit: int = 5) -> list[dict]:
    query_vector = np.asarray(embed_text(question), dtype=float)
    with connect() as connection:
        chunks = connection.execute(
            "SELECT source, section, content, embedding FROM rag_chunks"
        ).fetchall()
    scored = []
    for chunk in chunks:
        vector = np.asarray(json.loads(chunk["embedding"]), dtype=float)
        denominator = np.linalg.norm(query_vector) * np.linalg.norm(vector)
        score = float(np.dot(query_vector, vector) / denominator) if denominator else 0.0
        scored.append(
            {
                "source": chunk["source"],
                "section": chunk["section"],
                "content": chunk["content"],
                "score": score,
            }
        )
    return sorted(scored, key=lambda item: item["score"], reverse=True)[:limit]


def explain(question: str) -> dict:
    results = retrieve(question)
    if not results:
        raise RuntimeError("No indexed source passages found. Run `python -m backend.rag.ingest` first.")
    context = "\n\n".join(
        f"[{item['source']} | {item['section']}]\n{item['content']}" for item in results
    )
    answer = generate_grounded_answer(question, context)
    return {
        "answer": answer,
        "sources": [
            {"document": item["source"], "section": item["section"], "score": round(item["score"], 4)}
            for item in results
        ],
    }
