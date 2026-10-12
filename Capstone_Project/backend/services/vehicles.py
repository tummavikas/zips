from backend.db.database import load_vehicle_records


def affordable_vehicles(budget: float, category: str | None = None, fuel_type: str | None = None) -> list[dict]:
    result = []
    for vehicle in load_vehicle_records():
        if vehicle["on_road_price"] > budget:
            continue
        if category and category.casefold() not in vehicle["category"].casefold():
            continue
        if fuel_type and fuel_type.casefold() != vehicle["fuel_type"].casefold():
            continue
        vehicle["estimated_emi"] = round(vehicle["on_road_price"] * 0.105 / 12 / (1 - (1 + 0.105 / 12) ** -60), 2)
        result.append(vehicle)
    return result


def get_vehicle(vehicle_id: str) -> dict | None:
    return next((v for v in load_vehicle_records() if v["id"] == vehicle_id), None)
