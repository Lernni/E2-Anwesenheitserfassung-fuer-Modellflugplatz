import sqlite3
from flask_restx import Resource, inputs, fields

from globals import api, get_connection

# EditPilot.vue

pilots_parser = api.parser()
pilots_parser.add_argument('id', type=int)
pilots_parser.add_argument('is_active', type=inputs.boolean, default=True)

pilot_post_model = api.model('pilot_post_model', {
    'first_name': fields.String(description='Vorname des Piloten'),
    'last_name': fields.String(description='Nachname des Piloten'),
    'rfid': fields.Integer(description='RFID Tag des Piloten')
})

pilot_put_model = api.model('pilot_put_model', {
    'pilot_id': fields.Integer(description='PilotID', required=True),
    'pilot_name': fields.String(description='Vorname des Piloten'),
    'pilot_surname': fields.String(description='Nachname des Piloten'),
    #'entry_date': fields.Date(description='Eintrittsdatum'),

    # TODO geht nicht, da foreign key
    # 'rfid': fields.Integer(description='RFID Tag des Piloten'),
    'pilot_username': fields.String(description='Benutzername des Piloten'),
    'reset_password': fields.Boolean(description='Setzt das Passwort des Piloten auf NULL, wenn true'),
    'is_admin': fields.Boolean,
    'is_active': fields.Boolean,
})


class Pilots(Resource):
    # GET /pilots?id=1?is_active=true
    @api.expect(pilots_parser)
    def get(self):
        '''get pilots'''
        args = pilots_parser.parse_args()
        p_id = args['id']
        is_active = args['is_active']
        connection = get_connection("database_server.db")
        cursor = connection.cursor()
        return_dict = {
            'pilots': []
        }
        # /pilots?is_active=true
        if p_id is None:
            select_stmt = cursor.execute(
                'SELECT ROWID, Vorname, Nachname, Eintrittsdatum,RFID_Code,Ist_Aktiv FROM Pilot WHERE Ist_Aktiv IS ?',
                [is_active])
        # /pilots?id=1?is_active=true und /pilots?id=1
        else:
            # is_active ist NULL, wenn nur eine id übergeben wird?
            select_stmt = cursor.execute(
                'SELECT ROWID, Vorname, Nachname, Eintrittsdatum, RFID_Code, Ist_Aktiv, Nutzername, Ist_Admin FROM Pilot WHERE ROWID = ? AND '
                'Ist_Aktiv IS ?', [p_id, is_active])

        for row in select_stmt:
            pilot = {
                'pilot_id': row[0],
                'pilot_name': row[1],
                'pilot_surname': row[2],
                'entry_date': row[3],
                'rfid': hex(row[4]),
                'is_active': bool(row[5]),
                'pilot_username': row[6],
                'is_admin': bool(row[7])
            }
            return_dict['pilots'].append(pilot)
        connection.close()
        return return_dict

    # neuen Piloten anlegen
    # POST /pilots
    @api.expect(pilot_post_model)
    def post(self):
        '''create pilot'''
        payload = api.payload
        first_name = payload['first_name']
        last_name = payload['last_name']
        rfid = payload['rfid']

        connection = get_connection("database_server.db")
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO Pilot(RFID_Code, Nachname, Vorname, Eintrittsdatum, Ist_Aktiv) VALUES(?, ?, ?, date(), true)',
            [rfid, last_name, first_name])
        connection.commit()
        connection.close()
        return {}

    @api.expect(pilot_put_model)
    def put(self):
        '''update pilot'''
        payload = api.payload
        p_id = payload['pilot_id']

        connection = get_connection("database_server.db")
        cursor = connection.cursor()

        # da sqlite keine funktion zum updaten einer variablen anzahl von spalten anbietet, wird es ab hier hässlich
        if 'pilot_name' in payload.keys():
            new_first_name = payload['pilot_name']
            cursor.execute('UPDATE Pilot SET Vorname = ? WHERE ROWID = ?', [new_first_name, p_id])

        if 'pilot_surname' in payload.keys():
            new_last_name = payload['pilot_surname']
            cursor.execute('UPDATE Pilot SET Nachname = ? WHERE ROWID = ?', [new_last_name, p_id])

        # Eintrittsdatum soll eigentlich nicht verändert werden können
        # if 'entry_date' in payload.keys():
        #    new_entry_date = payload['entry_date']
        #    cursor.execute('UPDATE Pilot SET Eintrittsdatum = ? WHERE ROWID = ?', [new_entry_date, p_id])

        # update funktoniert nicht, da foreign key constraint
        # TODO:Lösung drop constraint -> update -> reapply constraint
        # if 'rfid' in payload.keys():
        #     new_rfid = payload['rfid']
        #     cursor.execute('UPDATE Pilot SET RFID_Code = ? WHERE ROWID = ?', [new_rfid, p_id])

        if 'pilot_username' in payload.keys():
            new_user_name = payload['pilot_username']
            cursor.execute('UPDATE Pilot SET Nutzername = ? WHERE ROWID = ?', [new_user_name, p_id])

        if 'is_admin' in payload.keys():
            new_admin = payload['is_admin']
            cursor.execute('UPDATE Pilot SET Ist_Admin = ? WHERE ROWID = ?', [new_admin, p_id])

        if 'reset_password' in payload.keys():
            new_password = payload['reset_password']
            if (new_password):
                cursor.execute('UPDATE Pilot SET Passwort = NULL WHERE ROWID = ?', [p_id])

        if 'is_active' in payload.keys():
            new_active = payload['is_active']
            cursor.execute('UPDATE Pilot SET Ist_Aktiv = ? WHERE ROWID = ?', [new_active, p_id])

        connection.commit()
        connection.close()
        return {}
