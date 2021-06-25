from datetime import date, time, datetime
from flask_restx import Resource, inputs, fields
from globals import api, get_connection, auth_parser, is_pilot, is_admin, TimeFormat

get_parser = api.parser()
get_parser.add_argument('name', type=str)
get_parser.add_argument('start_date', type=inputs.date)
get_parser.add_argument('end_date', type=inputs.date)
get_parser.add_argument('from', type=int, required=True)
get_parser.add_argument('to', type=int, required=True)

session_post_model = api.model('session_post_model', {
    'pilot_id': fields.Integer(description='ID of Pilot', required=True),
    'session_date': fields.Date(required=True),
    'start_time': TimeFormat(description='Time in 24 hour HH:MM format', required=True, default='HH:MM'),
    'end_time': TimeFormat(description='Time in 24 hour HH:MM format', default='HH:MM'),
    'is_leader': fields.Boolean(required=True),
    'guest_name': fields.String(),
    'guest_info': fields.String()
})

session_put_model = api.model('session_put_model', {
    'guest_name': fields.String(),
    'guest_info': fields.String(),
    'end_time': fields.DateTime(),
    'is_leader': fields.Boolean()
})
put_parser = api.parser()
put_parser.add_argument('id', type=int, required=True)


class Sessions(Resource):
    # jeder pilot darf diese request ausführen
    @api.expect(get_parser, auth_parser)
    def get(self):
        '''get Session info'''
        select_stmt = None
        connection = get_connection("database_server.db")
        cursor = connection.cursor()

        p_id = is_pilot(cursor)
        if p_id == -1:
            return {}, 404

        args = get_parser.parse_args()
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
                    'SELECT F.SessionID, P.PilotID, P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.PilotID = F.PilotID '
                    'LEFT JOIN Gast G on G.GastID = F.GastID '
                    'WHERE (instr(lower(P.Vorname), lower(?)) > 0 OR instr(lower(P.Nachname), lower(?)) > 0)'
                    'AND date(F.Startzeit) BETWEEN ? AND ?',
                    [name_list[0], name_list[0], args['start_date'], args['end_date']]
                )
            # z.B. 'Max Mustermann' -> vor(Max), nach(Mustermann) oder vor(Mustermann) nach(Max)
            if len(name_list) == 2:
                select_stmt = cursor.execute(
                    'SELECT F.SessionID, P.PilotID, P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.PilotID = F.PilotID '
                    'LEFT JOIN Gast G on G.GastID = F.GastID '
                    'WHERE ('
                    '(instr(lower(P.Vorname), lower(?)) > 0 AND instr(lower(P.Nachname), lower(?)) > 0) '
                    'OR '
                    '(instr(lower(P.Vorname), lower(?)) > 0 AND instr(lower(P.Nachname), lower(?)) > 0)'
                    ')'
                    'AND date(F.Startzeit) BETWEEN ? AND ?',
                    [name_list[0], name_list[1], name_list[1], name_list[0], args['start_date'], args['end_date']]
                )

        # GET sessions?name&start_date
        elif 'name' in args.keys() and 'start_date' in args.keys():
            name_list = args['name'].split()
            if len(name_list) == 1:
                select_stmt = cursor.execute(
                    'SELECT F.SessionID, P.PilotID, P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.PilotID = F.PilotID '
                    'LEFT JOIN Gast G on G.GastID = F.GastID '
                    'WHERE (instr(lower(P.Vorname), lower(?)) > 0 OR instr(lower(P.Nachname), lower(?)) > 0)'
                    'AND date(F.Startzeit) > ?',
                    [name_list[0], name_list[0], args['start_date']]
                )

            if len(name_list) == 2:
                select_stmt = cursor.execute(
                    'SELECT F.SessionID, P.PilotID, P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.PilotID = F.PilotID '
                    'LEFT JOIN Gast G on G.GastID = F.GastID '
                    'WHERE ('
                    '(instr(lower(P.Vorname), lower(?)) > 0 AND instr(lower(P.Nachname), lower(?)) > 0) '
                    'OR '
                    '(instr(lower(P.Vorname), lower(?)) > 0 AND instr(lower(P.Nachname), lower(?)) > 0)'
                    ')'
                    'AND date(F.Startzeit) BETWEEN ? AND ?'
                    'AND date(F.Startzeit) > ?',
                    [name_list[0], name_list[1], name_list[1], name_list[0], args['start_date']]
                )

        elif 'name' in args.keys() and 'end_date' in args.keys():
            name_list = args['name'].split()
            if len(name_list) == 1:
                select_stmt = cursor.execute(
                    'SELECT F.SessionID, P.PilotID, P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.PilotID = F.PilotID '
                    'LEFT JOIN Gast G on G.GastID = F.GastID '
                    'WHERE (instr(lower(P.Vorname), lower(?)) > 0 OR instr(lower(P.Nachname), lower(?)) > 0)'
                    'AND date(F.Startzeit) < ?',
                    [name_list[0], name_list[0], args['end_date']]
                )

            if len(name_list) == 2:
                select_stmt = cursor.execute(
                    'SELECT F.SessionID, P.PilotID, P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.PilotID = F.PilotID '
                    'LEFT JOIN Gast G on G.GastID = F.GastID '
                    'WHERE ('
                    '(instr(lower(P.Vorname), lower(?)) > 0 AND instr(lower(P.Nachname), lower(?)) > 0) '
                    'OR '
                    '(instr(lower(P.Vorname), lower(?)) > 0 AND instr(lower(P.Nachname), lower(?)) > 0)'
                    ')'
                    'AND date(F.Startzeit) BETWEEN ? AND ?'
                    'AND date(F.Startzeit) < ?',
                    [name_list[0], name_list[1], name_list[1], name_list[0], args['end_date']]
                )
        # GET sessions?start_date&end_date
        elif 'start_date' in args.keys() and 'end_date' in args.keys():
            select_stmt = cursor.execute(
                'SELECT F.SessionID, P.PilotID, P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
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
                    'SELECT F.SessionID, P.PilotID, P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.PilotID = F.PilotID '
                    'LEFT JOIN Gast G on G.GastID = F.GastID '
                    'WHERE (instr(lower(P.Vorname), lower(?)) > 0 OR instr(lower(P.Nachname), lower(?)) > 0)',
                    [name_list[0], name_list[0]]
                )
            if len(name_list) == 2:
                select_stmt = cursor.execute(
                    'SELECT F.SessionID, P.PilotID, P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                    'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                    'FROM Flugsession F '
                    'JOIN Pilot P on P.PilotID = F.PilotID '
                    'LEFT JOIN Gast G on G.GastID = F.GastID '
                    'WHERE ('
                    '(instr(lower(P.Vorname), lower(?)) > 0 AND instr(lower(P.Nachname), lower(?)) > 0) '
                    'OR '
                    '(instr(lower(P.Vorname), lower(?)) > 0 AND instr(lower(P.Nachname), lower(?)) > 0)'
                    ')'
                    'AND date(F.Startzeit) BETWEEN ? AND ?',
                    [name_list[0], name_list[1], name_list[1], name_list[0]]
                )

        elif 'start_date' in args.keys():
            select_stmt = cursor.execute(
                'SELECT F.SessionID, P.PilotID, P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                'FROM Flugsession F '
                'JOIN Pilot P on P.PilotID = F.PilotID '
                'LEFT JOIN Gast G on G.GastID = F.GastID '
                'WHERE date(F.Startzeit) > ?',
                [args['start_date']]
            )

        elif 'end_date' in args.keys():
            select_stmt = cursor.execute(
                'SELECT F.SessionID, P.PilotID, P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                'FROM Flugsession F '
                'JOIN Pilot P on P.PilotID = F.PilotID '
                'LEFT JOIN Gast G on G.GastID = F.GastID '
                'WHERE date(F.Startzeit) < ?',
                [args['end_date']]
            )

        else:
            select_stmt = cursor.execute(
                'SELECT F.SessionID, P.PilotID, P.Vorname, P.Nachname, date(F.Startzeit), time(F.Startzeit), '
                'time(F.Endzeit), F.Ist_Flugleiter, G.Gastname, G.Freitext '
                'FROM Flugsession F '
                'JOIN Pilot P on P.PilotID = F.PilotID '
                'LEFT JOIN Gast G on G.GastID = F.GastID '
            )

        return_dict = {
            'sessions': [],
            'session_count': 0
        }

        sessions_count = 0

        # alle ergebnisse von 'from' bis 'to'
        for row in select_stmt.fetchall():
            sessions_count += 1
            if from_ <= sessions_count <= to:
                session = {
                    'session_id': row[0],
                    'pilot_id': row[1],
                    'pilot_name': row[2] + " " + row[3],
                    'date': row[4],
                    'start_time': row[5],
                    'end_time': row[6],
                    'session_leader': row[7],
                    'guest': {
                        'name': row[8],
                        'text': row[9]
                    }
                }
                return_dict['sessions'].append(session)

        return_dict['session_count'] = sessions_count
        connection.close()
        return return_dict


