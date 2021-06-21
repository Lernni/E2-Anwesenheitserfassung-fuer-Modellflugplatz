import json

from flask_restx import Resource

from globals import api, get_connection, is_admin, auth_parser

settings_post_model = api.model('settings_post_model', {})


# nur admins dürfen diese request ausführen
class Settings(Resource):
    @api.expect(settings_post_model)
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