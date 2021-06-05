from flask_restx import Resource

from globals import api, get_connection, auth_parser, is_admin


# GET Request: /pilot-list -> Backend liefert Piloten: {pilot_id, pilot_name}
# nur admins dürfen diese requests ausführen
class PilotList(Resource):
    @api.expect(auth_parser)
    def get(self):
        '''get id, and name of every pilot'''
        connection = get_connection("database_server.db")
        cursor = connection.cursor()

        if not is_admin(cursor):
            return {}, 401

        return_dict = {
            'pilots': []
        }
        for row in cursor.execute('SELECT PilotID, Vorname, Nachname, Nutzername FROM Pilot'):
            pilot = {
                'pilot_id': row[0],
                'pilot_name': row[1] + " " + row[2],
                'pilot_username': row[3]
            }
            return_dict['pilots'].append(pilot)
        connection.close()
        return return_dict
