import importlib
import os
import sqlite3

serverConnection = importlib.import_module('serverConnection')

def get_connection(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError('Database not found')

    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    # foreign keys
    cursor.execute("PRAGMA FOREIGN_KEYS=ON")
    return connection

def create_session(RFID_Code):
    connection = get_connection('database_server.db')
    cursor = connection.cursor()

    pilot = get_pilot(RFID_Code)

    cursor.execute(
        "INSERT INTO Flugsession(PilotID, Startzeit, Endzeit, Ist_Flugleiter) VALUES(?, datetime('now'), NULL, FALSE)",
        pilot['pilot_id'])
    
    connection.commit()
    connection.close()
    return

def get_session(SessionID):
    connection = get_connection('database_server.db')
    cursor = connection.cursor()

    select_stmt = cursor.execute(
                'SELECT PilotID, Startzeit, Endzeit, Ist_Flugkeiter FROM Session WHERE SessionID = ?',
                SessionID)
    
    for row in select_stmt:
        return_dict = {
            'pilot_id': row[0],
            'start_time': row[1] + " " + row[2],
            'end_time': row[3],
            'is_controller': row[4]
        }

    connection.close()
    return return_dict

def end_session(SessionID):
    connection = get_connection('database_server.db')
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE Flugsession SET Endzeit = datetime('now') TRUE WHERE SessionID = ?",
        SessionID)
    
    connection.commit()
    connection.close()
    return

def set_flugleiter(SessionID):
    connection = get_connection('database_server.db')
    cursor = connection.cursor()

    cursor.execute(
        'UPDATE Flugsession SET Ist_Flugleiter = TRUE WHERE SessionID = ?',
        SessionID)
    
    connection.commit()
    connection.close()
    return

def get_pilot(RFID_Code):
    connection = get_connection('database_server.db')
    cursor = connection.cursor()

    select_stmt = cursor.execute(
                'SELECT ROWID, RFID_code, Nachname, Vorname, Eintrittsdatum, Ist_Aktiv FROM Pilot WHERE RFID_Code = ?',
                RFID_Code)
    
    for row in select_stmt:
        return_dict = {
            'pilot_id': row[0],
            'rfid_code': row[1],
            'pilot_name': row[2] + " " + row[3],
            'entry_date': row[4],
            'active': row[5]
        }

    connection.close()
    return return_dict

def sync_session(SessionID):
    session = get_session(SessionID)
    serverConnection.syncSession() 
    return

def sync_pilot():
    # TODO: implement POST request for server to sync new pilot data
    return