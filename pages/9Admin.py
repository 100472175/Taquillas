import hashlib
import logging
import re
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from confirmation.email_send import *
from database.database_functions import *
from streamlit_modal import Modal
from streamlit_extras.switch_page_button import switch_page
from time import sleep
from yaml.loader import SafeLoader
from database.bd_osciloscopio_generate import *

# Información de la página:
# La página está dividida en pestañas, cada una con una funcionalidad diferente. La mayoría de veces, el delegado solo
# tendrá que acceder a la pestaña de "Cambiar estado".
# El esquema que tiene la base de datos es el siguiente:
#   - ID: Identificador de la taquilla
#   - EDIFICIO: Edificio de la taquilla
#   - PLANTA: Planta de la taquilla
#   - BLOQUE: Bloque de la taquilla
#   - TAQUILLA: Número de la taquilla
#   - ESTADO: Estado de la taquilla. Puede ser "Reservada", "Ocupada" o "No Disponible"
#   - NIA: NIA del alumno que ha reservado la taquilla
#   - NOMBRE: Nombre del alumno que ha reservado la taquilla
#   - APELLIDOS: Apellidos del alumno que ha reservado la taquilla
#   - CODIGO: Código de verificación de la taquilla
#   - TIMESTAMP: Fecha de la reserva en formato YYYY-MM-DD HH:MM:SS.XXXXXX (X es el microsegundo)


