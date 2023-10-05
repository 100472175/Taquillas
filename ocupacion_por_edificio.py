import json
import pandas as pd
import streamlit as st
from database.database_functions import bloques_por_planta_todas
from database.database_functions import get_status_taquilla
from database.database_functions import taquillas_por_bloque_todas
from database.database_functions import taquillas_ocupadas_por_bloque
from database.database_functions import taquillas_totales_por_bloque



def colorea_disponibilidad(value):
    status = get_status_taquilla(value)
    if status == "Libre":
        color = 'green'
    elif status in ("Ocupada", "Reservada"):
        color = 'red'
    elif status == "No Disponible":
        color = 'grey'
    else:
        color = 'black'
    return f'background-color: {color}'




def ocupacion_draw(edificio_key, planta_key):
    with open("base/tamanos.json", "r") as f:
        tamanos = json.load(f)
    bloques_en_planta = bloques_por_planta_todas(edificio_key, planta_key)

    for bloque_key in bloques_en_planta:
        taquillas_en_bloque = taquillas_por_bloque_todas(edificio_key, planta_key, bloque_key)
        taquillas = []
        for taquilla in taquillas_en_bloque:
            taquillas.append(taquilla[4])

        bloque = []
        columna_size =tamanos[edificio_key][planta_key][bloque_key][0]
        for i in range(0, len(taquillas), columna_size):
            bloque.append(taquillas[i:i + columna_size])

        df = pd.DataFrame(bloque)
        st.subheader(bloque_key + ":")
        barra_col, _, _ = st.columns(3)
        with barra_col:
            number = int((taquillas_ocupadas_por_bloque(edificio_key, planta_key, bloque_key) /
                          taquillas_totales_por_bloque(edificio_key, planta_key, bloque_key)) * 100)
            st.progress(number)
            disponibles = taquillas_totales_por_bloque(edificio_key, planta_key, bloque_key) - taquillas_ocupadas_por_bloque(edificio_key, planta_key, bloque_key)
            if disponibles == 1:
                st.write(":red[**Queda 1 taquilla disponible!!**]")
            elif disponibles == 0:
                st.write(":red[**El bloque está lleno!!**]")
            elif number >= 75:
                st.write(
                    f":red[**¡Cuidado! El bloque está casi lleno, quedan solo {disponibles} taquillas disponibles**]")

        st.dataframe(df.style.map(colorea_disponibilidad))
