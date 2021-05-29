from datetime import date, time, datetime
from flask_restx import Resource, inputs, fields
from globals import api, get_connection


# für session_post_model - input Zeit
class TimeFormat(fields.String):
    def format(self, value):
        return time.strftime(value, "%H:%M")


session_post_model = api.model('session_post_model', {
    'pilot_id': fields.Integer(description='ID of Pilot', required=True),
    'session_date': fields.Date(required=True),
    'start_time': TimeFormat(description='Time in 24 hour HH:MM format', required=True, default='HH:MM'),
    'end_time': TimeFormat(description='Time in 24 hour HH:MM format', required=True, default='HH:MM'),
    'is_leader': fields.Boolean(required=True),
    'guest_name': fields.String(),
    'guest_info': fields.String()
})

sessions_parser = api.parser()
sessions_parser.add_argument('name', type=str)
sessions_parser.add_argument('start_date', type=inputs.date)
sessions_parser.add_argument('end_date', type=inputs.date)
sessions_parser.add_argument('from', type=int, required=True)
sessions_parser.add_argument('to', type=int, required=True)


class Sessions(Resource):
    @api.expect(sessions_parser)
    def get(self):
        '''get Session info'''
        select_stmt = None
        connection = get_connection("database_server.db")
        cursor = connection.cursor()
        args = sessions_parser.parse_args()
        from_ = args['from']
        to = args['to']

        # entferne alle argumente mit value 'None' (NULL)
        for k, v in list(args.items()):
            if v is None:
                args.pop(k)

        # GET sessions?name&start_date&end_date
        if 'name' in args.keys() and 'start_date' in args.keys() and 'end_date' in args.keys():
            name_list = args['name'].split()
            # z.B. 'Mustermann' -> in Vor- und Nachname suchen
            if len(name_list) == 1:
                select_stmt = cursor.execute(
                    'SELECT P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.PilotID = F.PilotID '
                    'LEFT JOIN Gast G on G.GastID = F.GastID '
                    'WHERE (lower(P.Vorname) LIKE lower(?) OR lower(P.Nachname) LIKE lower(?))'
                    'AND date(F.Startzeit) BETWEEN ? AND ?',
                    [name_list[0], name_list[0], args['start_date'], args['end_date']]
                )
            # z.B. 'Max Mustermann' -> vor(Max), nach(Mustermann) oder vor(Mustermann) nach(Max)
            if len(name_list) == 2:
                select_stmt = cursor.execute(
                    'SELECT P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.PilotID = F.PilotID '
                    'LEFT JOIN Gast G on G.GastID = F.GastID '
                    'WHERE ('
                    '(lower(P.Vorname) LIKE lower(?) AND lower(P.Nachname) LIKE lower(?)) '
                    '   OR '
                    '(lower(P.Vorname) LIKE lower(?) AND lower(P.Nachname) LIKE lower(?))'
                    ')'
                    'AND date(F.Startzeit) BETWEEN ? AND ?',
                    [name_list[0], name_list[1], name_list[1], name_list[0], args['start_date'], args['end_date']]
                )

        # GET sessions?name&start_date
        elif 'name' in args.keys() and 'start_date' in args.keys():
            name_list = args['name'].split()
            if len(name_list) == 1:
                select_stmt = cursor.execute(
                    'SELECT P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.PilotID = F.PilotID '
                    'LEFT JOIN Gast G on G.GastID = F.GastID '
                    'WHERE (lower(P.Vorname) LIKE lower(?) OR lower(P.Nachname) LIKE lower(?))'
                    'AND date(F.Startzeit) > ?',
                    [name_list[0], name_list[0], args['start_date']]
                )

            if len(name_list) == 2:
                select_stmt = cursor.execute(
                    'SELECT P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.PilotID = F.PilotID '
                    'LEFT JOIN Gast G on G.GastID = F.GastID '
                    'WHERE ('
                    '(lower(P.Vorname) LIKE lower(?) AND lower(P.Nachname) LIKE lower(?)) '
                    '   OR '
                    '(lower(P.Vorname) LIKE lower(?) AND lower(P.Nachname) LIKE lower(?))'
                    ')'
                    'AND date(F.Startzeit) > ?',
                    [name_list[0], name_list[1], name_list[1], name_list[0], args['start_date']]
                )

        elif 'name' in args.keys() and 'end_datum' in args.keys():
            name_list = args['name'].split()
            if len(name_list) == 1:
                select_stmt = cursor.execute(
                    'SELECT P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.PilotID = F.PilotID '
                    'LEFT JOIN Gast G on G.GastID = F.GastID '
                    'WHERE (lower(P.Vorname) LIKE lower(?) OR lower(P.Nachname) LIKE lower(?))'
                    'AND date(F.Startzeit) < ?',
                    [name_list[0], name_list[0], args['end_date']]
                )

            if len(name_list) == 2:
                select_stmt = cursor.execute(
                    'SELECT P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.PilotID = F.PilotID '
                    'LEFT JOIN Gast G on G.GastID = F.GastID '
                    'WHERE ('
                    '(lower(P.Vorname) LIKE lower(?) AND lower(P.Nachname) LIKE lower(?)) '
                    '   OR '
                    '(lower(P.Vorname) LIKE lower(?) AND lower(P.Nachname) LIKE lower(?))'
                    ')'
                    'AND date(F.Startzeit) < ?',
                    [name_list[0], name_list[1], name_list[1], name_list[0], args['end_date']]
                )
        # GET sessions?start_date&end_date
        elif 'start_date' in args.keys() and 'end_datum' in args.keys():
            select_stmt = cursor.execute(
                'SELECT P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                'FROM Flugsession F '
                'JOIN Pilot P on P.PilotID = F.PilotID '
                'LEFT JOIN Gast G on G.GastID = F.GastID '
                'WHERE date(F.Startzeit) BETWEEN ? AND ?',
                [args['start_date'], args['end_date']]
            )
        # /sessions?name
        elif 'name' in args.keys():
            name_list = args['name'].split()
            if len(name_list) == 1:
                select_stmt = cursor.execute(
                    'SELECT P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.PilotID = F.PilotID '
                    'LEFT JOIN Gast G on G.GastID = F.GastID '
                    'WHERE lower(P.Vorname) LIKE lower(?) OR lower(P.Nachname) LIKE lower(?)',
                    [name_list[0], name_list[0]]
                )
            if len(name_list) == 2:
                select_stmt = cursor.execute(
                    'SELECT P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.PilotID = F.PilotID '
                    'LEFT JOIN Gast G on G.GastID = F.GastID '
                    'WHERE (lower(P.Vorname) LIKE lower(?) AND lower(P.Nachname) LIKE lower(?)) '
                    'OR '
                    '(lower(P.Vorname) LIKE lower(?) AND lower(P.Nachname) LIKE lower(?))',
                    [name_list[0], name_list[1], name_list[1], name_list[0]]
                )

        elif 'start_date' in args.keys():
            select_stmt = cursor.execute(
                'SELECT P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                'FROM Flugsession F '
                'JOIN Pilot P on P.PilotID = F.PilotID '
                'LEFT JOIN Gast G on G.GastID = F.GastID '
                'WHERE date(F.Startzeit) > ?',
                [args['start_date']]
            )

        elif 'end_date' in args.keys():
            select_stmt = cursor.execute(
                'SELECT P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                'FROM Flugsession F '
                'JOIN Pilot P on P.PilotID = F.PilotID '
                'LEFT JOIN Gast G on G.GastID = F.GastID '
                'WHERE date(F.Startzeit) < ?',
                [args['end_date']]
            )

        else:
            select_stmt = cursor.execute(
                'SELECT P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                'FROM Flugsession F '
                'JOIN Pilot P on P.PilotID = F.PilotID '
                'LEFT JOIN Gast G on G.GastID = F.GastID '
            )

        return_dict = {
            'sessions': []
        }
        # alle ergebnisse von 'from' bis 'to'
        for row in select_stmt.fetchall()[from_:to]:
            session = {
                'pilot_name': row[0] + " " + row[1],
                'date': row[2],
                'start_time': row[3],
                'end_time': row[4],
                'flugleiter': row[5],
                'gast': {
                    'name': row[6],
                    'text': row[7]
                }
            }
            return_dict['sessions'].append(session)
        connection.close()
        return return_dict

    # Flugsession nachtragen
    # POST /sessions
    @api.expect(session_post_model)
    def post(self):
        '''add session'''
        connection = get_connection("database_server.db")
        cursor = connection.cursor()

        payload = api.payload
        start_time = datetime.combine(date.fromisoformat(payload['session_date']),
                                      datetime.strptime(payload['start_time'], "%H:%M").time())
        end_time = datetime.combine(date.fromisoformat(payload['session_date']),
                                    datetime.strptime(payload['end_time'], "%H:%M").time())

        try:
            guest_name = payload['guest_name']
            guest_info = payload['guest_info']
            # gast einfügen
            cursor.execute(
                'INSERT INTO Gast(Gastname, Freitext) VALUES (?,?)', [guest_name, guest_info]
            )
            connection.commit()
            guest_row_nr = cursor.lastrowid
            guest_id = cursor.execute('SELECT GastID FROM Gast WHERE ROWID = ?', [guest_row_nr]).fetchone()[0]

        except KeyError:
            guest_id = None

        # session einfügen
        cursor.execute(
            'INSERT INTO Flugsession(PilotID, GastID, Startzeit, Endzeit, Ist_Flugleiter) VALUES (?,?,?,?,?)',
            [payload['pilot_id'], guest_id, start_time, end_time, payload['is_leader']]
        )

        connection.commit()
        connection.close()
        return {}
