import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def load_json(filename):
    path = os.path.join(DATA_DIR, filename)

    with open(path, "r") as file:
        return json.load(file)


faculty_data = load_json("faculty.json")
subjects = load_json("subjects.json")
time_slots = load_json("slots.json")
blocks = load_json("blocks.json")
days = load_json("days.json")