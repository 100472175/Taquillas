import json
import pandas as pd

reservadas_path = "reservadas.json"
def generate_dataframe() -> pd.DataFrame:
    with open(reservadas_path, "r") as f:
        taquillas_reservadas = json.load(f)

    df = pd.DataFrame(
        columns=["Edificio", "Planta", "Bloque", "Taquilla", "NIA", "Estado", "Nombre", "Apellidos", "Código"])
    for edificio_key, edificio in taquillas_reservadas.items():
        for planta_key, planta in taquillas_reservadas[edificio_key].items():
            for bloque_key, bloque in taquillas_reservadas[edificio_key][planta_key].items():
                for reserva in taquillas_reservadas[edificio_key][planta_key][bloque_key]:
                    print(reserva)
                    taquilla = reserva[0]
                    nia = reserva[1]
                    estado = reserva[2]
                    nombre = reserva[3]
                    apellidos = reserva[4]
                    codigo = reserva[5]
                    new_row = {"Edificio": edificio_key, "Planta": planta_key, "Bloque": bloque_key,
                               "Taquilla": taquilla,
                               "NIA": nia, "Estado": estado, "Nombre": nombre, "Apellidos": apellidos, "Código": codigo}
                    df.loc[len(df)] = new_row
    return df
