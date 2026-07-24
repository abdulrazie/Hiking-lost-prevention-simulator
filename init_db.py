import json
from pathlib import Path
from database import get_connection

json_file = Path(__file__).with_name("people.json")


def create_people_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            role TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            heading REAL NOT NULL,
            status TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def migrate_people_from_json():
    with open(json_file, "r") as file:
        people = json.load(file)

    connection = get_connection()

    for person in people:
        connection.execute("""
            INSERT OR REPLACE INTO people (
                id,
                name,
                age,
                role,
                latitude,
                longitude,
                heading,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            person["id"],
            person["name"],
            person.get("age"),
            person["role"],
            person["latitude"],
            person["longitude"],
            person["heading"],
            person["status"]
        ))

    connection.commit()
    connection.close()

    print(f"Moved {len(people)} people into hikers.db.")


create_people_table()
migrate_people_from_json()