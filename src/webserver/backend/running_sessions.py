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
            'SELECT P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
            'F.Ist_Flugleiter, G.Gastname, G.Freitext '
            'FROM Flugsession F '
            'JOIN Pilot P on P.PilotID = F.PilotID '
            'LEFT JOIN Gast G on G.GastID = F.GastID '
            'WHERE F.Endzeit IS NULL'
        )

        return_dict = {
            'sessions': []
        }

        for row in select_stmt:
            session = {
                'pilot_name': row[0] + " " + row[1],
                'date': row[2],
                'start_time': row[3],
                'flugleiter': row[4],
                'gast': {
                    'name': row[5],
                    'text': row[6]
                }
            }
            return_dict['sessions'].append(session)

        connection.close()
        return return_dict
