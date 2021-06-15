# coding=utf-8
import pilot_list
import pilots
import rfid_available
import sessions
import running_sessions
import checkout_all
import signup
import login
import rfid_assigned
import rfid

from globals import api, app

# Ressourcen mit gewünschtem Pfad verknüpfen
api.add_resource(pilot_list.PilotList, '/pilot-list')
api.add_resource(rfid_available.RfidAvailable, '/rfid_available')
api.add_resource(pilots.Pilots, '/pilots')
api.add_resource(sessions.Sessions, '/sessions')
api.add_resource(running_sessions.RunningSessions, '/sessions/running')
api.add_resource(checkout_all.CheckoutAll, '/sessions/checkout-all')
api.add_resource(signup.signup, '/signup')
api.add_resource(login.login, '/login')
api.add_resource(rfid_assigned.RfidAssigned, '/rfid_assigned')
api.add_resource(rfid.Rfid, '/rfid')



if __name__ == '__main__':
    app.run(debug=True)
