from flask_restx import Resource

from globals import api, get_connection, auth_parser, is_admin


# GET /rfid_available
# nur admins dürfen diese request ausführen
class RfidAvailable(Resource):
    @api.expect(auth_parser)
    def get(self):
        '''available RFID tags'''
        connection = get_connection("database_server.db")
        cursor = connection.cursor()

        if not is_admin(cursor):
            return {}, 401

        return_dict = {
            'rfid_list': []
        }
        for row in cursor.execute(
                'SELECT RFID_Code FROM RFID_Ausweis '
                'WHERE RFID_Code NOT IN (SELECT RFID_Code FROM Pilot WHERE RFID_Code NOT NULL)'):
            rfid_tag = hex(row[0])
            return_dict['rfid_list'].append(rfid_tag)
        connection.close()
        return return_dict
