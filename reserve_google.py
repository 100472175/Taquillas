import sys
import mariadb

try:
    conn = mariadb.connect(
        user="admin",
        password="admin@admin",
        host="localhost",
        port=3306,
        database="db1"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()
cur.execute("SELECT * FROM tabla1")
print(f"Column names: {[i[0] for i in cur.description]}")
print(cur.fetchall())


