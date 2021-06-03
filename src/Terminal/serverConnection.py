import importlib
from flask_restx import Resource, inputs, fields
import requests
import os

serverURL = 'http://127.0.0.1:5000'

databaseAccess = importlib.import_module('databaseAccess')

# synchronisiere Sessions
def sync_sessions():
    sessions = databaseAccess.get_unsynced_sessions()

    try:
        response = requests.get(url = serverURL, timeout = 2)
    except:
        print('Server temporarily unavailable')
        return

    for session in sessions:
        print(session)

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