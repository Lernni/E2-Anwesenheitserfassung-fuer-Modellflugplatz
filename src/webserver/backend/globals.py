import os.path
import sqlite3

from flask import Flask
from flask_restx import Api
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
cors = CORS(app)


def get_connection(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError('Database not found')

    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    # foreign keys
    cursor.execute("PRAGMA FOREIGN_KEYS=ON")
    return connection
