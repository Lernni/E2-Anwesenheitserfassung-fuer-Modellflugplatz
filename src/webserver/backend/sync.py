import os, requests
from globals import get_connection

# todo: make IP static
RASPI_IP = '127.0.0.1'
RASPI_URL = 'http://127.0.0.1:6000'


# prüft ob raspi über netzwerk erreichbar
def is_online():
    is_up = True if os.system("ping -c 1 " + RASPI_IP) == 0 else False
    return is_up


def set_synced_pilot(pilot_id, is_synced):
    connection = get_connection("database_server.db")
    cursor = connection.cursor()

    cursor.execute(
        'UPDATE Pilot SET Synced = ? WHERE PilotID = ?', [is_synced, pilot_id]
    )

    connection.commit()
    connection.close()
    return


# synchronisiert alle neuen/geänderten Piloten
def sync_pilots():
    if not is_online():
        print("Terminal is offline")
        return

    connection = get_connection("database_server.db")
    cursor = connection.cursor()

    unsynced_pilot_list = cursor.execute(
        'SELECT PilotID, RFID_Code, Token  FROM Pilot WHERE Synced = FALSE'
    ).fetchall()

    for pilot in unsynced_pilot_list:
        payload = {
            'pilot_id': pilot[0],
            'rfid_code': pilot[1],
            'token': pilot[2]
        }

        try:
            response = requests.post(url=RASPI_URL + '/pilot', json=payload, timeout=2)
        except:
            print('Post failed')
            return

        if not response.ok:
            continue

        set_synced_pilot(pilot[0], True)

    return


def set_synced_rfid(rfid_code, is_synced):
    connection = get_connection("database_server.db")
    cursor = connection.cursor()

    cursor.execute(
        'UPDATE RFID_Ausweis SET Synced = ? WHERE RFID_Code = ?', [is_synced, rfid_code]
    )

    connection.commit()
    connection.close()
    return


# synchronisiert alle neuen rfids
def sync_rfids():
    if not is_online():
        print("Terminal offline")
        return
    connection = get_connection("database_server.db")
    cursor = connection.cursor()

    unsynced_rfid_list = cursor.execute(
        'SELECT RFID_Code  FROM RFID_Ausweis WHERE Synced = FALSE'
    ).fetchall()

    for rfid in unsynced_rfid_list:
        payload = {
            'rfid_code': rfid[0]
        }

        try:
            response = requests.post(url=RASPI_URL + '/rfid', data=payload, timeout=2)
        except:
            print('Post failed')
            return

        if not response.ok:
            continue

        set_synced_rfid(rfid[0], True)

    return


if __name__ == '__main__':
    sync_rfids()
    sync_pilots()
