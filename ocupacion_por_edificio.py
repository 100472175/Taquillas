import json
import pandas as pd
import streamlit as st
from database.database_functions import bloques_por_planta_todas
from database.database_functions import get_status_taquilla
from database.database_functions import taquillas_por_bloque_todas
from database.database_functions import taquillas_ocupadas_por_bloque
from database.database_functions import taquillas_totales_por_bloque


def colorea_disponibilidad(value):
    """
    Función que colorea las celdas de la tabla de ocupación de taquillas según su disponibilidad.
    :param value: Valor de la celda.
    :return: Color de la celda.
    """
    # Obtiene el estado de la taquilla
    global_temp = taquillas_en_bloque
    status = next((taquilla[5] for taquilla in global_temp if taquilla[4] == value), None)
    color = {
        'Libre': 'green',
        'Ocupada': 'red',
        'Reservada': 'red',
        'No Disponible': 'grey',
    }.get(status, 'black')
    return f'background-color: {color}'


def ocupacion_draw(edificio_key, planta_key):
    """
    Función principal que dibuja todas las tablas de ocupación de taquillas de cada bloque de una planta.
    :param edificio_key: Edificio seleccionado.
    :param planta_key: Planta seleccionada.
    :return: No "devuelve" nada, dibuja las tablas.
    """
    # Carga de datos
    # El formato de los datos es el siguiente:
    # size={
    #   "edificio": {
    #       "planta": {
    #           "bloque": [columnas, filas]
    #       }
    #   }
    # }
    with open("base/tamanos.json", "r") as f:
        size = json.load(f)
        f.close()

    # Obtiene las taquillas de todos los bloques de la planta seleccionada
    bloques_en_planta = bloques_por_planta_todas(edificio_key, planta_key)

    # Itera por todos los bloques que hay en la planta
    for bloque_key in bloques_en_planta:
        # Obtiene las taquillas de cada bloque
        global taquillas_en_bloque
        taquillas_en_bloque = taquillas_por_bloque_todas(edificio_key, planta_key, bloque_key)

        # Crea una lista con los números de las taquillas
        taquillas = []
        for taquilla in taquillas_en_bloque:
            taquillas.append(taquilla[4])

        # Crea una lista de listas con las taquillas de cada bloque, según su tamaño
        bloque = []
        columna_size = size[edificio_key][planta_key][bloque_key][0]
        # Coge las taquillas de n en n siendo n el número de columnas
        for i in range(0, len(taquillas), columna_size):
            bloque.append(taquillas[i:i + columna_size])

        # Crea un dataframe con las taquillas de cada bloque
        df = pd.DataFrame(bloque)

        # Crea una barra de progreso con el porcentaje de taquillas ocupadas, que ocupe un 33% de la pantalla
        barra_col, _, _ = st.columns(3)
        with barra_col:
            # Calcula el porcentaje de taquillas ocupadas, obteniendo el número de taquillas ocupadas y el número
            # total de taquillas del bloque
            ocupadas_por_bloque = taquillas_ocupadas_por_bloque(edificio_key, planta_key, bloque_key)
            totales_por_bloque = taquillas_totales_por_bloque(edificio_key, planta_key, bloque_key)
            # Calculamos el porcentaje de taquillas ocupadas en ese bloque y se muestra en una barra de progreso
            number = int(ocupadas_por_bloque / totales_por_bloque)
            # Se muestra el porcentaje de taquillas ocupadas en el bloque por 100
            st.progress(number * 100)
            # Se muestra el número de taquillas disponibles y se muestra un mensaje de alerta si quedan pocas
            disponibles = totales_por_bloque - ocupadas_por_bloque
            if disponibles == 1:
                st.write(":red[**Queda 1 taquilla disponible!!**]")
            elif disponibles == 0:
                st.write(":red[**El bloque está lleno!!**]")
            elif number >= 75:
                st.write(
                    f":red[**¡Cuidado! El bloque está casi lleno, quedan solo {disponibles} taquillas disponibles**]")

        # Añade un título a cada tabla y muestra la tabla, coloreando las celdas según su disponibilidad
        st.subheader(bloque_key + ":")
        st.dataframe(df.style.map(colorea_disponibilidad))
