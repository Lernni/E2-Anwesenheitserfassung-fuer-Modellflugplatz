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

def createSession(RFID_Code):
    return

def getSession(SessionID):
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
                'is_controller': row[4],
            }

    connection.close()
    return return_dict

def endSession(SessionID):
    return

def setFlugleiter(SessionID):
    connection = get_connection('database_server.db')
    cursor = connection.cursor()

    cursor.execute(
        'UPDATE Flugsession SET Ist_Flugleiter = TRUE WHERE SessionID = ?',
        SessionID)
    
    connection.close()
    return

def getPilot(RFID_Code):
    connection = get_connection('database_server.db')
    cursor = connection.cursor()

    select_stmt = cursor.execute(
                'SELECT RFID_code, Nachname, Vorname, Eintrittsdatum, Ist_Aktiv FROM Pilot WHERE RFID_Code = ?',
                RFID_Code)
    
    for row in select_stmt:
            return_dict = {
                'rfid_code': row[0],
                'pilot_last_name': row[1] + " " + row[2],
                'pilot_first_name': row[3],
                'entry_date': row[4],
                'active': row[5]
            }

    connection.close()
    return return_dict

def syncSession(SessionID):
    return

def syncPilot():
    return