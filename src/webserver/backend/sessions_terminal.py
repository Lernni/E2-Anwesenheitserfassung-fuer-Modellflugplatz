from datetime import date, time, datetime
from flask_restx import Resource, inputs, fields
from globals import api, get_connection, auth_parser, is_pilot, is_admin, TimeFormat

sessions_term_post_model = api.model('session_post_model', {
    'pilot_id': fields.Integer(description='ID of Pilot', required=True),
    'session_date': fields.Date(required=True),
    'start_time': TimeFormat(description='Time in 24 hour HH:MM format', required=True, default='HH:MM'),
    'end_time': TimeFormat(description='Time in 24 hour HH:MM format', default='HH:MM'),
    'is_leader': fields.Boolean(required=True)
})


# POST /sessions/terminal
# wenn die endzeit nicht im body enthalten ist, dann wird eine neue sessions angelegt, wenn doch, dann wird nur die bestehende geupdatet.
class SessionsTerminal(Resource):
    @api.expect(sessions_term_post_model)
    def post(self):
        '''Post finished and unfinished sessions from terminal to backend'''
        connection = get_connection("database_server.db")
        cursor = connection.cursor()
        payload = api.payload

        start_time = datetime.combine(date.fromisoformat(payload['session_date']),
                                      datetime.strptime(payload['start_time'], "%H:%M").time())

        # neue session
        if 'end_time' not in payload.keys():
            cursor.execute(
                'INSERT INTO Flugsession(PilotID, Startzeit, Ist_Flugleiter) VALUES (?,?,?)',
                [payload['pilot_id'], start_time, payload['is_leader']]
            )
        # vorhandene session updaten
        else:

            end_time = datetime.combine(date.fromisoformat(payload['session_date']),
                                        datetime.strptime(payload['end_time'], "%H:%M").time())
            cursor.execute(
                'UPDATE Flugsession SET Endzeit = ? WHERE PilotID = ? AND Startzeit = ? AND Ist_Flugleiter = ?',
                [end_time, payload['pilot_id'], start_time, payload['is_leader']]
            )
            # abbrechen, wenn nix eingefügt wurde - aka keine flugsession existiert hat
            if cursor.rowcount == 0:
                return {}, 500

        connection.commit()
        connection.close()
        return {}