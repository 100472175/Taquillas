import json
import re
import streamlit as st
#import streamlit_authenticator as stauth
import yaml
## from streamlit_modal import Modal
#from yaml.loader import SafeLoader
from Reserva_Taquillas import IMAGES

# Hay 3 cosas que descomentar, el import, el bloque de código de abajo y el de if session_state...

config_path = "config.yaml"
reservadas_path = "../reservadas.json"
disponibles_path = "../disponibles.json"

# with open(config_path) as file:
#     config = yaml.load(file, Loader=SafeLoader)
#
# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized']
# )
# me, authentication_status, username = authenticator.login('Login', 'main')
#

def get_taquilla_info(data, option) -> tuple:
    """
    Función que devuelve la información de una taquilla a partir de un NIA o un nombre
    :param data: El dato, NIA o nombre de la taquilla (ej.: 100000000/1.0.E.P001)
    :param option: Opción para saber si es un NIA o un nombre
    :return: Una tupla con la información de la taquilla o None si no se encuentra
    """
    if option.upper() == "NIA":
        option = 1
    elif option.upper() == "NOMBRE":
        option = 0
    with open(reservadas_path, "r") as f:
        taquillas_reservadas = json.load(f)
    for edificio_key, edificio in taquillas_reservadas.items():
        for planta_key, planta in edificio.items():
            for bloque_key, bloque in planta.items():
                for reserva_key in range(len(bloque)):
                    if bloque[reserva_key][option] == data:
                        return edificio_key, planta_key, bloque_key, reserva_key
    return None

def get_taquilla_info_nia(nia):
    """
    Función auxiliar para obtener la información de una taquilla a partir de un NIA
    :param nia:
    :return:
    """
    return get_taquilla_info(nia, "NIA")

    # Si lo ahcemos con la priemra está más centralizado y es más fácil de mantener
    # with open(reservadas_path, "r") as f:
    #     taquillas_reservadas = json.load(f)
    # for edificio_key, edificio in taquillas_reservadas.items():
    #     for planta_key, planta in edificio.items():
    #         for bloque_key, bloque in planta.items():
    #             for reserva_key in range(len(bloque)):
    #                 if bloque[reserva_key][1] == nia:
    #                     return edificio_key, planta_key, bloque_key, reserva_key
    #
    # return None

def get_taquilla_info_name(nombre):
    """
    Función auxiliar para obtener la información de una taquilla a partir del nombre de la taquilla
    :param nombre:
    :return:
    """
    return get_taquilla_info(nombre, "nombre")

    # with open(reservadas_path, "r") as f:
    #     taquillas_reservadas = json.load(f)
    # for edificio_key, edificio in taquillas_reservadas.items():
    #     for planta_key, planta in edificio.items():
    #         for bloque_key, bloque in planta.items():
    #             for reserva_key in range(len(bloque)):
    #                 if bloque[reserva_key][0] == nombre:
    #                     return edificio_key, planta_key, bloque_key, reserva_key
    # return None


