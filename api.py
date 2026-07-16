from fastapi import FastAPI, HTTPException
import json
from pathlib import Path

app = FastAPI(title="Hiker Simulator API")

data_file = Path(__file__).with_name("people.json")


def load_people():
    with open(data_file, "r") as file:
        return json.load(file)


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