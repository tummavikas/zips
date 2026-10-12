import json
import re
from pathlib import Path

from backend.config import POLICY_DIR, VEHICLE_DOC_DIR
from backend.db.database import connect, initialize_database, load_vehicle_records
from backend.db.seed import seed_vehicles
from backend.gemini import embed_text


def _chunks(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    sections = re.split(r"(?m)(?=^#{1,3} )", text)
    output = []
    for section in sections:
        section = section.strip()
        if not section:
            continue
        title_match = re.match(r"^#{1,3}\s+(.+)", section)
        title = title_match.group(1).strip() if title_match else "Overview"
        lines = section.splitlines()
        body = "\n".join(lines[1:]).strip() if title_match else section
        for start in range(0, max(1, len(body)), 900):
            text_chunk = body[start : start + 900].strip()
            if text_chunk:
                output.append((title, text_chunk))
    return output


def ingest() -> None:
    initialize_database()
    seed_vehicles()
    sources: list[tuple[str, str, str]] = []
    for path in list(Path(POLICY_DIR).glob("*.md")) + list(Path(VEHICLE_DOC_DIR).glob("*.md")):
        sources.extend((path.name, section, content) for section, content in _chunks(path))
    for vehicle in load_vehicle_records():
        vehicle_text = (
            f"{vehicle['name']} details. Category: {vehicle['category']}. "
            f"Fuel: {vehicle['fuel_type']}. Price: ₹{vehicle['on_road_price']}. "
            f"Mileage: {vehicle['mileage']}. Features: {', '.join(vehicle['features'])}. "
            f"Description: {vehicle['description']} Source: {vehicle['source']}"
        )
        sources.append(("synthetic_vehicle_catalogue", vehicle["name"], vehicle_text))

    with connect() as connection:
        connection.execute("DELETE FROM rag_chunks")
        for source, section, content in sources:
            embedding = embed_text(content)
            connection.execute(
                "INSERT INTO rag_chunks (source, section, content, embedding) VALUES (?, ?, ?, ?)",
                (source, section, content, json.dumps(embedding)),
            )
    print(f"Indexed {len(sources)} passages using Gemini embeddings.")


if __name__ == "__main__":
    ingest()
