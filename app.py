import streamlit as st

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



lista_edificios = ["1", "2", "4", "7"]
edificio = None
planta = None
bloque = None
numero = None
NIA = None

with st.container():
    st.title("Reserva tu taquilla:")
    col_edificio, col_planta, col_bloque, col_numero, col_NIA = st.columns(5)

    # EDIFICIO SELECTOR
    with col_edificio:
        edificio = st.selectbox("Selecciona el edificio", lista_edificios)
    if edificio == "1":
        lista_plantas = ["0", "1"]
    elif edificio == "2":
        lista_plantas = ["2", "3"]
    elif edificio in ["4", "7"]:
        lista_plantas = ["0", "1", "2"]

    # PLANTA SELECTOR
    with col_planta:
        planta = st.selectbox("Selecciona la planta", lista_plantas)
    if edificio == "1":
        if planta == "0":
            lista_bloques = {"1": "E", "2": "F", "3": "F", "4": "G"}
        elif planta == "1":
            lista_bloques = {"1": "F", "2": "G"}
    elif edificio == "2":
        if planta == "2":
            lista_bloques = {"1": "C", "2": "C"}
        elif planta == "3":
            lista_bloques = {"1": "A", "2": "A", "3": "B", "4": "B", "5": "C", "6": "C", "7": "C"}
    elif edificio == "4":
        if planta == "0":
            lista_bloques = {"1": "E", "2": "E", "3": "E", "4": "E", "5": "E", "6": "E"}
        elif planta == "1":
            lista_bloques = {"1": "E", "2": "E", "3": "E", "4": "E", "5": "E", "6": "E", "7": "E"}
        elif planta == "2":
            lista_bloques = {"1": "E", "2": "E", "3": "E", "4": "E", "5": "E"}
    elif edificio == "7":
        if planta == "0":
            lista_bloques = {"1": "J", "2": "J"}
        elif planta in ["1", "2"]:
            lista_bloques = {"1": "J"}

    with col_bloque:
        bloque = st.selectbox("Selecciona el bloque", lista_bloques)

    #Taquillas del edificio 1 planta 0
    if edificio == "1":
        if planta == "0":
            if bloque == "1":
                lista_numeros = [str(i+1) for i in range(0, 24)]
            elif bloque == "2":
                lista_numeros = [str(i+1) for i in range(25, 48)]
            elif bloque == "3":
                lista_numeros = [str(i+1) for i in range(48, 72)]
            elif bloque == "4":
                lista_numeros = [str(i+1) for i in range(73, 104)]

        elif planta == "1":
            if bloque == "1":
                lista_numeros = [str(i+1) for i in range(0, 12)]
            elif bloque == "2":
                lista_numeros = [str(i+1) for i in range(13, 24)]
            else:
                lista_numeros = ["-1"]
        else:
            lista_numeros = ["-1"]
    else:
        lista_numeros = ["-1"]


    st.write(lista_numeros)
    print(lista_numeros)

    with col_numero:
        numero = st.selectbox("Selecciona el número de taquilla", lista_numeros)

    with col_NIA:
        NIA = st.text_input("Introduce tu NIA")

    if st.button("Reservar"):
        st.write("Reservando...")
        st.balloons()
        # Aqui pondriamos la llamada a la base de datos para que se reservase la taquilla y
        # las comprombaciones las haría la base de datos
        # se envia el correo electrónico ?? Se puede hacer con python y https://realpython.com/python-send-email/


taquilla_nombre_temporal = ""
if edificio is not None:
    taquilla_nombre_temporal += edificio
    taquilla_nombre_temporal += "."
if planta is not None:
    taquilla_nombre_temporal += planta
    taquilla_nombre_temporal += "."
if bloque is not None:
    taquilla_nombre_temporal += lista_bloques[bloque]
if numero is not None:
    num_temp = f"{int(numero):03d}"
    taquilla_nombre_temporal += num_temp
st.write("Esta va a ser tu taquilla: ", taquilla_nombre_temporal)
st.write("NIA: ",NIA)


# Form
with st.container():
    st.write("---")
    st.write("Reserva la taquilla rellenando el formulario:")
    st.write("##")
    edificio = st.selectbox("Selecciona la taquilla", ["A1", "A2", "A3", "A4", "A5", "A6", "A7"])
    st.write(edificio)