# Flugsession nachtragen
# POST /sessions
# nur admins dürfen diese request ausführen
@api.expect(session_post_model, auth_parser)
def post(self):
    '''add session'''
    connection = get_connection("database_server.db")
    cursor = connection.cursor()

    if not is_admin(cursor):
        return {}, 401

    payload = api.payload
    start_time = datetime.combine(date.fromisoformat(payload['session_date']),
                                  datetime.strptime(payload['start_time'], "%H:%M").time())

    try:
        end_time = datetime.combine(date.fromisoformat(payload['session_date']),
                                    datetime.strptime(payload['end_time'], "%H:%M").time())
    except KeyError:
        end_time = None

    try:
        guest_name = payload['guest_name']
        guest_info = payload['guest_info']
        # gast einfügen
        cursor.execute(
            'INSERT INTO Gast(Gastname, Freitext) VALUES (?,?)', [guest_name, guest_info]
        )
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


# jeder pilot darf nur seine eigenen sessions bearbeiten
# 401 bei fehler - pilot ist kein admin, pilot versuch session von wem anders zu bearbeiten oder pilot versucht
# endzeit hinzuzufügen, wo endzeit nicht NULL ist.
@api.expect(put_parser, session_put_model, auth_parser)
def put(self):
    '''add guest name and info to session'''
    connection = get_connection("database_server.db")
    cursor = connection.cursor()

    payload = api.payload
    args = put_parser.parse_args()

    p_id = cursor.execute(
        'SELECT PilotID FROM Flugsession WHERE SessionID = ?', [args['id']]
    ).fetchone()[0]

    # wenn der pilot kein admin ist und die p_id nicht übereinstimmt, return 401
    if p_id != is_pilot(cursor) and not is_admin(cursor):
        connection.close()
        return {}, 401

    # wenn die endzeit mitgeschickt wurde, darf diese nur geändert werden, wenn die vorherige NULL war.
    if 'end_time' in payload.keys():
        end_time = cursor.execute(
            'SELECT Endzeit FROM Flugsession WHERE SessionID = ?', [args['id']]
        ).fetchone()[0]

        if end_time is None:
            cursor.execute(
                'UPDATE Flugsession SET Endzeit = ? WHERE SessionID = ?', [payload['end_time'], args['id']]
            )
        else:
            connection.close()
            return {}, 401

    if 'guest_name' in payload.keys():
        if 'guest_info' in payload.keys():
            guest_info = None
        else:
            guest_info = payload['guest_info']

        cursor.execute(
            'INSERT INTO Gast(Gastname, Freitext) VALUES (?,?)', [payload['guest_name'], guest_info]
        )

        guest_row_nr = cursor.lastrowid
        guest_id = cursor.execute('SELECT GastID FROM Gast WHERE ROWID = ?', [guest_row_nr]).fetchone()[0]

        cursor.execute(
            'UPDATE Flugsession SET GastID = ? WHERE SessionID = ?', [guest_id, args['id']]
        )

    if 'is_leader' in payload.keys():
        cursor.execute(
            'UPDATE Flugsession SET Ist_Flugleiter = ? WHERE SessionID = ?', [payload['is_leader'], args['id']]
        )

    connection.commit()
    connection.close()

    return {}