# if st.session_state["authentication_status"] == False:
#     st.error('Username/password is incorrect')
# elif st.session_state["authentication_status"] == None:
#     st.warning('Please enter your username and password')
# elif st.session_state["authentication_status"]:
#     authenticator.logout('Logout', 'main')
# # Esto de arriba reeplaza el with de abajo
#
with st.container():
    st.title("Administrador de taquillas")

    with st.container():
        st.write(f'Bienvenido *{st.session_state["name"]}*')
        st.write(":red[Desde aquí podemos cambiar las cosas para que se vean en la página web quien ha pagado y quien no. QUITAME]")

        with open(reservadas_path, "r") as f:
            taquillas_reservadas = json.load(f)

        estado_tab, mod_tab, del_tab, add_tab = st.tabs([":blue[**Cambiar estado**]", ":blue[**Modificar Reserva**]", ":blue[**Eliminar Reserva**]", ":blue[**Añadir Bloque**]"])

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

            taquilla_index = get_taquilla_info_nia(nia_estado)
            if taquilla_index is None:
                taquilla_index = get_taquilla_info_name(taquilla_estado)
            if taquilla_index is not None:
                taquilla = taquillas_reservadas[taquilla_index[0]][taquilla_index[1]][taquilla_index[2]][taquilla_index[3]]

                taquilla_col, nia_col, estado_col, nombre_col, apellidos_col = st.columns(5)
                with taquilla_col:
                    st.write("Taquilla", value=taquilla[0], key=taquilla[0])
                    st.write(taquilla[0])
                with nia_col:
                    st.write("NIA", value=taquilla[1], key=taquilla[1])
                    st.write(taquilla[1])
                with estado_col:
                    index = ["Reservada", "Ocupada", "No Disponible"].index(taquilla[2])
                    new_state = st.selectbox("Estado", options=["Reservada", "Ocupada", "No Disponible"], index=index, key=taquilla[2])
                    # st.write("Estado", value=taquilla[2], key=taquilla[2])
                    # st.write(taquilla[2])
                with nombre_col:
                    st.write("Nombre", value=taquilla[3], key=taquilla[3])
                    st.write(taquilla[3])
                with apellidos_col:
                    st.write("Apellidos", value=taquilla[4], key=taquilla[4])
                    st.write(taquilla[4])

                #st.write(taquilla) - Alternativa fea
                if st.button("Cambiar estado"):
                    taquilla[2] = new_state
                    with open(reservadas_path, "w") as f:
                        json.dump(taquillas_reservadas, f, indent=4)
                    st.success("Cambiado a " + new_state.lower())
                    st.toast("Cambiado a " + new_state.lower(), icon='🎉')
            else:
                st.error("No se ha encontrado tu reserva")

        with mod_tab:
            st.title("Cambia datos de la reserva:")
            st.warning("Para cambiar la taquilla, es necesario borrar la reserva y realizar otra")

            # Para que no se quede sin taquilla, primero que haga otra reserva con un NIA bogus y luego borramos
            nia_mod_col, taquilla_mod_col = st.columns(2)
            with nia_mod_col:
                nia_mod_estado = st.text_input("Introduce el NIA a consultar", key="NIA_mod")
            with taquilla_mod_col:
                taquilla_mod_estado = st.text_input("Introduce el nombre de la taquilla a consultar", key="taquilla_mod")

            taquilla_mod_index = get_taquilla_info_nia(nia_mod_estado)
            if taquilla_mod_index is None:
                taquilla_mod_index = get_taquilla_info_name(taquilla_mod_estado)
            if taquilla_mod_index is not None:
                taquilla_mod = taquillas_reservadas[taquilla_mod_index[0]][taquilla_mod_index[1]][taquilla_mod_index[2]][taquilla_mod_index[3]]

                taquilla_col, nia_col, estado_col, nombre_col, apellidos_col = st.columns(5)
                with taquilla_col:
                    st.write("Taquilla", value=taquilla_mod[0], key=taquilla_mod[0])
                    st.write(taquilla_mod[0])
                with nia_col:
                    new_nia = st.text_input("NIA", value=taquilla_mod[1], key=taquilla_mod[1])
                with estado_col:
                    #taquilla_mod[2] = st.text_input("Estado", value=taquilla_mod[2], key=taquilla_mod[2]+"mod")
                    index = ["Reservada", "Ocupada", "No Disponible"].index(taquilla_mod[2])
                    new_state = st.selectbox("Estado", options=["Reservada", "Ocupada", "No Disponible"], index=index,
                                             key=taquilla_mod[2]+"mod_selectbox")
                with nombre_col:
                    taquilla_mod[3] = st.text_input("Nombre", value=taquilla_mod[3], key=taquilla_mod[3])
                with apellidos_col:
                    taquilla_mod[4] = st.text_input("Apellidos", value=taquilla_mod[4], key=taquilla_mod[4])

                #st.write(taquilla_mod)
                #st.write(taquillas_reservadas)

                if st.button("Cambiar"):
                    if re.match(r"100[0-9]{6}", new_nia):
                        taquilla_mod[2] = new_state
                        with open(reservadas_path, "w") as f:
                            json.dump(taquillas_reservadas, f, indent=4)
                        if taquilla_mod[1] in str(taquillas_reservadas):
                            st.success("Cambiado")
                            st.toast("Cambiado", icon='🎉')

            else:
                st.error("No se ha encontrado tu reserva")


        with del_tab:
            st.title("Elimina una reserva")
            st.warning("¡El borrado de una reserva no se puede deshacer!")
            nia_del_col, taquilla_del_col = st.columns(2)
            with nia_del_col:
                nia_del_estado = st.text_input("Introduce el NIA de la reserva a eliminar", key="NIA_del")
            with taquilla_del_col:
                taquilla_del_estado = st.text_input("Introduce el nombre de la taquilla a consultar", key="taquilla_del")

            taquilla_del_index = get_taquilla_info_nia(nia_del_estado)
            if taquilla_del_index is None:
                taquilla_del_index = get_taquilla_info_name(taquilla_del_estado)
            if taquilla_del_index is not None:
                taquilla_delete = taquillas_reservadas[taquilla_del_index[0]][taquilla_del_index[1]][taquilla_del_index[2]][taquilla_del_index[3]]

                taquilla_col, nia_col, estado_col, nombre_col, apellidos_col = st.columns(5)
                with taquilla_col:
                    st.write("Taquilla", value=taquilla_delete[0], key=taquilla_delete[0])
                    st.write(taquilla_delete[0])
                with nia_col:
                    st.write("NIA", value=taquilla_delete[1], key=taquilla_delete[1])
                    st.write(taquilla_delete[1])
                with estado_col:
                    st.write("Estado", value=taquilla_delete[2], key=taquilla_delete[2])
                    st.write(taquilla_delete[2])
                with nombre_col:
                    st.write("Nombre", value=taquilla_delete[3], key=taquilla_delete[3])
                    st.write(taquilla_delete[3])
                with apellidos_col:
                    st.write("Apellidos", value=taquilla_delete[4], key=taquilla_delete[4])
                    st.write(taquilla_delete[4])


                modal = Modal(key="Demo Modal", title="")
                auth = False
                message_success = None
                show_confirmation = False
                if st.button(":red[Eliminar_new]", key="confirmation_button_eliminar"):
                    show_confirmation = True

                if show_confirmation:
                    st.error("¡El borrado de una reserva no se puede deshacer!  \n Estás seguro de que quieres borrar la reserva de " + taquilla_delete[3] + " " + taquilla_delete[4] + ": " + taquilla_delete[0] + " ?")
                    cancel_column,_,_,_,_,_,_,del_column = st.columns(8)
                    with cancel_column:
                        if st.button("Cancelar"):
                            print("Close button clicked")
                            show_confirmation = False
                    with del_column:
                        if st.button(":red[Delete]"):
                            print("Delete button clicked")
                            edificio = taquilla_del_index[0]
                            planta = taquilla_del_index[1]
                            bloque = taquilla_del_index[2]
                            st.write(edificio, planta, bloque)
                            st.write(taquilla_delete[0])
                            taquillas_reservadas[edificio][planta][bloque].remove(taquilla_delete)
                            with open(reservadas_path, "w") as f:
                                json.dump(taquillas_reservadas, f, indent=4)
                            with open(disponibles_path, "r") as f:
                                taquillas_disponibles = json.load(f)
                            taquillas_disponibles[edificio][planta][bloque].append(taquilla_delete[0])
                            taquillas_disponibles[edificio][planta][bloque] = sorted(
                                taquillas_disponibles[edificio][planta][bloque],
                                key=lambda num: num[-3:])
                            with open(disponibles_path, "w") as f:
                                json.dump(taquillas_disponibles, f, indent=4)
                            st.success("Eliminado")
                            st.toast("Eliminado", icon='🎉')


                open_modal = st.button(":red[Eliminar]", key="confirmation_button")
                if open_modal:
                    modal.open()
                if modal.is_open():
                    nombre_taquilla = taquilla_delete[0]
                    nombre = taquilla_delete[3]
                    apellidos = taquilla_delete[4]
                    with modal.container():
                        st.markdown(
                            f'<p style="color:{"#da2724"};font-size:36px;border-radius:2%;">Confirmación de eliminación</p>',
                            unsafe_allow_html=True)
                        content = "¿Estás seguro de que quieres borrar la reserva de " + nombre + " " + apellidos + ": " + \
                                  taquilla_delete[0] + " ?"
                        st.markdown(
                            f'<p style="text-align:left;color:{"#da2724"};font-size:24px;border-radius:2%;">{content}</p>',
                            unsafe_allow_html=True)
                        st.markdown(
                            f'<p style="text-align:left;color:{"#da2724"};font-size:24px;border-radius:2%;">{"¿Estás seguro? No se puede deshacer"}</p>',
                            unsafe_allow_html=True)
                        left_column, right_column = st.columns(2)
                        with left_column:
                            if st.button("Cancelar"):
                                print("Close button clicked")
                                modal.close()
                        with right_column:
                            if st.button(":red[Delete]"):
                                print("Delete button clicked")
                                edificio = taquilla_del_index[0]
                                planta = taquilla_del_index[1]
                                bloque = taquilla_del_index[2]
                                st.write(edificio, planta, bloque)
                                st.write(taquilla_delete[0])
                                taquillas_reservadas[edificio][planta][bloque].remove(taquilla_delete)
                                with open(reservadas_path, "w") as f:
                                    json.dump(taquillas_reservadas, f, indent=4)
                                with open(disponibles_path, "r") as f:
                                    taquillas_disponibles = json.load(f)
                                taquillas_disponibles[edificio][planta][bloque].append(taquilla_delete[0])
                                taquillas_disponibles[edificio][planta][bloque] = sorted(
                                    taquillas_disponibles[edificio][planta][bloque],
                                    key=lambda num: num[-3:])
                                with open(disponibles_path, "w") as f:
                                    json.dump(taquillas_disponibles, f, indent=4)
                                st.success("Eliminado")
                                st.toast("Eliminado", icon='🎉')
                                modal.close()

            else:
                st.error("No se ha encontrado tu reserva")
        with add_tab:
            st.subheader("Añadir bloque")
            st.write("Añade un bloque de taquillas a un edificio y planta concretos.")
            st.write("Utiliza esto como último recurso, si no puedes contactar con el administrador y que no tiene acceso al código fuente.")
            st.write("Si no sabes lo que estás haciendo, no lo hagas. :smile:")

            edificio_add_col, planta_add_col = st.columns(2)
            with open("disponibles.json", "r") as f:
                taquillas_disponibles = json.load(f)
            with edificio_add_col:
                edificio_add = st.selectbox("Edificio", options=list(taquillas_disponibles.keys()), key="edificio_add")
            with planta_add_col:
                planta_add = st.selectbox("Planta", options=list(taquillas_disponibles[edificio_add].keys()), key="planta_add")
            st.warning("¡Asegúrate de que el bloque que vas a añadir no existe ya!")
            bloques_disponibles = ""
            for bloque in taquillas_disponibles[edificio_add][planta_add]:
                bloques_disponibles += bloque
                bloques_disponibles += ", "
            st.write("Bloques disponibles: " + bloques_disponibles)
            st.image("images/" + IMAGES[edificio_add][planta_add], width=500)

            st.write("Para añadir un bloque, pon el nombre del bloque y las taquillas disponibles, separadas por comas y espacio.")
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



    ################################################################################################################

    # Dudas
    st.write("Si tienes alguna duda, consulta el manual de usuario en la [carpeta de Google Drive](https://drive.google.com/drive/folders/15tOcC8FqSK1vdOcjEdqS7Rf1iDFpjzNc?usp=share_link)")


with st.expander("Configuración para Developer:"):
    st.write("Para el indepentiende, hay que poner estos configs:")
    st.code("""
    config_path = "config.yaml"
    reservadas_path = "../reservadas.json"
    disponibles_path = "../disponibles.json"
    """)
    st.write("Y comentar las partes de las autorizaciones y logins:")