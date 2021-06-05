from flask_restx import Resource
from globals import api, get_connection, auth_parser, is_pilot


# diese request dürfen alle piloten ausführen
# GET /sessions/running
class RunningSessions(Resource):
    # für das frontend - ausgabe aller laufenden sessions auf startseite
    @api.expect(auth_parser)
    def get(self):
        '''all active sessions'''
        connection = get_connection("database_server.db")
        cursor = connection.cursor()

        p_id = is_pilot(cursor)
        if p_id == -1:
            return {}, 404

        return_dict = {
            'sessions': []
        }

        select_stmt = cursor.execute(
            'SELECT P.PilotID, P.Vorname, P.Nachname, time(F.Startzeit), F.Ist_Flugleiter '
            'FROM Flugsession F '
            'JOIN Pilot P on P.PilotID = F.PilotID '
            'WHERE F.Endzeit IS NULL'
        )

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
