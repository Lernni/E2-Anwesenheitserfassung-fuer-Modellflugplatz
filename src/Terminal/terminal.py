#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import sys, datetime
from server_connection import run_api

from database_access import create_session, end_session, get_active_sessions

sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522


def eval_rfid(rfid):
    ret = get_active_sessions(rfid)

    if ret == []:
        # keine aktive session mit rfid code vorhanden
        # -> neue session
        try:
            create_session(rfid)
        except ValueError as e:
            # todo: logging?
            print('ERROR: ' + str(e))
    else:
        # session beenden
        end_session(ret[0]['session_id'])


if __name__ == "__main__":
    reader = SimpleMFRC522()
    print("Now place tag next to the scanner to read")
    run_api()
    print("api done !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    try:
        time_old = datetime.datetime.now()
        while True:
            rfid_c, text = reader.read()
            time_new = datetime.datetime.now()
            # rfid scanner entprellen
            # rfid karte wird frühstens nach 2 sek. wieder ausgewertet.
            if (time_new - time_old).total_seconds() >= 2:
                time_old = time_new

                eval_rfid(rfid_c)
                print(rfid_c)
    finally:
        GPIO.cleanup()
