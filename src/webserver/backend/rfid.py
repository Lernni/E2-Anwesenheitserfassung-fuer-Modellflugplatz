from flask_restx import Resource, fields
from sync import sync_rfids
from globals import api, get_connection, auth_parser, is_admin

rfid_post_model = api.model('rfid_post_model', {
    'rfid': fields.String()
})


# POST /rfid
# nur admins dürfen diese request ausführen
class Rfid(Resource):
    @api.expect(auth_parser, rfid_post_model)
    def post(self):
        '''add RFID Tags to DB'''
        connection = get_connection("database_server.db")
        cursor = connection.cursor()

        payload = api.payload

        if not is_admin(cursor):
            return {}, 401

        cursor.execute(
            'INSERT INTO RFID_Ausweis (RFID_Code, Synced) VALUES (?, FALSE)', [int(payload['rfid'], 16)]
        )

        connection.commit()
        connection.close()

        sync_rfids()

        return {}
