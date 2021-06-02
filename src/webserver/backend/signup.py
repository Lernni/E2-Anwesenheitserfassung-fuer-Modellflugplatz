from flask_restx import Resource
from globals import api, get_connection, login_post_model


class signup(Resource):
    @api.doc(body=login_post_model, responses={
        512: 'Pilot already has a password',
        513: 'Pilot does not exist',
        200: 'Success'
    })
    def post(self):
        '''create login for pilot'''
        connection = get_connection("database_server.db")
        cursor = connection.cursor()

        payload = api.payload
        username = payload['username']
        password = payload['password']

        select_stmt = cursor.execute(
            'SELECT Passwort FROM Pilot WHERE Nutzername LIKE ?', [username]
        )
        try:
            # wenn der pilot schon ein passwort hat, return 512
            if select_stmt.fetchone()[0] is not None:
                return {}, 512
        # falls es keine ergebnisse gibt -> pilot existiert nicht
        except TypeError:
            return {}, 513

        cursor.execute(
            'UPDATE Pilot SET Passwort = ? WHERE Nutzername LIKE ?', [password, username]
        )
        connection.commit()

        return {}, 200
