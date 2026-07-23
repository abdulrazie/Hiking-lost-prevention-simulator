from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import random
import math
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

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

data_file = Path(__file__).with_name("people.json")


def load_people():
    with open(data_file, "r") as file:
        return json.load(file)


def save_people(people):
    with open(data_file, "w") as file:
        json.dump(people, file, indent=2)


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
    return load_people()


@app.get("/people/{person_id}")
def get_person(person_id: int):
    people = load_people()

    for person in people:
        if person["id"] == person_id:
            return person

    raise HTTPException(status_code=404, detail="Person not found")


@app.post("/people", status_code=201)
def create_person(new_person: PersonCreate):
    people = load_people()

    leader = next(
        (person for person in people if person["role"] == "Leader"),
        None
    )

    if leader is None:
        raise HTTPException(status_code=500, detail="No leader exists")

    latitude, longitude = random_location_near(leader)

    new_id = max((person["id"] for person in people), default=0) + 1

    person_to_add = {
        "id": new_id,
        **new_person.model_dump(),
        "latitude": latitude,
        "longitude": longitude
    }

    people.append(person_to_add)
    save_people(people)

    return person_to_add

@app.delete("/people/{person_id}", status_code=204)
def delete_person(person_id: int):
    people = load_people()

    person_to_delete = next(
        (person for person in people if person["id"] == person_id),
        None
    )

    if person_to_delete is None:
        raise HTTPException(status_code=404, detail="Person not found")

    people.remove(person_to_delete)
    save_people(people)