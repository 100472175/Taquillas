import json

with open("disponibles.json", "r") as f:
    taquillas_disponibles = json.load(f)

for edificio_key, edificio in taquillas_disponibles.items():
    for planta_key, planta in edificio.items():
        for bloque_key, bloque in planta.items():
            taquillas_disponibles[edificio_key][planta_key][bloque_key] = []
with open("reservadas.json", "w") as f:
    json.dump(taquillas_disponibles, f)
