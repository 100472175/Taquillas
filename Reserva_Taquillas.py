import streamlit as st
import json
import random
import re
from email_send import send_email_verification
from ocupacion_por_edificio import ocupacion_draw

# Configuración de la página, título, icono, estado de la sidebar(que posiblemente quitaremos), etc.
st.set_page_config(
    page_title="Reserva Taquillas UC3M",
	layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="collapsed",  # Can be "auto", "expanded", "collapsed"
	page_icon="images/eps_logo.png",  # String, anything supported by st.image, or None.
)


# ---- HEADER ----
st.image("images/eps_logo.png", width=100)
st.subheader("Reserva Taquillas UC3M", divider=True)
st.title("Aplicación para la reserva de taquillas del campus de Leganés de la UC3M")
#st.write("Esta aplicación permite reservar las taquillas del campus de Leganés de la UC3M.")
st.subheader("Instrucciones:", divider=True)


st.write("Para reservar una taquilla, elige primero el edificio donde se encuentra la taquilla,"
         " luego, la planta y el bloque, y, por último, la taquilla que quieres reservar. Además, "
         "deberás introducir tu nombre, tus apellidos y con el NIA para realizar la reserva."
         "Una vez enviados los datos, recibirás un correo electrónico con los datos asociados"
         " y un código de verificación. "
         "\nPara más información, accede a la página de Delegación.")


st.write("Para más información ve a la [página de Delegación](https://delegacion.uc3m.es/home/eps-taquillas/).")

