import math
import random
import time
import json

WARNING_DISTANCE_M = 50


def create_person(person_id, name, role, latitude, longitude):
    return {
        "id": person_id,
        "name": name,
        "role": role,
        "latitude": latitude,
        "longitude": longitude,
        "heading": random.uniform(0, 360),
        "status": "SAFE",
    }


with open("people.json", "r") as file:
    people = json.load(file)


def get_distance_meters(lat1, lon1, lat2, lon2):
    earth_radius_m = 6_371_000

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2)
        * math.sin(delta_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return earth_radius_m * c


def move(person, dt=2.0, speed_mps=1.3):
    person["heading"] = (person["heading"] + random.uniform(-15, 15)) % 360
    heading_rad = math.radians(person["heading"])

    distance_m = speed_mps * dt

    person["latitude"] += (distance_m * math.cos(heading_rad)) / 111_320
    person["longitude"] += (
        distance_m * math.sin(heading_rad)
        / (111_320 * math.cos(math.radians(person["latitude"])))
    )


step_count = 0

try:
    print("Simulating hiking trip — press Ctrl+C to stop.")

    while True:
        step_count += 1

        for person in people:
            move(person)

        leader = next(person for person in people if person["role"] == "Leader")

        print(f"\n========== Step {step_count} ==========")

        for person in people:
            print(f"{person['role']}: {person['name']}")
            print(f"Location: ({person['latitude']:.6f}, {person['longitude']:.6f})")

            if person["role"] == "Hiker":
                distance = get_distance_meters(
                    leader["latitude"],
                    leader["longitude"],
                    person["latitude"],
                    person["longitude"],
                )

                person["status"] = (
                    "WARNING" if distance > WARNING_DISTANCE_M else "SAFE"
                )

                print(f"Distance from leader: {distance:.2f}m")
                print(f"Status: {person['status']}")

            print("-" * 35)

        time.sleep(2)

except KeyboardInterrupt:
    print("\nSimulation stopped by user.")
    with open("people.json", "w") as file:
        json.dump(people, file, indent=2)

    print("Latest locations saved to people.json.")