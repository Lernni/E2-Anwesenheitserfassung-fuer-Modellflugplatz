import importlib
from flask_restx import Resource, inputs, fields
import os

databaseAccess = importlib.import_module('databaseAccess')

# synchronisiere Sessions
def sync_sessions():
    sessions = databaseAccess.get_unsynced_sessions()

    # TODO: Mechanismus zum Überprüfen der Internetverbindung

    for session in sessions:

        # TODO: POST Request an Webserver

        databaseAccess.set_synced(session['session_id'])