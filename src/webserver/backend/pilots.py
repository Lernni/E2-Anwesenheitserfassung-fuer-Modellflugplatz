from sync import sync_pilots
from flask_restx import Resource, inputs, fields
from globals import api, get_connection, auth_parser, is_admin

pilots_parser = api.parser()
pilots_parser.add_argument('id', type=int)
pilots_parser.add_argument('is_active', type=inputs.boolean)

pilot_post_model = api.model('pilot_post_model', {
    'pilot_name': fields.String(description='Vorname des Piloten', required=True),
    'pilot_surname': fields.String(description='Nachname des Piloten', required=True),
    'rfid': fields.String(description='RFID Tag des Piloten', required=True),
    'pilot_username': fields.String(description='Benutzername des Piloten', required=True),
    'is_admin': fields.Boolean(required=True)
})

pilot_put_model = api.model('pilot_put_model', {
    'pilot_id': fields.Integer(description='PilotID', required=True),
    'pilot_name': fields.String(description='Vorname des Piloten'),
    'pilot_surname': fields.String(description='Nachname des Piloten'),
    'rfid': fields.String(description='RFID Tag des Piloten'),
    'pilot_username': fields.String(description='Benutzername des Piloten'),
    'reset_password': fields.Boolean(description='Setzt das Passwort des Piloten auf NULL, wenn true'),
    'is_admin': fields.Boolean
})


# nur admins dürfen diese requests ausführen
class Pilots(Resource):
    # GET /pilots?id=1&is_active=true
    @api.expect(pilots_parser, auth_parser)
    def get(self):
        '''get pilots'''
        connection = get_connection("database_server.db")
        cursor = connection.cursor()

        if not is_admin(cursor):
            return {}, 401

        args = pilots_parser.parse_args()
        p_id = args['id']
        is_active = args['is_active']

        return_dict = {
            'pilots': []
        }

        # /pilots?is_active=true
        if p_id is None:
            if is_active:
                select_stmt = cursor.execute(
                    'SELECT PilotID, Vorname, Nachname, Eintrittsdatum, RFID_Code, Nutzername, Ist_Admin '
                    'FROM Pilot WHERE RFID_Code IS NOT NULL '
                )
            else:
                select_stmt = cursor.execute(
                    'SELECT PilotID, Vorname, Nachname, Eintrittsdatum, RFID_Code, Nutzername, Ist_Admin '
                    'FROM Pilot WHERE RFID_Code IS NULL '
                )
        # /pilots?id=1
        elif is_active is None:
            select_stmt = cursor.execute(
                'SELECT PilotID, Vorname, Nachname, Eintrittsdatum, RFID_Code, Nutzername, Ist_Admin '
                'FROM Pilot WHERE PilotID = ?', [p_id]
            )
        # /pilots?id=1&is_active=true
        else:
            if is_active:
                select_stmt = cursor.execute(
                    'SELECT PilotID, Vorname, Nachname, Eintrittsdatum, RFID_Code, Nutzername, Ist_Admin '
                    'FROM Pilot WHERE PilotID = ? AND RFID_Code IS NOT NULL', [p_id]
                )
            else:
                select_stmt = cursor.execute(
                    'SELECT PilotID, Vorname, Nachname, Eintrittsdatum, RFID_Code, Nutzername, Ist_Admin '
                    'FROM Pilot WHERE PilotID = ? AND RFID_Code IS NULL', [p_id]
                )

        for row in select_stmt:
            pilot = {
                'pilot_id': row[0],
                'pilot_name': row[1],
                'pilot_surname': row[2],
                'entry_date': row[3],
                'rfid': 'null' if row[4] is None else hex(row[4]),
                'pilot_username': row[5],
                'is_admin': bool(row[6])
            }
            return_dict['pilots'].append(pilot)
        connection.close()
        return return_dict

    # neuen Piloten anlegen
    # POST /pilots
    @api.expect(pilot_post_model, auth_parser)
    def post(self):
        '''create pilot'''
        connection = get_connection("database_server.db")
        cursor = connection.cursor()

        if not is_admin(cursor):
            return {}, 401

        payload = api.payload
        first_name = payload['pilot_name']
        last_name = payload['pilot_surname']
        rfid = int(payload['rfid'], 16)
        username = payload['pilot_username']
        admin = bool(payload['is_admin'])

        # erzeuge token
        token = abs(hash(username))
        select_stmt = cursor.execute(
            'SELECT Token FROM Pilot'
        ).fetchall()

        all_tokens = [t[0] for t in select_stmt]
        # wenn token vergeben, inkrementiere und prüfe erneut
        while token in all_tokens:
            token += 1

        cursor.execute(
            'INSERT INTO Pilot(RFID_Code, Nachname, Vorname, Eintrittsdatum, Nutzername, Passwort, Ist_Admin, Token, Synced) '
            'VALUES(?, ?, ?, date(), ?, NULL, ?, ?, FALSE)', [rfid, last_name, first_name, username, admin, str(token)]
        )
        connection.commit()
        connection.close()
        # piloten mit terminal synchronisieren
        sync_pilots()

        return {}

    @api.expect(pilot_put_model, auth_parser)
    def put(self):
        '''update pilot'''
        connection = get_connection("database_server.db")
        cursor = connection.cursor()

        if not is_admin(cursor):
            return {}, 401

        payload = api.payload
        p_id = payload['pilot_id']

        if 'pilot_name' in payload.keys():
            new_first_name = payload['pilot_name']
            cursor.execute('UPDATE Pilot SET Vorname = ? WHERE PilotID = ?', [new_first_name, p_id])

        if 'pilot_surname' in payload.keys():
            new_last_name = payload['pilot_surname']
            cursor.execute('UPDATE Pilot SET Nachname = ? WHERE PilotID = ?', [new_last_name, p_id])

        if 'rfid' in payload.keys():
            if not payload['rfid']:
                new_rfid = None
            else:
                new_rfid = int(payload['rfid'], 16)
            cursor.execute('UPDATE Pilot SET RFID_Code = ?, Synced = FALSE WHERE PilotID = ?', [new_rfid, p_id])

        if 'pilot_username' in payload.keys():
            new_user_name = payload['pilot_username']
            cursor.execute('UPDATE Pilot SET Nutzername = ? WHERE PilotID = ?', [new_user_name, p_id])

        if 'is_admin' in payload.keys():
            new_admin = payload['is_admin']
            cursor.execute('UPDATE Pilot SET Ist_Admin = ? WHERE PilotID = ?', [new_admin, p_id])

        if 'reset_password' in payload.keys():
            new_password = payload['reset_password']
            if new_password:
                cursor.execute('UPDATE Pilot SET Passwort = NULL WHERE PilotID = ?', [p_id])

        connection.commit()
        connection.close()
        # piloten mit terminal synchronisieren
        sync_pilots()

        return {}
