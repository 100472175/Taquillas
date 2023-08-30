import streamlit as st
import json
import re

st.set_page_config(
    page_title="Reserva Taquillas UC3M",
	layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="collapsed",  # Can be "auto", "expanded", "collapsed"
	page_icon=None,  # String, anything supported by st.image, or None.
)
# Notas para mañana, no de puede trabajar como diccionario, así que hay probar a hacerlo con
# dataframes, como lo hace en el formulario
# Y mirarse esto: https://docs.streamlit.io/library/advanced-features/session-state


# ---- HEADER ----
st.image("https://delegacion.uc3m.es/home/wp-content/uploads/2023/08/Untitled-1-768x319.jpg", width=300)
st.subheader("Reserva Taquillas UC3M")
st.title("Aplicación para la reserva de taquillas del campus de leganes de la UC3M")
st.write("Esta aplicación permite reservar las taquillas del campus de leganes de la UC3M.")
st.subheader("Instrucciones:")
st.write("Seleccionar la taquilla e introducir el NIA del solicitante; además, se debe"
         " introducir el nombre y el apellido del solicitante.  \n"
         " Una realizada la reserva, se enviará un correo electrónico al solicitante"
         " con los datos asociados y el método de pago :red[**(o no :)**]).")


st.write("Para más información ve a la [página de Delegación](https://delegacion.uc3m.es/home/eps-taquillas/).")
st.write("---")

with open("disponibles.json", "r") as f:
    taquillas_disponibles = json.load(f)

with open("reservadas.json", "r") as f:
    taquillas_reservadas = json.load(f)



nia = 0
reservable = False
reservableNIA = False
images = {'Edificio 1': {'Planta 0': "1.0.jpg", 'Planta 1': "1.1.jpg"},'Edificio 2':{'Planta 2': "2.2.jpg", 'Planta 3': "2.3.jpg"},'Edificio 4':{'Planta 0': "4.0.jpg", 'Planta 1': "4.1.jpg", 'Planta 2': "4.2.jpg"},'Edificio 7':{'Planta 0': "7.0.jpg", 'Planta 1': "7.1.jpg", 'Planta 2': "7.2.jpg"}}

with st.container():
    st.title("Reserva tu taquilla:")
    st.markdown("Ten en cuenta que las letras **P** y **G** indican el tamaño **P**equeño o **G**rande respectivamente.")


    col_edificio, col_planta, col_bloque, col_numero = st.columns(4)
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
        taquilla = st.selectbox("Selecciona la taquilla", lista_numeros)


    col_nombre, col_appellidos, col_NIA, col_warning = st.columns(4)
    with col_nombre:
        nombre = st.text_input("Introduce tu nombre")
    with col_appellidos:
        apellidos = st.text_input("Introduce tus apellidos")
    with col_NIA:
        nia = st.text_input("Introduce tu NIA")
        if re.match(r"100[0-9]{6}", nia) and nia != '':
            if nia in str(taquillas_reservadas):
                reservableNIA = False
                with col_warning:
                    st.warning("NIA ya reservado")
            else:
                reservableNIA = True
        else:
            with col_warning:
                st.write("NIA no válido")

    col1, _ = st.columns(2)
    with col1:
        text = ("""Acepto el tratamiento de mis datos por la Delegación de Estudiantes únicamente
                       con fines estadísticos y recopilación de información genérica, no siendo cedidos
                       a terceros en ningún caso.""")
        proteccion_datos = st.checkbox(text)

if proteccion_datos and reservableNIA and nombre and apellidos and edificio and planta and bloque and taquilla:
    reservable = True
    st.write("Reservable")
else:
    st.write("Por favor, rellena todos los campos (NIA + Nombre + Apellido)"
             " y acepta la política de protección de datos")


with st.container():
    if st.button("Reservar", disabled=not(reservable)):
        # Aquí pondriamos la llamada a la base de datos para que se reservase la taquilla y
        # las comprombaciones las haría la base de datos
        # se envia el correo electrónico ?? Se puede hacer con python y https://realpython.com/python-send-email/

        # Añadimos a las reservadas la taquilla que se ha solicitado
        estado = "Reservada"
        information = [taquilla, nia, estado, nombre, apellidos]
        taquillas_reservadas[edificio][planta][bloque].append(information)
        with open("reservadas.json", "w") as f:
            json.dump(taquillas_reservadas, f)


        # Eliminamos de las disponibles la taquilla que se ha solicitado
        taquillas_disponibles[edificio][planta][bloque].remove(taquilla)
        with open("disponibles.json", "w") as f:
            json.dump(taquillas_disponibles, f)

        # Mostramos la información de la reserva
        content = f"Reserva realizada con éxito :partying_face:  \n" \
                    f"Taquilla: {taquilla}  \n" \
                    f"NIA: {nia}  \n" \
                    f"Nombre: {nombre}  \n" \
                    f"Apellidos: {apellidos}  \n"


        st.success(content)
        st.balloons()

    if st.checkbox("Mostrar guía de bloques por planta", key="guia", value=True):
        st.image("images/"+images[edificio][planta])
st.write("---")
st.write("---")
st.write("---")
st.write("Esto no aparecería en la versión final, ha sido solo para testeo")


if st.button("Reset"):
    with open("base/disponibles.json", "r") as f:
        taquillas_disponibles = json.load(f)
        with open("disponibles.json", "w") as g:
            json.dump(taquillas_disponibles, g)

    with open("base/reservadas.json", "r") as f:
        taquillas_reservadas = json.load(f)
        with open("reservadas.json", "w") as g:
            json.dump(taquillas_reservadas, g)

    st.success("Reseteado con éxito")


if st.checkbox("Display Raw Data"):
    st.write("Esto es :blue[azul], como el cielo")
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.title("Taquillas Disponibles:")
            st.json(taquillas_disponibles)
        with right_column:
            st.title("Taquillas no Disponibles:")
            st.json(taquillas_reservadas)
