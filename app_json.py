import streamlit as st
import json
import re

st.set_page_config(page_title="Reserva Taquillas UC3M", page_icon=":smiley:", layout="wide")



# ---- HEADER ----
st.subheader("Reserva Taquillas UC3M")
st.title("Aplicaión para reservar las taquillas de la UC3M del capus de Leganés")
st.write("Esta aplicación permite reservar las taquillas de la UC3M del campus de Leganés."
         " Para ello, se debe seleccionar la taquilla e indicar el NIA. Además, se debe"
         " introducir el nombre y el correo electrónico de la persona que reserva la taquilla."
         " Una vez se haya realizado la reserva, se enviará un correo electrónico a la persona"
         " que ha realizado la reserva con los datos de la misma (o no :)).")
st.write("Para más información ve a la [página de delegación](https://delegacion.uc3m.es/home/eps/).")

# Load assets
lottie_coding = "https://assets7.lottiefiles.com/packages/lf20_8yjzqz.json"

# ---- About Us ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.image("https://delegacion.uc3m.es/home/wp-content/uploads/2023/08/Untitled-1-768x319.jpg", width=300)
        st.write("##")
        st.write("##")
        st.write("##")
    with right_column:
        st.title("Columna derecha")

with open("disponibles_base.json", "r") as f:
    taquillas_disponibles = json.load(f)
    BASE_DISPONIBLE = taquillas_disponibles.copy()
with open("reservadas_base.json", "r") as f:
    taquillas_reservadas = json.load(f)
    BASE_RESERVADA = taquillas_reservadas.copy()


NIA = 0
reservable = False
with st.container():
    st.title("Reserva tu taquilla:")
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

    st.subheader("Ten en cuenta que la P quiere decir que es pequeña y la G que es grande")

    with col_NIA:
        NIA = st.text_input("Introduce tu NIA")
    if re.match(r"[0-9]{9}", NIA):
        st.write("NIA válido")
        reservable = True
    else:
        st.write("NIA no válido")

with st.container():
    if reservable:
        if st.button("Reservar"):
            st.write("Reservando...")
            # Aqui pondriamos la llamada a la base de datos para que se reservase la taquilla y
            # las comprombaciones las haría la base de datos
            # se envia el correo electrónico ?? Se puede hacer con python y https://realpython.com/python-send-email/

            # Añadimos a las reservadas la taquilla que se ha solicitado
            estado = "No pagada"
            information = [taquilla, NIA, estado]
            taquillas_reservadas[edificio][planta][bloque].append(information)
            with open("reservadas.json", "w") as f:
                json.dump(taquillas_reservadas, f)

            # Eliminamos de las disponibles la taquilla que se ha solicitado
            taquillas_disponibles[edificio][planta][bloque].remove(taquilla)
            with open("disponibles.json", "w") as f:
                json.dump(taquillas_disponibles, f)
            st.success("Reserva realizada con éxito")



st.write("Esta va a ser tu taquilla: ", taquilla)
st.write("NIA: ", NIA)


st.write("This is :blue[test]")
with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.title("Taquillas Disponibles:")
        st.write(taquillas_disponibles)
    with right_column:
        st.title("Taquillas no Disponibles:")
        st.write(taquillas_reservadas)

if st.button("Reset"):
    with open("disponibles_base.json", "w") as f:
        json.dump(BASE_DISPONIBLE, f)
    with open("reservadas_base.json", "w") as f:
        json.dump(BASE_RESERVADA, f)
    st.success("Reseteado con éxito")