import random
import string
import sqlite3 as sql
import openpyxl
import streamlit_authenticator as stauth


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


def insertar_user(user, name, email, rol="despacho", psswd=None) -> tuple:
    """
    Inserta un usuario en la base de datos
    :param user: Nombre del usuario, con el formato n_apellido
    :param name: Nombre completo del usuario, con el formato Nombre Apellido1 Apellido2
    :param email: Correo del usuario, con el formato 100XXXXXX@alumnos.uc3m.es
    :param rol: Por defecto es despacho, pero si es escuela se pone escuela
    :param psswd: Contraseña del usuario, si no se pone se genera una aleatoria
    :return:
    """
    """
    #Importante: ACTUALMENTE NO FUNCIONA, Y SOLO DEVUELVE LA CONTRASEÑA Y EL HASH PARA QUE SE PUEDA INSERTAR EN CONFIG.YAML
    Cuando se quiera cambiar, hay que cambiar las lineas comentadas por las no comentadas.
    """
    if psswd is None:
        psswd = generate_password()
    else:
        psswd = psswd
    hashed = stauth.Hasher([psswd]).generate()
    if rol != "escuela":
        rol = "despacho"
    # base = sql.connect("database/database.db")
    # bd = base.cursor()
    # bd.execute("INSERT INTO credenciales values(?, ?, ?, ?, ?)", (user, name, email, rol, hashed[0]))
    # base.commit()
    # base.close()
    # with open("authentication/config.yaml", "r") as f:
    #     config = stauth.yaml.load(f, Loader=stauth.yaml.FullLoader)
    # config["credentials"]["usernames"][user] = {'email': f"{nia}@alumnos.uc3m.es", 'name': name, 'role': rol, 'password': hashed[0]}
    return psswd, hashed[0]


def del_user(user) -> None:
    """
    Borra un usuario de la base de datos
    :param user: Nombre de usuario, con el formato n_apellido
    :return: None
    """
    base = sql.connect("database/database.db")
    bd = base.cursor()
    bd.execute("DELETE FROM credenciales WHERE usuario=?", (user,))
    base.commit()
    base.close()


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
