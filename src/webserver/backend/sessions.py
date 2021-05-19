from flask_restx import Resource, inputs

from globals import api, get_connection

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
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Vorname, G.Nachname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.ROWID = F.PilotID '
                    'LEFT JOIN Gast G on G.ROWID = F.GastID '
                    'WHERE (lower(P.Vorname) LIKE lower(?) OR lower(P.Nachname) LIKE lower(?))'
                    'AND date(F.Startzeit) BETWEEN ? AND ?',
                    [name_list[0], name_list[0], args['start_date'], args['end_date']]
                )
            # z.B. 'Max Mustermann' -> vor(Max), nach(Mustermann) oder vor(Mustermann) nach(Max)
            if len(name_list) == 2:
                select_stmt = cursor.execute(
                    'SELECT P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Vorname, G.Nachname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.ROWID = F.PilotID '
                    'LEFT JOIN Gast G on G.ROWID = F.GastID '
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
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Vorname, G.Nachname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.ROWID = F.PilotID '
                    'LEFT JOIN Gast G on G.ROWID = F.GastID '
                    'WHERE (lower(P.Vorname) LIKE lower(?) OR lower(P.Nachname) LIKE lower(?))'
                    'AND date(F.Startzeit) > ?',
                    [name_list[0], name_list[0], args['start_date']]
                )

            if len(name_list) == 2:
                select_stmt = cursor.execute(
                    'SELECT P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Vorname, G.Nachname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.ROWID = F.PilotID '
                    'LEFT JOIN Gast G on G.ROWID = F.GastID '
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
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Vorname, G.Nachname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.ROWID = F.PilotID '
                    'LEFT JOIN Gast G on G.ROWID = F.GastID '
                    'WHERE (lower(P.Vorname) LIKE lower(?) OR lower(P.Nachname) LIKE lower(?))'
                    'AND date(F.Startzeit) < ?',
                    [name_list[0], name_list[0], args['end_date']]
                )

            if len(name_list) == 2:
                select_stmt = cursor.execute(
                    'SELECT P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Vorname, G.Nachname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.ROWID = F.PilotID '
                    'LEFT JOIN Gast G on G.ROWID = F.GastID '
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
                'time(F.Endzeit), F.Ist_Flugleiter, G.Vorname, G.Nachname, G.Freitext '
                'FROM Flugsession F '
                'JOIN Pilot P on P.ROWID = F.PilotID '
                'LEFT JOIN Gast G on G.ROWID = F.GastID '
                'WHERE date(F.Startzeit) BETWEEN ? AND ?',
                [args['start_date'], args['end_date']]
            )
        # /sessions?name
        elif 'name' in args.keys():
            name_list = args['name'].split()
            if len(name_list) == 1:
                select_stmt = cursor.execute(
                    'SELECT P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Vorname, G.Nachname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.ROWID = F.PilotID '
                    'LEFT JOIN Gast G on G.ROWID = F.GastID '
                    'WHERE lower(P.Vorname) LIKE lower(?) OR lower(P.Nachname) LIKE lower(?)',
                    [name_list[0], name_list[0]]
                )
            if len(name_list) == 2:
                select_stmt = cursor.execute(
                    'SELECT P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Vorname, G.Nachname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.ROWID = F.PilotID '
                    'LEFT JOIN Gast G on G.ROWID = F.GastID '
                    'WHERE (lower(P.Vorname) LIKE lower(?) AND lower(P.Nachname) LIKE lower(?)) '
                    'OR '
                    '(lower(P.Vorname) LIKE lower(?) AND lower(P.Nachname) LIKE lower(?))',
                    [name_list[0], name_list[1], name_list[1], name_list[0]]
                )

        elif 'start_date' in args.keys():
            select_stmt = cursor.execute(
                'SELECT P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                'time(F.Endzeit), F.Ist_Flugleiter, G.Vorname, G.Nachname, G.Freitext '
                'FROM Flugsession F '
                'JOIN Pilot P on P.ROWID = F.PilotID '
                'LEFT JOIN Gast G on G.ROWID = F.GastID '
                'WHERE date(F.Startzeit) > ?',
                [args['start_date']]
            )

        elif 'end_date' in args.keys():
            select_stmt = cursor.execute(
                'SELECT P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                'time(F.Endzeit), F.Ist_Flugleiter, G.Vorname, G.Nachname, G.Freitext '
                'FROM Flugsession F '
                'JOIN Pilot P on P.ROWID = F.PilotID '
                'LEFT JOIN Gast G on G.ROWID = F.GastID '
                'WHERE date(F.Startzeit) < ?',
                [args['end_date']]
            )

        return_dict = {
            'sessions': []
        }
        # alle ergebnisse von 'from' bis 'to'
        for row in select_stmt.fetchall()[from_:to]:
            try:
                guest_name = row[6] + " " + row[7]
            except TypeError:
                guest_name = None

            session = {
                'pilot_name': row[0] + " " + row[1],
                'date': row[2],
                'start_time': row[3],
                'end_time': row[4],
                'flugleiter': row[5],
                'gast': {
                    'name': guest_name,
                    'text': row[8]
                }
            }
            return_dict['sessions'].append(session)
        connection.close()
        return return_dict
