import json

from backend.db.database import connect, initialize_database

_VEHICLES = [
    ("swift", "Maruti Suzuki Swift", "hatchback", "Petrol", "Manual", 850000, "24 km/l"),
    ("i20", "Hyundai i20", "hatchback", "Petrol", "Automatic", 1050000, "20 km/l"),
    ("altroz", "Tata Altroz", "hatchback", "Diesel", "Manual", 980000, "23 km/l"),
    ("baleno", "Maruti Baleno", "hatchback", "Petrol", "Automatic", 1000000, "22 km/l"),

    ("punch", "Tata Punch", "compact SUV", "Petrol", "Automatic", 950000, "19 km/l"),
    ("exter", "Hyundai Exter", "compact SUV", "Petrol", "Automatic", 1000000, "19 km/l"),
    ("magnite", "Nissan Magnite", "compact SUV", "Petrol", "CVT", 1100000, "18 km/l"),
    ("kiger", "Renault Kiger", "compact SUV", "Petrol", "CVT", 1150000, "18 km/l"),

    ("nexon", "Tata Nexon", "SUV", "Petrol", "Automatic", 1500000, "18 km/l"),
    ("sonet", "Kia Sonet", "SUV", "Diesel", "Automatic", 1550000, "20 km/l"),
    ("venue", "Hyundai Venue", "SUV", "Petrol", "Automatic", 1500000, "18 km/l"),
    ("xuv3xo", "Mahindra XUV 3XO", "SUV", "Petrol", "Automatic", 1600000, "18 km/l"),

    ("creta", "Hyundai Creta", "SUV", "Petrol", "Automatic", 2100000, "17 km/l"),
    ("seltos", "Kia Seltos", "SUV", "Diesel", "Automatic", 2200000, "19 km/l"),
    ("elevate", "Honda Elevate", "SUV", "Petrol", "CVT", 2000000, "16 km/l"),

    ("city", "Honda City", "sedan", "Petrol", "CVT", 1800000, "18 km/l"),
    ("verna", "Hyundai Verna", "sedan", "Petrol", "Automatic", 1950000, "19 km/l"),
    ("virtus", "Volkswagen Virtus", "sedan", "Petrol", "Automatic", 2000000, "18 km/l"),
    ("slavia", "Skoda Slavia", "sedan", "Petrol", "Automatic", 1950000, "18 km/l"),

    ("tiagoev", "Tata Tiago EV", "EV", "Electric", "Automatic", 1150000, "315 km/charge"),
    ("punchev", "Tata Punch EV", "EV", "Electric", "Automatic", 1450000, "421 km/charge"),
    ("windsor", "MG Windsor EV", "EV", "Electric", "Automatic", 1700000, "332 km/charge"),
    ("zsev", "MG ZS EV", "EV", "Electric", "Automatic", 2800000, "461 km/charge"),

    ("scorpion", "Mahindra Scorpio N", "SUV", "Diesel", "Automatic", 2900000, "18 km/l"),
    ("xuv700", "Mahindra XUV700", "SUV", "Petrol", "Automatic", 3300000, "17 km/l"),
    ("innova", "Toyota Innova Hycross", "MPV", "Hybrid", "Automatic", 3600000, "21 km/l"),
]


def _features_for_category(category: str) -> list[str]:
    base = [
        "ABS",
        "Dual Airbags",
        "Rear Parking Sensors",
        "Power Windows",
        "Touchscreen Infotainment",
        "Android Auto",
        "Apple CarPlay",
    ]

    if category == "SUV":
        base.extend(
            [
                "Cruise Control",
                "Rear Camera",
                "Hill Hold Assist",
            ]
        )

    if category == "EV":
        base.extend(
            [
                "Fast Charging Support",
                "Connected Car Technology",
                "Regenerative Braking",
            ]
        )

    if category == "MPV":
        base.extend(
            [
                "Flexible Seating",
                "Rear AC Vents",
                "Large Cargo Space",
            ]
        )

    return base


def seed_vehicles() -> None:
    initialize_database()

    with connect() as connection:

        count = connection.execute(
            "SELECT COUNT(*) FROM vehicles"
        ).fetchone()[0]

        if count:
            return

        for (
            vehicle_id,
            name,
            category,
            fuel,
            transmission,
            price,
            mileage,
        ) in _VEHICLES:

            seating = 7 if category == "MPV" else 5

            vehicle = {
                "id": vehicle_id,
                "name": name,
                "category": category,
                "fuel_type": fuel,
                "transmission": transmission,
                "ex_showroom_price": int(price * 0.88),
                "on_road_price": price,
                "seating": seating,
                "mileage": mileage,
                "variants": [
                    {
                        "name": "Base",
                        "on_road_price": price,
                        "transmission": transmission,
                    },
                    {
                        "name": "Premium",
                        "on_road_price": int(price * 1.10),
                        "transmission": transmission,
                    },
                ],
                "specifications": {
                    "engine_or_motor": "Representative specification",
                    "fuel_type": fuel,
                    "transmission": transmission,
                    "seating_capacity": seating,
                    "claimed_efficiency": mileage,
                },
                "features": _features_for_category(category),
                "description": (
                    f"{name} is a {category} vehicle with "
                    f"{fuel.lower()} powertrain and "
                    f"{transmission.lower()} transmission. "
                    f"The estimated on-road price is ₹{price:,.0f} "
                    f"with a claimed efficiency/range of {mileage}."
                ),
                "source": (
                    "Representative educational vehicle catalogue "
                    "based on publicly available market information."
                ),
            }

            connection.execute(
                """
                INSERT INTO vehicles
                (
                    id,
                    name,
                    category,
                    fuel_type,
                    transmission,
                    ex_showroom_price,
                    on_road_price,
                    seating,
                    mileage,
                    variants,
                    specifications,
                    features,
                    description,
                    source
                )
                VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    vehicle["id"],
                    vehicle["name"],
                    vehicle["category"],
                    vehicle["fuel_type"],
                    vehicle["transmission"],
                    vehicle["ex_showroom_price"],
                    vehicle["on_road_price"],
                    vehicle["seating"],
                    vehicle["mileage"],
                    json.dumps(vehicle["variants"]),
                    json.dumps(vehicle["specifications"]),
                    json.dumps(vehicle["features"]),
                    vehicle["description"],
                    vehicle["source"],
                ),
            )