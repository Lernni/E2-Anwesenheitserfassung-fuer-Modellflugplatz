import importlib
import json
from flask import Flask, request
import os
import requests
import threading

serverURL = 'http://127.0.0.1:5000'

databaseAccess = importlib.import_module('databaseAccess')

# synchronisiere Sessions
def sync_sessions():
    try:
        response = requests.get(url = serverURL, timeout = 2)
    except:
        print('Server temporarily unavailable')
        return

    sessions = databaseAccess.get_unsynced_sessions()

    for session in sessions:
        sessionDate = session['start_time'].split(' ')[0]
        startTime = session['start_time'].split(' ')[1].split(':')[0] + ':' + session['start_time'].split(' ')[1].split(':')[1]

        if session['end_time'] != None:
            endTime = session['end_time'].split(' ')[1].split(':')[0] + ':' + session['end_time'].split(' ')[1].split(':')[1]

            payload = {
                'pilot_id': session['pilot_id'],
                'session_date': sessionDate,
                'start_time': startTime,
                'end_time': endTime,
                'is_leader': session['is_controller']
            }

        else:
            payload = {
                'pilot_id': session['pilot_id'],
                'session_date': sessionDate,
                'start_time': startTime,
                'is_leader': session['is_controller']
            }

        try:
         response = requests.post(url = serverURL + '/sessions', json = payload, timeout = 2)
        except:
            print('Server temporarily unavailable')
            return

        if not response.ok:
            continue

        databaseAccess.set_synced(session['session_id'])
    
    return

# minimale REST-API zur Synchronisierung von Piloten, RFID-Ausweisen und Einstellungen
def run_api():
    app = Flask(__name__)

    @app.route('/pilot', methods=['POST'])
    def insert_pilot():
        insert_dict = {
            'pilot_id': request.form['pilot_id'],
            'rfid_code': request.form['rfid_code'],
            'pilot_name': request.form['pilot_name'],
            'pilot_surname': request.form['pilot_surname'],
            'entry_date': request.form['entry_date'],
            'is_active': request.form['is_active']
        }
        databaseAccess.insert_pilot(insert_dict)
        return insert_dict

    @app.route('/rfid', methods=['POST'])
    def insert_rfid():
        insert_dict = {
            'rfid_code': request.form['rfid_code']
        }
        databaseAccess.insert_rfid(insert_dict)
        return insert_dict

    t = threading.Thread(target = app.run)
    t.start()

    return