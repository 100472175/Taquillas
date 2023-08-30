import streamlit as st
import json
import re

st.set_page_config(page_title="Reserva Taquillas UC3M", page_icon=":smiley:", layout="wide")

# Notas para mañana, no de puede trabajar como diccionario, así que hay probar a hacerlo con
# dataframes, como lo hace en el formulario
# Y mirarse esto: https://docs.streamlit.io/library/advanced-features/session-state


# ---- HEADER ----
st.subheader("Reserva Taquillas UC3M")
st.title("Aplicaión para reservar las taquillas de la UC3M del capus de Leganés")
st.write("Esta aplicación permite reservar las taquillas de la UC3M del campus de Leganés."
         " Para ello, se debe seleccionar la taquilla e indicar el NIA. Además, se debe"
         " introducir el nombre y el correo electrónico de la persona que reserva la taquilla."
         " Una vez se haya realizado la reserva, se enviará un correo electrónico a la persona"
         " que ha realizado la reserva con los datos de la misma (o no :)).")
st.write("Para más información ve a la [página de delegación](https://delegacion.uc3m.es/home/eps/).")
st.write("---")

with open("disponibles.json", "r") as f:
    taquillas_disponibles = json.load(f)

with open("reservadas.json", "r") as f:
    taquillas_reservadas = json.load(f)

with open("NIAS.json", "r") as f:
    NIAS = json.load(f)


NIA = 0
reservable = False
reservableNIA = False

with st.container():
    st.title("Reserva tu taquilla:")
    st.markdown("Ten en cuenta que la **P** quiere decir que es pequeña y la **G** que es grande")
    st.text("""Tratamiento de datos: \n
            Acepto el tratamiento de mis datos por la Delegación de Estudiantes únicamente
            con fines estadísticos y recopilación de información genérica, no siendo cedidos
            a terceros en ningún caso.""")
    proteccion_datos = st.checkbox("Acepto el tratamiento de mis datos")
    col_edificio, col_planta, col_bloque, col_numero, col_NIA = st.columns(5)

    # EDIFICIO SELECTOR
    with col_edificio:
        edificio = st.selectbox("Selecciona el edificio", taquillas_disponibles.keys())
        lista_plantas = list(taquillas_disponibles[edificio].keys())

    # PLANTA SELECTOR
    with col_planta:
        planta = st.selectbox("Selecciona la planta", lista_plantas)
        lista_bloques = list(taquillas_disponibles[edificio][planta].keys())

    with col_bloque:
        bloque = st.selectbox("Selecciona el bloque", lista_bloques)
        lista_numeros = taquillas_disponibles[edificio][planta][bloque]

    with col_numero:
        taquilla = st.selectbox("Selecciona el número de taquilla", lista_numeros)



    with col_NIA:
        NIA = st.text_input("Introduce tu NIA")
        if NIA != '':
            if re.match(r"100[0-9]{6}", NIA) and NIA != '':
                if str(NIA) not in NIAS:
                    st.write("NIA válido")
                    reservableNIA = True
                else:
                    st.write("NIA no válido porque ya tiene una reserva")
            else:
                st.write("NIA no válido")

    col_nombre, col_appellidos, _, _, _ = st.columns(5)
    with col_nombre:
        nombre = st.text_input("Introduce tu nombre")
    with col_appellidos:
        apellidos = st.text_input("Introduce tus apellidos")

if proteccion_datos and reservableNIA and nombre and apellidos:
    reservable = True
    st.write("Reservable")
else:
    st.write("No reservable. Por favor, rellena todos los campos (NIA + Nombre + Apellido)"
             " y acepta la protección de datos")
with st.container():
    if st.button("Reservar", disabled=not(reservable)):
        # Aquí pondriamos la llamada a la base de datos para que se reservase la taquilla y
        # las comprombaciones las haría la base de datos
        # se envia el correo electrónico ?? Se puede hacer con python y https://realpython.com/python-send-email/

        # Añadimos a las reservadas la taquilla que se ha solicitado
        estado = "No pagada"
        information = [taquilla, NIA, estado, nombre, apellidos]
        taquillas_reservadas[edificio][planta][bloque].append(information)
        with open("reservadas.json", "w") as f:
            json.dump(taquillas_reservadas, f)
        # Añadimos el NIA a la lista de NIAS, para mejorar la eficiencia y no tener que recorrer
        # el diccionario completo
        NIAS.append(NIA)
        with open("NIAS.json", "w") as f:
             json.dump(NIAS, f)

        # Eliminamos de las disponibles la taquilla que se ha solicitado
        taquillas_disponibles[edificio][planta][bloque].remove(taquilla)
        with open("disponibles.json", "w") as f:
            json.dump(taquillas_disponibles, f)
        st.success("Reserva realizada con éxito")


st.write("Esta va a ser tu taquilla: ", taquilla)
st.write("NIA: ", NIA)
st.write("Nombre: ", nombre)
st.write("Apellidos: ", apellidos)
st.write("Correo electrónico: " + NIA + "@alumnos.uc3m.es")

# ---- About Us ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.image("https://delegacion.uc3m.es/home/wp-content/uploads/2023/08/Untitled-1-768x319.jpg", width=300)
        st.write("##")
        st.write("##")
    with right_column:
        st.title("Columna derecha")


if st.button("Reset"):
    with open("base/disponibles.json", "r") as f:
        taquillas_disponibles = json.load(f)
        with open("disponibles.json", "w") as g:
            json.dump(taquillas_disponibles, g)

    with open("base/reservadas.json", "r") as f:
        taquillas_reservadas = json.load(f)
        with open("reservadas.json", "w") as g:
            json.dump(taquillas_reservadas, g)

    with open("NIAS.json", "w") as f:
        json.dump([], f)
        NIAS = []
    st.success("Reseteado con éxito")


st.write(NIAS)
if st.checkbox("Display Raw Data"):
    st.write("Esto es :blue[azul], como el cielo")
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.title("Taquillas Disponibles:")
            st.write(taquillas_disponibles)
        with right_column:
            st.title("Taquillas no Disponibles:")
            st.write(taquillas_reservadas)