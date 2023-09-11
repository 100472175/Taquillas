import pandas as pd
import streamlit as st
import json
import numpy as np

with open("base/disponibles.json", "r") as f:
    disponibles_total = json.load(f)

with open("base/tamanos.json", "r") as f:
    tamanos = json.load(f)

with open("disponibles.json", "r") as f:
    disponibles = json.load(f)


def colorea_disponibilidad(value, data):
    if value in disponibles[data[0]][data[1]][data[2]]:
        return "background-color: green"
    return "background-color: red"


def ocupación_draw(edificio_key, planta_key=None):
    edificio = disponibles_total[edificio_key]
    planta = edificio[planta_key]
    for bloque_key, bloque in planta.items():
        bloque = []
        for i in range(tamanos[edificio_key][planta_key][bloque_key][1]):
            fila = []
            for j in range(tamanos[edificio_key][planta_key][bloque_key][0]):
                fila.append(disponibles_total[edificio_key][planta_key][bloque_key][
                                i * tamanos[edificio_key][planta_key][bloque_key][0] + j])
            bloque.append(fila)
        df = pd.DataFrame(bloque)
        st.subheader(bloque_key + ":")
        st.dataframe(df.style.applymap(colorea_disponibilidad,
                                       data=[edificio_key, planta_key, bloque_key]),
                    hide_index=True)
