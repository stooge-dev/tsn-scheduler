import json

def write_offsets_to_file(filename: str, offsets):
    with open(filename, "w") as file:
        json.dump(offsets, file)

def read_offsets_from_file(filename: str):
    with open(filename) as file:
        return json.loads(file)