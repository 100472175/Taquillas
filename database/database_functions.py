import pandas as pd
import sqlite3 as sql
from confirmation.code_generator import generate_code

db_file = "database/database.db"


def create_connection(db_file=db_file):
    conn = sql.connect(db_file)
    return conn


def taquillas_por_nia(nia) -> int:
    """
    Devuelve el número de las taquillas reservadas por un usuario dada un NIA
    :param nia:
    :return: int
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Taquillas WHERE NIA = ?", (nia,))
    rows = cur.fetchall()
    conn.close()
    return rows[0][0]


def edificios_disponibles() -> list:
    """
    Devuelve una lista con los distintos edificios donde hay taquillas disponibles obtenida con sql
    :return: lista con los distintos edificios done hay taquillas disponibles
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT(EDIFICIO) FROM Taquillas WHERE ESTADO = ?", ('Libre',))
    rows = cur.fetchall()
    conn.close()
    result = []
    for i in range(len(rows)):
        result.append(rows[i][0])
    return result


def plantas_por_edificio(edificio) -> list:
    """
    Lista de las distintas plantas que hay en un edificio obtenida con sql
    :param edificio:
    :return: lista de las distintas plantas que hay en un edificio
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT(PLANTA) FROM Taquillas WHERE EDIFICIO = ? AND ESTADO = ?", (edificio, 'Libre',))
    rows = cur.fetchall()
    conn.close()
    result = []
    for i in range(len(rows)):
        result.append(rows[i][0])
    return result


def bloques_por_planta(edificio, planta) -> list:
    """
    Lista de los distintos bloques que hay en una planta de un edificio obtenida con sql
    :param edificio:
    :param planta:
    :return: lista de los distintos bloques que hay en una planta de un edificio
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT(BLOQUE) FROM Taquillas WHERE EDIFICIO = ? AND PLANTA = ? AND ESTADO = ?",
                (edificio, planta, 'Libre',))
    rows = cur.fetchall()
    conn.close()
    result = []
    for i in range(len(rows)):
        result.append(rows[i][0])
    return result


def bloques_por_planta_todas(edificio, planta) -> list:
    """
    Lista de los distintos bloques que hay en una planta de un edificio obtenida con sql, tanto los libres
    como los ocupados
    :param edificio:
    :param planta:
    :return: lista de los distintos bloques que hay en una planta de un edificio
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT(BLOQUE) FROM Taquillas WHERE EDIFICIO = ? AND PLANTA = ? ORDER BY ID",
                (edificio, planta,))
    rows = cur.fetchall()
    conn.close()
    result = []
    for i in range(len(rows)):
        result.append(rows[i][0])
    return result


def taquillas_por_bloque(edificio, planta, bloque) -> list:
    """
    Lista de las distintas taquillas libres que hay en un bloque de una planta de un edificio obtenida con sql
    :param edificio:
    :param planta:
    :param bloque:
    :return: lista de las distintas taquillas libres que hay en un bloque de una planta de un edificio
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT DISTINCT(TAQUILLA) FROM Taquillas WHERE EDIFICIO = ? AND PLANTA = ? AND BLOQUE = ? AND ESTADO = ?",
        (edificio, planta, bloque, 'Libre',))
    rows = cur.fetchall()
    conn.close()
    result = []
    for i in range(len(rows)):
        result.append(rows[i][0])
    return result


def taquillas_por_bloque_todas(edificio, planta, bloque) -> list:
    """
    Lista de todas las taquillas que hay en un bloque de una planta de un edificio obtenida con sql
    :param edificio:
    :param planta:
    :param bloque:
    :return:
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Taquillas WHERE EDIFICIO = ? AND PLANTA = ? AND BLOQUE = ?", (edificio, planta, bloque,))
    rows = cur.fetchall()
    conn.close()
    result = []
    for i in range(len(rows)):
        result.append(rows[i])
    return result


def taquillas_ocupadas_por_bloque(edificio, planta, bloque) -> int:
    """
    Devuelve el número de taquillas ocupadas que hay en un bloque de una planta de un edificio obtenida con sql
    :param edificio:
    :param planta:
    :param bloque:
    :return:
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Taquillas WHERE EDIFICIO = ? AND PLANTA = ? AND BLOQUE = ? AND ESTADO IN (?, ?) ",
                (edificio, planta, bloque, 'Ocupada', 'Reservada',))
    rows = cur.fetchall()
    conn.close()
    return rows[0][0]


def taquillas_totales_por_bloque(edificio, planta, bloque) -> int:
    """
    Devuelve el número de taquillas totales que hay en un bloque de una planta de un edificio obtenida con sql
    :param edificio:
    :param planta:
    :param bloque:
    :return:
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Taquillas WHERE EDIFICIO = ? AND PLANTA = ? AND BLOQUE = ?",
                (edificio, planta, bloque,))
    rows = cur.fetchall()
    conn.close()
    return rows[0][0]


def get_status_taquilla(taquilla) -> str:
    """
    Devuelve el estado de una taquilla, libre, reservada, ocupada o no disponible
    :param taquilla:
    :return:
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT ESTADO FROM Taquillas WHERE TAQUILLA = ?", (taquilla,))
    rows = cur.fetchall()
    conn.close()
    return rows[0][0]


