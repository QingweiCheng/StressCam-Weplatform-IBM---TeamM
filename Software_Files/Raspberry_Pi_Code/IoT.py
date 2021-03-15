
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
from sys import path
path.append("/home/pi/.local/lib/python3.7/site-packages")
path.append("/home/pi")
import PIL
from PIL import Image
import argparse
import os
from subprocess import Popen
import linecache

import platform
import json
import signal
import datetime
import random

#### Custom Modules ####
import commands
import hologram_commands 
from commandProcessor import commandProcessor
import wiotp_processes
#### Custom Modules ####

from time import sleep
import gpiozero as gpz

###############import values from device_info file#######################


from uuid import getnode as get_mac

hologram_commands.network_connect()

try:
    import wiotp.sdk.device #changed from import wiotp.sdk.device
except ImportError:
    # This part is only required to run the sample from within the samples
    # directory when the module itself is not installed.
    #
    # If you have the module installed, just use "import wiotp.sdk"
    import os
    import inspect

    cmd_subfolder = os.path.realpath(
        os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "../../../src"))
    )
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
    import wiotp.sdk.device


#if the iot.py file is called
if __name__ == "__main__":
    signal.signal(signal.SIGINT, wiotp_processes.interruptHandler)

    street = os.listdir('/home/pi/Pictures/') #list image name insde 'Picture" folder

    while True:
        print("taking Image")
       	currDate = datetime.datetime.now().strftime("%d_%m_%y")
       	currTime = datetime.datetime.now().strftime("%H_%M_%S")
        commands.capture_image(currDate,currTime)
        ####
        #use tensor_flow_process here
        ####

        #CPU Temp
        cpu = gpz.CPUTemperature()
        cpuTemp = cpu.temperature
        print("Sensor Reading")
        #Sensor Reading
        #Get wittyPi Temperature
        #with open('/home/pi/test.txt','w+') as fout:
        #    wittyPi = Popen(["sudo","/home/pi/wittyPi/wittyPi.sh"],stdout=fout)
        #    sleep(15)
        #    os.system("sudo kill %s" %(wittyPi.pid,))
        #    tempLine = linecache.getline("/home/pi/test.txt",8)
        #    wittyPiTemp = float(tempLine[25:30])
        #    fout.close()
        data = {
            "DEVICE_ID": deviceId,
            "DEVICE_STATUS": "On",
            "LATITUDE": cameraLatitude,
            "LONGITUDE": cameraLongitude,
            "WATER_STRESS_LEVEL":waterStressLevel,
            "WITTYPI_TEMPERATURE": random.randrange(30,40), #wittyPiTemp,
            "CPU_TEMPERATURE": cpuTemp,
            "DATE_1":currDate,
            "TIME_1":currTime,
        }
        print("Sending Data")
        client.publishEvent("status","json", data)
	formatted_data  = json.dumps(data, seperator=(" ", ":"))
	recv=hologram.senMessage(formatted_data)
	print("Recieved Code:", recv)
	print("0 Means Succesful Transmission")
        with open('/home/pi/data.txt', 'a') as outfile:
            json.dump(data, outfile)
            outfile.write('\n')
        sleep(statusInterval)
