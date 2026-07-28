from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import math
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from database import get_connection

class PersonUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    role: Optional[str] = None
    status: Optional[str] = None

app = FastAPI(title="Hiker Simulator API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_methods=["*"],
    allow_headers=["*"]
)



def random_location_near(person, max_distance_m=50):
    angle = random.uniform(0, 2 * math.pi)

    # Random distance somewhere inside a 50m circle
    distance_m = max_distance_m * math.sqrt(random.random())

    latitude_change = (distance_m * math.cos(angle)) / 111_320

    longitude_change = (
        distance_m * math.sin(angle)
        / (111_320 * math.cos(math.radians(person["latitude"])))
    )

    return (
        person["latitude"] + latitude_change,
        person["longitude"] + longitude_change
    )

def get_all_people_from_db():
    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM people
        ORDER BY id
    """).fetchall()

    connection.close()

    return [dict(row) for row in rows]


class PersonCreate(BaseModel):
    name: str
    age: int
    role: str = "Hiker"
    heading: float = 0
    status: str = "SAFE"


@app.get("/")
def home():
    return {"message": "Hiker Simulator API is running"}


@app.get("/people")
def get_people():
    return get_all_people_from_db()



@app.get("/people/{person_id}")
def get_person(person_id: int):
    connection = get_connection()

    row = connection.execute("""
        SELECT *
        FROM people
        WHERE id = ?
    """, (person_id,)).fetchone()

    connection.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Person not found")

    return dict(row)


@app.post("/people", status_code=201)
def create_person(new_person: PersonCreate):
    connection = get_connection()

    leader = connection.execute("""
        SELECT *
        FROM people
        WHERE role = ?
    """, ("Leader",)).fetchone()

    if leader is None:
        connection.close()
        raise HTTPException(status_code=500, detail="No leader exists")

    latitude, longitude = random_location_near(dict(leader))

    cursor = connection.execute("""
        INSERT INTO people (
            name,
            age,
            role,
            latitude,
            longitude,
            heading,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        new_person.name,
        new_person.age,
        new_person.role,
        latitude,
        longitude,
        new_person.heading,
        new_person.status
    ))

    connection.commit()

    new_id = cursor.lastrowid

    row = connection.execute("""
        SELECT *
        FROM people
        WHERE id = ?
    """, (new_id,)).fetchone()

    connection.close()

    return dict(row)

@app.delete("/people/{person_id}", status_code=204)
def delete_person(person_id: int):
    people = get_all_people_from_db()

    person_to_delete = next(
        (person for person in people if person["id"] == person_id),
        None
    )

    if person_to_delete is None:
        raise HTTPException(status_code=404, detail="Person not found")

    people.remove(person_to_delete)
    save_people(people)

@app.patch("/people/{person_id}")
def update_person(person_id: int, updates: PersonUpdate):
    people = get_all_people_from_db()

    person_to_update = next(
        (person for person in people if person["id"] == person_id),
        None
    )

    if person_to_update is None:
        raise HTTPException(status_code=404, detail="Person not found")

    update_data = updates.model_dump(exclude_unset=True)
    person_to_update.update(update_data)

    save_people(people)
    return person_to_update   