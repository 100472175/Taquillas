import sqlite3 as sql
import pandas as pd
from authentication.code_generator import generate_code

db_file = "database/database.db"
def create_connection(db_file = db_file):
    conn = sql.connect(db_file)
    return conn

def taquillas_por_nia(nia):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Taquillas WHERE NIA = ?", (nia,))
    rows = cur.fetchall()
    conn.close()
    return rows[0][0]


def edificios_disponibles() -> list:
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT(EDIFICIO) FROM Taquillas")
    rows = cur.fetchall()
    conn.close()
    result = []
    for i in range(len(rows)):
        result.append(rows[i][0])
    return result

def plantas_por_edificio(edificio):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT(PLANTA) FROM Taquillas WHERE EDIFICIO = ? AND ESTADO = ?", (edificio, 'Libre',))
    rows = cur.fetchall()
    conn.close()
    result = []
    for i in range(len(rows)):
        result.append(rows[i][0])
    return result

def bloques_por_planta(edificio, planta):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT(BLOQUE) FROM Taquillas WHERE EDIFICIO = ? AND PLANTA = ? AND ESTADO = ?", (edificio, planta, 'Libre',))
    rows = cur.fetchall()
    conn.close()
    result = []
    for i in range(len(rows)):
        result.append(rows[i][0])
    return result

def bloques_por_planta_todas(edificio, planta):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT(BLOQUE) FROM Taquillas WHERE EDIFICIO = ? AND PLANTA = ? ORDER BY ID", (edificio, planta,))
    rows = cur.fetchall()
    conn.close()
    result = []
    for i in range(len(rows)):
        result.append(rows[i][0])
    return result

def taquillas_por_bloque(edificio, planta, bloque):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT(TAQUILLA) FROM Taquillas WHERE EDIFICIO = ? AND PLANTA = ? AND BLOQUE = ? AND ESTADO = ?", (edificio, planta, bloque, 'Libre',))
    rows = cur.fetchall()
    conn.close()
    result = []
    for i in range(len(rows)):
        result.append(rows[i][0])
    return result

def taquillas_por_bloque_todas(edificio, planta, bloque):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Taquillas WHERE EDIFICIO = ? AND PLANTA = ? AND BLOQUE = ?", (edificio, planta, bloque,))
    rows = cur.fetchall()
    conn.close()
    result = []
    for i in range(len(rows)):
        result.append(rows[i])
    return result

def taquillas_ocupadas_por_bloque(edificio, planta, bloque):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Taquillas WHERE EDIFICIO = ? AND PLANTA = ? AND BLOQUE = ? AND ESTADO IN (?, ?) ",
                (edificio, planta, bloque, 'Ocupada', 'Reservada',))
    rows = cur.fetchall()
    conn.close()
    return rows[0][0]
def taquillas_totales_por_bloque(edificio, planta, bloque):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Taquillas WHERE EDIFICIO = ? AND PLANTA = ? AND BLOQUE = ?", (edificio, planta, bloque,))
    rows = cur.fetchall()
    conn.close()
    return rows[0][0]

def get_status_taquilla(taquilla):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT ESTADO FROM Taquillas WHERE TAQUILLA = ?", (taquilla,))
    rows = cur.fetchall()
    conn.close()
    return rows[0][0]


def hacer_reserva(taquilla, nia, nombre, apellidos):
    conn = create_connection()
    cur = conn.cursor()
    code = generate_code()
    cur.execute("UPDATE Taquillas SET ESTADO = 'Reservada', NIA = ?, NOMBRE = ?, APELLIDOS = ?, CODIGO = ?  WHERE TAQUILLA = ?", (nia, nombre, apellidos, code, taquilla,))
    conn.commit()
    conn.close()
    return code

def get_info_taquilla_nia(nia):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Taquillas WHERE NIA = ?", (nia,))
    rows = cur.fetchall()
    conn.close()
    if len(rows) == 0:
        return None
    for reserva in rows:
        result = []
        for i in reserva:
            result.append(i)
        return result

def get_info_taquilla_codigo(code):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Taquillas WHERE TAQUILLA = ?", (code,))
    rows = cur.fetchall()
    conn.close()
    match len(rows):
        case 0:
            return None
        case 1:
            return list(rows[0])

def update_taquila_estado(taquilla, estado):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Taquillas SET ESTADO = ? WHERE TAQUILLA = ?", (estado, taquilla,))
    conn.commit()
    conn.close()

def update_taquilla_codigo(taquilla, codigo):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Taquillas SET CODIGO = ? WHERE TAQUILLA = ?", (codigo, taquilla,))
    conn.commit()
    conn.close()

def update_taquilla_completo(taquilla, nia, estado, nombre, apellidos):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Taquillas SET NIA = ?, ESTADO = ?, NOMBRE = ?, APELLIDOS = ? WHERE TAQUILLA = ?", (nia, estado, nombre, apellidos, taquilla,))
    conn.commit()
    conn.close()

def delete_taquilla_reserva(taquilla):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Taquillas SET NIA = NULL, ESTADO = 'Libre', NOMBRE = NULL, APELLIDOS = NULL, CODIGO = NULL WHERE TAQUILLA = ?", (taquilla,))
    conn.commit()
    conn.close()

def change_taquilla(taquilla, new_taquilla, nia, nombre, apellidos):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Taquillas WHERE TAQUILLA = ?", (new_taquilla,))
    rows = cur.fetchall()
    new_row = rows[0]
    conn.commit()
    conn.close()
    delete_taquilla_reserva(taquilla)
    code = hacer_reserva(new_taquilla, nia, nombre, apellidos)
    return code

def taquillas_not_libres():
    cnx = create_connection()
    df = pd.read_sql_query("SELECT * FROM Taquillas WHERE ESTADO IN ('Reservada', 'Ocupada')", cnx)
    cnx.close()
    return df

def taquillas_libres():
    cnx = create_connection()
    df = pd.read_sql_query("SELECT * FROM Taquillas WHERE ESTADO = 'Libre'", cnx)
    cnx.close()
    return df

def taquillas_rotas():
    cnx = create_connection()
    df = pd.read_sql_query("SELECT * FROM Taquillas WHERE ESTADO = 'No Disponible'", cnx)
    cnx.close()
    return df

def reset_database():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""UPDATE Taquillas
SET NIA = NULL, NOMBRE = NULL, APELLIDOS = NULL, CODIGO = NULL,
    ESTADO = CASE
                WHEN ESTADO <> 'No Disponible' THEN 'Libre'
                ELSE ESTADO
             END;
    """)
    conn.commit()
    conn.close()



if __name__ == "__main__":
    print(get_info_taquilla_codigo('1.0.E.P001'))