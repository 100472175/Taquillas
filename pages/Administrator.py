import streamlit as st
import streamlit_authenticator as stauth
import json
import yaml
from yaml.loader import SafeLoader

with open('pages/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

def get_taquilla_info_nia(nia):
    with open("reservadas.json", "r") as f:
        taquillas_reservadas = json.load(f)
    for edificio_key, edificio in taquillas_reservadas.items():
        for planta_key, planta in edificio.items():
            for bloque_key, bloque in planta.items():
                for reserva_key in range(len(bloque)):
                    if bloque[reserva_key][1] == nia:
                        return edificio_key, planta_key, bloque_key, reserva_key
    return None

def get_taquilla_info_name(nombre):
    with open("reservadas.json", "r") as f:
        taquillas_reservadas = json.load(f)
    for edificio_key, edificio in taquillas_reservadas.items():
        for planta_key, planta in edificio.items():
            for bloque_key, bloque in planta.items():
                for reserva_key in range(len(bloque)):
                    if bloque[reserva_key][1] == nombre:
                        return edificio_key, planta_key, bloque_key, reserva_key
    return None

if st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')
elif st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')
    st.write(f'Bienvenido *{st.session_state["name"]}*')
    st.write("Desde aqui podemos cambiar las cosas para que se vean en la página web quien ha pagado y quien no.")

    with open("reservadas.json", "r") as f:
        taquillas_reservadas = json.load(f)

    estado_tab, mod_tab, del_tab = st.tabs(["Cambiar estado", "Modificar Reserva", "Eliminar Reserva"])

    with estado_tab:
        st.title("Cambia el estado de la taquilla:")
        st.subheader("Comprueba que han pagado la taquilla antes de darles el status de ocupada")
        nia_estado_col, taquilla_estado_col = st.columns(2)
        with nia_estado_col:
            nia_estado = st.text_input("Introduce el NIA a consultar")
        with taquilla_estado_col:
            taquilla_estado = st.text_input("Introduce el nombre de la taquilla a consultar")

        taquilla_index = get_taquilla_info_nia(nia_estado)
        if taquilla_index is None:
            taquilla_index = get_taquilla_info_name(taquilla_estado)
        if taquilla_index is not None:
            taquilla = taquillas_reservadas[taquilla_index[0]][taquilla_index[1]][taquilla_index[2]][taquilla_index[3]]

            #st.write("Es tu taquilla la : " + taquilla[0] + " ?")
            st.write(taquilla)
            if st.button("Cambiar estado a ocupada"):
                taquilla[2] = "Ocupada"
                with open("reservadas.json", "w") as f:
                    json.dump(taquillas_reservadas, f, indent=4)
                st.success("Cambiado estado a ocupada")
        else:
            st.error("No se ha encontrado tu reserva")

    with mod_tab:
        st.title("Cambia otro dato de la taquilla:")
        st.warning("""Recuerda no cambiar la taquilla reservada, solo el NIA, el estado, el nombre o los apellidos.  
                           Si se quiere cambiar la taquilla, pasa al siguiente apartado\n""")
        nia_mod_col, taquilla_mod_col = st.columns(2)
        with nia_mod_col:
            nia_mod_estado = st.text_input("Introduce el NIA a consultar", key="NIA_mod")
        with taquilla_mod_col:
            taquilla_mod_estado = st.text_input("Introduce el nombre de la taquilla a consultar", key="taquilla_mod")

        taquilla_mod_index = get_taquilla_info_nia(nia_mod_estado)
        if taquilla_mod_index is None:
            taquilla_mod_index = get_taquilla_info_name(taquilla_estado)
        if taquilla_mod_index is not None:
            taquilla_mod = taquillas_reservadas[taquilla_mod_index[0]][taquilla_mod_index[1]][taquilla_mod_index[2]][taquilla_mod_index[3]]

            taquilla_col, nia_col, estado_col, nombre_col, apellidos_col = st.columns(5)
            with taquilla_col:
                st.write("Taquilla", value=taquilla_mod[0], key=taquilla_mod[0])
                st.write(taquilla_mod[0])
            with nia_col:
                new_nia = st.text_input("NIA", value=taquilla_mod[1], key=taquilla_mod[1])
            with estado_col:
                taquilla_mod[2] = st.text_input("Estado", value=taquilla_mod[2], key=taquilla_mod[2])
            with nombre_col:
                taquilla_mod[3] = st.text_input("Nombre", value=taquilla_mod[3], key=taquilla_mod[3])
            with apellidos_col:
                taquilla_mod[4] = st.text_input("Apellidos", value=taquilla_mod[4], key=taquilla_mod[4])

            st.write(taquilla_mod)
            st.write(taquillas_reservadas)

            if st.button("Cambiar"):
                with open("reservadas.json", "w") as f:
                    json.dump(taquillas_reservadas, f, indent=4)
                print(taquilla_mod)
                if taquilla_mod[1] in str(taquillas_reservadas):
                    st.success("Cambiado")

        else:
            st.error("No se ha encontrado tu reserva")


    with del_tab:
        st.title("Elimina una reserva")

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
        else:
            st.error("No se ha encontrado tu reserva")

        if st.button("Eliminar"):
            edificio = taquilla_del_index[0]
            planta = taquilla_del_index[1]
            bloque = taquilla_del_index[2]
            st.write(edificio, planta, bloque)
            st.write(taquilla_delete[0])
            taquillas_reservadas[edificio][planta][bloque].remove(taquilla_delete)
            with open("reservadas.json", "w") as f:
                json.dump(taquillas_reservadas, f, indent=4)
            st.success("Eliminado")
            with open("disponibles.json", "r") as f:
                taquillas_disponibles = json.load(f)
            taquillas_disponibles[edificio][planta][bloque].append(taquilla_delete[0])
            taquillas_disponibles[edificio][planta][bloque] = sorted(taquillas_disponibles[edificio][planta][bloque],
                                                                     key=lambda num: num[-3:])
            with open("disponibles.json", "w") as f:
                json.dump(taquillas_disponibles, f, indent=4)