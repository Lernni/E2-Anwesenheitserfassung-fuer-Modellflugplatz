# coding=utf-8
import sqlite3

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

class Pilots(Resource):
    def get(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        # wichtig, damit foreign keys eingehalten werden, hier aber egal
        cursor.execute("PRAGMA FOREIGN_KEYS=ON")

        return_dict = {
            "pilots": [],
            "other_values": "..."
        }

        # IMPORTANT hierfür müssen erst lokal die tabellen definiert sein
        for row in cursor.execute("SELECT * FROM Pilot"):
            pilot_id = row[0]
            rfid_code = row[1]
            nachname = row[2]
            vorname = row[3]
            eintrittsdatum = row[4]
            ist_aktiv = row[5]
            pilot = {
                "pilot_id": pilot_id,
                "rfid_code": rfid_code,
                "name": vorname + " " + nachname,
                "eintrittsdatum": eintrittsdatum,
                "aktiv": ist_aktiv
            }
            return_dict["pilots"].append(pilot)
        # falls ändeurngen vorgenommen werden, wie cursor.execute(INSERT INTO ...), muss hier noch die zeile
        # connection.commit()
        # eingefügt werden
        return return_dict

# Ressourcen mit gewünschtem Pfad verknüpfen

api.add_resource(ActivePilots, '/active_pilots')
api.add_resource(Pilots, '/pilots')

if __name__ == '__main__':
    app.run(debug=True)
