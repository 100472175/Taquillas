import json
import pick


with open("disponibles.json", "r") as f:
    taquillas_disponibles = json.load(f)


def genera_reservadas_vacias():
    for edificio_key, edificio in taquillas_disponibles.items():
        for planta_key, planta in edificio.items():
            for bloque_key, bloque in planta.items():
                taquillas_disponibles[edificio_key][planta_key][bloque_key] = []
    with open("reservadas.json", "w") as f:
        json.dump(taquillas_disponibles, f, indent=4)
    print("reservadas.json generado")


def genera_cantidad_taquillas():
    for edificio_key, edificio in taquillas_disponibles.items():
        for planta_key, planta in edificio.items():
            for bloque_key, bloque in planta.items():
                taquillas_disponibles[edificio_key][planta_key][bloque_key] = len(bloque)
    with open("cantidad.json", "w") as f:
        json.dump(taquillas_disponibles, f, indent=4)
    print("cantidad.json generado")

options = ["genera_reservas_vacias", "genera_cantidad_taquillas"]
option, index = pick.pick(options, "¿Qué quieres haces?", indicator='=>', default_index=0)
exec(option + "()")