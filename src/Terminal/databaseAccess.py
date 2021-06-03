# coding=utf-8

import importlib
import os
import sqlite3

serverConnection = importlib.import_module('serverConnection')


# baut Verbindung zur Datenbank auf
def get_connection(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError('Database not found')

    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    # foreign keys
    cursor.execute("PRAGMA FOREIGN_KEYS=ON")
    return connection


# gibt Details eines Piloten mit RFID_Code zurück, -1 falls keiner gefunden
def get_pilot(RFID_Code):
    connection = get_connection('database_terminal.db')
    cursor = connection.cursor()

    select_stmt = cursor.execute(
        'SELECT PilotID, RFID_code, Nachname, Vorname, Eintrittsdatum, Ist_Aktiv FROM Pilot WHERE RFID_Code = ?',
        (RFID_Code,))

    return_dict = -1
    for row in select_stmt:
        return_dict = {
            'pilot_id': row[0],
            'rfid_code': row[1],
            'pilot_name': row[3] + " " + row[2],
            'entry_date': row[4],
            'active': row[5]
        }

    connection.close()
    return return_dict


# erstellt neue Session mit aktueller Uhrzeit, gibt SessionID der neuen Session zurück, -1 wenn RFID_Code nicht existiert
def create_session(RFID_Code):
    connection = get_connection('database_terminal.db')
    cursor = connection.cursor()

    pilot = get_pilot(RFID_Code)
    if pilot == -1:
        raise ValueError('RFID Code nicht vorhanden oder keinem Piloten zugewiesen')

    cursor.execute(
        'INSERT INTO Flugsession(PilotID, Startzeit, Endzeit, Ist_Flugleiter) VALUES(?, datetime("now"), NULL, 0)',
        (pilot['pilot_id'],))

    select_stmt = cursor.execute('SELECT SessionID FROM Flugsession WHERE ROWID = last_insert_rowid()')

    for row in select_stmt:
        ret = row[0]

    connection.commit()
    connection.close()
    serverConnection.sync_sessions()
    return ret


# gibt Details einer Session mit SessionID zurück, -1 falls keine gefunden
def get_session(SessionID):
    connection = get_connection('database_terminal.db')
    cursor = connection.cursor()

    select_stmt = cursor.execute(
        'SELECT SessionID, PilotID, Startzeit, Endzeit, Ist_Flugleiter FROM Flugsession WHERE SessionID = ?',
        (SessionID,))

    return_dict = -1
    for row in select_stmt:
        return_dict = {
            'session_id': row[0],
            'pilot_id': row[1],
            'start_time': row[2],
            'end_time': row[3],
            'is_controller': row[4]
        }

    connection.close()
    return return_dict


# gibt Liste aktiver Sessions eines Piloten mit RFID_Code zurück, [] falls keine gefunden
def get_active_sessions(RFID_Code):
    connection = get_connection('database_terminal.db')
    cursor = connection.cursor()

    pilot = get_pilot(RFID_Code)
    if pilot == -1:
        return []

    select_stmt = cursor.execute(
        'SELECT SessionID, PilotID, Startzeit, Endzeit, Ist_Flugleiter FROM Flugsession WHERE PilotID = ? AND Endzeit IS NULL',
        (pilot['pilot_id'],))

    sessions = []
    return_dict = -1
    for row in select_stmt:
        return_dict = {
            'session_id': row[0],
            'pilot_id': row[1],
            'start_time': row[2],
            'end_time': row[3],
            'is_controller': row[4]
        }
        sessions.append(return_dict)

    connection.close()
    return sessions

# gibt Liste unsynchronisierter Sessions zurück, [] falls keine gefunden
def get_unsynced_sessions():
    connection = get_connection('database_terminal.db')
    cursor = connection.cursor()

    select_stmt = cursor.execute(
        'SELECT SessionID, PilotID, Startzeit, Endzeit, Ist_Flugleiter FROM Flugsession WHERE Synced = 0')

    sessions = []
    return_dict = -1
    for row in select_stmt:
        return_dict = {
            'session_id': row[0],
            'pilot_id': row[1],
            'start_time': row[2],
            'end_time': row[3],
            'is_controller': row[4]
        }
        sessions.append(return_dict)

    connection.close()
    return sessions

# markiert Session mit SessionID als synchronisiert
def set_synced(SessionID):
    connection = get_connection('database_terminal.db')
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE Flugsession SET Synced = 1 WHERE SessionID = ?",
        (SessionID,))

    connection.commit()
    connection.close()
    return

# setzt Endzeit einer Session auf aktuelle Zeit
def end_session(SessionID):
    connection = get_connection('database_terminal.db')
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE Flugsession SET Endzeit = datetime('now'), Synced = 0 WHERE SessionID = ?",
        (SessionID,))

    connection.commit()
    connection.close()
    serverConnection.sync_sessions()
    return


# setzt Endzeit aller aktiven Sessions auf aktuelle Zeit
def end_all_sessions():
    connection = get_connection('database_terminal.db')
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE Flugsession SET Endzeit = datetime('now'), Synced = 0 WHERE Endzeit IS NULL")

    connection.commit()
    connection.close()
    serverConnection.sync_sessions()
    return


# setzt Flugleiterstatus
def set_flugleiter(SessionID):
    connection = get_connection('database_terminal.db')
    cursor = connection.cursor()

    cursor.execute(
        'UPDATE Flugsession SET Ist_Flugleiter = 1, Synced = 0 WHERE SessionID = ?',
        (SessionID,))

    connection.commit()
    connection.close()
    serverConnection.sync_sessions()
    return

# zu Testzwecken
if __name__ == '__main__':
    connection = get_connection('database_terminal.db')
    cursor = connection.cursor()

    select_stmt = cursor.execute("SELECT RFID_Code FROM RFID_Ausweis")
    rfidcode = 0
    for row in select_stmt:
        rfidcode = row[0]

    if rfidcode != 346352:
        cursor.execute("INSERT INTO RFID_Ausweis(RFID_Code) VALUES (346352)")
        cursor.execute(
            'INSERT INTO Pilot(PilotID, RFID_Code, Nachname, Vorname, Eintrittsdatum, Ist_Aktiv) VALUES(123, 346352, "Mustermann", "Max", date("2017-05-15"), 0)')

    connection.commit()
    connection.close()

    id = create_session(346352)
    end_all_sessions()
