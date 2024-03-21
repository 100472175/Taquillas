import random
import string
import sqlite3 as sql
import openpyxl
import streamlit_authenticator as stauth
from authentication.send_passwords_email import send_email_password


def crear_tabla_credenciales() -> None:
    """
    Crea la tabla "credenciales" en la base de datos
    :return:
    """
    base = sql.connect("database/database.db")
    bd = base.cursor()
    bd.execute("CREATE TABLE credenciales("
               "user varchar(25),"
               "name varchar(25),"
               "email varchar(9),"
               "rol varchar(10) default 'despacho',"
               "passowrd char(9),"
               "PRIMARY KEY (user))")
    base.close()


def borrar_tabla_credenciales() -> None:
    """
    Borra la tabla credenciales de la base de datos
    :return: None
    """
    base = sql.connect("database/database.db")
    bd = base.cursor()
    bd.execute("DROP TABLE credenciales")
    base.close()


def hash_password(password) -> str:
    """
    Hashea una contraseña
    :param password: Contraseña a hashear
    :return: Contraseña hasheada
    """
    hashed = stauth.Hasher([password]).generate()
    return hashed[0]


def insertar_user(user: str, name: str, email, rol="despacho", psswd=None) -> None:
    """
    Inserta un usuario en la base de datos
    :param user: Nombre del usuario, con el formato n_apellido
    :param name: Nombre completo del usuario, con el formato Nombre Apellido1 Apellido2
    :param email: Correo del usuario, con el formato 100XXXXXX@alumnos.uc3m.es
    :param rol: Por defecto es despacho, pero si es escuela se pone escuela
    :param psswd: Contraseña del usuario, si no se pone se genera una aleatoria
    :return:
    """
    if not psswd:
        psswd = generate_password()
    hashed = stauth.Hasher([psswd]).generate()
    if rol != "escuela":
        rol = "despacho"

    # Open the file in read mode
    with open("authentication/config.yaml", "r") as f:
        # Load the file
        config = stauth.yaml.load(f, Loader=stauth.yaml.FullLoader)
        print(config)
    # Add the new user
    config["credentials"]["usernames"][user] = {'email': email, 'name': name, 'rol': rol, 'password': hashed[0]}
    print("-------------------" * 4)
    print(config)
    # Open the file in write mode to overwrite the previous content
    with open("authentication/config.yaml", "w") as f:
        stauth.yaml.dump(config, f)


def delete_user(user) -> None:
    """
    Borra un usuario de la base de datos
    :param user: Nombre de usuario, con el formato n_apellido
    :return: None
    """
    with open("authentication/config.yaml", "r") as f:
        config = stauth.yaml.load(f, Loader=stauth.yaml.FullLoader)
    if user in config["credentials"]["usernames"]:
        if config["credentials"]["usernames"][user]["rol"] != "escuela":
            del config["credentials"]["usernames"][user]
        else:
            raise ValueError("No se puede borrar un usuario de que tenga rol escuela")
    else:
        raise ValueError("El usuario solicitado no existe")

    with open("authentication/config.yaml", "w") as f:
        stauth.yaml.dump(config, f)


def get_user(user) -> dict | None:
    """
    Devuelve la información de un usuario
    :param user: Nombre de
    :return:
    """
    with open("authentication/config.yaml", "r") as f:
        config = stauth.yaml.load(f, Loader=stauth.yaml.FullLoader)
    return config["credentials"]["usernames"][user]


def get_users_list() -> list:
    """
    Devuelve una lista con los nombres de todos los usuarios
    :return:
    """
    with open("authentication/config.yaml", "r") as f:
        config = stauth.yaml.load(f, Loader=stauth.yaml.FullLoader)
    # Filter the users that are not from the school
    return [user for user in config["credentials"]["usernames"].keys() if config["credentials"]["usernames"][user]["rol"] != "escuela"]


def generate_password() -> str:
    """
    Genera una contraseña aleatoria de 9 caracteres con el formato XXXX-XXXX
    :return:
    """
    content = ''
    for _ in range(4):
        rand = random.choice(string.ascii_letters)
        content += rand
    content += '-'
    for _ in range(4):
        rand = random.choice(string.ascii_letters)
        content += rand
    return content.upper()


def mod_password(user) -> str:
    """
    Modifica la contraseña de un usuario de la base de datos por una aleatoria
    :param user: Nombre de usuario, con el formato n_apellido
    :return: Contraseña aleatoria generada para el usuario
    """
    base = sql.connect("database/database.db")
    bd = base.cursor()
    new_password = generate_password()
    bd.execute("UPDATE credenciales SET contrasena = ? WHERE usuario=?", (new_password, user))
    base.commit()
    base.close()
    return new_password


def add_all_users(origin, destination) -> None:
    """
    Añade todos los usuarios de un excel a la base de datos
    :param origin: Ruta del excel de origen
    :param destination: Ruta del excel de destino, con las contraseñas añadidas
    :return: None
    """
    with open(origin, "r") as f:
        base = openpyxl.load_workbook(origin)
        sheet = base["Hoja1"]
        i = 2
        while sheet[f"A{i}"].value is not None:
            sheet[f"E{i}"].value = insertar_user(sheet[f"A{i}"].value, sheet[f"B{i}"].value, sheet[f"C{i}"].value,
                                                 sheet[f"D{i}"].value, sheet[f"E{i}"].value)
            i += 1
        base.save(destination)


if __name__ == "__main__":
    if input("¿Qué quieres hacer?") == "todo":
        archivo = openpyxl.load_workbook("pax_atencion.xlsx")
        sheet = archivo["Hoja1"]
        i = 2
        while sheet[f"A{i}"].value is not None:
            sheet[f"E{i}"].value, sheet[f"F{i}"].value = insertar_user(sheet[f"A{i}"].value, sheet[f"B{i}"].value,
                                                                       sheet[f"C{i}"].value, sheet[f"D{i}"].value,
                                                                       sheet[f"E{i}"].value)
            print(sheet[f"A{i}"].value)  # Name
            print(sheet[f"B{i}"].value)  # User
            print(sheet[f"C{i}"].value)  # NIA
            print(sheet[f"D{i}"].value)  # Rol (Escuela si o no)
            print(sheet[f"E{i}"].value)  # Password
            print(sheet[f"F{i}"].value)  # Hashed
            i += 1
        archivo.save("tax.xlsx")
    else:
        password = input("contraseña: ")
        b = stauth.Hasher([password]).generate()
        print(b)
