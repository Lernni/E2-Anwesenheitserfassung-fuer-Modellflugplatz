#   *** settings.py ***
#   - implementiert das Aktualisieren von settings.json
#   - Autor: Max Haufe
#   - Mail: max.haufe@htw-dresden.de

import json

from flask_restx import Resource

from sync import sync_settings
from globals import api, get_connection, is_admin, auth_parser

settings_post_model = api.model('settings_post_model', {})

# POST /settings
# der body der request wird als settings.json gespeichert
# nur admins dürfen diese request ausführen
class Settings(Resource):
    @api.expect(settings_post_model, auth_parser)
    def post(self):
        '''post settings to server'''

        connection = get_connection("database_server.db")
        cursor = connection.cursor()

        if not is_admin(cursor):
            connection.close()
            return {}, 401

        file = open('settings.json', 'w')
        file.write(json.dumps(api.payload))
        file.close()

        sync_settings()

        # todo: prüfen, ob erfolgreich synchronisiert, ggf. neu synchronisieren

        return {}

    @api.expect(auth_parser)
    def get(self):
        '''get settings'''
        connection = get_connection("database_server.db")
        cursor = connection.cursor()

        if not is_admin(cursor):
            connection.close()
            return {}, 401

        settings = {}

        with open('settings.json') as settings_file:
            settings['settings'] = json.load(settings_file)
            return settings   