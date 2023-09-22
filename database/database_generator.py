import openpyxl
import sqlite3 as sql

db_file = "database.db"


def get_all_information():
    """
    Función hecha por salva para importar del excel a la base de datos de sql.
    :return:
    """
    # Leer el dashboard (excel del que se sacan los datos
    archivo = openpyxl.load_workbook("DASHBOARD.xlsx")
    # Escoger base de datos como página del excel
    sheet = archivo['BASE DE DATOS']

    # Crear variables (return y contador)
    formated_taquillas = []
    i = 3
    # Iterar hasta que no haya nada (fin)
    while sheet[f"A{i}"].value is not None:
        # Indice (del 1 a X)
        taquilla = [i - 3]
        # Formatear edificio/planta/bloque
        # E1 P0 B1 -> (1,0,1)
        indice = sheet[f"A{i}"].value
        edificio = indice[1]
        planta = indice[4]
        bloque = indice[7]
        taquilla.extend((edificio, planta, bloque))
        # Extraer nombre de taquilla
        taquilla.append(sheet[f"B{i}"].value)
        # Añadir la taquilla a la lista
        formated_taquillas.append(taquilla)

        # Aumentar el contador para pasar a la siguiente
        i += 1

    return formated_taquillas

def database_creation():
    conn = sql.connect(db_file)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE Taquillas (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    EDIFICIO CHAR(1),
    PLANTA CHAR(1),
    BLOQUE CHAR(1),
    TAQUILLA CHAR(10),
    ESTADO VARCHAR(20) DEFAULT 'Libre',
    NIA CHAR(9),
    NOMBRE VARCHAR(50),
    APELLIDOS VARCHAR(120),
    CODIGO CHAR(10)
);
""")
    conn.commit()
    conn.close()

def database_importer():
    data = get_all_information()
    """
    I have a list and I want ot import it to my table Taquillas
    :return:
    """
    con = sql.connect(db_file)
    cur = con.cursor()
    sql_text = "INSERT INTO Taquillas (ID, EDIFICIO, PLANTA, BLOQUE, TAQUILLA) values(?, ?, ?, ?, ?)"
    with con:
        con.executemany(sql_text, data)
    con.commit()
    con.close()

def database_deletion():
    conn = sql.connect(db_file)
    cur = conn.cursor()
    cur.execute("DROP TABLE Taquillas")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    database_deletion()
    database_creation()
    database_importer()


