import test3
import json
import wiotp.sdk.device
with open('c:/Users/qincheng/github/StressCam-Weplatform-IBM---TeamM/Software_Files/Raspberry_Pi_Code/device_info.json') as f:
    data = json.load(f)
f.close()

def client_setup():
    return wiotp.sdk.device.DeviceClient(data['wiotp_info']), test3.commandProcessor
