from Hologram.HologramCloud import HologramCloud
from subprocess import run
import json

def network_connect():
    run("sudo hologram network connect", shell=True)
    credentials ={'devicekey':'a_jbDNcZ'}
    hologram = HologramCloud(credentials, network='cellular',authentication_type='csrpsk')

def network_disconnect():
    run("sudo hologram network disconnect", shell=True)

def message_publish(data):
    formatted_data  = json.dumps(data, seperator=(" ", ":"))