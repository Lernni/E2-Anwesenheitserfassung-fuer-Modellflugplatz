#   *** globals.py ***
#   - implementiert verschiedene Funktionen wie:
#         - get_connection
#         - is_pilot() und is_admin() für die Authentifikation
#         - sowie andere globale Variablen wie app und api
#   - Autor: Max Haufe
#   - Mail: max.haufe@htw-dresden.de

import os.path
import sqlite3
import time

from flask import Flask, Blueprint
from flask_restx import Api, fields
from flask_cors import CORS

app = Flask(__name__)
api_bp = Blueprint("api", __name__, url_prefix="/api/")
api = Api(api_bp)
app.register_blueprint(api_bp)
cors = CORS(app)


# für session_post_model
# => um Zeit im Format HH:MM im Body als input zu ermöglichen
class TimeFormat(fields.String):
    def format(self, value):
        return time.strftime(value, "%H:%M")


login_post_model = api.model('login_post_model', {
    'username': fields.String(description='username'),
    'password': fields.String(description='password hash')
})


# gibt connection-objekt zurück, schaltet foreign keys an und schaut, ob DB existiert
def get_connection(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError('Database not found')

    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    # foreign keys
    cursor.execute("PRAGMA FOREIGN_KEYS=ON")
    return connection


auth_parser = api.parser()
auth_parser.add_argument('token', type=str, location='headers', required=True)


# gibt True zurück, wenn der im Header mit gesendete Token der eines Admins ist, sonst false
# um diese funktion in einer request zu nutzen, muss diese vorher mit dem decorator
# @api.expect(auth_parser)
# versehen werden
def is_admin(cursor):
    try:
        token = auth_parser.parse_args()['token']

        is_admin_db = cursor.execute(
            'SELECT Ist_Admin FROM Pilot WHERE Token LIKE ?', [token]
        ).fetchone()[0]

        if not is_admin_db:
            return False
    except TypeError:
        return False

    return True


# gibt True zurück, wenn der im Header mit gesendete Token der eines Piloten ist, sonst false
# um diese funktion in einer request zu nutzen, muss diese vorher mit dem decorator
# @api.expect(auth_parser)
# versehen werden
def is_pilot(cursor):
    # wenn der Token nicht existiert, return -1, sonnst piloten_id
    try:
        token = auth_parser.parse_args()['token']

        p_id = cursor.execute(
            'SELECT PilotID FROM Pilot WHERE Token LIKE ?', [token]
        ).fetchone()[0]

        return p_id

    except TypeError:
        return -1
