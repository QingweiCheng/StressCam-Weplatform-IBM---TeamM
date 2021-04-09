from Hologram.HologramCloud import HologramCloud
from subprocess import run
import json

def network_connect():
    run("sudo hologram network connect", shell=True)
    credentials ={'devicekey':'a_jbDNcZ'}
    return HologramCloud(credentials, network='cellular',authentication_type='csrpsk') #return cloud routing credentials

def network_disconnect():
    run("sudo hologram network disconnect", shell=True)

def message_publish(hologram,data):
    formatted_data = json.dumps(data, separators=(" ", ":"))
    recv=hologram.sendMessage(formatted_data)
    print("Recieved Code:", recv)
    print("0 Means Succesful Transmission")
