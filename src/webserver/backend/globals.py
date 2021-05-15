import os.path
import sqlite3

from flask import Flask
from flask_restx import Api, cors

app = Flask(__name__)
api = Api(app)
api.decorators = [cors.crossdomain(origin='*')]


def get_connection(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError('Database not found')

    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    # foreign keys
    cursor.execute("PRAGMA FOREIGN_KEYS=ON")
    return connection
