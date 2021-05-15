from flask_restx import Resource

from globals import get_connection


# EditPilot.vue
# GET /rfid
class RfidAvailable(Resource):
    def get(self):
        '''available RFID tags'''
        connection = get_connection("database_server.db")
        cursor = connection.cursor()
        return_dict = {
            'rfid_list': []
        }
        for row in cursor.execute(
                'SELECT RFID_Code, ROWID FROM RFID_Ausweis WHERE RFID_Code NOT IN (SELECT RFID_Code FROM Pilot)'):
            rfid_tag = {
                'value': row[1],
                'text': hex(row[0])
            }
            return_dict['rfid_list'].append(rfid_tag)
        connection.close()
        return return_dict
