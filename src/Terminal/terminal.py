#!/usr/bin/env python
import RPi.GPIO as GPIO
import sys

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

    try:
        rfid_c, text = reader.read()
        print(rfid_c)
        eval_rfid(rfid_c)
    finally:
        GPIO.cleanup()
