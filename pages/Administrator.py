import hashlib
import json
import re
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_extras.switch_page_button import switch_page
from time import sleep
import yaml
from streamlit_modal import Modal
from yaml.loader import SafeLoader
from authentication.code_generator import generate_code
from authentication.email_send import send_email_verification
from database.database_functions import get_info_taquilla_nia
from database.database_functions import get_info_taquilla_codigo
from database.database_functions import update_taquila_estado
from database.database_functions import update_taquilla_codigo
from database.database_functions import update_taquilla_completo
from database.database_functions import delete_taquilla_reserva
from database.database_functions import edificios_disponibles
from database.database_functions import plantas_por_edificio
from database.database_functions import bloques_por_planta
from database.database_functions import taquillas_por_bloque
from database.database_functions import change_taquilla
from database.database_functions import reset_database
from database.database_functions import taquillas_not_libres
from database.database_functions import taquillas_libres
from database.database_functions import taquillas_rotas
# from database.database_functions import *

IMAGES = {'1': {'0': "1.0.jpg", '1': "1.1.jpg"},
          '2': {'2': "2.2.jpg", '3': "2.3.jpg"},
          '4': {'0': "4.0.jpg", '1': "4.1.jpg", '2': "4.2.jpg"},
          '7': {'0': "7.0.jpg", '1': "7.1.jpg", '2': "7.2.jpg"}}
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