reserva_tab, ocupacion_tab = st.tabs([":blue[**Reservar Taquilla**]", ":blue[**Ocupación**]"])
with reserva_tab:
    # Cargamos los datos de las taquillas disponibles y reservadas
    # Como esto se carga cada vez que se actualiza la página, estará siempre actualizada
    with open("disponibles.json", "r") as f:
        taquillas_disponibles = json.load(f)
    with open("reservadas.json", "r") as f:
        taquillas_reservadas = json.load(f)

    # Inicializamos las variables que vamos a utilizar y modificar
    reservable = False
    reservableNIA = False

    # Inicializamos las constantes que vamos a utilizar
    IMAGES = {'Edificio 1': {'Planta 0': "1.0.jpg", 'Planta 1': "1.1.jpg"}, 'Edificio 2':{'Planta 2': "2.2.jpg", 'Planta 3': "2.3.jpg"}, 'Edificio 4':{'Planta 0': "4.0.jpg", 'Planta 1': "4.1.jpg", 'Planta 2': "4.2.jpg"}, 'Edificio 7':{'Planta 0': "7.0.jpg", 'Planta 1': "7.1.jpg", 'Planta 2': "7.2.jpg"}}
    RESERVADAS_PATH = "reservadas.json"
    DISPONIBLES_PATH = "disponibles.json"
    MAX_TAQUILLAS = 3

    def nia_counter(nia) -> int:
        """
        Función que cuenta el número de taquillas reservadas por un NIA
        :param nia:
        :return: Número de taquillas reservadas por el NIA
        """
        with open(RESERVADAS_PATH, "r") as f:
            taquillas_reservadas = json.load(f)
        counter = 0
        for edificio_key, edificio in taquillas_reservadas.items():
            for planta_key, planta in edificio.items():
                for bloque_key, bloque in planta.items():
                    for reserva_key in range(len(bloque)):
                        if bloque[reserva_key][1] == nia:
                            counter += 1
        return counter

    def generate_code() -> str:
        code = str(random.randint(100000, 999999))
        number = 0
        for digit in str(code):
            number += int(digit)
        letter = chr(number % 26 + 65)
        if letter == "O" or letter == "I":
            letter = chr((number + 1) % 26 + 65)
        return code[3:] + "-" + code[:3] + "-" + letter

    with st.container():
        st.title("Reserva tu taquilla:")
        st.markdown("Ten en cuenta que las letras **P** y **G** indican el tamaño **P**equeño o **G**rande respectivamente.  \n"
            "El precio de las taquillas es de 6€ para las grandes y 4€ para las pequeñas para el curso completo.  \n"
            "El pago se realizará en efectivo en la Delegación de Estudiantes de la EPS.")

        # Dividimos el espacio en 4 columnas para los desplegables
        col_edificio, col_planta, col_bloque, col_numero = st.columns(4)

        # Para acceder a los datos, navegamos por el diccionario, utilizando los desplegables como índices
        # Desplegable de la lista de edificios
        with col_edificio:
            edificio = st.selectbox("Selecciona el edificio", taquillas_disponibles.keys())
            lista_plantas = list(taquillas_disponibles[edificio].keys())

        # Desplegable de la lista de plantas del edificio seleccionado
        with col_planta:
            planta = st.selectbox("Selecciona la planta", lista_plantas)
            lista_bloques = list(taquillas_disponibles[edificio][planta].keys())

        # Desplegable de la lista de bloques de la planta seleccionada
        with col_bloque:
            bloque = st.selectbox("Selecciona el bloque", lista_bloques)
            lista_numeros = taquillas_disponibles[edificio][planta][bloque]

        # Desplegable de la lista de taquillas del bloque seleccionado
        with col_numero:
            taquilla = st.selectbox("Selecciona la taquilla", lista_numeros)


        # Creamos otro bloque de 4 espacios, para los campos en los que el usuario tiene que
        # introducir datos manualmente, en vez de desplegables
        col_nombre, col_appellidos, col_NIA, col_warning = st.columns(4)

        # Campos de texto para el nombre, apellidos y NIA
        with col_nombre:
            nombre = st.text_input("Introduce tu nombre")
        with col_appellidos:
            apellidos = st.text_input("Introduce tus apellidos")
        with col_NIA:
            # Comprobamos que el NIA introducido es válido, empieza por 100 y luego 6 dígitos
            # Si ese NIA ya tiene una reserva, no se puede reservar y mostramos un mensaje de error
            nia = st.text_input("Introduce tu NIA")
            if re.match(r"100[0-9]{6}", nia) and nia != '':
                # Comprobamos que el NIA no tiene más del número máximo de taquillas reservadas
                # Función hecha.
                # Esta es la parte que se puede cambiar, introducir una función que nos permite que
                # un mismo NIA tenega hasta N taquillas reservadas. Ahora mismo solo se puede reservar 1
                # --------------------------------------------------------------------------------------


                numero_taquillas_por_nia = nia_counter(nia)
                with col_warning:
                    if numero_taquillas_por_nia >= MAX_TAQUILLAS:
                        reservableNIA = False
                        st.warning("NIA ya tiene el máximo de reservas.")
                    else:
                        if numero_taquillas_por_nia > 0:
                            st.warning(f"Llevas reservadas: {numero_taquillas_por_nia} taquillas")
                        reservableNIA = True
            else:
                with col_warning:
                    st.error("NIA no válido")

        # Checkbox para aceptar la política de protección de datos, usando la mitad de la pantalla
        col1, _ = st.columns(2)
        with col1:
            text = ("""Acepto el tratamiento de mis datos por la Delegación de Estudiantes únicamente
                           con fines estadísticos y recopilación de información genérica, no siendo cedidos
                           a terceros en ningún caso.""")
            proteccion_datos = st.checkbox(text)

    # Comprobamos que se han rellenado todos los campos y que se ha aceptado la política de protección de datos
    if proteccion_datos and reservableNIA and nombre and apellidos and edificio and planta and bloque and taquilla:
        reservable = True
        st.write("Reservable")
    else:
        st.write("Por favor, rellena todos los campos (NIA + Nombre + Apellido)"
                 " y acepta la política de protección de datos")

    # Si se puede reservar, habilitamos el botón de reservar
    with st.container():
        if st.button("Reservar", disabled=not(reservable)):
            try:
                # Generamos un código de verificación aleatorio
                codigo = generate_code()

                # Añadimos a las reservadas la taquilla que se ha solicitado y la guardamos en el json
                reserva = [taquilla, nia, "Reservada", nombre, apellidos, codigo]
                taquillas_reservadas[edificio][planta][bloque].append(reserva)
                with open("reservadas.json", "w") as f:
                    json.dump(taquillas_reservadas, f)

                # Eliminamos de las disponibles la taquilla que se ha solicitado
                taquillas_disponibles[edificio][planta][bloque].remove(taquilla)
                with open("disponibles.json", "w") as f:
                    json.dump(taquillas_disponibles, f)

                # Enviamos el correo electrónico con el código de verificación
                send_email_verification(nombre, nia, taquilla, codigo)

                # Mostramos la información de la reserva, mostramos mensaje temporal y lanzamos los confetis
                content = f"Reserva realizada con éxito :partying_face:  \n" \
                            f"Taquilla: {taquilla}  \n" \
                            f"NIA: {nia}  \n" \
                            f"Nombre: {nombre}  \n" \
                            f"Apellidos: {apellidos}  \n"
                st.success(content)
                reduced = content[:content.find("NIA:")]
                st.toast(reduced, icon='🎉')
                st.balloons()
            except:
                st.error("No se ha podido hacer la reserva, contacta con delegación para que puedan arreglarlo")

        # Toggle para mostrar la guía en imágenes de la localización de bloques por planta
        if st.toggle("Mostrar guía de bloques por planta", key="guia", value=True):
            st.image("images/" + IMAGES[edificio][planta], width=500)

with ocupacion_tab:
    refresh = True
    st.subheader("Consulta la ocupación de los bloques eligiendo un edificio y una planta")
    with open("disponibles.json", "r") as f:
        taquillas_disponibles = json.load(f)
    with open("reservadas.json", "r") as f:
        taquillas_reservadas = json.load(f)
    edificio_tab_sel, planta_tab_sel, refresh_tab_sel = st.columns(3)
    with edificio_tab_sel:
        edificio = st.selectbox("Selecciona el edificio para consultar su disponibilidad", taquillas_disponibles.keys())
    with planta_tab_sel:
        planta = st.selectbox("Selecciona la planta para consultar su disponibilidad", list(taquillas_disponibles[edificio].keys()))
    with refresh_tab_sel:
        if st.button("Actualizar", key="refresh"):
            refresh = True
    if refresh:
        ocupacion_draw(edificio, planta)
        refresh = False
