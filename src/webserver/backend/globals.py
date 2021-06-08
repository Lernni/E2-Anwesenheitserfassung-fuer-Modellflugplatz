import os.path
import sqlite3

from flask import Flask
from flask_restx import Api, fields
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

login_post_model = api.model('signup_post_model', {
    'username': fields.String(description='username'),
    'password': fields.String(description='password hash')
})


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


def is_admin(cursor):
    # auth
    # wenn der Pilot kein Admin ist oder der Token nicht existiert, false, sonst true
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