# Configuración de los logs
logging.basicConfig(filename='logs/app.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)
# Cargar el fichero de configuración y aplicarla
config_path = "authentication/config.yaml"
with open(config_path) as file:
    config = yaml.load(file, Loader=SafeLoader)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

me, authentication_status, username = authenticator.login('Login', 'main')
if not st.session_state["authentication_status"]:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
elif st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')
    rol = config['credentials']['usernames'][username]['rol']
    st.title("Administrador de taquillas")

    # Pone el nombre del usuario en la sesión y generamos las pestañas
    st.write(f'Te damos la bienvenida, *{st.session_state["name"]}*')
    estado_tab, mod_data_tab, change_taquilla_tab, del_tab, general_view_tab, reset_tab, manage_credentials_tab, osciloscopios_tab = st.tabs(
        [":blue[**Cambiar estado**]", ":blue[**Modificar Datos Reserva**]", ":blue[**Modificar Taquilla**]",
         ":blue[**Eliminar Reserva**]", ":blue[**Vista General**]",
         ":blue[**Reset**]", ":blue[**Gestión de credenciales**]", ":blue[**Osciloscopios**]"])
    css = '''
    <style>
        .stTabs [data-baseweb="tab-highlight"] {
            background-color:blue;
        }
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

    # Pestaña de cambiar estado. Esta es la más utilizada por el delegado, ya que es la que se utiliza para cambiar el
    # estado de una taquilla. Se introduce el NIA o el nombre de la taquilla y se muestra la información de la taquilla.
    # Se puede cambiar el estado de la taquilla con un desplegable. Si se pulsa el botón de "Cambiar estado", se
    # cambiará el estado de la taquilla. Los diferentes estados son: Reservada, Ocupada y No Disponible.
    with estado_tab:
        st.title("Cambio del estado de la reserva")
        st.warning("¡Comprueba que han pagado la reserva antes de darles el status de ocupada!")
        # Genera los campos de búsqueda de la taquilla, tanto por NIA como por número de la taquilla
        nia_estado_col, taquilla_estado_col = st.columns(2)
        with nia_estado_col:
            nia_estado = st.text_input("NIA")
        with taquilla_estado_col:
            taquilla_estado = st.text_input("Taquilla")
            # Obtenemos toda la información de la taquilla que se ha reservado.
        # TODO: Hacer esto una función, para reducir el número de líneas de código.
        taquilla = get_info_taquilla_nia(nia_estado)
        if taquilla is None:
            taquilla = get_info_taquilla_codigo(taquilla_estado)
        # Si se ha encontrado la taquilla, se muestra la información de la taquilla, generando las columnas e
        # insertando la información de la taquilla en cada columna.
        if taquilla:
            taquilla_col, nia_col, estado_col, nombre_col, apellidos_col, codigo_col = st.columns(6)
            with taquilla_col:
                st.write("Taquilla", key=taquilla[4])
                st.write(taquilla[4])
            with nia_col:
                st.write("NIA", key=taquilla[6])
                st.write(taquilla[6])
            with estado_col:
                index = ["Reservada", "Ocupada", "No Disponible"].index(taquilla[5])
                new_state = st.selectbox("Estado", options=["Reservada", "Ocupada", "No Disponible"], index=index,
                                         key=taquilla[5])
            with nombre_col:
                st.write("Nombre", key=taquilla[7])
                st.write(taquilla[7])
            with apellidos_col:
                st.write("Apellidos", key=taquilla[8])
                st.write(taquilla[8])
            with codigo_col:
                st.write("Código", key=taquilla[9])
                st.write(taquilla[9])

            # Si se pulsa el botón de "Cambiar estado", se cambia el estado de la taquilla al seleccionado.
            if st.button("Cambiar estado"):
                try:
                    update_taquilla_estado(taquilla[4], new_state)
                    st.success("Cambiado a " + new_state)
                    st.toast("Cambiado a " + new_state, icon='🎉')

                    logging.info(
                        f'{st.session_state["name"]} ha cambiado el estado de la taquilla de {taquilla[6]} de {taquilla[4]} a {new_state}')
                except Exception as exc:
                    st.error("No se ha podido cambiar el estado")
                    st.error(exc)
            else:
                st.error("No se ha encontrado tu reserva")

    # Pestaña de modificar datos de la reserva. Se puede cambiar el NIA, el estado, el nombre y los apellidos de la
    # reserva.
    with mod_data_tab:
        st.title("Cambia datos de la reserva:")
        st.warning("Para cambiar la taquilla, es necesario borrar la reserva y realizar otra")

        # Genera los campos de búsqueda de la taquilla, tanto por NIA como por número de la taquilla
        nia_mod_col, taquilla_mod_col = st.columns(2)
        with nia_mod_col:
            nia_mod_estado = st.text_input("Introduce el NIA a consultar")
        with taquilla_mod_col:
            taquilla_mod_estado = st.text_input("Introduce el nombre de la taquilla a consultar")

        # Obtenemos toda la información de la taquilla que se ha reservado.
        # TODO: Hacer esto una función, para reducir el número de líneas de código.
        taquilla_mod = get_info_taquilla_nia(nia_mod_estado)
        if taquilla_mod is None:
            taquilla_mod = get_info_taquilla_codigo(taquilla_mod_estado)
        if taquilla_mod:
            taquilla_col, nia_col, estado_col, nombre_col, apellidos_col, codigo_col = st.columns(6)
            with taquilla_col:
                st.write("Taquilla")
                st.write(taquilla_mod[4])
            with nia_col:
                new_nia = st.text_input("NIA", value=taquilla_mod[6])
            with estado_col:
                index = ["Reservada", "Ocupada", "No Disponible"].index(taquilla_mod[5])
                new_state = st.selectbox("Estado", options=["Reservada", "Ocupada", "No Disponible"], index=index,
                                         key="estado")
            with nombre_col:
                taquilla_mod[7] = st.text_input("Nombre", value=taquilla_mod[7])
            with apellidos_col:
                taquilla_mod[8] = st.text_input("Apellidos", value=taquilla_mod[8])
            with codigo_col:
                st.write("Código")
                st.write(str(taquilla_mod[9]))
                if st.button("Generar nuevo código"):
                    code = generate_code()
                    send_email_verification(taquilla_mod[7], taquilla_mod[6], taquilla_mod[4], code)
                    update_taquilla_codigo(taquilla_mod[4], code)
                    st.success("Código generado y enviado al correo")
                    sleep(1)
                    switch_page("Administrator")
            # Si se pulsa el botón de "Cambiar datos", se cambian los datos de la taquilla al seleccionado.
            if st.button("Cambiar datos"):
                if re.match(r"100[0-9]{6}", new_nia):
                    taquilla_mod[2] = new_state
                    taquilla_mod[1] = new_nia
                    update_taquilla_completo(taquilla_mod[4], new_nia, new_state, taquilla_mod[7], taquilla_mod[8])
                    st.success("Datos cambiados")
                    st.toast("Datos cambiados", icon='🎉')
                    logging.info(
                        f'{st.session_state["name"]} ha cambiado los datos de la taquilla {taquilla_mod[4]}')
                    sleep(1)
                    switch_page("Administrator")
        else:
            st.error("No se ha encontrado tu reserva")

    # Pestaña de modificar taquilla. Se puede cambiar la taquilla de una reserva, pero no se puede cambiar el NIA,
    # el estado, el nombre y los apellidos de la reserva. Para cambiar el NIA, el estado, el nombre y los apellidos de
    # la reserva, se debe utilizar la pestaña de "Modificar datos de la reserva".
    with change_taquilla_tab:
        st.title("Modificar taquilla")
        st.write("Aquí puedes modificar los datos de una taquilla concreta.")

        nia_mod_col, taquilla_mod_col = st.columns(2)
        with nia_mod_col:
            nia_cambio_estado = st.text_input("Introduce el NIA a consultar", key="mod_nia")
        with taquilla_mod_col:
            taquilla_cambio_estado = st.text_input("Introduce el nombre de la taquilla a consultar", key="mod_taq")

        taquilla_cambio = get_info_taquilla_nia(nia_cambio_estado)
        if taquilla_cambio is None:
            taquilla_cambio = get_info_taquilla_codigo(taquilla_cambio_estado)
        if taquilla_cambio:
            # Datos de la reserva antigua
            taquilla_col, nia_col, estado_col, nombre_col, apellidos_col, codigo_col = st.columns(6)
            with taquilla_col:
                st.write("Taquilla")
                st.write(taquilla_cambio[4])
            with nia_col:
                st.write("NIA")
                st.write(taquilla_cambio[6])
                nia = taquilla_cambio[6]
            with estado_col:
                st.write("Estado")
                st.write(taquilla_cambio[5])
            with nombre_col:
                st.write("Nombre")
                st.write(taquilla_cambio[7])
                nombre = taquilla_cambio[7]
            with apellidos_col:
                st.write("Apellidos")
                st.write(taquilla_cambio[8])
                apellidos = taquilla_cambio[8]
            with codigo_col:
                st.write("Código")
                st.write(taquilla_cambio[9])

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
                taquilla = st.selectbox("Selecciona la taquilla",
                                        taquillas_por_bloque(edificio, planta, bloque))

            if st.button("Modificar taquilla"):
                code = change_taquilla(taquilla_cambio[4], taquilla, nia, nombre, apellidos, taquilla_cambio[5])
                logging.info(
                    f'{st.session_state["name"]} ha cambiado la taquilla {taquilla_cambio[4]} a {taquilla}')

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
        else:
            st.error("No se ha encontrado tu reserva")

    with del_tab:
        st.title("Elimina una reserva")
        st.warning("¡El borrado de una reserva no se puede deshacer!")
        nia_del_col, taquilla_del_col = st.columns(2)
        # TODO: Hacer esto una función, para reducir el número de líneas de código.
        with nia_del_col:
            nia_del_estado = st.text_input("Introduce el NIA de la reserva a eliminar", key="del_nia")
        with taquilla_del_col:
            taquilla_del_estado = st.text_input("Introduce el nombre de la taquilla a consultar", key="del_taq")
        taquilla_del = get_info_taquilla_nia(nia_del_estado)
        if taquilla_del is None:
            taquilla_del = get_info_taquilla_codigo(taquilla_del_estado)
        if taquilla_del:
            taquilla_col, nia_col, estado_col, nombre_col, apellidos_col, codigo_col = st.columns(6)
            with taquilla_col:
                st.write("Taquilla", )
                st.write(taquilla_del[4])
            with nia_col:
                st.write("NIA", )
                st.write(taquilla_del[6])
            with estado_col:
                st.write("Estado", )
                st.write(taquilla_del[5])
            with nombre_col:
                st.write("Nombre", )
                st.write(taquilla_del[7])
            with apellidos_col:
                st.write("Apellidos", )
                st.write(taquilla_del[8])
            with codigo_col:
                st.write("Código", )
                st.write(taquilla_del[9])

            # Configurar una ventana modal para confirmar el borrado de una reserva.
            modal = Modal(key="Demo Modal", title="", max_width=900)
            auth = False
            message_success = None
            show_confirmation = False
            open_modal = st.button(":red[Eliminar]")
            # Abrir el modal
            if open_modal:
                modal.open()
            if modal.is_open():
                nombre_taquilla = taquilla_del[4]
                nombre = taquilla_del[7]
                apellidos = taquilla_del[8]
                # Definir el contenido en HTML de la ventana modal. Hay cosas feas porque el título no se veía siempre.
                with modal.container():
                    st.markdown(
                        f'<p style="color:{"#da2724"};font-size:36px;border-radius:2%;">Confirmación de '
                        f'eliminación</p>',
                        unsafe_allow_html=True)

                    # Colocamos en posiciones opuestas los botones de eliminaar y confirmación, para que por error
                    # no se elimine una reserva.
                    left_column, _, _, _, right_column = st.columns(5)
                    with left_column:
                        if st.button("Cancelar"):
                            modal.close()
                    with right_column:
                        if st.button(":red[Delete]"):
                            delete_taquilla_reserva(nombre_taquilla)
                            st.success("Eliminado")
                            st.toast("Eliminado", icon='🎉')
                            logging.info(f'{st.session_state["name"]} ha eliminado la taquilla {nombre_taquilla}')
                            modal.close()
                            sleep(1)
                            switch_page("Administrator")
        else:
            st.error("No se ha encontrado tu reserva")

    # Vista general, donde se pueden ver estadísticas del uso de las taquillas en la universidad,
    # así como quien las ha reservado y algunos controles para generar tablas de uso.
    with general_view_tab:
        st.title("Vista general")
        st.write("Aquí puedes ver las taquillas reservadas y todos lo datos de las reservas.")
        # Se generan 5 columnas para poder representar en horizontal la información del uso.
        ocupada, reservada, libres, rotas, pasadas = st.columns(5)
        with ocupada:
            st.write("Taquillas ocupadas: ", taquillas_ocupadas_numero())
        with reservada:
            st.write("Taquillas reservadas: ", taquillas_reservadas_numero())
        with libres:
            st.write("Taquillas libres: ", taquillas_libres_numero())
        with rotas:
            st.write("Taquillas rotas: ", taquillas_rotas_numero())
        with pasadas:
            st.write("Taquillas que se han pasado de fecha: ", taquillas_pasadas_de_tiempo_numero())

        # Genera, al pulsar el botón, la tabla de:
        # La tabla de las taquillas ocupadas.
        if st.button("Genera ocupadas/reservadas"):
            st.dataframe(taquillas_not_libres())
        # La tabla de las taquillas libres.
        if st.button("Genera libres"):
            st.dataframe(taquillas_libres())
        # La tabla de las taquillas rotas / no disponibles.
        if st.button("Genera Rotas"):
            st.dataframe(taquillas_rotas())
        # La tabla de las taquillas, que se han reservado, pero no se han ocupado en un tiempo determinado.
        if st.button("Genera las pasadas de tiempo"):
            st.dataframe(taquillas_pasadas_de_tiempo())

        # Botón que elimina las reservas que se han pasado de tiempo y no se han ocupado (pagado).
        if st.button("Haz click para eliminar las reservas"):
            delete_taquillas_pasadas_de_tiempo()
            st.success("Eliminadas las reservas pasadas de tiempo")
            st.toast("Eliminadas las reservas pasadas de tiempo", icon='🎉')
            logging.info(f'{st.session_state["name"]} ha eliminado las reservas pasadas de tiempo')

    # Página de la web, a la que solo tienen acceso los delegados que tienen el rol de escuela, la delegada de escuela,
    # el subdelegado de escuela y la cuenta del sys-admin.
    with reset_tab:
        if rol == "escuela":
            st.title("Gestión de la base de datos")
            st.subheader("Reset de todas las reservas")
            st.warning("Esto solo se debe ejecutar una vez al año. ¡No se puede deshacer!")
            passwd = st.text_input("Introduce contraseña")
            # Se le pide al usuario que se introduzca una contraseña, que no es pública, para resetear la base de datos.
            # Se eliminan las entradas de los usuarios, y se regeneran las taquillas.
            if hashlib.md5(passwd.encode()).hexdigest() == config["reset_password"]["password"]:
                if st.button("Borrado definitivo"):
                    logging.info(f'{st.session_state["name"]} ha reseteado la base de datos')
                    reset_database()
                    st.success("Reseteado con éxito")
                    st.toast("Reseteado con éxito", icon='🎉')
                    sleep(2)
            else:
                st.error("Contraseña incorrecta")

            with open("database/database.db", "rb") as fp:
                btn_db = st.download_button(
                    label="Descarga la base de datos",
                    data=fp,
                    file_name="database.db"  # Nombre del archivo que se va a descargar en local.
                )
                if btn_db:
                    logging.info(f'{st.session_state["name"]} ha descargado la base de datos')

            # Subseccicón para subir una snapshot de la base de datos, por si se pierde,
            # se corrompe o pasa algo en algún momento, una manera con GUI de restaurar la aplicación
            st.subheader("Subir nueva base de datos")
            uploaded_file = st.file_uploader("Elige un fichero para subir como nueva base de datos")
            if uploaded_file is not None:
                with open("database/database.db", "wb") as fp:
                    fp.write(uploaded_file.getvalue())
                st.success("Base de datos subida con éxito")
                logging.info(f'{st.session_state["name"]} ha subido una nueva base de datos')

            # Descarga los logs, al igual que la base de datos, como archivo .log
            st.subheader("Descargar los logs de los delegados")
            with open("logs/app.log", "rb") as fp:
                btn_logs = st.download_button(
                    label="Descarga los logs de los delegados",
                    data=fp,
                    file_name="app_taquillas.log"  # Any file name
                )
                if btn_logs:
                    logging.info(f'{st.session_state["name"]} ha descargado los logs')

            # Crear una copia de la base de datos y enviarla por correo, al mismo correo que envia los datos.
            if st.button("Envia base de datos por correo"):
                send_backup_email_db()
                st.success("Base de datos enviada con éxito")
        # Si no se tiene el rol de delegado de centro, no se puede acceder a la página, y para que no esté vacía,
        # se coloca este mensaje
        else:
            st.subheader("No tienes permiso para ejecutar esta acción")

    # Página para añadir usuarios a la aplicación, todavía en proceso de construcción.
    with manage_credentials_tab:
        st.title("Gestión de credenciales")
        if rol == "escuela":
            st.text("In development, subir un excel y que se generen todas las contraseñas")
        else:
            st.subheader("No tienes permiso para ejecutar esta acción")

    # Página no relacionada con la aplicación de taquillas, pero si con las reservas que ofrece
    # la delegación de estudiantes, que permite eliminar la tabla que contiene las reservas y volver a crear la tabla.
    with osciloscopios_tab:
        st.title("Reserva de osciloscopios")
        if rol == "escuela":
            if st.button("Crear tabla de reservas"):
                huecos_table_creation()
                huecos_table_importer(NUM_OSCILOS)
                st.success("Tabla creada con éxito")
            if st.button("Borrar tabla de reservas"):
                drop_huecos_table()
                st.success("Tabla borrada con éxito")
        else:
            st.subheader("No tienes permiso para ejecutar esta acción")

# Información general que aparece en la página, en cualquiera de las pestañas, ya que es informativa.
with st.container():
    # Dudas, acude a delegación
    st.write(
        "Si tienes alguna duda, consulta el manual de usuario en la [carpeta de Google Drive]("
        "https://drive.google.com/drive/folders/15tOcC8FqSK1vdOcjEdqS7Rf1iDFpjzNc?usp=share_link)")
