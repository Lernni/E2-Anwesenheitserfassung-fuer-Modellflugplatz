#   *** database_access.py ***
#   - implementiert Datenbankzugriffe auf dem Terminal
#   - Autor: Dirk Zimmermann
#   - Mail: dirk.zimmermann@htw-dresden.de

# coding=utf-8

import importlib
import os
import sqlite3

serverConnection = importlib.import_module('server_connection')


# baut Verbindung zur Datenbank auf
def get_connection(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError('Database not found')

    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    # foreign keys
    cursor.execute("PRAGMA FOREIGN_KEYS=ON")
    return connection

# fügt neuen RFID Ausweis ein
def insert_rfid(insert_dict):
    connection = get_connection('database_terminal.db')
    cursor = connection.cursor()

    select_stmt = cursor.execute(
        'SELECT RFID_Code FROM RFID_Ausweis WHERE RFID_Code = ?',
        (insert_dict['rfid_code'],))

    if(select_stmt.fetchone() is None):
        cursor.execute(
            'INSERT INTO RFID_Ausweis(RFID_Code) VALUES(?)',
            (insert_dict['rfid_code'],))

    connection.commit()
    connection.close()
    return

# gibt Details eines Piloten mit RFID_Code zurück, -1 falls keiner gefunden
def get_pilot(RFID_Code):
    connection = get_connection('database_terminal.db')
    cursor = connection.cursor()

    select_stmt = cursor.execute(
        'SELECT PilotID, RFID_code, Token FROM Pilot WHERE RFID_Code = ?',
        (RFID_Code,))

    return_dict = -1
    for row in select_stmt:
        return_dict = {
            'pilot_id': row[0],
            'rfid_code': row[1],
            'token': row[2]
        }

    connection.close()
    return return_dict

# fügt neuen Piloten ein
def insert_pilot(insert_dict):
    connection = get_connection('database_terminal.db')
    cursor = connection.cursor()

    try:
        cursor.execute(
            'INSERT INTO Pilot(PilotID, RFID_Code, Token) VALUES(?, ?, ?)',
            (insert_dict['pilot_id'], insert_dict['rfid_code'], insert_dict['token'],))
    except:
        cursor.execute(
            'UPDATE Pilot SET RFID_Code = ?, Token = ? WHERE PilotID = ?',
            (insert_dict['rfid_code'], insert_dict['token'], insert_dict['pilot_id'],))

    connection.commit()
    connection.close()
    return

# gibt Token eines Piloten mit PilotID zurück, -1 falls Pilot gefunden
def get_token(PilotID):
    connection = get_connection('database_terminal.db')
    cursor = connection.cursor()

    token = -1
    select_stmt = cursor.execute(
        'SELECT Token FROM Pilot WHERE PilotID = ?',
        (PilotID,))

    for row in select_stmt:
        token = row[0]

    connection.close()
    return token

# erstellt neue Session mit aktueller Uhrzeit, gibt SessionID der neuen Session zurück, -1 wenn RFID_Code nicht existiert
def create_session(RFID_Code):
    connection = get_connection('database_terminal.db')
    cursor = connection.cursor()

    pilot = get_pilot(RFID_Code)
    if pilot == -1:
        raise ValueError('RFID Code nicht vorhanden oder keinem Piloten zugewiesen')

    cursor.execute(
        'INSERT INTO Flugsession(PilotID, Startzeit, Endzeit, Ist_Flugleiter) VALUES(?, datetime("now", "localtime"), NULL, 0)',
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
        connection.close()
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
        "UPDATE Flugsession SET Endzeit = datetime('now', 'localtime'), Synced = 0 WHERE SessionID = ?",
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
        "UPDATE Flugsession SET Endzeit = datetime('now', 'localtime'), Synced = 0 WHERE Endzeit IS NULL")

    connection.commit()
    connection.close()
    serverConnection.sync_sessions()
    return

# gibt SessionID des aktiven Flugleiters zurück, -1 falls keiner vorhanden
def get_flugleiter():
    connection = get_connection('database_terminal.db')
    cursor = connection.cursor()

    select_stmt = cursor.execute(
        'SELECT SessionID FROM Flugsession WHERE Ist_Flugleiter = 1 AND Endzeit IS NULL')

    ret = -1
    for row in select_stmt:
        ret = row[0]

    connection.close()
    return ret

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

# startet api zur Synchronisierung von RFID-Ausweisen und Piloten
def run_api():
    serverConnection.run_api()
    return