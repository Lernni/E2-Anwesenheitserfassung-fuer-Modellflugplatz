# coding=utf-8
import pilot_list
import pilots
import rfid_available
import sessions
from globals import api, app

# Ressourcen mit gewünschtem Pfad verknüpfen
api.add_resource(pilot_list.PilotList, '/pilot-list')
api.add_resource(rfid_available.RfidAvailable, '/rfid')
api.add_resource(pilots.Pilots, '/pilots')
api.add_resource(sessions.Sessions, '/sessions')

if __name__ == '__main__':
    app.run(debug=True)