def hacer_reserva(taquilla, nia, nombre, apellidos):
    """
    Hace una reserva de una taquilla, dada la taquilla que se quiere reservar, el nia del usuario que la reserva,
    el nombre y los apellidos del usuario que la reserva. Devuelve el código de la taquilla reservada para que se envie
    el correo electrónicp
    :param taquilla:
    :param nia:
    :param nombre:
    :param apellidos:
    :return:
    """
    conn = create_connection()
    cur = conn.cursor()
    code = generate_code()
    cur.execute(
        "UPDATE Taquillas SET ESTADO = 'Reservada', NIA = ?, NOMBRE = ?, APELLIDOS = ?, CODIGO = ?  WHERE TAQUILLA = ?",
        (nia, nombre, apellidos, code, taquilla,))
    conn.commit()
    conn.close()
    return code


def get_info_taquilla_nia(nia) -> list:
    """
    Devuelve la información de la taquilla reservada por un usuario dada su NIA, únicamente la primera que encuentre
    :param nia:
    :return:
    """
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


def get_info_taquilla_codigo(taquilla) -> list:
    """
    Devuelve la información de la taquilla reservada por un usuario dada su código, únicamente la primera que encuentre
    :param taquilla:
    :return:
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Taquillas WHERE TAQUILLA = ?", (taquilla,))
    rows = cur.fetchall()
    conn.close()
    if len(rows) == 0:
        return None
    else:
        return list(rows[0])


def update_taquilla_estado(taquilla, estado) -> None:
    """
    Actualiza el estado de una taquilla, libre, reservada, ocupada o no disponible
    :param taquilla:
    :param estado:
    :return: Actualiza la base de datos
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Taquillas SET ESTADO = ? WHERE TAQUILLA = ?", (estado, taquilla,))
    conn.commit()
    conn.close()


def update_taquilla_codigo(taquilla, codigo) -> None:
    """
    Actualiza el código de una taquilla, para que se pueda comprobar que el usuario tiene el NIA que dice tener
    :param taquilla:
    :param codigo:
    :return:
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Taquillas SET CODIGO = ? WHERE TAQUILLA = ?", (codigo, taquilla,))
    conn.commit()
    conn.close()


def update_taquilla_completo(taquilla, nia, estado, nombre, apellidos) -> None:
    """
    Actualiza la información de una taquilla, útil para cuando se hace una reserva: el NIA, el estado, el nombre y los
    apellidos
    :param taquilla:
    :param nia:
    :param estado:
    :param nombre:
    :param apellidos:
    :return:
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Taquillas SET NIA = ?, ESTADO = ?, NOMBRE = ?, APELLIDOS = ? WHERE TAQUILLA = ?",
                (nia, estado, nombre, apellidos, taquilla,))
    conn.commit()
    conn.close()


def delete_taquilla_reserva(taquilla) -> None:
    """
    Elimina la reserva de una taquilla, por si alguien la ha hecho por error o se ha equivocado.
    :param taquilla:
    :return:
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Taquillas SET NIA = NULL, ESTADO = 'Libre', NOMBRE = NULL, APELLIDOS = NULL, CODIGO = NULL WHERE TAQUILLA = ?",
        (taquilla,))
    conn.commit()
    conn.close()


def change_taquilla(taquilla, new_taquilla, nia, nombre, apellidos) -> str:
    """
    Cambia la taquilla reservada por un usuario, por si se ha equivocado o quiere cambiarla por otra
    :param taquilla:
    :param new_taquilla:
    :param nia:
    :param nombre:
    :param apellidos:
    :return:
    """
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


def taquillas_not_libres() -> pd.DataFrame:
    """
    Devuelve un dataframe con todas las taquillas que no están libres, es decir, reservadas u ocupadas
    :return:
    """
    cnx = create_connection()
    df = pd.read_sql_query("SELECT * FROM Taquillas WHERE ESTADO IN ('Reservada', 'Ocupada')", cnx)
    cnx.close()
    return df


def taquillas_libres() -> pd.DataFrame:
    """
    Devuelve un dataframe con todas las taquillas que están libres
    :return:
    """
    cnx = create_connection()
    df = pd.read_sql_query("SELECT * FROM Taquillas WHERE ESTADO = 'Libre'", cnx)
    cnx.close()
    return df


def taquillas_rotas() -> pd.DataFrame:
    """
    Devuelve un dataframe con todas las taquillas que están rotas
    :return:
    """
    cnx = create_connection()
    df = pd.read_sql_query("SELECT * FROM Taquillas WHERE ESTADO = 'No Disponible'", cnx)
    cnx.close()
    return df


def reset_database() -> None:
    """
    Resetea la base de datos, poniendo todas las taquillas libres y sin ningún usuario
    :return:
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""UPDATE Taquillas
SET NIA = NULL, NOMBRE = NULL, APELLIDOS = NULL, CODIGO = NULL,
    ESTADO = CASE
                WHEN ESTADO <> 'No Disponible' THEN 'Libre'
                ELSE ESTADO
             END;
    """)
    cur.execute("SELECT COUNT(*) FROM Taquillas WHERE ESTADO <> 'Libre'")
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    if rows[0][0] == 0:
        return None
    else:
        raise Exception("Error al resetear la base de datos. Han quedado taquillas ocupadas, rows: ", rows)


if __name__ == "__main__":
    print(get_info_taquilla_codigo('1.0.E.P001'))
