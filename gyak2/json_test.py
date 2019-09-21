import json

data = {"name": "Jani", "age": 69}

with open("asd.json", "w") as f:
    json.dump(data, f)
