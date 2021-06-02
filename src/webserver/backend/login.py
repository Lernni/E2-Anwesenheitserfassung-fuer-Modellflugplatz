from bcrypt import checkpw
from flask_restx import Resource
from globals import api, get_connection, login_post_model


class login(Resource):
    '''login pilot'''

    @api.doc(body=login_post_model, responses={
        403: 'Wrong password',
        513: 'Pilot does not exist',
        514: 'Pilot does not have a Password',
        200: 'Success'
    })
    def post(self):
        '''login pilot'''
        connection = get_connection("database_server.db")
        cursor = connection.cursor()

        payload = api.payload
        username = payload['username']
        password = payload['password']

        select_stmt = cursor.execute(
            'SELECT Passwort FROM Pilot WHERE Nutzername LIKE ?', [username]
        )
        try:
            # wenn der pilot kein passwort hat, return 514
            pwd_db = select_stmt.fetchone()[0]
            if pwd_db is None:
                return {}, 514
        # falls es keine ergebnisse gibt -> pilot existiert nicht
        except TypeError:
            return {}, 513

        if checkpw(password.encode('utf8'), pwd_db.encode('utf8')):
            return {}, 200
        else:
            return {}, 403
