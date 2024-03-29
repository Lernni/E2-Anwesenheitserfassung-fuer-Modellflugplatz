#   *** login.py ***
#   - implementiert die Login-Funktionalität
#   - Autor: Max Haufe
#   - Mail: max.haufe@htw-dresden.de

from bcrypt import checkpw
from flask_restx import Resource
from globals import api, get_connection, login_post_model


class login(Resource):
    '''login pilot'''

    # POST /login
    # im body sind username und passwort jeweils im klartext enthalten
    # wenn der Login erfolgreich ist, werden der token und Daten des users zurückgesendet
    # der token wird für zukünftige Vorgänge auf der Website benötigt (z.B. bearbeiten der eigenen Session)
    @api.doc(body=login_post_model, responses={
        403: 'Error',
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
            # wenn der pilot kein passwort hat, return 403
            pwd_db = select_stmt.fetchone()[0]
            if pwd_db is None:
                connection.close()
                return {}, 403
        # falls es keine ergebnisse gibt -> pilot existiert nicht, return 403
        except TypeError:
            connection.close()
            return {}, 403

        user_stmt = cursor.execute(
            'SELECT PilotID, Vorname, Nachname, Nutzername, Ist_Admin, Token FROM Pilot WHERE Nutzername LIKE ?',
            [username]
        )
        # wenn das passwort stimmt, return daten und token, sonst 403
        if checkpw(password.encode('utf8'), pwd_db.encode('utf8')):
            user = user_stmt.fetchone()
            connection.close()
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
