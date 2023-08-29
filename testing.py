import json

with open("disponibles_base.json", "r") as f:
    taquillas_disponibles = json.load(f)
print(type(taquillas_disponibles))
print(taquillas_disponibles.keys())

