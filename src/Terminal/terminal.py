#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import sys, datetime
from server_connection import run_api

from database_access import create_session, end_session, get_active_sessions, set_flugleiter

sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522

# button zeugs
# globale Flag, welche jedes mal, nachdem ein RFID chip an den scanner gehalten wird, zurück auf False gesetzt wird
# button wird gedrückt -> nächster RFID wird Flugleiter
button_was_pressed = False

GPIO.setmode(GPIO.BCM)

buttonPin = 19

GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def button_pressed(pin):
    global button_was_pressed
    button_was_pressed = True
    print("Button pressed!")


GPIO.add_event_detect(buttonPin, GPIO.BOTH, bouncetime=700)
GPIO.add_event_callback(buttonPin, button_pressed)


# rfid zeugs


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


def eval_rfid_button(rfid):
    ret = get_active_sessions(rfid)

    # todo: dirk: funktion, ob es bereits anderen flugleiter auf platz gibt
    # if flugleiter_exists():
    # raise error oder return oder sowas

    # wenn keine aktive session vorhanden
    # -> neue anlegen und flugleiter ernennne
    if ret == []:
        try:
            session_id = create_session(rfid)
        except ValueError as e:
            # todo: logging?
            print('ERROR: ' + str(e))
        set_flugleiter(session_id)
    else:
        set_flugleiter(ret[0]['session_id'])


if __name__ == "__main__":
    reader = SimpleMFRC522()
    print("Now place tag next to the scanner to read")
    run_api()
    try:
        time_old = datetime.datetime.now()
        time_old_button = datetime.datetime.now()
        while True:
            rfid_c, text = reader.read()
            time_new = datetime.datetime.now()
            # rfid scanner entprellen
            # rfid karte wird frühstens nach 2 sek. wieder ausgewertet.
            if (time_new - time_old).total_seconds() >= 2:
                time_old = time_new
                if button_was_pressed:
                    eval_rfid_button(rfid_c)
                else:
                    eval_rfid(rfid_c)
                print(rfid_c)

            button_was_pressed = False

    finally:
        GPIO.cleanup()