if st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')
elif st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')

    st.title("Administrador de taquillas")

    with st.container():
        st.write(f'Bienvenido *{st.session_state["name"]}*')
        estado_tab, mod_data_tab, change_taquilla_tab, del_tab, general_view_tab, add_tab, reset_tab = st.tabs(
            [":blue[**Cambiar estado**]", ":blue[**Modificar Datos Reserva**]", ":blue[**Modificar Taquilla**]",
             ":blue[**Eliminar Reserva**]", ":blue[**Vista General**]", ":blue[**Añadir Bloque**]",
             ":blue[**Reset**]"])
        css = '''
        <style>
            .stTabs [data-baseweb="tab-highlight"] {
                background-color:blue;
            }
        </style>
        '''
        st.markdown(css, unsafe_allow_html=True)

        with estado_tab:
            st.title("Cambio del estado de la reserva")
            st.warning("¡Comprueba que han pagado la reserva antes de darles el status de ocupada!")
            nia_estado_col, taquilla_estado_col = st.columns(2)
            with nia_estado_col:
                nia_estado = st.text_input("NIA")
            with taquilla_estado_col:
                taquilla_estado = st.text_input("Taquilla")

            taquilla = get_info_taquilla_nia(nia_estado)
            if taquilla is None:
                taquilla = get_info_taquilla_codigo(taquilla_estado)
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

                if st.button("Cambiar estado"):
                    try:
                        update_taquila_estado(taquilla[4], new_state)
                        st.success("Cambiado a " + new_state)
                        st.toast("Cambiado a " + new_state, icon='🎉')
                    except Exception as exc:
                        st.error("No se ha podido cambiar el estado")
                        st.error(exc)
            else:
                st.error("No se ha encontrado tu reserva")

        with mod_data_tab:
            st.title("Cambia datos de la reserva:")
            st.warning("Para cambiar la taquilla, es necesario borrar la reserva y realizar otra")

            nia_mod_col, taquilla_mod_col = st.columns(2)
            with nia_mod_col:
                nia_mod_estado = st.text_input("Introduce el NIA a consultar", key="NIA_mod")
            with taquilla_mod_col:
                taquilla_mod_estado = st.text_input("Introduce el nombre de la taquilla a consultar",
                                                    key="taquilla_mod")

            taquilla_mod = get_info_taquilla_nia(nia_mod_estado)
            if taquilla_mod is None:
                taquilla_mod = get_info_taquilla_codigo(taquilla_mod_estado)
            if taquilla_mod:
                taquilla_col, nia_col, estado_col, nombre_col, apellidos_col, codigo_col = st.columns(6)
                with taquilla_col:
                    st.write("Taquilla", key="taquilla_mod" + taquilla_mod[4])
                    st.write(taquilla_mod[4])
                with nia_col:
                    new_nia = st.text_input("NIA", value=taquilla_mod[6], key="nia" + taquilla_mod[6])
                with estado_col:
                    index = ["Reservada", "Ocupada", "No Disponible"].index(taquilla_mod[5])
                    new_state = st.selectbox("Estado", options=["Reservada", "Ocupada", "No Disponible"], index=index,
                                             key=taquilla_mod[5] + "mod_selectbox")
                with nombre_col:
                    taquilla_mod[7] = st.text_input("Nombre", value=taquilla_mod[7], key="nombre" + taquilla_mod[7])
                with apellidos_col:
                    taquilla_mod[8] = st.text_input("Apellidos", value=taquilla_mod[8],
                                                    key="apellido" + taquilla_mod[8])
                with codigo_col:
                    st.write("Código", key="código_mod")
                    st.write(taquilla_mod[9])
                    if st.button("Generar nuevo código"):
                        code = generate_code()
                        send_email_verification(taquilla_mod[7], taquilla_mod[6], taquilla_mod[4], code)
                        update_taquilla_codigo(taquilla_mod[4], code)
                        st.success("Código generado y enviado al correo")
                        sleep(1)
                        switch_page("Administrator")

                if st.button("Cambiar datos"):
                    if re.match(r"100[0-9]{6}", new_nia):
                        taquilla_mod[2] = new_state
                        taquilla_mod[1] = new_nia
                        update_taquilla_completo(taquilla_mod[4], new_nia, new_state, taquilla_mod[7], taquilla_mod[8])
                        st.success("Datos cambiados")
                        st.toast("Datos cambiados", icon='🎉')
                        sleep(1)
                        switch_page("Administrator")

            else:
                st.error("No se ha encontrado tu reserva")

        with del_tab:
            st.title("Elimina una reserva")
            st.warning("¡El borrado de una reserva no se puede deshacer!")
            nia_del_col, taquilla_del_col = st.columns(2)
            with nia_del_col:
                nia_del_estado = st.text_input("Introduce el NIA de la reserva a eliminar", key="NIA_del")
            with taquilla_del_col:
                taquilla_del_estado = st.text_input("Introduce el nombre de la taquilla a consultar",
                                                    key="taquilla_del")

            taquilla_del = get_info_taquilla_nia(nia_del_estado)
            if taquilla_del is None:
                taquilla_del = get_info_taquilla_codigo(taquilla_del_estado)
            if taquilla_del:
                taquilla_col, nia_col, estado_col, nombre_col, apellidos_col, codigo_col = st.columns(6)
                with taquilla_col:
                    st.write("Taquilla", key=str(taquilla_del[4]))
                    st.write(taquilla_del[4])
                with nia_col:
                    st.write("NIA", key=str(taquilla_del[6]))
                    st.write(taquilla_del[6])
                with estado_col:
                    st.write("Estado", key=str(taquilla_del[5]))
                    st.write(taquilla_del[5])
                with nombre_col:
                    st.write("Nombre", key=str(taquilla_del[7]))
                    st.write(taquilla_del[7])
                with apellidos_col:
                    st.write("Apellidos", key=str(taquilla_del[8]))
                    st.write(taquilla_del[8])
                with codigo_col:
                    st.write("Código", key=str(taquilla_del[9]))
                    st.write(taquilla_del[9])

                modal = Modal(key="Demo Modal", title="", max_width=900)
                auth = False
                message_success = None
                show_confirmation = False
                open_modal = st.button(":red[Eliminar_modal]", key="confirmation_button")
                if open_modal:
                    modal.open()
                if modal.is_open():
                    nombre_taquilla = taquilla_del[4]
                    nombre = taquilla_del[7]
                    apellidos = taquilla_del[8]
                    with modal.container():
                        st.markdown(
                            f'<p style="color:{"#da2724"};font-size:36px;border-radius:2%;">Confirmación de '
                            f'eliminación</p>',
                            unsafe_allow_html=True)

                        left_column, _, _, _, right_column = st.columns(5)
                        with left_column:
                            if st.button("Cancelar"):
                                modal.close()
                        with right_column:
                            if st.button(":red[Delete]"):
                                delete_taquilla_reserva(nombre_taquilla)
                                st.success("Eliminado")
                                st.toast("Eliminado", icon='🎉')
                                modal.close()
                                sleep(1)
                                switch_page("Administrator")

            else:
                st.error("No se ha encontrado tu reserva")

        # This will be done in the future, as we have no plans to add blocks in the near future
        with add_tab:
            st.title("Añadir bloque")
            st.write("Añade un bloque de taquillas a un edificio y planta concretos.")
            st.write(
                "Utiliza esto como último recurso, si no puedes contactar con el administrador y que no tiene acceso "
                "al código fuente.")
            st.write("Si no sabes lo que estás haciendo, no lo hagas. :smile:")

            edificio_add_col, planta_add_col = st.columns(2)
            with open("disponibles.json", "r") as f:
                taquillas_disponibles = json.load(f)
            with edificio_add_col:
                edificio_add = st.selectbox("Edificio", options=list(taquillas_disponibles.keys()), key="edificio_add")
            with planta_add_col:
                planta_add = st.selectbox("Planta", options=list(taquillas_disponibles[edificio_add].keys()),
                                          key="planta_add")
            st.warning("¡Asegúrate de que el bloque que vas a añadir no existe ya!")
            bloques_disponibles = ""
            for bloque in taquillas_disponibles[edificio_add][planta_add]:
                bloques_disponibles += bloque
                bloques_disponibles += ", "
            st.write("Bloques disponibles: " + bloques_disponibles)
            st.image("images/" + IMAGES[edificio_add][planta_add], width=500)

            st.write("Para añadir un bloque, pon el nombre del bloque y las taquillas disponibles, separadas por "
                     "comas y espacio.")
            bloque_add_col, taquillas_add_col = st.columns(2)
            with bloque_add_col:
                bloque_add = st.text_input("Nombre del bloque", key="bloque_add")
            with taquillas_add_col:
                taquillas_add = st.text_input("Taquillas disponibles", key="taquillas_add")
            if st.button("Añadir bloque"):
                taquillas_disponibles[edificio_add][planta_add][bloque_add] = taquillas_add.split(", ")
                with open("disponibles.json", "w") as f:
                    json.dump(taquillas_disponibles, f, indent=4)
                st.success("Bloque añadido")
                st.toast("Bloque añadido", icon='🎉')

        with general_view_tab:
            st.title("Vista general")
            st.write("Aquí puedes ver las taquillas reservadas y todos lo datos de las reservas.")
            if st.button("Genera no libres"):
                st.dataframe(taquillas_not_libres())
            if st.button("Genera Disponibles"):
                st.dataframe(taquillas_libres())

            for i in range(30):
                st.text(" ")

            if st.button("Genera Rotas"):
                st.dataframe(taquillas_rotas())

        with change_taquilla_tab:
            st.title("Modificar taquilla")
            st.write("Aquí puedes modificar los datos de una taquilla concreta.")

            nia_mod_col, taquilla_mod_col = st.columns(2)
            with nia_mod_col:
                nia_cambio_estado = st.text_input("Introduce el NIA a consultar", key="NIA_mod_del_add")
            with taquilla_mod_col:
                taquilla_cambio_estado = st.text_input("Introduce el nombre de la taquilla a consultar",
                                                    key="taquilla_mod_del_add")

            taquilla_cambio = get_info_taquilla_nia(nia_cambio_estado)
            if taquilla_cambio is None:
                taquilla_cambio = get_info_taquilla_codigo(taquilla_cambio_estado)
            if taquilla_cambio:
                # Datos de la reserva antigua
                taquilla_col, nia_col, estado_col, nombre_col, apellidos_col, codigo_col = st.columns(6)
                with taquilla_col:
                    st.write("Taquilla", key=taquilla_cambio[4])
                    st.write(taquilla_cambio[4])
                with nia_col:
                    st.write("NIA", key="nia" + taquilla_cambio[6])
                    st.write(taquilla_cambio[6])
                    nia = taquilla_cambio[6]
                with estado_col:
                    st.write("Estado", key="estado" + taquilla_cambio[5])
                    st.write(taquilla_cambio[5])
                with nombre_col:
                    st.write("Nombre", key="nombre" + taquilla_cambio[7])
                    st.write(taquilla_cambio[7])
                    nombre = taquilla_cambio[7]
                with apellidos_col:
                    st.write("Apellidos", key="apellidos" + taquilla_cambio[8])
                    st.write(taquilla_cambio[8])
                    apellidos = taquilla_cambio[8]
                with codigo_col:
                    st.write("Código", key="código_mod")
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
                    code = change_taquilla(taquilla_cambio[4], taquilla, nia, nombre, apellidos)

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

        with reset_tab:
            st.title("Reset de todas las reservas")
            st.warning("Esto solo se debe ejecutar una vez al año")
            if username == "delegado":
                st.error("No tienes permiso para ejecutar esta acción")
            else:
                passwd = st.text_input("itroduce contraseña")
                if hashlib.md5(passwd.encode()).hexdigest() == config["reset_password"]["password"]:
                    if st.button("Borrado definitivo"):
                        reset_database()
                        st.success("Reseteado con éxito")
                        st.toast("Reseteado con éxito", icon='🎉')
                else:
                    st.error("Contraseña incorrecta")

    #################################################################################################

with st.container():
    # Dudas, acude a delegación
    st.write(
        "Si tienes alguna duda, consulta el manual de usuario en la [carpeta de Google Drive]("
        "https://drive.google.com/drive/folders/15tOcC8FqSK1vdOcjEdqS7Rf1iDFpjzNc?usp=share_link)")
