from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from pathlib import Path

app = FastAPI(title="Hiker Simulator API")

data_file = Path(__file__).with_name("people.json")


def load_people():
    with open(data_file, "r") as file:
        return json.load(file)
    
def save_people(people):
    with open(data_file, "w") as file:
        json.dump(people, file, indent=2)

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


class PersonCreate(BaseModel):
    name: str
    age: int


@app.post("/people", status_code=201)
def create_person(new_person: PersonCreate):
    people = load_people()

    new_id = max((person["id"] for person in people), default=0) + 1

    person_to_add = {
        "id": new_id,
        **new_person.model_dump()
    }

    people.append(person_to_add)
    save_people(people)

    return person_to_add