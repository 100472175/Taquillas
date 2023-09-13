import pandas as pd
import streamlit as st
import json
import numpy as np


def colorea_disponibilidad(value, data):
    with open("disponibles.json", "r") as f:
        disponibles = json.load(f)
    if value in disponibles[data[0]][data[1]][data[2]]:
        return "background-color: green"
    return "background-color: red"


def ocupacion_draw(edificio_key, planta_key=None):
    with open("base/disponibles.json", "r") as f:
        disponibles_total = json.load(f)
    with open("base/tamanos.json", "r") as f:
        tamanos = json.load(f)


    edificio = disponibles_total[edificio_key]
    planta = edificio[planta_key]
    for bloque_key, bloque_select in planta.items():
        bloque = []
        for i in range(tamanos[edificio_key][planta_key][bloque_key][1]):
            fila = []
            for j in range(tamanos[edificio_key][planta_key][bloque_key][0]):
                fila.append(disponibles_total[edificio_key][planta_key][bloque_key][
                                i * tamanos[edificio_key][planta_key][bloque_key][0] + j])
            bloque.append(fila)
        df = pd.DataFrame(bloque)
        st.subheader(bloque_key + ":")
        with open("reservadas.json", "r") as f:
            reservadas = json.load(f)
        bloque_reserved = reservadas[edificio_key][planta_key][bloque_key]
        barra_col, _, _ = st.columns(3)
        with barra_col:
            number = int((len(bloque_reserved) / len(bloque_select)) * 100)
            st.progress(number)
            disponibles = len(bloque_select) - len(bloque_reserved)
            if disponibles == 1:
                st.write(":red[**Queda 1 taquilla disponible!!**]")
            elif disponibles == 0:
                st.write(":red[**El bloque está lleno!!**]")
            elif number >= 75:
                st.write(f":red[**¡Cuidado! El bloque está casi lleno, quedan solo {disponibles} taquillas disponibles**]")

        st.dataframe(df.style.applymap(colorea_disponibilidad,
                                       data=[edificio_key, planta_key, bloque_key]),
                    hide_index=True)
