import sqlite3 as sql
from datetime import datetime

HORARIOS = {"1": [11, 12, 15, 16, 17, 18],
            "2": [9, 10, 11, 12, 15, 16, 17, 18],
            "3": [10, 11, 12, 15, 16, 17, 18],
            "4": [11, 12, 14, 15, 16],
            "5": [9, 10, 11, 12, 15, 16, 17, 18]}
HORARIOS_LEN = sum(len(numbers) for numbers in HORARIOS.values())
DB_FILE = "database/database.db"
NUM_OSCILOS = 3


def create_connection(db_file=DB_FILE):
    return sql.connect(db_file)


def huecos_table_creation():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE OsciloscopioReservas (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    CW INT,
    DIA INT,
    HORA INT,
    NIA VARCHAR(50),
    OSCILOSCOPIO INT
    );
    """)
    conn.commit()
    conn.close()


def drop_huecos_table():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE OsciloscopioReservas")
    conn.commit()
    conn.close()


def insert_hueco(index, oscilo, cw, week_day, hour):
    conn = sql.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO OsciloscopioReservas (ID, OSCILOSCOPIO, CW, DIA, HORA) VALUES (?, ?, ?, ?, ?)",
                (index, oscilo, cw, week_day, hour))
    conn.commit()
    conn.close()


def huecos_table_importer(num_oscilos=2):
    counter = 0
    for osc in range(num_oscilos):
        osc += 1
        for i in range(53):
            for j in HORARIOS.keys():
                for k in HORARIOS[j]:
                    insert_hueco(counter, osc, i, j, k)
                    counter += 1


def get_5_free_spots_today(oscilo):
    year, cw, week_day = datetime.now().isocalendar()
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM OsciloscopioReservas WHERE CW = ? AND DIA = ? and OSCILOSCOPIO = ?",
                (cw, week_day, oscilo))
    rows = cur.fetchall()
    querry = f"""
        SELECT *
        FROM (
        SELECT *
        FROM OsciloscopioReservas
        WHERE ID >= ?
        ORDER BY ID
        LIMIT ?) AS Subquery
        WHERE NIA IS NULL;
"""
    cur.execute(querry, (rows[0][0], HORARIOS_LEN + (rows[0][2] * len(HORARIOS[str(rows[0][2])]))))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_free_sports_specific_day(day, oscilo):
    year, cw, week_day = datetime.now().isocalendar()
    if week_day > day:
        cw += 1
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT HORA FROM OsciloscopioReservas WHERE CW = ? AND DIA = ? AND OSCILOSCOPIO = ?",
                (cw, day, oscilo))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_string_nias(id_reserva):
    conn = create_connection()
    cur = conn.cursor()
    querry = """
    WITH query AS (
        SELECT CW, DIA
        FROM OsciloscopioReservas
        WHERE ID = ?
    )
    SELECT NIA
    FROM OsciloscopioReservas
    WHERE CW = (SELECT CW FROM query)
      AND DIA = (SELECT DIA FROM query);
    """
    # Una query Manu
    # querry = """
    # WITH query AS (SELECT CW as cw, DIA as dia FROM OsciloscopioReservas WHERE ID = ?)
    # SELECT NIA FROM OsciloscopioReservas WHERE CW = query.cw AND DIA = query.dia;
    # """
    # Dos querys
    # querry = """
    # SELECT * FROM OsciloscopioReservas WHERE ID = ?"""
    # cur.execute(querry, (id_reserva,))
    # datos = cur.fetchall()
    # querry = """
    # SELECT NIA FROM OsciloscopioReservas WHERE CW = ? AND DIA = ?"""
    # cur.execute(querry, (datos[0][1], datos[0][2]))
    # rows = cur.fetchall()
    # return rows
    cur.execute(querry, (id_reserva,))
    datos = cur.fetchall()
    conn.close()
    return datos


def check_nia_validity(nias, id_reserva):
    data = get_string_nias(id_reserva)
    for nia in nias:
        for row in data:
            if nia in row:
                raise ValueError("Ya has reservado un hueco para este día")


def haz_reserva(id_reserva, nias):
    query_data = """SELECT * FROM OsciloscopioReservas WHERE ID = ?;"""
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query_data, (id_reserva,))
    rows = cur.fetchall()
    cw = rows[0][1]
    week_day = rows[0][2]

    query_select = """SELECT NIA FROM OsciloscopioReservas WHERE CW = ? AND DIA = ?"""
    cur.execute(query_select, (cw, week_day))
    rows = str(cur.fetchall())
    nias_list_add = ""
    for nia in nias:
        if nia in rows:
            raise ValueError("Ya has reservado un hueco para este día")
        else:
            nias_list_add += nia
    else:
        query_update = """UPDATE OsciloscopioReservas SET NIA = ? WHERE ID = ?"""
        cur.execute(query_update, (nias_list_add, id_reserva))
        conn.commit()
        conn.close()
        return True
