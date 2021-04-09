
#!/usr/bin/env python3
#!/home/pi/.local/lib/python3.7/site-packages

# *****************************************************************************
# Copyright (c) 2014, 2019 IBM Corporation and other Contributors.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
# *****************************************************************************
from time import sleep
from os import listdir
import json
import signal
import datetime


from sys import path,exit
path.insert(0,"/home/pi")
path.insert(0,"/usr/local/lib/python3.7/dist-packages")
#### Custom Modules ####
from commands import capture_image, publish_data, load_file
import hologram_commands 
from commandProcessor import commandProcessor
import tensor_flow_process
#### Custom Modules ####


hologram = hologram_commands.network_connect()
from wiotp_login import client
def interruptHandler(signal, frame):
#    hologram_commands.network_disconnect()
    client.disconnect()
    exit(0)

#if the iot.py file is called
if __name__ == "__main__":
    signal.signal(signal.SIGINT, interruptHandler)

    with open('/home/pi/device_info.json') as f:
        data = json.load(f)
    f.close()
    try:
        client.commandCallback = commandProcessor # set commandCallback to commandProcessor  
        client.connect() # Use MQTT connection to IBM Watson IoT Plateform for publishing events
    except Exception as e:         # store error message in 'e'
        print(str(e))         #  printout error message
        exit(1)         # issue occured, program exit
    print("(Press Ctrl+C to disconnect)")
    street = listdir('/home/pi/images/') #list image name insde "images" folder
    i=0 # setting i to be the counter referencing most recent picture
    
    while True:
        print("taking Image")
       	currDate = datetime.datetime.now().strftime("%d_%m_%y")
       	currTime = datetime.datetime.now().strftime("%H_%M_%S")
        capture_image(currDate,currTime)
        ####
        water_stress_lv=tensor_flow_process.ml_process(street,i)
        ####
        #Get wittyPi Temperature
        #with open('/home/pi/test.txt','w+') as fout:
        #    wittyPi = Popen(["sudo","/home/pi/wittyPi/wittyPi.sh"],stdout=fout)
        #    sleep(15)
        #    os.system("sudo kill %s" %(wittyPi.pid,))
        #    tempLine = linecache.getline("/home/pi/test.txt",8)
        #    wittyPiTemp = float(tempLine[25:30])
        #    fout.close()
        camera_data = publish_data(currDate,currTime,water_stress_lv)
        client.publishEvent('status','json',camera_data)
        hologram_commands.message_publish(hologram, camera_data)
        with open('/home/pi/data.txt', 'a') as outfile:
            json.dump(camera_data, outfile)
            outfile.write('\n')
        device_info = load_file('device')
#        sleep(device_info['statusInterval'])
