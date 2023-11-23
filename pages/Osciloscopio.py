import streamlit as st
from datetime import datetime
from database.bd_osciloscopio_generate import *
import re


# Esta va a ser la página principal para reservar un osciloscopio en la delegación
# Tenemos un horario concreto, y tendremos un desplegable con las horas que están disponibles
# La hora se reserva para un día concreto, y se puede reservar con uns semana de antelación
# Se puede reservar un máximo de 1 horas por día y eso se identifica por NIA
# Se puede cancelar la reserva con un día de antelación
# Se puede consultar las reservas que se tienen para un día concreto

def num_to_day(num):
    conv = {1: "lunes", 2: "martes", 3: "miercoles", 4: "jueves", 5: "viernes"}
    return conv[num]


def day_to_num(day):
    conv = {"lunes": 1, "martes": 2, "miercoles": 3, "jueves": 4, "viernes": 5}
    return conv[day]


def app(osciloscopio=2):
    st.title("Reserva de osciloscopios")
    today = num_to_day(datetime.isoweekday(datetime.now()))
    lista_huecos = []
    id_reserva = -1

    oscilo_col, dia_col, hora_col, nia_col = st.columns([2, 2, 2, 3])
    with oscilo_col:
        lista_temp = []
        for i in range(osciloscopio):
            lista_temp.append(str(i + 1))
        oscilo = st.selectbox("Osciloscopio", lista_temp, index=0)
        st.write("Has seleccionado el osciloscopio: ", oscilo)
        oscilo = int(oscilo)
        select_today_index = get_5_free_spots_today(oscilo)

    with dia_col:
        index_letter = st.selectbox("Día de la semana", ["lunes", "martes", "miercoles", "jueves", "viernes"],
                                    index=day_to_num(today) - 1)
        st.write("Has seleccionado el día: ", index_letter)
        # Get the index of the list selected before and get the day of the week
        dia = day_to_num(index_letter)

    with hora_col:
        lista = get_free_sports_specific_day(dia, oscilo)
        # Do some list comprehension to add :00 to the end of the hour
        lista = [str(i[0]) + ":00" for i in lista]
        hora_larga = st.selectbox("Hora", lista, index=0)
        st.write("Has seleccionado la hora: ", hora_larga)
        hora = hora_larga[:-3]

    with nia_col:
        todo_ok = True
        nias = st.text_input("NIA", value="")
        if not nias:
            todo_ok = False
        # If there is a character different from numbers, spaces or comas, we output an error, with st.rror
        if re.search("[^0-9, ]", nias):
            st.error("El NIA solo puede contener números, comas y espacios")
            todo_ok = False
        if nias:
            # The NIA is a number like 100XXXXXX, and they can be separated by comas and or spaces
            nias = re.split(",| ", nias)
            # We remove the empty strings
            nias = [i for i in nias if i]
            if len(nias) > 1:
                # We remove the duplicates
                nias = list(set(nias))
                # We check if the NIA is valid with regex
                for nia in nias:
                    if not re.search("100[0-9]{6}", nia):
                        st.error("El NIA " + nia + " no es válido")
                        todo_ok = False

    for i in select_today_index:
        if i[3] == int(hora):
            id_reserva = i[0]
            break
    if todo_ok and id_reserva != -1:
        st.warning(f"Se va a reservar el osciloscopio {oscilo} para el {index_letter} a las {hora}:00")
        if st.button("Reservar"):
            try:
                check_nia_validity(nias, id_reserva)
                haz_reserva(id_reserva, nias)
                st.success("Reserva realizada con éxito")
                st.balloons()
            except ValueError as error:
                st.error(error)
    st.write("Huecos disponibles para los próximos días: ", len(select_today_index))
    st.dataframe(select_today_index)


app(osciloscopio=NUM_OSCILOS)
