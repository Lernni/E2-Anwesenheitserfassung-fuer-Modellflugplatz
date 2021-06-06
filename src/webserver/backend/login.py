from bcrypt import checkpw, gensalt, hashpw
from flask_restx import Resource
from globals import api, get_connection, login_post_model


class login(Resource):
    '''login pilot'''

    # return header
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
                connection.close()
                return {}, 514
        # falls es keine ergebnisse gibt -> pilot existiert nicht
        except TypeError:
            connection.close()
            return {}, 513

        user_stmt = cursor.execute(
            'SELECT PilotID, Vorname, Nachname, Nutzername, Ist_Admin, Token FROM Pilot WHERE Nutzername LIKE ?', [username]
        )

        if checkpw(password.encode('utf8'), pwd_db.encode('utf8')):
            # salt = gensalt()

            user = user_stmt.fetchone()
            # hashed_token = hashpw(str(token).encode('utf8'), salt)
            connection.close()
            # return token in header
            return {
                'token': user[5],
                'user': {
                    'id': user[0],
                    'name': user[1] + ' ' + user[2],
                    'username': user[3],
                    'is_admin': user[4]
                }
            }
        else:
            connection.close()
            return {}, 403
