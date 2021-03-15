import commandProcessor

def interruptHandler(signal, frame):
    client.disconnect()
    sys.exit(0)

def client_init():
    client = None
    try:
        client = wiotp.sdk.device.DeviceClient(#wiotp_info) # create a client using preset values
        client.commandCallback = commandProcessor # set commandCallback to commandProcessor  
        client.connect() # Use MQTT connection to IBM Watson IoT Plateform for publishing events
    except Exception as e:         # store error message in 'e'
        print(str(e))         #  printout error message
        sys.exit(1)         # issue occured, program exit
    print("(Press Ctrl+C to disconnect)")
