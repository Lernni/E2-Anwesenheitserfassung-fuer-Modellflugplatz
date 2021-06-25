#   *** make_server_db.py ***
#   - erstellt die Datenbank des Servers basierend auf database_server.sql
#   - Autor: Max Haufe
#   - Mail: max.haufe@htw-dresden.de

import sqlite3
import os.path

if __name__ == "__main__":
    if not os.path.exists("database_server.db"):
        first_connection = sqlite3.connect("database_server.db")
        c = first_connection.cursor()
        fd = open('database_server.sql', 'r')
        sql_file = fd.read()
        fd.close()
        sql_commands = sql_file.split(';')

        for command in sql_commands:
            c.execute(command)

        first_connection.commit()
        first_connection.close()
    else:
        print("db already exists")
        exit(1)
