from flask_restx import Resource

from globals import get_connection


# AddSession.vue
# GET Request: /pilot-list -> Backend liefert aktive Piloten: {pilot_id, pilot_name}
class PilotList(Resource):
    def get(self):
        '''get id, and name of every pilot'''
        connection = get_connection("database_server.db")
        cursor = connection.cursor()
        return_dict = {
            'pilots': []
        }
        for row in cursor.execute('SELECT ROWID, Vorname, Nachname FROM Pilot'):
            pilot = {
                'value': row[0],
                'text': "[" + str(row[0]) + "] " + row[1] + " " + row[2]
            }
            return_dict['pilots'].append(pilot)
        connection.close()
        return return_dict
