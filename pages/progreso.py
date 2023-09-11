import streamlit as st
import json

with open("disponibles.json", "r") as f:
    taquillas_disponibles = json.load(f)

st.title("Modificar taquilla")
st.write("Aquí puedes modificar los datos de una taquilla concreta.")

nia_mod_col, taquilla_mod_col = st.columns(2)
with nia_mod_col:
nia_mod_estado = st.text_input("Introduce el NIA a consultar", key="NIA_mod")
with taquilla_mod_col:
taquilla_mod_estado = st.text_input("Introduce el nombre de la taquilla a consultar",
                                    key="taquilla_mod")

taquilla_mod_index = get_taquilla_info_nia(nia_mod_estado)
if taquilla_mod_index is None:
taquilla_mod_index = get_taquilla_info_name(taquilla_mod_estado)
if taquilla_mod_index is not None:
taquilla_mod = \
taquillas_reservadas[taquilla_mod_index[0]][taquilla_mod_index[1]][taquilla_mod_index[2]][
    taquilla_mod_index[3]]

taquilla_col, nia_col, estado_col, nombre_col, apellidos_col, codigo_col = st.columns(6)
with taquilla_col:
    st.write("Taquilla", key="taquilla"+taquilla_mod[0])
    st.write(taquilla_mod[0])
with nia_col:
    new_nia = st.text_input("NIA", value=taquilla_mod[1], key="nia"+taquilla_mod[1])
with estado_col:
    # taquilla_mod[2] = st.text_input("Estado", value=taquilla_mod[2], key=taquilla_mod[2]+"mod")
    index = ["Reservada", "Ocupada", "No Disponible"].index(taquilla_mod[2])
    new_state = st.selectbox("Estado", options=["Reservada", "Ocupada", "No Disponible"], index=index,
                             key=taquilla_mod[2] + "mod_selectbox")
with nombre_col:
    taquilla_mod[3] = st.text_input("Nombre", value=taquilla_mod[3], key="nombre"+taquilla_mod[3])
with apellidos_col:
    taquilla_mod[4] = st.text_input("Apellidos", value=taquilla_mod[4], key="apellido"+taquilla_mod[4])
with codigo_col:
    st.write("Código", key="código_mod")
    st.write(taquilla_mod[5])

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

# Botón para modificar la taquilla
if st.button("Modificar"):
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

# Reservar taquilla
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