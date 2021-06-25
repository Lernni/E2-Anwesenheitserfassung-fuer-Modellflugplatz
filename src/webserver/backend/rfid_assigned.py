#   *** rfid_assigned.py ***
#   - implementiert das Abrufen aller vergebenen RFID Tags (GET)
#   - Autor: Max Haufe
#   - Mail: max.haufe@htw-dresden.de

from flask_restx import Resource

from globals import api, get_connection, auth_parser, is_admin


# GET /rfid_assigned
# nur admins dürfen diese request ausführen
class RfidAssigned(Resource):
    @api.expect(auth_parser)
    # gibt alle vergebenen RFID tags zurück
    def get(self):
        '''assigned RFID tags'''
        connection = get_connection("database_server.db")
        cursor = connection.cursor()

        if not is_admin(cursor):
            return {}, 401

        return_dict = {
            'rfid_list': []
        }

        for row in cursor.execute(
                'SELECT PilotID, RFID_Code, Vorname, Nachname '
                'FROM Pilot WHERE RFID_CODE IS NOT NULL'):
            list_item = {
                'pilot_id': row[0],
                'pilot_name': row[2] + ' ' + row[3],
                'rfid': hex(row[1])
            }
            return_dict['rfid_list'].append(list_item)
        connection.close()
        return return_dict
