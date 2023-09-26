import random
import string
import sqlite3 as sql
import openpyxl
import streamlit_authenticator as stauth



def crear_tabla_credenciales():
    base = sql.connect("database/database.db")
    bd = base.cursor()
    bd.execute("CREATE TABLE credenciales("
               "usuario varchar(25),"
               "contrasena char(9),"
               "rol varchar(10) default 'despacho',"
               "PRIMARY KEY (usuario))")
    base.close()


def borrar_tabla_credenciales():
    base = sql.connect("database/database.db")
    bd = base.cursor()
    bd.execute("DROP TABLE credenciales")
    base.close()


def insertar_user(name, user, nia, rol, password=None):
    if password is None:
        password = [generate_password()]
    else:
        password = [password]
    hashed = stauth.Hasher(password).generate()
    if rol != "escuela":
        rol = "despacho"
    # base = sql.connect("database/database.db")
    # bd = base.cursor()
    # bd.execute("INSERT INTO credenciales values(?, ?, ?)", (user, generate_password(), rol))
    # base.commit()
    # base.close()
    # with open("authentication/config.yaml", "r") as f:
    #     config = stauth.yaml.load(f, Loader=stauth.yaml.FullLoader)
    # config["credentials"]["usernames"][user] = {'email': f"{nia}@alumnos.uc3m.es", 'name': name, 'role': rol, 'password': hashed[0]}

    return password[0], hashed[0]


def del_user(user):
    base = sql.connect("database/database.db")
    bd = base.cursor()
    bd.execute("DELETE FROM credenciales WHERE usuario=?", (user,))
    base.commit()
    base.close()


def generate_password():
    content = ''
    for _ in range(4):
        rand = random.choice(string.ascii_letters)
        content += rand
    content += '-'
    for _ in range(4):
        rand = random.choice(string.ascii_letters)
        content += rand
    return content.upper()


def mod_password(user):
    base = sql.connect("database/database.db")
    bd = base.cursor()
    bd.execute("UPDATE credenciales SET contrasena = ? WHERE usuario=?", (generate_password(), user))
    base.commit()
    base.close()

def add_all_users(origin, destination):
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
    if input() == "todo":
        archivo = openpyxl.load_workbook("pax_atencion.xlsx")
        sheet = archivo["Hoja1"]
        i = 2
        while sheet[f"A{i}"].value is not None:
            sheet[f"E{i}"].value, sheet[f"F{i}"].value = insertar_user(sheet[f"A{i}"].value, sheet[f"B{i}"].value, sheet[f"C{i}"].value, sheet[f"D{i}"].value, sheet[f"E{i}"].value)
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


