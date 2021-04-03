# coding=utf-8

from flask import Flask
from flask_restx import Resource, Api

app = Flask(__name__)
api = Api(app)

# Ressourcen definieren

class ActivePilots(Resource):
    def get(self):
        return {
            "active_pilots": [
                {
                    "id": "1",
                    "name": "Max Muster",
                    "start_time": "03.06.2021 15:23:10"
                },
                {
                    "id": "2",
                    "name": "Jens Müller",
                    "start_time": "03.06.2021 14:17:40"
                }
            ],
            "leader": "1"
        }


# Ressourcen mit gewünschtem Pfad verknüpfen

api.add_resource(ActivePilots, '/active_pilots')

if __name__ == '__main__':
    app.run(debug=True)