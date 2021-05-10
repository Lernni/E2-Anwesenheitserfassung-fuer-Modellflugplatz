import sqlite3
import os.path

if __name__ == "__main__":
    if not os.path.exists("database_terminal.db"):
        first_connection = sqlite3.connect("database_terminal.db")
        c = first_connection.cursor()
        fd = open('database_terminal.sql', 'r')
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
