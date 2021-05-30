from flask_restx import Resource
from globals import get_connection


# GET /sessions/running
class RunningSessions(Resource):
    # für das frontend - ausgabe aller laufenden sessions auf startseite
    def get(self):
        '''all active sessions'''

        connection = get_connection("database_server.db")
        cursor = connection.cursor()

        select_stmt = cursor.execute(
            'SELECT P.PilotID, P.Vorname, P.Nachname, time(F.Startzeit), F.Ist_Flugleiter '
            'FROM Flugsession F '
            'JOIN Pilot P on P.PilotID = F.PilotID '
            'WHERE F.Endzeit IS NULL'
        )

        return_dict = {
            'sessions': []
        }

        for row in select_stmt:
            session = {
                'pilot_id': row[0],
                'pilot_name': row[1] + " " + row[2],
                'start_time': row[3],
                'session_leader': row[4]
            }
            return_dict['sessions'].append(session)

        connection.close()
        return return_dict
