import re
import streamlit as st
from authentication.email_send import send_email_verification
from database.database_functions import bloques_por_planta
from database.database_functions import edificios_disponibles
from database.database_functions import hacer_reserva
from database.database_functions import plantas_por_edificio
from database.database_functions import taquillas_por_nia
from database.database_functions import taquillas_por_bloque
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
st.subheader("Instrucciones:", divider=True)

st.write("Para reservar una taquilla, elige primero el edificio donde se encuentra la taquilla,"
         " luego, la planta y el bloque, y, por último, la taquilla que quieres reservar. Además, "
         "deberás introducir tu nombre, tus apellidos y con el NIA para realizar la reserva."
         " Una vez enviados los datos, recibirás un correo electrónico con los datos asociados"
         " y un código de verificación. "
         "\nPara más información, accede a la página de Delegación.")

st.write("Para más información ve a la [página de Delegación](https://delegacion.uc3m.es/home/eps-taquillas/).")

reserva_tab, ocupacion_tab = st.tabs([":blue[**Reservar Taquilla**]", ":blue[**Ocupación**]"])
with reserva_tab:
    # Inicializamos las variables que vamos a utilizar y modificar
    reservable = False
    reservable_NIA = False

    # Inicializamos las constantes que vamos a utilizar
    IMAGES = {'1': {'0': "1.0.jpg", '1': "1.1.jpg"},
              '2': {'2': "2.2.jpg", '3': "2.3.jpg"},
              '4': {'0': "4.0.jpg", '1': "4.1.jpg", '2': "4.2.jpg"},
              '7': {'0': "7.0.jpg", '1': "7.1.jpg", '2': "7.2.jpg"}}
    MAX_TAQUILLAS = 3

    with st.container():
        titulo_descr_col, img_01 = st.columns([3, 1])
        with titulo_descr_col:
            # Título y descripción de la página
            st.title("Reserva tu taquilla:")
            st.markdown(
                "Ten en cuenta que las letras **P** y **G** indican el tamaño **P**equeño o **G**rande respectivamente.  \n"
                "El precio de las taquillas es de 6€ para las grandes y 4€ para las pequeñas para el curso completo.  \n"
                "El pago se realizará en efectivo en la Delegación de Estudiantes de la EPS.")
        with img_01:
            # Imagen de la página
            st.image("images/taquilla-info.png")

        # Dividimos el espacio en 4 columnas para los desplegables
        col_edificio, col_planta, col_bloque, col_numero = st.columns(4)

        # Para acceder a los datos, vamos seleccionando las columnas de sql
        # Desplegable de la lista de edificios
        with col_edificio:
            edificio = st.selectbox("Selecciona el edificio", edificios_disponibles())

        # Desplegable de la lista de plantas del edificio seleccionado
        with col_planta:
            planta = st.selectbox("Selecciona la planta", plantas_por_edificio(edificio))

        # Desplegable de la lista de bloques de la planta seleccionada
        with col_bloque:
            bloque = st.selectbox("Selecciona el bloque", bloques_por_planta(edificio, planta))

        # Desplegable de la lista de taquillas del bloque seleccionado
        with col_numero:
            taquilla = st.selectbox("Selecciona la taquilla", taquillas_por_bloque(edificio, planta, bloque))

        # Creamos otro bloque de 4 espacios, para los campos en los que el usuario tiene que
        # introducir datos manualmente, en vez de desplegables
        col_nombre, col_appellidos, col_NIA, col_warning = st.columns(4)

        # Campos de texto para el nombre, apellidos y NIA
        # Comprobamos que el nombre y apellidos introducidos son válidos, son solo letras
        with col_nombre:
            nombre = st.text_input("Introduce tu nombre")
            if re.match(r"^[A-záéíóúèàìòùäëïöÜÁÉÍÓÚÀÈÌÒÙÄËÏÖÜçÇ]+", nombre):
                nombre_reservable = True
        with col_appellidos:
            apellidos = st.text_input("Introduce tus apellidos")
            if re.match(r"^[A-záéíóúèàìòùäëïöÜÁÉÍÓÚÀÈÌÒÙÄËÏÖÜçÇ]+", apellidos):
                apellido_reservable = True
        with col_NIA:
            # Comprobamos que el NIA introducido es válido, empieza por 100 y luego 6 dígitos
            # Si ese NIA ya tiene una reserva, no se puede reservar y mostramos un mensaje de error
            nia = st.text_input("Introduce tu NIA")
            if re.match(r"^100[0-9]{6}$", nia) and nia != '':
                # Comprobamos que el NIA no tiene más del número máximo de taquillas reservadas
                num_taquillas_por_nia = taquillas_por_nia(nia)
                with col_warning:
                    if num_taquillas_por_nia >= MAX_TAQUILLAS:
                        reservable_NIA = False
                        st.warning("NIA ya tiene el máximo de reservas.")
                    else:
                        if num_taquillas_por_nia > 0:
                            st.warning(f"Llevas reservadas: {num_taquillas_por_nia} taquillas")
                        reservable_NIA = True
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
    if proteccion_datos and reservable_NIA and nombre_reservable and apellido_reservable and edificio and planta and bloque and taquilla:
        reservable = True
        st.write("Reservable")
    else:
        st.write("Por favor, rellena todos los campos (NIA + Nombre + Apellido)"
                 " y acepta la política de protección de datos")

    # Si se puede reservar, habilitamos el botón de reservar
    with st.container():
        if st.button("Reservar", disabled=not (reservable)):
            try:
                code = hacer_reserva(taquilla, nia, nombre, apellidos)

                # Enviamos el correo electrónico con el código de verificación
                send_email_verification(nombre, nia, taquilla, code)

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
            st.image("images/" + IMAGES[edificio][planta], width=400)

with ocupacion_tab:
    # Tab para ver la ocupación por bloques de un edificio y planta específicos
    # Para que no se esté actualizando siempre, y solo una vez cuando se carga la página, usamos un botón de actualizar
    refresh = True
    st.subheader("Consulta la ocupación de los bloques eligiendo un edificio y una planta")

    edificio_tab_sel, planta_tab_sel, refresh_tab_sel = st.columns(3)
    with edificio_tab_sel:
        edificio = st.selectbox("Selecciona el edificio para consultar su disponibilidad", edificios_disponibles())
    with planta_tab_sel:
        planta = st.selectbox("Selecciona la planta para consultar su disponibilidad", plantas_por_edificio(edificio))
    with refresh_tab_sel:
        if st.button("Actualizar", key="refresh"):
            refresh = True
    if refresh:
        ocupacion_draw(edificio, planta)
        refresh = False
